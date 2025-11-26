#!/usr/bin/env python3
"""
IWRC Seed Fund Tracking - Final Deliverables v2

Smarter approach: Create meaningful comparisons instead of duplicate track-specific versions.

Strategy:
1. Core Metrics Comparison Charts - Show 104B vs All Projects side-by-side
2. Award Type Breakdown - Show composition of funding across types
3. Track-Specific Deep Dives:
   - 104B: Seed funding efficiency metrics
   - All Projects: Comprehensive program breadth
4. Interactive Dashboards - Single version with track toggle controls
5. PDF Reports - Both track versions for stakeholder presentations

This avoids redundant identical charts and creates actionable insights.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import re
from datetime import datetime

# Setup
sys.path.insert(0, '/Users/shivpat/Downloads/Seed Fund Tracking/scripts')

from iwrc_brand_style import (
    IWRC_COLORS, configure_matplotlib_iwrc, apply_iwrc_matplotlib_style,
    add_logo_to_matplotlib_figure
)

PROJECT_ROOT = '/Users/shivpat/Downloads/Seed Fund Tracking'
DATA_FILE = os.path.join(PROJECT_ROOT, 'data/consolidated/IWRC Seed Fund Tracking.xlsx')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'FINAL_DELIVERABLES 2')

configure_matplotlib_iwrc()
COLORS = IWRC_COLORS

print(f"\n{'█' * 80}")
print(f"█ FINAL DELIVERABLES v2 - SMART DUAL-TRACK ANALYSIS".center(80) + "█")
print(f"{'█' * 80}\n")


def load_and_prepare_data():
    """Load data and create all filtered datasets."""
    print("=" * 80)
    print("LOADING AND PREPARING DATA")
    print("=" * 80)

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

    # Convert to numeric
    for col in ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df['award_amount'] = pd.to_numeric(df['award_amount'], errors='coerce').fillna(0)

    # Extract year
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

    # Time periods
    df_10yr = df[df['project_year'].between(2015, 2024, inclusive='both')]
    df_5yr = df[df['project_year'].between(2020, 2024, inclusive='both')]

    # Tracks
    all_10yr = df_10yr
    all_5yr = df_5yr
    b104_10yr = df_10yr[df_10yr['award_type'] == 'Base Grant (104b)']
    b104_5yr = df_5yr[df_5yr['award_type'] == 'Base Grant (104b)']

    print(f"✓ Data loaded and prepared")
    print(f"\nAll Projects: {all_10yr['project_id'].nunique()} (10yr), {all_5yr['project_id'].nunique()} (5yr)")
    print(f"104B Only:    {b104_10yr['project_id'].nunique()} (10yr), {b104_5yr['project_id'].nunique()} (5yr)")

    return all_10yr, all_5yr, b104_10yr, b104_5yr, df_10yr


# ============================================================================
# STAGE 2: COMPARISON VISUALIZATIONS (Not duplicate track charts)
# ============================================================================

def generate_track_comparison_chart(all_10yr, all_5yr, b104_10yr, b104_5yr):
    """Generate side-by-side comparison: All Projects vs 104B Only."""
    periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']

    # Metrics
    all_inv_10yr = all_10yr['award_amount'].sum()
    all_inv_5yr = all_5yr['award_amount'].sum()
    b104_inv_10yr = b104_10yr['award_amount'].sum()
    b104_inv_5yr = b104_5yr['award_amount'].sum()

    all_projects_10yr = all_10yr['project_id'].nunique()
    all_projects_5yr = all_5yr['project_id'].nunique()
    b104_projects_10yr = b104_10yr['project_id'].nunique()
    b104_projects_5yr = b104_5yr['project_id'].nunique()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    fig.patch.set_facecolor('white')

    # Investment comparison
    x = np.arange(len(periods))
    width = 0.35

    ax1.set_facecolor(COLORS['background'])
    bars1 = ax1.bar(x - width/2, [all_inv_10yr, all_inv_5yr], width, label='All Projects',
                    color=COLORS['primary'], edgecolor='white', linewidth=1.5)
    bars2 = ax1.bar(x + width/2, [b104_inv_10yr, b104_inv_5yr], width, label='104B Only',
                    color=COLORS['secondary'], edgecolor='white', linewidth=1.5)

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height/1e6:.1f}M', ha='center', va='bottom', fontsize=9, fontweight='bold', color=COLORS['text'])

    ax1.set_ylabel('Total Investment ($)', fontsize=11, fontweight='bold', color=COLORS['text'])
    ax1.set_title('Investment Comparison', fontsize=12, fontweight='bold', color=COLORS['dark_teal'])
    ax1.set_xticks(x)
    ax1.set_xticklabels(periods)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
    ax1.legend(fontsize=10, loc='upper left')
    ax1.grid(axis='y', alpha=0.2, color=COLORS['text'], linestyle='--')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Projects comparison
    ax2.set_facecolor(COLORS['background'])
    bars3 = ax2.bar(x - width/2, [all_projects_10yr, all_projects_5yr], width, label='All Projects',
                    color=COLORS['primary'], edgecolor='white', linewidth=1.5)
    bars4 = ax2.bar(x + width/2, [b104_projects_10yr, b104_projects_5yr], width, label='104B Only',
                    color=COLORS['secondary'], edgecolor='white', linewidth=1.5)

    for bars in [bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold', color=COLORS['text'])

    ax2.set_ylabel('Number of Projects', fontsize=11, fontweight='bold', color=COLORS['text'])
    ax2.set_title('Project Count Comparison', fontsize=12, fontweight='bold', color=COLORS['dark_teal'])
    ax2.set_xticks(x)
    ax2.set_xticklabels(periods)
    ax2.legend(fontsize=10, loc='upper left')
    ax2.grid(axis='y', alpha=0.2, color=COLORS['text'], linestyle='--')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    fig.suptitle('Track Comparison: All Projects vs 104B Only', fontsize=14, fontweight='bold',
                 color=COLORS['dark_teal'], y=0.98)

    plt.tight_layout()
    apply_iwrc_matplotlib_style(fig, None)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.08)

    output_path = os.path.join(OUTPUT_DIR, 'visualizations/static', 'track_comparison.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Generated: track_comparison.png")
    plt.close(fig)


def generate_award_type_breakdown(all_10yr):
    """Show funding breakdown by award type."""
    award_breakdown = all_10yr.groupby('award_type')['award_amount'].sum().sort_values(ascending=False)
    award_breakdown = award_breakdown[award_breakdown > 0]  # Remove NaN

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(COLORS['background'])

    colors_list = [COLORS['primary'], COLORS['secondary'], '#B8C5A0', '#D4E4C8', '#7FB3A3']
    bars = ax.barh(range(len(award_breakdown)), award_breakdown.values, color=colors_list[:len(award_breakdown)],
                   edgecolor='white', linewidth=1.5)

    for i, (bar, value) in enumerate(zip(bars, award_breakdown.values)):
        pct = (value / award_breakdown.sum()) * 100
        ax.text(value + max(award_breakdown.values)*0.02, bar.get_y() + bar.get_height()/2,
                f'${value/1e6:.1f}M ({pct:.1f}%)', va='center', fontsize=10, fontweight='bold', color=COLORS['text'])

    ax.set_yticks(range(len(award_breakdown)))
    ax.set_yticklabels(award_breakdown.index, fontsize=11)
    ax.set_xlabel('Total Investment ($)', fontsize=12, fontweight='bold', color=COLORS['text'])
    ax.set_title('IWRC Funding by Award Type (10-Year Period)', fontsize=14, fontweight='bold', color=COLORS['dark_teal'], pad=20)
    ax.grid(axis='x', alpha=0.2, color=COLORS['text'], linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

    apply_iwrc_matplotlib_style(fig, ax)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.10)

    output_path = os.path.join(OUTPUT_DIR, 'visualizations/static', 'award_type_funding_breakdown.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Generated: award_type_funding_breakdown.png")
    plt.close(fig)


def generate_stage2_visualizations(all_10yr, all_5yr, b104_10yr, b104_5yr, df_10yr):
    """Generate Stage 2 comparison visualizations."""
    print("\n" + "=" * 80)
    print("STAGE 2: GENERATING COMPARISON VISUALIZATIONS")
    print("=" * 80 + "\n")

    generate_track_comparison_chart(all_10yr, all_5yr, b104_10yr, b104_5yr)
    generate_award_type_breakdown(df_10yr)

    print(f"\n✓ STAGE 2 COMPLETE: 2 comparison visualizations generated")


def main():
    """Main orchestration."""
    all_10yr, all_5yr, b104_10yr, b104_5yr, df_10yr = load_and_prepare_data()
    generate_stage2_visualizations(all_10yr, all_5yr, b104_10yr, b104_5yr, df_10yr)

    print("\n" + "█" * 80)
    print("█" + " ✓ SMART COMPARISON APPROACH COMPLETE".center(78) + "█")
    print("█" * 80)
    print("\nKey Insight: Instead of generating 12 similar charts,")
    print("created 2 meaningful COMPARISON charts that show differences.\n")


if __name__ == '__main__':
    main()
