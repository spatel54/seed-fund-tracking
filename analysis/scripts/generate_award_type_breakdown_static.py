#!/usr/bin/env python3
"""
Generate Award Type Static Visualizations (10-Year and 5-Year)
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys
import os
import re

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

# Import IWRC branding
from iwrc_brand_style import (
    IWRC_COLORS, 
    configure_matplotlib_iwrc, 
    apply_iwrc_matplotlib_style, 
    add_logo_to_matplotlib_figure
)

# Configuration
# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_FILE = PROJECT_ROOT / 'data/processed/clean_iwrc_tracking.xlsx'
OUTPUT_DIR = PROJECT_ROOT / 'deliverables_final/visualizations/static/awards'

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configure matplotlib
configure_matplotlib_iwrc()

def load_data():
    """Load and prepare data."""
    print(f"Loading data from {DATA_FILE}...")
    df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')
    
    # Column mapping
    col_map = {
        'Project ID ': 'project_id',
        'Award Type': 'award_type',
        'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount',
    }
    df = df.rename(columns=col_map)
    
    # Extract year
    def extract_year(project_id):
        if pd.isna(project_id):
            return None
        project_id_str = str(project_id).strip()
        year_match = re.search(r'(20\d{2}|19\d{2})', project_id_str)
        if year_match:
            return int(year_match.group(1))
        return None

    df['year'] = df['project_id'].apply(extract_year)
    
    # Clean award amount
    df['award_amount'] = pd.to_numeric(df['award_amount'], errors='coerce').fillna(0)
    
    # Categorize award type
    def categorize_award(award_type):
        if pd.isna(award_type):
            return 'Other'
        award_str = str(award_type).lower()
        if '104b' in award_str:
            return '104B'
        elif '104g' in award_str:
            return '104G'
        elif 'coordination' in award_str:
            return 'Coordination'
        return 'Other'

    df['award_category'] = df['award_type'].apply(categorize_award)
    
    return df

def generate_charts(df, period_label, start_year, end_year):
    """Generate charts for a specific period."""
    print(f"\nGenerating charts for {period_label} ({start_year}-{end_year})...")
    
    # Filter data
    df_period = df[df['year'].between(start_year, end_year, inclusive='both')].copy()
    
    if df_period.empty:
        print(f"No data found for {period_label}")
        return

    # Filter to main categories
    df_period = df_period[df_period['award_category'].isin(['104B', '104G', 'Coordination'])]
    
    # Aggregate data
    agg = df_period.groupby('award_category').agg({
        'project_id': 'nunique',
        'award_amount': 'sum'
    }).reset_index()
    
    agg['avg_per_project'] = agg['award_amount'] / agg['project_id']
    
    # Colors
    colors = [IWRC_COLORS['primary'], IWRC_COLORS['secondary'], IWRC_COLORS['accent']]
    
    # 1. Average Award per Project
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(agg['award_category'], agg['avg_per_project'], color=colors)
    
    ax.set_title(f'Average Award Amount per Project\n{period_label}', fontsize=14, fontweight='bold', color=IWRC_COLORS['dark_teal'])
    ax.set_ylabel('Average Amount ($)', fontweight='bold')
    
    # Add labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}',
                ha='center', va='bottom', fontweight='bold')
                
    apply_iwrc_matplotlib_style(fig, ax)
    # Logo disabled per user request
    # add_logo_to_matplotlib_figure(fig)
    
    filename = f'award_type_avg_per_project_{period_label.split()[0].lower()}.png'
    # Also save as the base name if it's the 10-year period (to match original request if needed, but user asked for specific files)
    # The user asked for "award_type_avg_per_project.png" originally, which was likely 10-year.
    # I will save with suffix to be clear.
    
    save_path = OUTPUT_DIR / filename
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved {filename}")
    plt.close(fig)

    # 2. Investment Comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(agg['award_category'], agg['award_amount'], color=colors)
    
    ax.set_title(f'Total Investment by Award Type\n{period_label}', fontsize=14, fontweight='bold', color=IWRC_COLORS['dark_teal'])
    ax.set_ylabel('Total Investment ($)', fontweight='bold')
    
    # Add labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height/1e6:.2f}M',
                ha='center', va='bottom', fontweight='bold')
                
    apply_iwrc_matplotlib_style(fig, ax)
    # Logo disabled per user request
    
    filename = f'award_type_investment_comparison_{period_label.split()[0].lower()}.png'
    save_path = OUTPUT_DIR / filename
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved {filename}")
    plt.close(fig)

    # 3. Overview (Project Count)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(agg['award_category'], agg['project_id'], color=colors)
    
    ax.set_title(f'Project Count by Award Type\n{period_label}', fontsize=14, fontweight='bold', color=IWRC_COLORS['dark_teal'])
    ax.set_ylabel('Number of Projects', fontweight='bold')
    
    # Add labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
                
    apply_iwrc_matplotlib_style(fig, ax)
    # Logo disabled per user request
    
    filename = f'award_type_overview_{period_label.split()[0].lower()}.png'
    save_path = OUTPUT_DIR / filename
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved {filename}")
    plt.close(fig)

def main():
    df = load_data()
    
    # Generate for 10-Year
    generate_charts(df, '10-Year (2015-2024)', 2015, 2024)
    
    # Generate for 5-Year
    generate_charts(df, '5-Year (2020-2024)', 2020, 2024)
    
    # Rename 10-year files to match original filenames if needed, 
    # but user asked for "pngs for 2020-2024 as well just like how you did for 2015-2024"
    # This implies they want distinct files. I will keep the suffixes for clarity.
    # However, to replace the "original" files the user pointed to, I should probably copy the 10-year ones to the base names.
    
    import shutil
    for base_name in ['award_type_avg_per_project', 'award_type_investment_comparison', 'award_type_overview']:
        src = OUTPUT_DIR / f'{base_name}_10-year.png'
        dst = OUTPUT_DIR / f'{base_name}.png'
        if src.exists():
            shutil.copy(src, dst)
            print(f"Copied {src.name} to {dst.name}")

if __name__ == "__main__":
    main()
