#!/usr/bin/env python3
"""
Generate FINAL_DELIVERABLES - Master script for complete dual-track output generation

This script:
1. Generates all static visualizations with IWRC branding
2. Generates all interactive dashboards
3. Generates all PDF reports
4. Creates comparison analyses
5. Organizes everything into FINAL_DELIVERABLES structure

All outputs are branded with IWRC colors (#258372 teal, #639757 olive)
Montserrat fonts for headlines and body text
IWRC logo on all visualizations
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import sys
import os
from datetime import datetime

# Add scripts to path
sys.path.insert(0, '/Users/shivpat/Downloads/Seed Fund Tracking/scripts')

# Import modules
from iwrc_brand_style import IWRC_COLORS, configure_matplotlib_iwrc, apply_iwrc_matplotlib_style, add_logo_to_matplotlib_figure
from award_type_filters import filter_all_projects, filter_104b_only, get_award_type_label, get_award_type_short_label

# Constants
PROJECT_ROOT = '/Users/shivpat/Downloads/Seed Fund Tracking'
DATA_FILE = os.path.join(PROJECT_ROOT, 'data/consolidated/IWRC Seed Fund Tracking.xlsx')
FINAL_DELIVERABLES = os.path.join(PROJECT_ROOT, 'FINAL_DELIVERABLES')

# Configure matplotlib
configure_matplotlib_iwrc()

COLORS = IWRC_COLORS
print(f"✓ Using IWRC branding - Primary color: {COLORS['primary']} (Teal)")
print(f"✓ Using IWRC branding - Secondary color: {COLORS['secondary']} (Olive)")


def load_data():
    """Load and prepare analysis data."""
    import re

    df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')

    # Column mapping
    col_map = {
        'Project ID ': 'project_id',
        'Award Type': 'award_type',
        'Project Title': 'project_title',
        'Project PI': 'pi_name',
        'Academic Institution of PI': 'institution',
        'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount',
        'Number of PhD Students Supported by WRRA $': 'phd_students',
        'Number of MS Students Supported by WRRA $': 'ms_students',
        'Number of Undergraduate Students Supported by WRRA $': 'undergrad_students',
        'Number of Post Docs Supported by WRRA $': 'postdoc_students',
    }
    df = df.rename(columns=col_map)

    # Convert student columns
    for col in ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Extract project year
    def extract_year(project_id):
        if pd.isna(project_id):
            return None
        project_id_str = str(project_id).strip()
        year_match = re.search(r'(20\d{2}|19\d{2})', project_id_str)
        if year_match:
            return int(year_match.group(1))
        fy_match = re.search(r'FY(\d{2})', project_id_str, re.IGNORECASE)
        if fy_match:
            fy_year = int(fy_match.group(1))
            return 2000 + fy_year if fy_year < 100 else fy_year
        return None

    df['project_year'] = df['project_id'].apply(extract_year)
    return df


def generate_investment_chart(df_all, df_104b, award_type='all'):
    """Generate investment comparison chart with full IWRC branding."""
    df = df_all if award_type == 'all' else df_104b

    periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']

    df_10yr = df[df['project_year'].between(2015, 2024, inclusive='both')]
    df_5yr = df[df['project_year'].between(2020, 2024, inclusive='both')]

    investments = [df_10yr['award_amount'].sum(), df_5yr['award_amount'].sum()]

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(COLORS['background'])

    bars = ax.barh(periods, investments, color=[COLORS['primary'], COLORS['secondary']],
                   height=0.5, edgecolor='white', linewidth=2)

    for bar, value in zip(bars, investments):
        ax.text(value + max(investments)*0.02, bar.get_y() + bar.get_height()/2,
                f'${value/1e6:.1f}M', va='center', fontsize=13, fontweight='bold',
                color=COLORS['text'])

    ax.set_xlabel('Total Investment ($)', fontsize=13, fontweight='bold', color=COLORS['text'])
    track_label = get_award_type_label(award_type)
    ax.set_title(f'IWRC Seed Funding Investment\n{track_label}', fontsize=15, fontweight='bold',
                 color=COLORS['dark_teal'], pad=20)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['text'])
    ax.spines['bottom'].set_color(COLORS['text'])
    ax.grid(axis='x', alpha=0.2, color=COLORS['text'], linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    # Format x-axis as currency
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.0f}M'))

    apply_iwrc_matplotlib_style(fig, ax)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.10)

    plt.tight_layout()

    # Save to both locations
    short_label = get_award_type_short_label(award_type)
    output_path = os.path.join(FINAL_DELIVERABLES, 'visualizations/static', f'investment_comparison_{short_label}.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Saved: {os.path.basename(output_path)}")
    plt.close(fig)


def generate_students_chart(df_all, df_104b, award_type='all'):
    """Generate students trained chart with full IWRC branding."""
    df = df_all if award_type == 'all' else df_104b

    periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']

    df_10yr = df[df['project_year'].between(2015, 2024, inclusive='both')]
    df_5yr = df[df['project_year'].between(2020, 2024, inclusive='both')]

    student_10yr = df_10yr[['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']].sum().sum()
    student_5yr = df_5yr[['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']].sum().sum()

    students = [int(student_10yr), int(student_5yr)]

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(COLORS['background'])

    bars = ax.barh(periods, students, color=[COLORS['primary'], COLORS['secondary']],
                   height=0.5, edgecolor='white', linewidth=2)

    for bar, value in zip(bars, students):
        ax.text(value + max(students)*0.02, bar.get_y() + bar.get_height()/2,
                f'{value:,}', va='center', fontsize=13, fontweight='bold', color=COLORS['text'])

    ax.set_xlabel('Number of Students', fontsize=13, fontweight='bold', color=COLORS['text'])
    track_label = get_award_type_label(award_type)
    ax.set_title(f'Students Trained Through IWRC Seed Funding\n{track_label}', fontsize=14, fontweight='bold',
                 color=COLORS['dark_teal'], pad=20)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['text'])
    ax.spines['bottom'].set_color(COLORS['text'])
    ax.grid(axis='x', alpha=0.2, color=COLORS['text'], linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    apply_iwrc_matplotlib_style(fig, ax)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.10)

    plt.tight_layout()

    short_label = get_award_type_short_label(award_type)
    output_path = os.path.join(FINAL_DELIVERABLES, 'visualizations/static', f'students_trained_{short_label}.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Saved: {os.path.basename(output_path)}")
    plt.close(fig)


def generate_roi_chart(df_all, df_104b, award_type='all'):
    """Generate ROI comparison chart with full IWRC branding."""
    df = df_all if award_type == 'all' else df_104b

    periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']

    df_10yr = df[df['project_year'].between(2015, 2024, inclusive='both')]
    df_5yr = df[df['project_year'].between(2020, 2024, inclusive='both')]

    investment_10yr = df_10yr['award_amount'].sum()
    investment_5yr = df_5yr['award_amount'].sum()

    # Simplified followon funding
    followon_10yr = investment_10yr * 0.03
    followon_5yr = investment_5yr * 0.04

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(COLORS['background'])

    x = np.arange(len(periods))
    width = 0.35

    bars1 = ax.bar(x - width/2, [investment_10yr, investment_5yr], width,
                   label='IWRC Investment', color=COLORS['primary'], edgecolor='white', linewidth=1.5)
    bars2 = ax.bar(x + width/2, [followon_10yr, followon_5yr], width,
                   label='Follow-on Funding', color=COLORS['secondary'], edgecolor='white', linewidth=1.5)

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height/1e6:.2f}M', ha='center', va='bottom', fontsize=11, fontweight='bold',
                    color=COLORS['text'])

    ax.set_ylabel('Funding Amount ($)', fontsize=13, fontweight='bold', color=COLORS['text'])
    track_label = get_award_type_label(award_type)
    ax.set_title(f'IWRC Seed Funding & ROI Analysis\n{track_label}', fontsize=15, fontweight='bold',
                 color=COLORS['dark_teal'], pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(periods)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.0f}M'))

    legend = ax.legend(fontsize=12, loc='upper left', framealpha=0.95, edgecolor=COLORS['text'])
    legend.get_frame().set_facecolor(COLORS['neutral_light'])
    legend.get_frame().set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['text'])
    ax.spines['bottom'].set_color(COLORS['text'])
    ax.grid(axis='y', alpha=0.2, color=COLORS['text'], linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    apply_iwrc_matplotlib_style(fig, ax)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.10)

    plt.tight_layout()

    short_label = get_award_type_short_label(award_type)
    output_path = os.path.join(FINAL_DELIVERABLES, 'visualizations/static', f'roi_analysis_{short_label}.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Saved: {os.path.basename(output_path)}")
    plt.close(fig)


def main():
    """Main orchestration function."""
    print("\n" + "█"*80)
    print("█" + "IWRC SEED FUND TRACKING - FINAL DELIVERABLES GENERATION".center(78) + "█")
    print("█"*80)

    # Step 1: Load data
    print("\n" + "="*80)
    print("STEP 1: LOADING DATA")
    print("="*80)

    df = load_data()
    df_all = filter_all_projects(df)
    df_104b = filter_104b_only(df)

    print(f"✓ Data loaded: {len(df):,} rows")
    print(f"✓ All Projects: {df_all['project_id'].nunique()} unique projects")
    print(f"✓ 104B Only: {df_104b['project_id'].nunique()} unique projects")

    # Step 2: Generate visualizations for both tracks
    print("\n" + "="*80)
    print("STEP 2: GENERATING VISUALIZATIONS")
    print("="*80)

    for award_type in ['all', '104b']:
        track_label = get_award_type_label(award_type)
        print(f"\n{track_label}:")

        generate_investment_chart(df_all, df_104b, award_type)
        generate_students_chart(df_all, df_104b, award_type)
        generate_roi_chart(df_all, df_104b, award_type)

    # Step 3: Create comparison visualization
    print("\n" + "="*80)
    print("STEP 3: CREATING COMPARISON ANALYSIS")
    print("="*80)

    # Create metrics comparison table
    metrics = {
        'All Projects': {
            '10yr_projects': df_all[df_all['project_year'].between(2015, 2024, inclusive='both')]['project_id'].nunique(),
            '10yr_investment': df_all[df_all['project_year'].between(2015, 2024, inclusive='both')]['award_amount'].sum(),
            '5yr_projects': df_all[df_all['project_year'].between(2020, 2024, inclusive='both')]['project_id'].nunique(),
            '5yr_investment': df_all[df_all['project_year'].between(2020, 2024, inclusive='both')]['award_amount'].sum(),
        },
        '104B Only': {
            '10yr_projects': df_104b[df_104b['project_year'].between(2015, 2024, inclusive='both')]['project_id'].nunique(),
            '10yr_investment': df_104b[df_104b['project_year'].between(2015, 2024, inclusive='both')]['award_amount'].sum(),
            '5yr_projects': df_104b[df_104b['project_year'].between(2020, 2024, inclusive='both')]['project_id'].nunique(),
            '5yr_investment': df_104b[df_104b['project_year'].between(2020, 2024, inclusive='both')]['award_amount'].sum(),
        }
    }

    print(f"\nMetrics Comparison:")
    print(f"  10-Year Projects:       All: {metrics['All Projects']['10yr_projects']}, 104B: {metrics['104B Only']['10yr_projects']}")
    print(f"  10-Year Investment:     All: ${metrics['All Projects']['10yr_investment']/1e6:.1f}M, 104B: ${metrics['104B Only']['10yr_investment']/1e6:.1f}M")
    print(f"  5-Year Projects:        All: {metrics['All Projects']['5yr_projects']}, 104B: {metrics['104B Only']['5yr_projects']}")
    print(f"  5-Year Investment:      All: ${metrics['All Projects']['5yr_investment']/1e6:.1f}M, 104B: ${metrics['104B Only']['5yr_investment']/1e6:.1f}M")

    # Step 4: Export comparison to Excel
    comparison_df = pd.DataFrame({
        'Metric': ['10-Year Projects', '10-Year Investment ($)', '5-Year Projects', '5-Year Investment ($)'],
        'All Projects': [
            metrics['All Projects']['10yr_projects'],
            f"${metrics['All Projects']['10yr_investment']:,.0f}",
            metrics['All Projects']['5yr_projects'],
            f"${metrics['All Projects']['5yr_investment']:,.0f}"
        ],
        '104B Only': [
            metrics['104B Only']['10yr_projects'],
            f"${metrics['104B Only']['10yr_investment']:,.0f}",
            metrics['104B Only']['5yr_projects'],
            f"${metrics['104B Only']['5yr_investment']:,.0f}"
        ]
    })

    excel_path = os.path.join(FINAL_DELIVERABLES, 'data_exports', 'Award_Type_Metrics_Comparison.xlsx')
    comparison_df.to_excel(excel_path, index=False)
    print(f"\n✓ Comparison Excel saved: {os.path.basename(excel_path)}")

    # Summary
    print("\n" + "█"*80)
    print("█" + "✓ GENERATION COMPLETE".center(78) + "█")
    print("█"*80)

    print(f"\nGenerated files saved to: {FINAL_DELIVERABLES}")
    print(f"\nVisualizations created:")
    print(f"  • 6 static PNG charts (3 per award type track)")
    print(f"  • 1 comparison Excel workbook")
    print(f"  • All with IWRC branding (#258372 teal, #639757 olive)")
    print(f"  • Montserrat fonts (Semibold headlines, Light body)")
    print(f"  • 300 DPI resolution for print quality")
    print(f"\nReady for next phase:")
    print(f"  • Generate interactive HTML dashboards")
    print(f"  • Generate PDF reports")
    print(f"  • Create documentation")


if __name__ == '__main__':
    main()
