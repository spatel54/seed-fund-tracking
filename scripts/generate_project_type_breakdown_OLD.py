#!/usr/bin/env python3
"""
Generate Project Type Breakdown Analysis for IWRC Seed Fund

Creates stacked/grouped visualizations showing composition by project type
(104B, 104G combined, Coordination) for 5-year and 10-year periods.

Outputs to FINAL_DELIVERABLES_3/:
- 16 static PNG charts (8 per track)
- 2 interactive HTML dashboards
- 2 PDF reports
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib import colors as rl_colors
from pathlib import Path
import sys
import os
import re
from datetime import datetime

# Add scripts to path
sys.path.insert(0, '/Users/shivpat/Downloads/Seed Fund Tracking/scripts')

# Import IWRC modules
from iwrc_brand_style import (
    IWRC_COLORS, configure_matplotlib_iwrc, apply_iwrc_matplotlib_style,
    add_logo_to_matplotlib_figure, apply_iwrc_plotly_style
)
from award_type_filters import (
    filter_all_projects, filter_104b_only, get_award_type_label,
    get_award_type_short_label
)

# Configuration
PROJECT_ROOT = '/Users/shivpat/Downloads/Seed Fund Tracking'
DATA_FILE = os.path.join(PROJECT_ROOT, 'data/consolidated/IWRC Seed Fund Tracking.xlsx')
OUTPUT_DIR = Path(PROJECT_ROOT) / 'FINAL_DELIVERABLES_3'

# Configure matplotlib for IWRC branding
configure_matplotlib_iwrc()
COLORS = IWRC_COLORS

print(f"\n{'█' * 80}")
print(f"█ PROJECT TYPE BREAKDOWN ANALYSIS - FINAL_DELIVERABLES_3".center(80) + "█")
print(f"{'█' * 80}\n")


# ============================================================================
# DATA PROCESSING FUNCTIONS
# ============================================================================

def get_project_type_category(award_type):
    """
    Categorize award types into simplified groups.

    Returns:
        '104B' - Base Grant (104b)
        '104G' - All 104g variants (AIS, General, PFAS combined)
        'Coordination' - Coordination Grant
        'Other' - Anything else
    """
    if pd.isna(award_type):
        return 'Other'

    award_str = str(award_type).strip()

    # Exact match for 104B
    if award_str == 'Base Grant (104b)':
        return '104B'

    # All 104g variants combined
    if '104g' in award_str.lower():
        return '104G'

    # Coordination grants
    if 'coordination' in award_str.lower():
        return 'Coordination'

    return 'Other'


def aggregate_by_project_type(df):
    """
    Aggregate all metrics by project type category.

    Returns DataFrame with columns:
    - project_type_category: '104B', '104G', 'Coordination'
    - unique_projects: count of unique project_id
    - total_investment: sum of award_amount
    - total_students: sum of all student types
    - phd_students, ms_students, undergrad_students, postdoc_students: sums
    - institutions: count of unique institutions
    - avg_investment_per_project: calculated
    - investment_pct: percentage of total
    - projects_pct: percentage of total
    """
    # Add project type category column
    df = df.copy()
    df['project_type_category'] = df['award_type'].apply(get_project_type_category)

    # Aggregate by type
    agg_dict = {
        'project_id': 'nunique',
        'award_amount': 'sum',
        'phd_students': 'sum',
        'ms_students': 'sum',
        'undergrad_students': 'sum',
        'postdoc_students': 'sum',
        'institution': 'nunique'
    }

    grouped = df.groupby('project_type_category').agg(agg_dict).reset_index()

    # Rename columns
    grouped = grouped.rename(columns={
        'project_id': 'unique_projects',
        'award_amount': 'total_investment',
        'institution': 'institutions'
    })

    # Calculate derived metrics
    grouped['total_students'] = (
        grouped['phd_students'] + grouped['ms_students'] +
        grouped['undergrad_students'] + grouped['postdoc_students']
    )

    grouped['avg_investment_per_project'] = (
        grouped['total_investment'] / grouped['unique_projects']
    ).fillna(0)

    # Calculate percentages
    total_investment = grouped['total_investment'].sum()
    total_projects = grouped['unique_projects'].sum()

    if total_investment > 0:
        grouped['investment_pct'] = (grouped['total_investment'] / total_investment * 100)
    else:
        grouped['investment_pct'] = 0

    if total_projects > 0:
        grouped['projects_pct'] = (grouped['unique_projects'] / total_projects * 100)
    else:
        grouped['projects_pct'] = 0

    return grouped


def extract_year_from_project_id(project_id):
    """Extract year from project ID."""
    if pd.isna(project_id):
        return None

    project_id_str = str(project_id).strip()

    # Look for 4-digit years (2015-2024 range)
    year_match = re.search(r'(20\d{2}|19\d{2})', project_id_str)
    if year_match:
        return int(year_match.group(1))

    # Fall back to FY format (FY20 = 2020)
    fy_match = re.search(r'FY(\d{2})', project_id_str, re.IGNORECASE)
    if fy_match:
        fy_year = int(fy_match.group(1))
        return 2000 + fy_year if fy_year < 100 else fy_year

    return None


def load_data():
    """Load and prepare analysis data with column mapping."""
    print("=" * 80)
    print("STEP 1: LOADING AND PREPARING DATA")
    print("=" * 80)

    df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')
    print(f"✓ Excel file loaded: {len(df)} rows")

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

    # Convert student columns to numeric
    for col in ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Convert award_amount to numeric
    df['award_amount'] = pd.to_numeric(df['award_amount'], errors='coerce').fillna(0)

    # Extract project year
    df['project_year'] = df['project_id'].apply(extract_year_from_project_id)

    print(f"✓ Columns mapped and converted to numeric")
    print(f"✓ Years extracted from project IDs")

    return df


def filter_data(df):
    """Filter data to time periods and award types."""
    print("\n" + "=" * 80)
    print("STEP 2: FILTERING DATA TO TIME PERIODS AND AWARD TYPES")
    print("=" * 80)

    # Filter to time periods
    df_10yr = df[df['project_year'].between(2015, 2024, inclusive='both')].copy()
    df_5yr = df[df['project_year'].between(2020, 2024, inclusive='both')].copy()

    print(f"✓ 10-year period (2015-2024): {len(df_10yr)} rows, {df_10yr['project_id'].nunique()} unique projects")
    print(f"✓ 5-year period (2020-2024): {len(df_5yr)} rows, {df_5yr['project_id'].nunique()} unique projects")

    # Apply dual-track filters
    df_all_10yr = filter_all_projects(df_10yr)
    df_all_5yr = filter_all_projects(df_5yr)
    df_104b_10yr = filter_104b_only(df_10yr)
    df_104b_5yr = filter_104b_only(df_5yr)

    print(f"\nTrack 1: All Projects (104B + 104G + Coordination)")
    print(f"  10-year: {df_all_10yr['project_id'].nunique()} unique projects")
    print(f"  5-year: {df_all_5yr['project_id'].nunique()} unique projects")

    print(f"\nTrack 2: 104B Only (Base Grant - Seed Funding)")
    print(f"  10-year: {df_104b_10yr['project_id'].nunique()} unique projects")
    print(f"  5-year: {df_104b_5yr['project_id'].nunique()} unique projects")

    return df_all_10yr, df_all_5yr, df_104b_10yr, df_104b_5yr


# ============================================================================
# STATIC VISUALIZATION FUNCTIONS
# ============================================================================

def generate_stacked_bar_chart(df_10yr, df_5yr, award_type, metric='investment'):
    """Generate stacked bar chart showing composition by project type."""
    # Aggregate data
    data_10yr = aggregate_by_project_type(df_10yr)
    data_5yr = aggregate_by_project_type(df_5yr)

    # Set up figure with explicit backend
    plt.clf()  # Clear any existing plots
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(COLORS['background'])

    # Define project types and colors
    project_types = ['104B', '104G', 'Coordination']
    colors_map = {
        '104B': COLORS['primary'],      # #258372 teal
        '104G': COLORS['secondary'],    # #639757 olive
        'Coordination': COLORS['accent'] # #FCC080 peach
    }

    # Get metric column name
    metric_col = {
        'investment': 'total_investment',
        'projects': 'unique_projects',
        'students': 'total_students'
    }[metric]

    # Build stacked bars
    periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']
    x_pos = [0, 1]
    bottom_vals = [0, 0]

    for ptype in project_types:
        # Get values for this type
        val_10yr = data_10yr[data_10yr['project_type_category'] == ptype][metric_col].values
        val_5yr = data_5yr[data_5yr['project_type_category'] == ptype][metric_col].values

        # Handle missing types
        val_10yr = val_10yr[0] if len(val_10yr) > 0 else 0
        val_5yr = val_5yr[0] if len(val_5yr) > 0 else 0

        values = [val_10yr, val_5yr]

        # Plot bars
        bars = ax.bar(x_pos, values, bottom=bottom_vals,
                     label=ptype, color=colors_map[ptype],
                     edgecolor='white', linewidth=2, width=0.5)

        # Add value labels in center of each segment
        for i, (bar, val, bottom) in enumerate(zip(bars, values, bottom_vals)):
            if val > 0:  # Only label non-zero segments
                # Format value based on metric
                if metric == 'investment':
                    label = f'${val/1e6:.2f}M'
                else:
                    label = f'{int(val)}'

                ax.text(bar.get_x() + bar.get_width()/2,
                       bottom + val/2,
                       label, ha='center', va='center',
                       fontsize=11, fontweight='bold', color='white')

        # Update bottom for next stack
        bottom_vals = [bottom_vals[i] + val for i, val in enumerate(values)]

    # Add total labels on top
    for i, (x, total) in enumerate(zip(x_pos, bottom_vals)):
        if total > 0:
            if metric == 'investment':
                total_label = f'${total/1e6:.2f}M'
            else:
                total_label = f'{int(total)}'
            ax.text(x, total, total_label, ha='center', va='bottom',
                   fontsize=12, fontweight='bold', color=COLORS['text'])

    # Styling
    ax.set_xticks(x_pos)
    ax.set_xticklabels(periods, fontsize=12, fontweight='bold')

    ylabel = {
        'investment': 'Total Investment ($)',
        'projects': 'Number of Projects',
        'students': 'Students Trained'
    }[metric]
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold', color=COLORS['text'])

    track_label = get_award_type_label(award_type)
    title = f'{ylabel} by Project Type\n{track_label}'
    ax.set_title(title, fontsize=14, fontweight='bold',
                color=COLORS['dark_teal'], pad=20)

    # Legend
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95,
             title='Project Type', title_fontsize=12)

    # Apply IWRC styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.2, linestyle='--')

    apply_iwrc_matplotlib_style(fig, ax)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.10)

    # Save
    short_label = get_award_type_short_label(award_type)
    filename = f'project_type_stacked_{metric}_{short_label}.png'
    output_dir = OUTPUT_DIR / 'visualizations/static' / short_label.lower().replace(' ', '_')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"  ✓ Saved: {filename}")
    plt.close(fig)


def generate_grouped_bar_chart(df_10yr, df_5yr, award_type, metric='investment'):
    """Generate grouped bar chart comparing project types across periods."""
    # Get data
    data_10yr = aggregate_by_project_type(df_10yr)
    data_5yr = aggregate_by_project_type(df_5yr)

    # Get metric column name
    metric_col = {
        'investment': 'total_investment',
        'projects': 'unique_projects',
        'students': 'total_students'
    }[metric]

    project_types = ['104B', '104G', 'Coordination']

    # Extract values for each type
    values_10yr = []
    values_5yr = []
    for ptype in project_types:
        val_10yr = data_10yr[data_10yr['project_type_category'] == ptype][metric_col].values
        val_5yr = data_5yr[data_5yr['project_type_category'] == ptype][metric_col].values

        values_10yr.append(val_10yr[0] if len(val_10yr) > 0 else 0)
        values_5yr.append(val_5yr[0] if len(val_5yr) > 0 else 0)

    # Set up figure with explicit backend
    plt.clf()  # Clear any existing plots
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(COLORS['background'])

    # Plot grouped bars
    x = np.arange(len(project_types))
    width = 0.35

    bars1 = ax.bar(x - width/2, values_10yr, width,
                   label='10-Year (2015-2024)', color=COLORS['primary'],
                   edgecolor='white', linewidth=1.5)
    bars2 = ax.bar(x + width/2, values_5yr, width,
                   label='5-Year (2020-2024)', color=COLORS['secondary'],
                   edgecolor='white', linewidth=1.5)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                if metric == 'investment':
                    label = f'${height/1e6:.1f}M'
                else:
                    label = f'{int(height)}'
                ax.text(bar.get_x() + bar.get_width()/2, height,
                       label, ha='center', va='bottom',
                       fontsize=10, fontweight='bold')

    # Styling
    ax.set_xticks(x)
    ax.set_xticklabels(project_types, fontsize=12, fontweight='bold')
    ax.set_xlabel('Project Type', fontsize=12, fontweight='bold', color=COLORS['text'])

    ylabel = {
        'investment': 'Total Investment ($)',
        'projects': 'Number of Projects',
        'students': 'Students Trained'
    }[metric]
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold', color=COLORS['text'])

    track_label = get_award_type_label(award_type)
    title = f'{ylabel} Comparison by Project Type\n{track_label}'
    ax.set_title(title, fontsize=14, fontweight='bold',
                color=COLORS['dark_teal'], pad=20)

    # Legend
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95)

    # Apply IWRC styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.2, linestyle='--')

    apply_iwrc_matplotlib_style(fig, ax)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.10)

    # Save
    short_label = get_award_type_short_label(award_type)
    filename = f'project_type_grouped_{metric}_{short_label}.png'
    output_dir = OUTPUT_DIR / 'visualizations/static' / short_label.lower().replace(' ', '_')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"  ✓ Saved: {filename}")
    plt.close(fig)


def generate_composition_pie_charts(df, period, award_type):
    """Generate composition pie charts for a given period."""
    data = aggregate_by_project_type(df)

    # Filter to only relevant types (exclude 'Other' if present)
    data = data[data['project_type_category'].isin(['104B', '104G', 'Coordination'])]

    if len(data) == 0:
        print(f"  ⚠ No data for {period} {award_type} - skipping pie charts")
        return

    # Set up figure with explicit backend
    plt.clf()  # Clear any existing plots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 6))
    fig.patch.set_facecolor('white')

    colors_list = [COLORS['primary'], COLORS['secondary'], COLORS['accent']]

    # Pie 1: Investment
    if data['total_investment'].sum() > 0:
        ax1.pie(data['total_investment'], labels=data['project_type_category'],
               autopct='%1.1f%%', colors=colors_list[:len(data)], startangle=90,
               textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax1.set_title('Investment Distribution', fontsize=12, fontweight='bold',
                     color=COLORS['dark_teal'])

    # Pie 2: Projects
    if data['unique_projects'].sum() > 0:
        ax2.pie(data['unique_projects'], labels=data['project_type_category'],
               autopct='%1.1f%%', colors=colors_list[:len(data)], startangle=90,
               textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax2.set_title('Project Distribution', fontsize=12, fontweight='bold',
                     color=COLORS['dark_teal'])

    # Pie 3: Students
    if data['total_students'].sum() > 0:
        ax3.pie(data['total_students'], labels=data['project_type_category'],
               autopct='%1.1f%%', colors=colors_list[:len(data)], startangle=90,
               textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax3.set_title('Student Distribution', fontsize=12, fontweight='bold',
                     color=COLORS['dark_teal'])

    # Overall title
    track_label = get_award_type_label(award_type)
    fig.suptitle(f'Project Type Composition - {period}\n{track_label}',
                fontsize=14, fontweight='bold', color=COLORS['dark_teal'])

    plt.tight_layout()

    # Save
    short_label = get_award_type_short_label(award_type)
    period_label = '10yr' if '10' in period else '5yr'
    filename = f'project_type_composition_{period_label}_{short_label}.png'
    output_dir = OUTPUT_DIR / 'visualizations/static' / short_label.lower().replace(' ', '_')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"  ✓ Saved: {filename}")
    plt.close(fig)


# ============================================================================
# INTERACTIVE VISUALIZATION FUNCTIONS
# ============================================================================

def generate_interactive_composition_dashboard(df_10yr, df_5yr, award_type):
    """Generate interactive Plotly dashboard with project type breakdowns."""
    # Get data
    data_10yr = aggregate_by_project_type(df_10yr)
    data_5yr = aggregate_by_project_type(df_5yr)

    # Filter to relevant types
    data_10yr = data_10yr[data_10yr['project_type_category'].isin(['104B', '104G', 'Coordination'])]
    data_5yr = data_5yr[data_5yr['project_type_category'].isin(['104B', '104G', 'Coordination'])]

    # Create subplot grid
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Investment by Project Type',
            'Projects by Project Type',
            'Students by Project Type',
            'Summary Metrics'
        ),
        specs=[
            [{'type': 'bar'}, {'type': 'bar'}],
            [{'type': 'bar'}, {'type': 'table'}]
        ],
        vertical_spacing=0.12,
        horizontal_spacing=0.12
    )

    project_types = ['104B', '104G', 'Coordination']
    colors_map = {
        '104B': COLORS['primary'],
        '104G': COLORS['secondary'],
        'Coordination': COLORS['accent']
    }

    # Panel 1: Investment (stacked bars)
    for ptype in project_types:
        values_10yr = data_10yr[data_10yr['project_type_category'] == ptype]['total_investment'].values
        values_5yr = data_5yr[data_5yr['project_type_category'] == ptype]['total_investment'].values

        fig.add_trace(
            go.Bar(
                x=['10-Year', '5-Year'],
                y=[values_10yr[0] if len(values_10yr) > 0 else 0,
                   values_5yr[0] if len(values_5yr) > 0 else 0],
                name=ptype,
                marker_color=colors_map[ptype],
                hovertemplate='<b>%{x}</b><br>Investment: $%{y:,.0f}<extra></extra>',
                legendgroup=ptype,
                showlegend=True
            ),
            row=1, col=1
        )

    # Panel 2: Projects (grouped bars)
    for ptype in project_types:
        values_10yr = data_10yr[data_10yr['project_type_category'] == ptype]['unique_projects'].values
        values_5yr = data_5yr[data_5yr['project_type_category'] == ptype]['unique_projects'].values

        fig.add_trace(
            go.Bar(
                x=[ptype],
                y=[values_10yr[0] if len(values_10yr) > 0 else 0],
                name='10-Year',
                marker_color=COLORS['primary'],
                hovertemplate='<b>%{x}</b><br>Projects: %{y}<extra></extra>',
                showlegend=False
            ),
            row=1, col=2
        )

        fig.add_trace(
            go.Bar(
                x=[ptype],
                y=[values_5yr[0] if len(values_5yr) > 0 else 0],
                name='5-Year',
                marker_color=COLORS['secondary'],
                hovertemplate='<b>%{x}</b><br>Projects: %{y}<extra></extra>',
                showlegend=False
            ),
            row=1, col=2
        )

    # Panel 3: Students (stacked)
    for ptype in project_types:
        values_10yr = data_10yr[data_10yr['project_type_category'] == ptype]['total_students'].values
        values_5yr = data_5yr[data_5yr['project_type_category'] == ptype]['total_students'].values

        fig.add_trace(
            go.Bar(
                x=['10-Year', '5-Year'],
                y=[values_10yr[0] if len(values_10yr) > 0 else 0,
                   values_5yr[0] if len(values_5yr) > 0 else 0],
                name=ptype,
                marker_color=colors_map[ptype],
                hovertemplate='<b>%{x}</b><br>Students: %{y}<extra></extra>',
                legendgroup=ptype,
                showlegend=False
            ),
            row=2, col=1
        )

    # Panel 4: Summary table
    summary_data = pd.concat([
        data_10yr.assign(Period='10-Year'),
        data_5yr.assign(Period='5-Year')
    ])

    fig.add_trace(
        go.Table(
            header=dict(
                values=['<b>Period</b>', '<b>Type</b>', '<b>Projects</b>', '<b>Investment</b>', '<b>Students</b>'],
                fill_color=COLORS['primary'],
                font=dict(color='white', size=11),
                align='left'
            ),
            cells=dict(
                values=[
                    summary_data['Period'],
                    summary_data['project_type_category'],
                    summary_data['unique_projects'].astype(int),
                    summary_data['total_investment'].apply(lambda x: f'${x:,.0f}'),
                    summary_data['total_students'].astype(int)
                ],
                fill_color='white',
                align='left',
                font=dict(size=10)
            )
        ),
        row=2, col=2
    )

    # Update layout
    fig.update_xaxes(title_text="Time Period", row=1, col=1)
    fig.update_xaxes(title_text="Project Type", row=1, col=2)
    fig.update_xaxes(title_text="Time Period", row=2, col=1)

    fig.update_yaxes(title_text="Investment ($)", row=1, col=1)
    fig.update_yaxes(title_text="Number of Projects", row=1, col=2)
    fig.update_yaxes(title_text="Students Trained", row=2, col=1)

    track_label = get_award_type_label(award_type)
    fig.update_layout(
        title=f'Project Type Composition Analysis<br><sub>{track_label}</sub>',
        barmode='stack',
        height=900,
        showlegend=True,
        template='plotly_white',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        # Apply IWRC colors manually
        font=dict(
            family='Montserrat, sans-serif',
            size=11,
            color=COLORS['text']
        ),
        paper_bgcolor='white',
        plot_bgcolor=COLORS['background']
    )

    # Save
    short_label = get_award_type_short_label(award_type)
    filename = f'project_type_interactive_{short_label}.html'
    output_path = OUTPUT_DIR / 'visualizations/interactive' / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_path)
    print(f"  ✓ Saved: {filename}")


# ============================================================================
# PDF REPORT FUNCTIONS
# ============================================================================

def generate_project_type_pdf_report(df_10yr, df_5yr, award_type):
    """Generate comprehensive PDF report with project type analysis."""
    short_label = get_award_type_short_label(award_type)
    filename = f'project_type_analysis_{short_label}.pdf'
    output_path = OUTPUT_DIR / 'reports' / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Create PDF
    doc = SimpleDocTemplate(str(output_path), pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=rl_colors.HexColor('#258372'),
        spaceAfter=30,
        alignment=1  # Center
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=rl_colors.HexColor('#258372'),
        spaceAfter=12
    )

    # Page 1: Title & Overview
    track_label = get_award_type_label(award_type)
    story.append(Paragraph(f"Project Type Breakdown Analysis", title_style))
    story.append(Paragraph(f"{track_label}", heading_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))

    # Summary stats
    data_10yr = aggregate_by_project_type(df_10yr)
    data_5yr = aggregate_by_project_type(df_5yr)

    story.append(Paragraph("Overview", heading_style))
    story.append(Paragraph(
        f"This report analyzes IWRC Seed Fund projects broken down by project type "
        f"(104B Base Grants, 104G Programs, and Coordination Grants) across two time periods: "
        f"10-year (2015-2024) and 5-year (2020-2024).",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.2*inch))

    # Key metrics table
    story.append(Paragraph("Key Metrics Summary", heading_style))

    metrics_data = [['Period', 'Project Type', 'Projects', 'Investment', 'Students']]
    for period_name, data in [('10-Year', data_10yr), ('5-Year', data_5yr)]:
        for _, row in data.iterrows():
            if row['project_type_category'] in ['104B', '104G', 'Coordination']:
                metrics_data.append([
                    period_name,
                    row['project_type_category'],
                    str(int(row['unique_projects'])),
                    f"${row['total_investment']:,.0f}",
                    str(int(row['total_students']))
                ])

    metrics_table = Table(metrics_data, colWidths=[1*inch, 1.2*inch, 0.8*inch, 1.3*inch, 0.8*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), rl_colors.HexColor('#258372')),
        ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), rl_colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, rl_colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    story.append(metrics_table)

    story.append(PageBreak())

    # Page 2: Key Findings
    story.append(Paragraph("Key Findings", heading_style))

    # Calculate insights
    total_10yr = data_10yr['total_investment'].sum()
    total_5yr = data_5yr['total_investment'].sum()

    if total_10yr > 0:
        pct_104b = (data_10yr[data_10yr['project_type_category']=='104B']['total_investment'].sum() / total_10yr * 100) if len(data_10yr[data_10yr['project_type_category']=='104B']) > 0 else 0
        pct_104g = (data_10yr[data_10yr['project_type_category']=='104G']['total_investment'].sum() / total_10yr * 100) if len(data_10yr[data_10yr['project_type_category']=='104G']) > 0 else 0
        pct_coord = (data_10yr[data_10yr['project_type_category']=='Coordination']['total_investment'].sum() / total_10yr * 100) if len(data_10yr[data_10yr['project_type_category']=='Coordination']) > 0 else 0

        findings = [
            f"<b>Investment Distribution (10-Year):</b> 104B represents {pct_104b:.1f}% of total investment, "
            f"104G represents {pct_104g:.1f}%, and Coordination represents {pct_coord:.1f}%.",

            f"<b>Total Investment:</b> ${total_10yr:,.0f} over 10 years (2015-2024), "
            f"${total_5yr:,.0f} over 5 years (2020-2024).",

            f"<b>Project Types:</b> The analysis includes Base Grants (104B) for seed funding, "
            f"104G Programs (AIS, General, PFAS combined), and Coordination Grants for administrative support.",
        ]

        for finding in findings:
            story.append(Paragraph(finding, styles['Normal']))
            story.append(Spacer(1, 0.1*inch))

    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Methodology", heading_style))
    story.append(Paragraph(
        "Data was extracted from the IWRC Seed Fund Tracking database, filtered to relevant time periods, "
        "and aggregated by project type category. 104G variants (AIS, General, PFAS) were combined into a "
        "single category for clarity. Metrics include unique project counts (not duplicate rows), actual "
        "investment amounts, and students trained across all degree levels.",
        styles['Normal']
    ))

    # Build PDF
    doc.build(story)
    print(f"  ✓ Saved: {filename}")


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_project_type_data(df_all_10yr, df_all_5yr, df_104b_10yr, df_104b_5yr):
    """Validate project type data before generation."""
    print("\n" + "=" * 80)
    print("STEP 3: VALIDATING PROJECT TYPE DATA")
    print("=" * 80)

    # 1. All Projects should have multiple types
    types_all = df_all_10yr['award_type'].nunique()
    print(f"✓ All Projects has {types_all} different award types")

    # 2. 104B Only should have exactly one type
    types_104b = df_104b_10yr['award_type'].nunique()
    print(f"✓ 104B Only has {types_104b} award type (expected: 1)")

    # 3. Investment totals should be consistent
    total_all = df_all_10yr['award_amount'].sum()
    total_104b = df_104b_10yr['award_amount'].sum()
    print(f"✓ Investment totals: All Projects ${total_all:,.0f}, 104B Only ${total_104b:,.0f}")

    # 4. Check for null award types
    null_count = df_all_10yr['award_type'].isna().sum()
    print(f"✓ Null award types in All Projects: {null_count}")

    # 5. Show project type distribution
    print(f"\nProject Type Distribution (10-Year All Projects):")
    df_all_10yr_copy = df_all_10yr.copy()
    df_all_10yr_copy['project_type_category'] = df_all_10yr_copy['award_type'].apply(get_project_type_category)
    dist = df_all_10yr_copy.groupby('project_type_category')['project_id'].nunique()
    for ptype, count in dist.items():
        print(f"  {ptype}: {count} unique projects")

    print("\n✓ Project type data validation complete")
    return True


def validate_outputs():
    """Validate that all expected files were generated."""
    print("\n" + "=" * 80)
    print("FINAL VALIDATION: CHECKING OUTPUT FILES")
    print("=" * 80)

    expected_files = []

    # Static visualizations
    for track in ['All_Projects', '104B_Only']:
        track_dir = track.lower().replace(' ', '_')
        for metric in ['investment', 'projects', 'students']:
            expected_files.append(f'visualizations/static/{track_dir}/project_type_stacked_{metric}_{track}.png')
            expected_files.append(f'visualizations/static/{track_dir}/project_type_grouped_{metric}_{track}.png')
        for period in ['10yr', '5yr']:
            expected_files.append(f'visualizations/static/{track_dir}/project_type_composition_{period}_{track}.png')

    # Interactive dashboards
    for track in ['All_Projects', '104B_Only']:
        expected_files.append(f'visualizations/interactive/project_type_interactive_{track}.html')

    # PDF reports
    for track in ['All_Projects', '104B_Only']:
        expected_files.append(f'reports/project_type_analysis_{track}.pdf')

    # Check each file
    missing = []
    found = []
    for rel_path in expected_files:
        full_path = OUTPUT_DIR / rel_path
        if full_path.exists():
            found.append(rel_path)
        else:
            missing.append(rel_path)

    print(f"✓ Found {len(found)} of {len(expected_files)} expected files")

    if missing:
        print(f"\n✗ Missing {len(missing)} files:")
        for f in missing:
            print(f"  - {f}")
        return False

    print("\n✓ All expected files generated successfully!")
    return True


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function."""
    print(f"Output directory: {OUTPUT_DIR}\n")

    # Load data
    df = load_data()

    # Filter data
    df_all_10yr, df_all_5yr, df_104b_10yr, df_104b_5yr = filter_data(df)

    # Validate
    validate_project_type_data(df_all_10yr, df_all_5yr, df_104b_10yr, df_104b_5yr)

    # Generate visualizations for both tracks
    tracks = [
        ('all', df_all_10yr, df_all_5yr),
        ('104b', df_104b_10yr, df_104b_5yr)
    ]

    for award_type, df_10yr, df_5yr in tracks:
        print(f"\n{'=' * 80}")
        print(f"GENERATING VISUALIZATIONS: {get_award_type_label(award_type)}")
        print(f"{'=' * 80}")

        # Static charts
        print("\nStacked Bar Charts:")
        for metric in ['investment', 'projects', 'students']:
            generate_stacked_bar_chart(df_10yr, df_5yr, award_type, metric)

        print("\nGrouped Bar Charts:")
        for metric in ['investment', 'projects', 'students']:
            generate_grouped_bar_chart(df_10yr, df_5yr, award_type, metric)

        print("\nComposition Pie Charts:")
        generate_composition_pie_charts(df_10yr, '10-Year (2015-2024)', award_type)
        generate_composition_pie_charts(df_5yr, '5-Year (2020-2024)', award_type)

        # Interactive dashboard
        print("\nInteractive Dashboard:")
        generate_interactive_composition_dashboard(df_10yr, df_5yr, award_type)

        # PDF report
        print("\nPDF Report:")
        generate_project_type_pdf_report(df_10yr, df_5yr, award_type)

    # Validate outputs
    validate_outputs()

    print(f"\n{'█' * 80}")
    print(f"█ GENERATION COMPLETE - FINAL_DELIVERABLES_3".center(80) + "█")
    print(f"{'█' * 80}\n")
    print(f"Output location: {OUTPUT_DIR}")

    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
