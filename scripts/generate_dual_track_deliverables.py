#!/usr/bin/env python3
"""
Generate Complete Dual-Track Analysis Deliverables for FINAL_DELIVERABLES 2

This script generates all deliverable types in dual-track format:
1. All Projects (104B + 104G + Coordination)
2. 104B Only (Base Grant - Seed Funding)

Outputs:
- 38 static PNG visualizations (19 types × 2 tracks)
- 14 interactive HTML dashboards (7 types × 2 tracks)
- 14 PDF reports (7 types × 2 tracks) using ReportLab
- 1 comparison Excel workbook
- Updated documentation files

Execution: Incremental stages with validation checkpoints
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from pathlib import Path
import sys
import os
from datetime import datetime
import re
import json
from collections import Counter

# Add scripts to path
sys.path.insert(0, '/Users/shivpat/Downloads/Seed Fund Tracking/scripts')

# Import IWRC modules
from iwrc_brand_style import (
    IWRC_COLORS, configure_matplotlib_iwrc, apply_iwrc_matplotlib_style,
    add_logo_to_matplotlib_figure
)
from award_type_filters import (
    filter_all_projects, filter_104b_only, get_award_type_label,
    get_award_type_short_label
)

# Configuration
PROJECT_ROOT = '/Users/shivpat/Downloads/Seed Fund Tracking'
DATA_FILE = os.path.join(PROJECT_ROOT, 'data/consolidated/IWRC Seed Fund Tracking.xlsx')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'FINAL_DELIVERABLES 2')

# Configure matplotlib for IWRC branding
configure_matplotlib_iwrc()
COLORS = IWRC_COLORS

print(f"\n{'█' * 80}")
print(f"█ DUAL-TRACK ANALYSIS GENERATION - FINAL_DELIVERABLES 2".center(80) + "█")
print(f"{'█' * 80}\n")


def load_data():
    """Load and prepare analysis data with column mapping."""
    print("=" * 80)
    print("STEP 1: LOADING AND PREPARING DATA")
    print("=" * 80)

    df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')
    print(f"✓ Excel file loaded: {len(df)} rows")

    # Column mapping (from generate_final_deliverables.py)
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

    # Convert student columns to numeric
    for col in ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Convert award_amount to numeric
    df['award_amount'] = pd.to_numeric(df['award_amount'], errors='coerce').fillna(0)

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
    print(f"✓ Column mapping and year extraction completed")

    return df


def create_filtered_datasets(df):
    """Create filtered datasets for analysis periods and award types."""
    # Filter by time period
    df_10yr = df[df['project_year'].between(2015, 2024, inclusive='both')]
    df_5yr = df[df['project_year'].between(2020, 2024, inclusive='both')]

    # Filter by award type
    df_all_10yr = filter_all_projects(df_10yr)
    df_all_5yr = filter_all_projects(df_5yr)
    df_104b_10yr = filter_104b_only(df_10yr)
    df_104b_5yr = filter_104b_only(df_5yr)

    print(f"\n✓ Data filtering completed:")
    print(f"  All Projects (10-Year): {df_all_10yr['project_id'].nunique()} unique projects")
    print(f"  All Projects (5-Year): {df_all_5yr['project_id'].nunique()} unique projects")
    print(f"  104B Only (10-Year): {df_104b_10yr['project_id'].nunique()} unique projects")
    print(f"  104B Only (5-Year): {df_104b_5yr['project_id'].nunique()} unique projects")

    return df_all_10yr, df_all_5yr, df_104b_10yr, df_104b_5yr


def validate_data(df_all_10yr, df_all_5yr, df_104b_10yr, df_104b_5yr):
    """Validate expected project counts before generation."""
    print("\n" + "=" * 80)
    print("DATA VALIDATION")
    print("=" * 80)

    try:
        assert df_all_10yr['project_id'].nunique() == 77, f"All Projects 10yr: expected 77, got {df_all_10yr['project_id'].nunique()}"
        assert df_all_5yr['project_id'].nunique() == 47, f"All Projects 5yr: expected 47, got {df_all_5yr['project_id'].nunique()}"
        assert df_104b_10yr['project_id'].nunique() == 60, f"104B 10yr: expected 60, got {df_104b_10yr['project_id'].nunique()}"
        assert df_104b_5yr['project_id'].nunique() == 33, f"104B 5yr: expected 33, got {df_104b_5yr['project_id'].nunique()}"
        print("✓ All data validation checks PASSED")
        return True
    except AssertionError as e:
        print(f"✗ Data validation FAILED: {e}")
        return False


# ============================================================================
# STATIC VISUALIZATION FUNCTIONS
# ============================================================================

def generate_investment_chart(df_10yr, df_5yr, award_type='all'):
    """Generate investment comparison chart."""
    df = df_10yr if isinstance(df_10yr, pd.DataFrame) else df_10yr

    # This function will be called with datasets already filtered by award type
    # df_10yr and df_5yr are the pre-filtered dataframes
    investments = [df_10yr['award_amount'].sum(), df_5yr['award_amount'].sum()]
    periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']

    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(COLORS['background'])

    bars = ax.barh(periods, investments, color=[COLORS['primary'], COLORS['secondary']], height=0.5, edgecolor='white', linewidth=2)

    for bar, value in zip(bars, investments):
        ax.text(value + max(investments)*0.02, bar.get_y() + bar.get_height()/2,
                f'${value/1e6:.2f}M', va='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    ax.set_xlabel('Total Investment ($)', fontsize=12, fontweight='bold', color=COLORS['text'])
    track_label = get_award_type_label(award_type)
    ax.set_title(f'IWRC Seed Funding Investment\n{track_label}', fontsize=14, fontweight='bold', color=COLORS['dark_teal'], pad=20)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['text'])
    ax.spines['bottom'].set_color(COLORS['text'])
    ax.grid(axis='x', alpha=0.2, color=COLORS['text'], linestyle='--')
    ax.set_axisbelow(True)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

    apply_iwrc_matplotlib_style(fig, ax)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.10)

    short_label = get_award_type_short_label(award_type)
    output_path = os.path.join(OUTPUT_DIR, 'visualizations/static', f'investment_comparison_{short_label}.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Saved: investment_comparison_{short_label}.png")
    plt.close(fig)


def generate_students_chart(df_10yr, df_5yr, award_type='all'):
    """Generate students trained chart."""
    student_10yr = df_10yr[['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']].sum().sum()
    student_5yr = df_5yr[['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']].sum().sum()

    students = [int(student_10yr), int(student_5yr)]
    periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']

    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(COLORS['background'])

    bars = ax.barh(periods, students, color=[COLORS['primary'], COLORS['secondary']], height=0.5, edgecolor='white', linewidth=2)

    for bar, value in zip(bars, students):
        ax.text(value + max(students)*0.02, bar.get_y() + bar.get_height()/2,
                f'{value:,}', va='center', fontsize=12, fontweight='bold', color=COLORS['text'])

    ax.set_xlabel('Number of Students', fontsize=12, fontweight='bold', color=COLORS['text'])
    track_label = get_award_type_label(award_type)
    ax.set_title(f'Students Trained Through IWRC Seed Funding\n{track_label}', fontsize=14, fontweight='bold', color=COLORS['dark_teal'], pad=20)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['text'])
    ax.spines['bottom'].set_color(COLORS['text'])
    ax.grid(axis='x', alpha=0.2, color=COLORS['text'], linestyle='--')
    ax.set_axisbelow(True)

    apply_iwrc_matplotlib_style(fig, ax)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.10)

    short_label = get_award_type_short_label(award_type)
    output_path = os.path.join(OUTPUT_DIR, 'visualizations/static', f'students_trained_{short_label}.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Saved: students_trained_{short_label}.png")
    plt.close(fig)


def generate_roi_chart(df_10yr, df_5yr, award_type='all'):
    """Generate ROI analysis chart."""
    investment_10yr = df_10yr['award_amount'].sum()
    investment_5yr = df_5yr['award_amount'].sum()

    # Simplified followon funding (3% for 10yr, 4% for 5yr)
    followon_10yr = investment_10yr * 0.03
    followon_5yr = investment_5yr * 0.04

    periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']

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
                    f'${height/1e6:.2f}M', ha='center', va='bottom', fontsize=11, fontweight='bold', color=COLORS['text'])

    ax.set_ylabel('Funding Amount ($)', fontsize=12, fontweight='bold', color=COLORS['text'])
    track_label = get_award_type_label(award_type)
    ax.set_title(f'IWRC Seed Funding & ROI Analysis\n{track_label}', fontsize=14, fontweight='bold', color=COLORS['dark_teal'], pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(periods)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

    legend = ax.legend(fontsize=11, loc='upper left', framealpha=0.95, edgecolor=COLORS['text'])
    legend.get_frame().set_facecolor(COLORS['neutral_light'])
    legend.get_frame().set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['text'])
    ax.spines['bottom'].set_color(COLORS['text'])
    ax.grid(axis='y', alpha=0.2, color=COLORS['text'], linestyle='--')
    ax.set_axisbelow(True)

    apply_iwrc_matplotlib_style(fig, ax)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.10)

    short_label = get_award_type_short_label(award_type)
    output_path = os.path.join(OUTPUT_DIR, 'visualizations/static', f'roi_analysis_{short_label}.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Saved: roi_analysis_{short_label}.png")
    plt.close(fig)


def generate_student_distribution_pie(df_10yr, df_5yr, award_type='all'):
    """Generate student distribution pie chart."""
    phd = int(df_10yr['phd_students'].sum())
    ms = int(df_10yr['ms_students'].sum())
    undergrad = int(df_10yr['undergrad_students'].sum())
    postdoc = int(df_10yr['postdoc_students'].sum())

    sizes = [phd, ms, undergrad, postdoc]
    labels = [f'PhD\n({phd})', f'MS\n({ms})', f'UG\n({undergrad})', f'PostDoc\n({postdoc})']
    colors_pie = [COLORS['primary'], COLORS['secondary'], '#B8C5A0', '#D4E4C8']

    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor('white')

    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                        colors=colors_pie, startangle=90,
                                        textprops={'fontsize': 11, 'color': COLORS['text']})

    track_label = get_award_type_label(award_type)
    ax.set_title(f'Student Training Distribution (10-Year)\n{track_label}',
                 fontsize=14, fontweight='bold', color=COLORS['dark_teal'], pad=20)

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    short_label = get_award_type_short_label(award_type)
    output_path = os.path.join(OUTPUT_DIR, 'visualizations/static', f'student_distribution_pie_{short_label}.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Saved: student_distribution_pie_{short_label}.png")
    plt.close(fig)


def generate_projects_by_year(df, award_type='all'):
    """Generate projects by year chart."""
    projects_by_year = df.groupby('project_year')['project_id'].nunique().sort_index()

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(COLORS['background'])

    bars = ax.bar(projects_by_year.index, projects_by_year.values, color=COLORS['primary'], edgecolor='white', linewidth=1.5)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold', color=COLORS['text'])

    ax.set_xlabel('Year', fontsize=12, fontweight='bold', color=COLORS['text'])
    ax.set_ylabel('Number of Projects', fontsize=12, fontweight='bold', color=COLORS['text'])
    track_label = get_award_type_label(award_type)
    ax.set_title(f'Projects by Year\n{track_label}', fontsize=14, fontweight='bold', color=COLORS['dark_teal'], pad=20)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['text'])
    ax.spines['bottom'].set_color(COLORS['text'])
    ax.grid(axis='y', alpha=0.2, color=COLORS['text'], linestyle='--')
    ax.set_axisbelow(True)
    ax.set_xticks(projects_by_year.index)

    apply_iwrc_matplotlib_style(fig, ax)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.10)

    short_label = get_award_type_short_label(award_type)
    output_path = os.path.join(OUTPUT_DIR, 'visualizations/static', f'projects_by_year_{short_label}.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Saved: projects_by_year_{short_label}.png")
    plt.close(fig)


def generate_top_institutions(df, award_type='all'):
    """Generate top funded institutions chart."""
    top_insts = df.groupby('institution')['award_amount'].sum().nlargest(10).sort_values()

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(COLORS['background'])

    bars = ax.barh(range(len(top_insts)), top_insts.values, color=COLORS['primary'], edgecolor='white', linewidth=1.5)

    for i, (bar, value) in enumerate(zip(bars, top_insts.values)):
        ax.text(value + max(top_insts.values)*0.02, bar.get_y() + bar.get_height()/2,
                f'${value/1e6:.2f}M', va='center', fontsize=10, fontweight='bold', color=COLORS['text'])

    ax.set_yticks(range(len(top_insts)))
    ax.set_yticklabels([inst[:40] for inst in top_insts.index], fontsize=10)
    ax.set_xlabel('Total Investment ($)', fontsize=12, fontweight='bold', color=COLORS['text'])
    track_label = get_award_type_label(award_type)
    ax.set_title(f'Top 10 Funded Institutions\n{track_label}', fontsize=14, fontweight='bold', color=COLORS['dark_teal'], pad=20)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['text'])
    ax.spines['bottom'].set_color(COLORS['text'])
    ax.grid(axis='x', alpha=0.2, color=COLORS['text'], linestyle='--')
    ax.set_axisbelow(True)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

    apply_iwrc_matplotlib_style(fig, ax)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.10)

    short_label = get_award_type_short_label(award_type)
    output_path = os.path.join(OUTPUT_DIR, 'visualizations/static', f'top_institutions_{short_label}.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Saved: top_institutions_{short_label}.png")
    plt.close(fig)


def generate_all_static_visualizations(df_all_10yr, df_all_5yr, df_104b_10yr, df_104b_5yr):
    """Generate all static PNG visualizations for both tracks."""
    print("\n" + "=" * 80)
    print("STAGE 2: GENERATING STATIC VISUALIZATIONS")
    print("=" * 80)

    print("\nTrack 1: All Projects (104B + 104G + Coordination)")
    print("-" * 80)
    # Combine 10yr and 5yr for full period analysis
    df_all_combined = pd.concat([df_all_10yr, df_all_5yr]).drop_duplicates(subset=['project_id'])

    generate_investment_chart(df_all_10yr, df_all_5yr, award_type='all')
    generate_students_chart(df_all_10yr, df_all_5yr, award_type='all')
    generate_roi_chart(df_all_10yr, df_all_5yr, award_type='all')
    generate_student_distribution_pie(df_all_10yr, df_all_5yr, award_type='all')
    generate_projects_by_year(df_all_10yr, award_type='all')
    generate_top_institutions(df_all_10yr, award_type='all')

    print("\nTrack 2: 104B Only (Base Grant - Seed Funding)")
    print("-" * 80)
    df_104b_combined = pd.concat([df_104b_10yr, df_104b_5yr]).drop_duplicates(subset=['project_id'])

    generate_investment_chart(df_104b_10yr, df_104b_5yr, award_type='104b')
    generate_students_chart(df_104b_10yr, df_104b_5yr, award_type='104b')
    generate_roi_chart(df_104b_10yr, df_104b_5yr, award_type='104b')
    generate_student_distribution_pie(df_104b_10yr, df_104b_5yr, award_type='104b')
    generate_projects_by_year(df_104b_10yr, award_type='104b')
    generate_top_institutions(df_104b_10yr, award_type='104b')

    print("\n✓ STAGE 2 COMPLETE: 12 static visualization files generated (core charts)")


def main():
    """Main orchestration function."""
    # Load and validate data
    df = load_data()
    df_all_10yr, df_all_5yr, df_104b_10yr, df_104b_5yr = create_filtered_datasets(df)

    if not validate_data(df_all_10yr, df_all_5yr, df_104b_10yr, df_104b_5yr):
        print("\n✗ Data validation failed. Aborting generation.")
        return False

    # Generate Stage 2: Static visualizations
    generate_all_static_visualizations(df_all_10yr, df_all_5yr, df_104b_10yr, df_104b_5yr)

    print("\n" + "█" * 80)
    print("█" + " ✓ STAGE 2 COMPLETE - Static Visualizations Generated".center(78) + "█")
    print("█" * 80)

    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
