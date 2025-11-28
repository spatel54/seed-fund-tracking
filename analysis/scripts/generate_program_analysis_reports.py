#!/usr/bin/env python3
"""
Generate Fresh IWRC Reports - CORRECTED VERSION

This script replaces generate_fresh_reports.py which had double-counting errors.

Key Improvements:
- Uses IWRCDataLoader for proper deduplication
- Calculates metrics correctly (no double-counting)
- Applies IWRC branding (Montserrat font)
- Generates clean PDF reports

Generates:
1. IWRC_Program_Summary.pdf
2. IWRC_Analysis_Deep_Dive.pdf

Author: IWRC Data Quality Team
Date: November 27, 2025
Version: 1.0 (CORRECTED)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import sys
from pathlib import Path
from datetime import datetime

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import IWRC modules
from iwrc_brand_style import IWRC_COLORS, configure_matplotlib_iwrc, apply_iwrc_matplotlib_style
from iwrc_data_loader import IWRCDataLoader

# Configure matplotlib with IWRC branding
configure_matplotlib_iwrc()

# Configuration
BASE_DIR = Path("/Users/shivpat/seed-fund-tracking")
OUTPUT_DIR = BASE_DIR / "FINAL_DELIVERABLES_2_backup_20251125_194954 copy 2/reports/fresh"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Font family constant
FONT_FAMILY = "Montserrat"


def create_header(ax, title, subtitle=None):
    """Create a standard IWRC header."""
    ax.add_patch(plt.Rectangle((0, 0.90), 1, 0.10, facecolor=IWRC_COLORS['primary'], transform=ax.transAxes))
    ax.text(0.5, 0.96, title, ha='center', fontsize=16, fontweight='bold', color='white', 
            transform=ax.transAxes, family=FONT_FAMILY)
    if subtitle:
        ax.text(0.5, 0.92, subtitle, ha='center', fontsize=12, style='italic', color='white', 
                transform=ax.transAxes, family=FONT_FAMILY)


def generate_program_summary(df, metrics):
    """Generate IWRC_Program_Summary.pdf with CORRECTED metrics"""
    pdf_path = OUTPUT_DIR / 'IWRC_Program_Summary.pdf'
    print(f"Generating {pdf_path}...")
    
    with PdfPages(pdf_path) as pdf:
        # Page 1: Executive Summary
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        create_header(ax, 'IWRC SEED FUND PROGRAM', 'Program Summary & Impact')
        
        # Display Metrics
        y_start = 0.75
        metric_values = [
            ('Total Investment', f"${metrics['investment']:,.0f}"),
            ('Projects Funded', f"{metrics['projects']}"),
            ('Students Supported', f"{metrics['students']}"),
            ('Institutions Served', f"{df['institution'].nunique()}")
        ]
        
        for i, (label, value) in enumerate(metric_values):
            x = 0.25 if i % 2 == 0 else 0.75
            y = y_start if i < 2 else y_start - 0.15
            
            ax.text(x, y, value, ha='center', fontsize=24, fontweight='bold', 
                   color=IWRC_COLORS['primary'], transform=ax.transAxes, family=FONT_FAMILY)
            ax.text(x, y-0.04, label, ha='center', fontsize=12, color=IWRC_COLORS['text'], 
                   transform=ax.transAxes, family=FONT_FAMILY)
            
        # Student Breakdown Chart
        ax_chart = fig.add_axes([0.15, 0.15, 0.7, 0.35])
        student_types = ['PhD', "Master's", 'Undergrad', 'PostDoc']
        student_counts = [metrics['phd'], metrics['masters'], metrics['undergrad'], metrics['postdoc']]
        
        bars = ax_chart.bar(student_types, student_counts, color=IWRC_COLORS['secondary'])
        ax_chart.set_title('Student Training by Degree Level', fontsize=12, fontweight='bold', 
                           color=IWRC_COLORS['dark_teal'], family=FONT_FAMILY)
        
        # Add margins to prevent label cutoff
        ax_chart.margins(y=0.2)
        
        apply_iwrc_matplotlib_style(fig, ax_chart)
        
        # Add labels
        for bar in bars:
            height = bar.get_height()
            ax_chart.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', color=IWRC_COLORS['text'], family=FONT_FAMILY)
        
        pdf.savefig(fig)
        plt.close()
        
        # Page 2: Institutional Reach
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_subplot(111)
        ax.axis('off')
        create_header(ax, 'INSTITUTIONAL REACH', 'Supporting Research Across Illinois')
        
        # Top Institutions Chart
        inst_counts = df['institution'].value_counts().head(10)
        # Increased left margin from 0.15 to 0.4 to accommodate long institution names
        ax_chart = fig.add_axes([0.4, 0.2, 0.5, 0.6])
        y_pos = np.arange(len(inst_counts))
        
        bars = ax_chart.barh(y_pos, inst_counts.values, color=IWRC_COLORS['primary'])
        ax_chart.set_yticks(y_pos)
        ax_chart.set_yticklabels(inst_counts.index, family=FONT_FAMILY)
        ax_chart.invert_yaxis()
        ax_chart.set_xlabel('Number of Projects', family=FONT_FAMILY)
        ax_chart.set_title('Top 10 Institutions by Projects Funded', fontsize=12, 
                          fontweight='bold', color=IWRC_COLORS['dark_teal'], family=FONT_FAMILY)
        
        # Add margins to prevent label cutoff
        ax_chart.margins(x=0.2)
        
        apply_iwrc_matplotlib_style(fig, ax_chart)
        
        # Add value labels to horizontal bars
        for i, v in enumerate(inst_counts.values):
            ax_chart.text(v + 0.5, i, str(v), color=IWRC_COLORS['text'], 
                         va='center', fontweight='bold', family=FONT_FAMILY)
        
        pdf.savefig(fig)
        plt.close()
    
    print(f"✓ Saved: {pdf_path}")


def generate_analysis_deep_dive(df):
    """Generate IWRC_Analysis_Deep_Dive.pdf"""
    pdf_path = OUTPUT_DIR / 'IWRC_Analysis_Deep_Dive.pdf'
    print(f"Generating {pdf_path}...")
    
    with PdfPages(pdf_path) as pdf:
        # Page 1: Financial Overview
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_subplot(111)
        ax.axis('off')
        create_header(ax, 'ANALYSIS DEEP DIVE', 'Financial & Research Insights')
        
        # Award Type Analysis
        ax_chart = fig.add_axes([0.15, 0.5, 0.7, 0.3])
        award_type_counts = df['award_type'].value_counts()
        award_type_counts = award_type_counts[award_type_counts > 1]
        
        colors = [IWRC_COLORS['primary'], IWRC_COLORS['secondary'], 
                 IWRC_COLORS['accent'], IWRC_COLORS['light_teal']]
        
        # Use legend instead of labels to prevent overlap
        # Hide percentages < 3% to prevent overlap
        wedges, texts, autotexts = ax_chart.pie(award_type_counts, labels=None, 
                                               autopct=lambda p: f'{p:.1f}%' if p >= 3 else '', 
                                               pctdistance=0.75,
                                               colors=colors, startangle=90,
                                               textprops={'family': FONT_FAMILY, 'color': 'white', 'weight': 'bold'})
        
        # Add legend
        ax_chart.legend(wedges, award_type_counts.index,
                       title="Award Types",
                       loc="center left",
                       bbox_to_anchor=(0.9, 0, 0.5, 1))
                       
        ax_chart.set_title('Distribution of Award Types', fontsize=12, fontweight='bold', 
                          color=IWRC_COLORS['dark_teal'], family=FONT_FAMILY)
        
        # Research Topics (Keywords)
        # Increased left margin from 0.15 to 0.4 to accommodate long labels
        ax_topics = fig.add_axes([0.4, 0.1, 0.5, 0.3])
        # Use science_priority if available
        if 'science_priority' in df.columns:
            keywords = df['science_priority'].dropna()
        else:
            keywords = pd.Series(dtype=str)
        
        if len(keywords) > 0:
            top_keywords = keywords.value_counts().head(8)
            
            bars = ax_topics.barh(np.arange(len(top_keywords)), top_keywords.values, 
                                 color=IWRC_COLORS['sage'])
            ax_topics.set_yticks(np.arange(len(top_keywords)))
            ax_topics.set_yticklabels(top_keywords.index, family=FONT_FAMILY)
            ax_topics.invert_yaxis()
            ax_topics.set_title('Top Research Topics', fontsize=12, fontweight='bold', 
                              color=IWRC_COLORS['dark_teal'], family=FONT_FAMILY)
            
            # Add margins to prevent label cutoff
            ax_topics.margins(x=0.2)
            
            apply_iwrc_matplotlib_style(fig, ax_topics)
            
            # Add value labels to horizontal bars
            for i, v in enumerate(top_keywords.values):
                ax_topics.text(v + 0.5, i, str(v), color=IWRC_COLORS['text'], 
                             va='center', fontweight='bold', family=FONT_FAMILY)
        
        pdf.savefig(fig)
        plt.close()
    
    print(f"✓ Saved: {pdf_path}")


def main():
    """Main execution function."""
    print("="*80)
    print("GENERATE FRESH IWRC REPORTS - CORRECTED VERSION")
    print("="*80)
    print("\nThis script uses IWRCDataLoader for proper deduplication.")
    print("Replacing generate_fresh_reports.py which had double-counting errors.\n")
    
    # Initialize loader
    print("="*80)
    print("STEP 1: Load Data with Deduplication")
    print("="*80)
    loader = IWRCDataLoader()
    df = loader.load_master_data(deduplicate=True)
    
    # Calculate metrics using CORRECTED loader
    print("\n" + "="*80)
    print("STEP 2: Calculate Metrics (10-Year Period)")
    print("="*80)
    metrics = loader.calculate_metrics(df, period='10yr')
    
    print(f"  Projects: {metrics['projects']}")
    print(f"  Investment: ${metrics['investment']:,.2f}")
    print(f"  Students: {metrics['students']}")
    print(f"  Institutions: {metrics['institutions']}")
    
    # Generate PDFs
    print("\n" + "="*80)
    print("STEP 3: Generate PDF Reports")
    print("="*80)
    
    generate_program_summary(df, metrics)
    generate_analysis_deep_dive(df)
    
    print("\n" + "="*80)
    print("✅ FRESH REPORTS GENERATED SUCCESSFULLY")
    print("="*80)
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print(f"  - IWRC_Program_Summary.pdf")
    print(f"  - IWRC_Analysis_Deep_Dive.pdf")
    print("\n✅ All metrics use CORRECTED values (no double-counting)")
    print("="*80)


if __name__ == "__main__":
    main()
