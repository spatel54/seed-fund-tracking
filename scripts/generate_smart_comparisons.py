#!/usr/bin/env python3
"""
Smart Dual-Track Visualizations - Focus on EFFICIENCY, not totals

Key Insight: 104B has MORE projects (78%) but LESS funding (20%)
This reveals 104B's TRUE value: seed funding efficiency

Visualizations that tell the real story:
1. Stacked bar: Show composition (104B + Other = All Projects)
2. Efficiency metrics: Cost per student, cost per project
3. Impact per dollar: Students/projects per $1M invested
4. Award size distribution: 104B is smaller, more numerous
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import re

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
print(f"█ SMART DUAL-TRACK COMPARISONS - Efficiency-Focused Visualizations".center(80) + "█")
print(f"{'█' * 80}\n")


def load_data():
    """Load and prepare data."""
    df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')

    col_map = {
        'Project ID ': 'project_id',
        'Award Type': 'award_type',
        'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount',
        'Number of PhD Students Supported by WRRA $': 'phd_students',
        'Number of MS Students Supported by WRRA $': 'ms_students',
        'Number of Undergraduate Students Supported by WRRA $': 'undergrad_students',
        'Number of Post Docs Supported by WRRA $': 'postdoc_students',
        'Academic Institution of PI': 'institution',
    }
    df = df.rename(columns=col_map)

    for col in ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df['award_amount'] = pd.to_numeric(df['award_amount'], errors='coerce').fillna(0)

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


def calculate_metrics(df_all, df_104b):
    """Calculate efficiency metrics for both tracks."""
    metrics = {}

    # Total metrics
    metrics['all_projects'] = df_all['project_id'].nunique()
    metrics['all_investment'] = df_all['award_amount'].sum()
    metrics['all_students'] = int(df_all[['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']].sum().sum())

    metrics['b104_projects'] = df_104b['project_id'].nunique()
    metrics['b104_investment'] = df_104b['award_amount'].sum()
    metrics['b104_students'] = int(df_104b[['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']].sum().sum())

    metrics['other_projects'] = metrics['all_projects'] - metrics['b104_projects']
    metrics['other_investment'] = metrics['all_investment'] - metrics['b104_investment']
    metrics['other_students'] = metrics['all_students'] - metrics['b104_students']

    # Efficiency metrics
    metrics['all_cost_per_project'] = metrics['all_investment'] / metrics['all_projects']
    metrics['b104_cost_per_project'] = metrics['b104_investment'] / metrics['b104_projects']
    metrics['other_cost_per_project'] = metrics['other_investment'] / metrics['other_projects'] if metrics['other_projects'] > 0 else 0

    metrics['all_cost_per_student'] = metrics['all_investment'] / metrics['all_students']
    metrics['b104_cost_per_student'] = metrics['b104_investment'] / metrics['b104_students']
    metrics['other_cost_per_student'] = metrics['other_investment'] / metrics['other_students'] if metrics['other_students'] > 0 else 0

    # Impact per dollar
    metrics['all_projects_per_m'] = metrics['all_projects'] / (metrics['all_investment'] / 1e6)
    metrics['b104_projects_per_m'] = metrics['b104_projects'] / (metrics['b104_investment'] / 1e6)
    metrics['other_projects_per_m'] = metrics['other_projects'] / (metrics['other_investment'] / 1e6) if metrics['other_investment'] > 0 else 0

    metrics['all_students_per_m'] = metrics['all_students'] / (metrics['all_investment'] / 1e6)
    metrics['b104_students_per_m'] = metrics['b104_students'] / (metrics['b104_investment'] / 1e6)
    metrics['other_students_per_m'] = metrics['other_students'] / (metrics['other_investment'] / 1e6) if metrics['other_investment'] > 0 else 0

    return metrics


def generate_composition_stacked_bar(metrics):
    """Generate stacked bar showing 104B + Other = All Projects."""
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(COLORS['background'])

    # Create stacked data
    categories = ['Funding\nInvestment', 'Projects', 'Students\nTrained']
    all_vals = [metrics['all_investment']/1e6, metrics['all_projects'], metrics['all_students']]
    b104_vals = [metrics['b104_investment']/1e6, metrics['b104_projects'], metrics['b104_students']]
    other_vals = [metrics['other_investment']/1e6, metrics['other_projects'], metrics['other_students']]

    x = np.arange(len(categories))
    width = 0.4

    bars1 = ax.bar(x - width/2, b104_vals, width, label='104B (Seed Funding)',
                   color=COLORS['primary'], edgecolor='white', linewidth=1.5)
    bars2 = ax.bar(x - width/2, other_vals, width, bottom=b104_vals, label='104G + Coordination',
                   color=COLORS['secondary'], edgecolor='white', linewidth=1.5)

    # Add value labels
    for i, (b, o, total) in enumerate(zip(b104_vals, other_vals, all_vals)):
        # 104B label
        ax.text(i - width/2, b/2, f'{b:.1f}' if i == 0 else f'{int(b)}',
                ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        # Other label
        ax.text(i - width/2, b + o/2, f'{o:.1f}' if i == 0 else f'{int(o)}',
                ha='center', va='center', fontsize=10, fontweight='bold', color='white')

    ax.set_ylabel('Amount', fontsize=12, fontweight='bold', color=COLORS['text'])
    ax.set_title('IWRC Funding Composition: 104B vs Other Awards (10-Year)',
                 fontsize=14, fontweight='bold', color=COLORS['dark_teal'], pad=20)
    ax.set_xticks(x - width/2)
    ax.set_xticklabels(categories)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(axis='y', alpha=0.2, color=COLORS['text'], linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    apply_iwrc_matplotlib_style(fig, ax)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.10)

    output_path = os.path.join(OUTPUT_DIR, 'visualizations/static', 'composition_stacked.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Generated: composition_stacked.png")
    plt.close(fig)


def generate_efficiency_metrics(metrics):
    """Generate efficiency comparison chart."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('white')

    # Cost per project
    ax1.set_facecolor(COLORS['background'])
    tracks = ['104B\n(Seed Funding)', 'Other Awards\n(104G + Coord)', 'All Projects\n(Average)']
    costs = [metrics['b104_cost_per_project']/1e3, metrics['other_cost_per_project']/1e3,
             metrics['all_cost_per_project']/1e3]
    colors_bar = [COLORS['primary'], COLORS['secondary'], '#7FB3A3']

    bars1 = ax1.bar(tracks, costs, color=colors_bar, edgecolor='white', linewidth=1.5)
    for bar, cost in zip(bars1, costs):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.0f}K', ha='center', va='bottom', fontsize=10, fontweight='bold', color=COLORS['text'])

    ax1.set_ylabel('Cost per Project ($1000s)', fontsize=11, fontweight='bold', color=COLORS['text'])
    ax1.set_title('Cost per Project Comparison', fontsize=12, fontweight='bold', color=COLORS['dark_teal'])
    ax1.grid(axis='y', alpha=0.2, color=COLORS['text'], linestyle='--')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Cost per student
    ax2.set_facecolor(COLORS['background'])
    costs_student = [metrics['b104_cost_per_student']/1e3, metrics['other_cost_per_student']/1e3,
                     metrics['all_cost_per_student']/1e3]

    bars2 = ax2.bar(tracks, costs_student, color=colors_bar, edgecolor='white', linewidth=1.5)
    for bar, cost in zip(bars2, costs_student):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.0f}K', ha='center', va='bottom', fontsize=10, fontweight='bold', color=COLORS['text'])

    ax2.set_ylabel('Cost per Student ($1000s)', fontsize=11, fontweight='bold', color=COLORS['text'])
    ax2.set_title('Cost per Student Comparison', fontsize=12, fontweight='bold', color=COLORS['dark_teal'])
    ax2.grid(axis='y', alpha=0.2, color=COLORS['text'], linestyle='--')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    fig.suptitle('Efficiency Metrics: Where IWRC Funding is Most Efficient',
                 fontsize=14, fontweight='bold', color=COLORS['dark_teal'], y=0.98)
    plt.tight_layout()
    apply_iwrc_matplotlib_style(fig, None)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.08)

    output_path = os.path.join(OUTPUT_DIR, 'visualizations/static', 'efficiency_metrics.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Generated: efficiency_metrics.png")
    plt.close(fig)


def generate_impact_per_dollar(metrics):
    """Generate impact per dollar invested - designed for maximum clarity."""
    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor('white')

    # Create custom grid
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, :])

    # ========== TOP LEFT: Projects per $1M ==========
    ax1.set_facecolor(COLORS['background'])
    b104_proj_per_m = metrics['b104_projects_per_m']
    other_proj_per_m = metrics['other_projects_per_m']

    tracks_1 = ['104B\n(Seed)', 'Other Awards\n(Strategic)']
    values_1 = [b104_proj_per_m, other_proj_per_m]
    colors_1 = [COLORS['primary'], COLORS['secondary']]

    bars1 = ax1.bar(tracks_1, values_1, color=colors_1, edgecolor='white', linewidth=2, width=0.5)

    # Add values with comparison multiplier
    for i, (bar, val) in enumerate(zip(bars1, values_1)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}', ha='center', va='bottom', fontsize=13, fontweight='bold', color=COLORS['text'])

        # Add efficiency multiplier for 104B
        if i == 0:
            multiplier = b104_proj_per_m / other_proj_per_m
            ax1.text(bar.get_x() + bar.get_width()/2., height/2,
                    f'{multiplier:.1f}x\nmore\nefficient', ha='center', va='center',
                    fontsize=11, fontweight='bold', color='white',
                    bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['dark_teal'], alpha=0.8))

    ax1.set_ylabel('Projects per $1M Invested', fontsize=11, fontweight='bold', color=COLORS['text'])
    ax1.set_title('Project Creation Efficiency', fontsize=12, fontweight='bold', color=COLORS['dark_teal'])
    ax1.set_ylim(0, max(values_1) * 1.3)
    ax1.grid(axis='y', alpha=0.2, color=COLORS['text'], linestyle='--')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color(COLORS['text'])
    ax1.spines['bottom'].set_color(COLORS['text'])

    # ========== TOP RIGHT: Students per $1M ==========
    ax2.set_facecolor(COLORS['background'])
    b104_stud_per_m = metrics['b104_students_per_m']
    other_stud_per_m = metrics['other_students_per_m']

    values_2 = [b104_stud_per_m, other_stud_per_m]

    bars2 = ax2.bar(tracks_1, values_2, color=colors_1, edgecolor='white', linewidth=2, width=0.5)

    for i, (bar, val) in enumerate(zip(bars2, values_2)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{height:.0f}', ha='center', va='bottom', fontsize=13, fontweight='bold', color=COLORS['text'])

        # Add efficiency multiplier for 104B
        if i == 0:
            multiplier = b104_stud_per_m / other_stud_per_m
            ax2.text(bar.get_x() + bar.get_width()/2., height/2,
                    f'{multiplier:.1f}x\nmore\nstudents', ha='center', va='center',
                    fontsize=11, fontweight='bold', color='white',
                    bbox=dict(boxstyle='round,pad=0.4', facecolor=COLORS['dark_teal'], alpha=0.8))

    ax2.set_ylabel('Students per $1M Invested', fontsize=11, fontweight='bold', color=COLORS['text'])
    ax2.set_title('Student Training Efficiency', fontsize=12, fontweight='bold', color=COLORS['dark_teal'])
    ax2.set_ylim(0, max(values_2) * 1.3)
    ax2.grid(axis='y', alpha=0.2, color=COLORS['text'], linestyle='--')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(COLORS['text'])
    ax2.spines['bottom'].set_color(COLORS['text'])

    # ========== BOTTOM: Large efficiency comparison ==========
    ax3.set_facecolor('white')
    ax3.axis('off')

    # Create efficiency table
    efficiency_text = f"""
    IMPACT PER $1 MILLION INVESTED

    104B (Seed Funding)                                Other Awards (Strategic)
    ────────────────────────────────────────────────────────────────────────────

    ✓ {b104_proj_per_m:.1f} projects created                    ✓ {other_proj_per_m:.1f} projects created
    ✓ {b104_stud_per_m:.0f} students trained                    ✓ {other_stud_per_m:.0f} students trained
    ✓ ${metrics['b104_cost_per_project']/1e3:.0f}K average per project        ✓ ${metrics['other_cost_per_project']/1e3:.0f}K average per project

    104B IS {b104_proj_per_m/other_proj_per_m:.1f}x MORE EFFICIENT AT CREATING PROJECTS
    104B TRAINS {b104_stud_per_m/other_stud_per_m:.1f}x MORE STUDENTS PER DOLLAR

    KEY INSIGHT: 104B maximizes breadth through many small-grant projects,
    while Other Awards focus on depth with larger, strategic initiatives.
    """

    ax3.text(0.5, 0.5, efficiency_text, transform=ax3.transAxes,
            fontsize=10, verticalalignment='center', horizontalalignment='center',
            family='monospace', color=COLORS['text'],
            bbox=dict(boxstyle='round,pad=1', facecolor=COLORS['background'], edgecolor=COLORS['primary'], linewidth=2))

    fig.suptitle('Impact per Dollar: The 104B Advantage',
                 fontsize=15, fontweight='bold', color=COLORS['dark_teal'], y=0.97)

    apply_iwrc_matplotlib_style(fig, None)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.08)

    output_path = os.path.join(OUTPUT_DIR, 'visualizations/static', 'impact_per_dollar.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"  ✓ Generated: impact_per_dollar.png (redesigned for clarity)")
    plt.close(fig)


def main():
    """Main orchestration."""
    print("=" * 80)
    print("LOADING AND CALCULATING METRICS")
    print("=" * 80)

    df = load_data()
    df_10yr = df[df['project_year'].between(2015, 2024, inclusive='both')]
    df_all = df_10yr
    df_104b = df_10yr[df_10yr['award_type'] == 'Base Grant (104b)']

    metrics = calculate_metrics(df_all, df_104b)

    print(f"✓ Data loaded and metrics calculated")
    print(f"\n104B Efficiency: ${metrics['b104_cost_per_project']/1e3:.0f}K per project, {metrics['b104_projects_per_m']:.1f} projects per $1M")
    print(f"Other Awards:   ${metrics['other_cost_per_project']/1e3:.0f}K per project, {metrics['other_projects_per_m']:.1f} projects per $1M")

    print("\n" + "=" * 80)
    print("GENERATING SMART COMPARISON VISUALIZATIONS")
    print("=" * 80 + "\n")

    generate_composition_stacked_bar(metrics)
    generate_efficiency_metrics(metrics)
    generate_impact_per_dollar(metrics)

    print(f"\n✓ SMART COMPARISONS COMPLETE")
    print(f"\nKey Insight: 104B is {metrics['b104_projects_per_m']/metrics['other_projects_per_m']:.1f}x more efficient")
    print(f"at creating projects per dollar invested!")


if __name__ == '__main__':
    main()
