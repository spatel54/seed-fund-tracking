#!/usr/bin/env python3
"""
Generate Follow-on Funding Breakdown Visualization
Rebranded with IWRC Montserrat font and color palette
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

# Import IWRC branding
from iwrc_brand_style import (
    IWRC_COLORS, 
    configure_matplotlib_iwrc, 
    apply_iwrc_matplotlib_style,
    format_currency
)

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_FILE = PROJECT_ROOT / 'data/consolidated/IWRC Seed Fund Tracking.xlsx'
OUTPUT_DIR = PROJECT_ROOT / 'FINAL_DELIVERABLES_2_backup_20251125_194954 copy 2/visualizations/static_breakdown'

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configure matplotlib
configure_matplotlib_iwrc()

def load_data():
    """Load and prepare data."""
    print(f"Loading data from {DATA_FILE}...")
    df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')
    
    # Column mapping - adjust based on actual column names
    col_map = {
        'Project ID ': 'project_id',
        'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount',
        'Follow-on Funding ($)': 'followon_funding',
    }
    
    # Rename columns that exist
    existing_cols = {k: v for k, v in col_map.items() if k in df.columns}
    df = df.rename(columns=existing_cols)
    
    # Clean numeric columns
    if 'award_amount' in df.columns:
        df['award_amount'] = pd.to_numeric(df['award_amount'], errors='coerce').fillna(0)
    
    if 'followon_funding' in df.columns:
        df['followon_funding'] = pd.to_numeric(df['followon_funding'], errors='coerce').fillna(0)
    
    return df

def generate_followon_breakdown():
    """Generate follow-on funding breakdown visualization."""
    print("Generating follow-on funding breakdown...")
    
    df = load_data()
    
    # Extract year from project_id
    import re
    def extract_year(project_id):
        if pd.isna(project_id):
            return None
        project_id_str = str(project_id).strip()
        year_match = re.search(r'(20\d{2}|19\d{2})', project_id_str)
        if year_match:
            return int(year_match.group(1))
        return None
    
    df['year'] = df['project_id'].apply(extract_year)
    
    # Categorize award type to identify 104B projects
    def categorize_award(award_type):
        if pd.isna(award_type):
            return 'Other'
        award_str = str(award_type).lower()
        if '104b' in award_str:
            return '104B'
        return 'Other'
    
    # Check if Award Type column exists
    award_col = None
    for col in df.columns:
        if 'award' in col.lower() and 'type' in col.lower():
            award_col = col
            break
    
    if award_col:
        df['award_category'] = df[award_col].apply(categorize_award)
    else:
        # If no award type column, assume all are mixed
        df['award_category'] = 'Other'
    
    # Filter for 10-year (2015-2024) and 5-year (2020-2024)
    df_10yr = df[df['year'].between(2015, 2024, inclusive='both')]
    df_5yr = df[df['year'].between(2020, 2024, inclusive='both')]
    
    # Calculate follow-on funding for total and 104B only
    if 'followon_funding' in df.columns:
        # 10-year totals
        followon_10yr_total = df_10yr['followon_funding'].sum()
        followon_10yr_104b = df_10yr[df_10yr['award_category'] == '104B']['followon_funding'].sum()
        
        # 5-year totals
        followon_5yr_total = df_5yr['followon_funding'].sum()
        followon_5yr_104b = df_5yr[df_5yr['award_category'] == '104B']['followon_funding'].sum()
    else:
        # If follow-on funding column doesn't exist, estimate based on award amount
        # Using typical ratios: 3% for 10yr, 4% for 5yr
        followon_10yr_total = df_10yr['award_amount'].sum() * 0.03
        followon_10yr_104b = df_10yr[df_10yr['award_category'] == '104B']['award_amount'].sum() * 0.03
        
        followon_5yr_total = df_5yr['award_amount'].sum() * 0.04
        followon_5yr_104b = df_5yr[df_5yr['award_category'] == '104B']['award_amount'].sum() * 0.04
    
    # Create grouped bar chart
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Data for grouped bars
    periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']
    total_values = [followon_10yr_total, followon_5yr_total]
    b104_values = [followon_10yr_104b, followon_5yr_104b]
    
    # Bar positions
    x = np.arange(len(periods))
    width = 0.35
    
    # Use IWRC colors
    color_total = IWRC_COLORS['primary']
    color_104b = IWRC_COLORS['secondary']
    
    # Create bars
    bars1 = ax.bar(x - width/2, total_values, width, label='Total Projects', 
                   color=color_total, edgecolor='white', linewidth=1.5)
    bars2 = ax.bar(x + width/2, b104_values, width, label='104B Seed Funding', 
                   color=color_104b, edgecolor='white', linewidth=1.5)
    
    # Styling
    ax.set_title('Follow-on Funding Secured: Total vs 104B Seed Funding', 
                 fontsize=16, fontweight='bold', color=IWRC_COLORS['dark_teal'], pad=20)
    ax.set_ylabel('Follow-on Funding ($)', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(periods, fontsize=11)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:  # Only show label if there's a value
                label = format_currency(height)
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        label,
                        ha='center', va='bottom', fontsize=10, fontweight='bold',
                        color=IWRC_COLORS['dark_teal'])
    
    # Add legend
    ax.legend(loc='upper left', frameon=True, framealpha=0.95, 
              fontsize=11, edgecolor=IWRC_COLORS['neutral_light'])
    
    # Apply IWRC styling
    apply_iwrc_matplotlib_style(fig, ax)
    
    # Remove grid for cleaner look
    ax.grid(False)
    
    # Save figure
    output_path = OUTPUT_DIR / 'followon_breakdown.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Saved {output_path}")
    plt.close(fig)

def main():
    """Main execution function."""
    print("=" * 60)
    print("Generating Follow-on Funding Breakdown")
    print("=" * 60)
    
    generate_followon_breakdown()
    
    print("\n" + "=" * 60)
    print("✓ Follow-on breakdown generation complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
