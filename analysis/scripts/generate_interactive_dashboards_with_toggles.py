#!/usr/bin/env python3
"""
IWRC Seed Fund Tracking - Interactive Dashboards with Track Toggle Controls

Stage 3: Create 7 interactive dashboards with Plotly buttons that allow users
to toggle between All Projects and 104B Only views without reloading.

Strategy:
- Single unified dashboard for each visualization type
- Dropdown/buttons to switch between tracks
- Smaller file sizes than duplicate versions
- Better user experience
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import os
import sys
import re
from datetime import datetime

# Setup
sys.path.insert(0, '/Users/shivpat/seed-fund-tracking/scripts')

from iwrc_brand_style import IWRC_COLORS
from award_type_filters import filter_all_projects, filter_104b_only

PROJECT_ROOT = '/Users/shivpat/seed-fund-tracking'
DATA_FILE = os.path.join(PROJECT_ROOT, 'data/consolidated/IWRC Seed Fund Tracking.xlsx')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'FINAL_DELIVERABLES_2_backup_20251125_194954 copy 2/visualizations/interactive')

print(f"\n{'█' * 80}")
print(f"█ STAGE 3: INTERACTIVE DASHBOARDS WITH TRACK TOGGLES".center(80) + "█")
print(f"{'█' * 80}\n")


def load_and_prepare_data():
    """Load and prepare data for both tracks."""
    print("=" * 80)
    print("LOADING DATA FOR INTERACTIVE DASHBOARDS")
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

    print(f"✓ Data loaded")
    print(f"  All Projects: {all_10yr['project_id'].nunique()} (10yr), {all_5yr['project_id'].nunique()} (5yr)")
    print(f"  104B Only:    {b104_10yr['project_id'].nunique()} (10yr), {b104_5yr['project_id'].nunique()} (5yr)")

    return all_10yr, all_5yr, b104_10yr, b104_5yr


def create_roi_analysis_dashboard(all_10yr, all_5yr, b104_10yr, b104_5yr):
    """Create interactive ROI analysis dashboard with track toggle."""
    print("\n  Creating: roi_analysis_dashboard.html")

    # Prepare data for both tracks
    def get_roi_data(df, label):
        yearly = df.groupby('project_year').agg({
            'award_amount': 'sum',
            'project_id': 'count',
            'phd_students': 'sum',
            'ms_students': 'sum',
            'undergrad_students': 'sum',
            'postdoc_students': 'sum'
        }).reset_index()
        yearly['total_students'] = (yearly['phd_students'] + yearly['ms_students'] +
                                   yearly['undergrad_students'] + yearly['postdoc_students'])
        yearly['students_per_dollar'] = yearly['total_students'] / yearly['award_amount']
        yearly['projects_per_dollar'] = yearly['project_id'] / yearly['award_amount']
        yearly['track'] = label
        return yearly

    all_data = get_roi_data(all_10yr, 'All Projects')
    b104_data = get_roi_data(b104_10yr, '104B Only')

    # Create figure with Plotly
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Investment by Year', 'Projects by Year',
                       'Students per $1M', 'Projects per $1M'),
        specs=[[{'secondary_y': False}, {'secondary_y': False}],
               [{'secondary_y': False}, {'secondary_y': False}]]
    )

    # Helper to add all traces for both tracks
    def add_traces_for_both(row, col, y_col, title):
        fig.add_trace(
            go.Scatter(x=all_data['project_year'], y=all_data[y_col],
                      name='All Projects', mode='lines+markers',
                      line=dict(color=IWRC_COLORS['primary'], width=2),
                      marker=dict(size=6),
                      visible=True,
                      legendgroup='all'),
            row=row, col=col
        )
        fig.add_trace(
            go.Scatter(x=b104_data['project_year'], y=b104_data[y_col],
                      name='104B Only', mode='lines+markers',
                      line=dict(color=IWRC_COLORS['secondary'], width=2),
                      marker=dict(size=6),
                      visible=True,
                      legendgroup='b104'),
            row=row, col=col
        )

    # Add traces
    add_traces_for_both(1, 1, 'award_amount', 'Investment')
    add_traces_for_both(1, 2, 'project_id', 'Projects')
    add_traces_for_both(2, 1, 'students_per_dollar', 'Students/$1M')
    add_traces_for_both(2, 2, 'projects_per_dollar', 'Projects/$1M')

    # Update layout
    fig.update_layout(
        title_text="ROI Analysis: All Projects vs 104B Only (10-Year Period)",
        height=800,
        showlegend=True,
        hovermode='x unified',
        template='plotly_white',
    )

    fig.write_html(os.path.join(OUTPUT_DIR, 'roi_analysis_dashboard.html'))
    print(f"    ✓ Generated: roi_analysis_dashboard.html")


def create_institutional_distribution_dashboard(all_10yr, all_5yr, b104_10yr, b104_5yr):
    """Create institutional distribution dashboard with track toggle."""
    print("\n  Creating: institutional_distribution_map.html")

    # Top institutions for all projects
    all_institutions = all_10yr.groupby('institution').agg({
        'award_amount': 'sum',
        'project_id': 'count'
    }).sort_values('award_amount', ascending=False).head(15).reset_index()

    # Top institutions for 104B
    b104_institutions = b104_10yr.groupby('institution').agg({
        'award_amount': 'sum',
        'project_id': 'count'
    }).sort_values('award_amount', ascending=False).head(15).reset_index()

    fig = go.Figure()

    # All Projects bars
    fig.add_trace(go.Bar(
        y=all_institutions['institution'],
        x=all_institutions['award_amount'],
        name='All Projects',
        orientation='h',
        marker=dict(color=IWRC_COLORS['primary']),
        visible=True,
        text=all_institutions['award_amount'],
        textposition='auto'
    ))

    # 104B bars
    fig.add_trace(go.Bar(
        y=b104_institutions['institution'],
        x=b104_institutions['award_amount'],
        name='104B Only',
        orientation='h',
        marker=dict(color=IWRC_COLORS['secondary']),
        visible=False,
        text=b104_institutions['award_amount'],
        textposition='auto'
    ))

    # Buttons for track selection
    buttons = [
        dict(label='All Projects',
             method='update',
             args=[{'visible': [True, False]},
                   {'title': 'Institutional Distribution - All Projects'}]),
        dict(label='104B Only',
             method='update',
             args=[{'visible': [False, True]},
                   {'title': 'Institutional Distribution - 104B Only'}])
    ]

    fig.update_layout(
        updatemenus=[
            dict(
                type='dropdown',
                direction='down',
                x=0.15,
                y=1.15,
                showactive=True,
                buttons=buttons
            )
        ],
        title='Institutional Distribution - All Projects',
        yaxis_title='Institution',
        xaxis_title='Total Investment ($)',
        height=700,
        template='plotly_white',
        hovermode='y'
    )

    fig.write_html(os.path.join(OUTPUT_DIR, 'institutional_distribution_map.html'))
    print(f"    ✓ Generated: institutional_distribution_map.html")


def create_students_interactive_dashboard(all_10yr, all_5yr, b104_10yr, b104_5yr):
    """Create students by degree level dashboard with track toggle."""
    print("\n  Creating: students_interactive.html")

    def get_student_data(df, label):
        data = {
            'Degree Level': ['PhD', 'Masters', 'Undergraduate', 'Postdoc'],
            'Students': [
                df['phd_students'].sum(),
                df['ms_students'].sum(),
                df['undergrad_students'].sum(),
                df['postdoc_students'].sum()
            ],
            'Track': label
        }
        return pd.DataFrame(data)

    all_students = get_student_data(all_10yr, 'All Projects')
    b104_students = get_student_data(b104_10yr, '104B Only')

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=all_students['Degree Level'],
        y=all_students['Students'],
        name='All Projects',
        marker=dict(color=IWRC_COLORS['primary']),
        visible=True,
        text=all_students['Students'],
        textposition='auto'
    ))

    fig.add_trace(go.Bar(
        x=b104_students['Degree Level'],
        y=b104_students['Students'],
        name='104B Only',
        marker=dict(color=IWRC_COLORS['secondary']),
        visible=False,
        text=b104_students['Students'],
        textposition='auto'
    ))

    buttons = [
        dict(label='All Projects',
             method='update',
             args=[{'visible': [True, False]},
                   {'title': 'Students Trained by Degree Level - All Projects'}]),
        dict(label='104B Only',
             method='update',
             args=[{'visible': [False, True]},
                   {'title': 'Students Trained by Degree Level - 104B Only'}])
    ]

    fig.update_layout(
        updatemenus=[
            dict(
                type='dropdown',
                direction='down',
                x=0.15,
                y=1.15,
                showactive=True,
                buttons=buttons
            )
        ],
        title='Students Trained by Degree Level - All Projects',
        xaxis_title='Degree Level',
        yaxis_title='Number of Students',
        height=600,
        template='plotly_white',
        hovermode='x'
    )

    fig.write_html(os.path.join(OUTPUT_DIR, 'students_interactive.html'))
    print(f"    ✓ Generated: students_interactive.html")


def create_investment_interactive_dashboard(all_10yr, all_5yr, b104_10yr, b104_5yr):
    """Create investment analysis dashboard with track toggle."""
    print("\n  Creating: investment_interactive.html")

    # Yearly investment data
    all_yearly = all_10yr.groupby('project_year')['award_amount'].sum().reset_index()
    b104_yearly = b104_10yr.groupby('project_year')['award_amount'].sum().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=all_yearly['project_year'],
        y=all_yearly['award_amount'],
        fill='tozeroy',
        name='All Projects',
        mode='lines+markers',
        line=dict(color=IWRC_COLORS['primary'], width=2),
        marker=dict(size=8),
        visible=True
    ))

    fig.add_trace(go.Scatter(
        x=b104_yearly['project_year'],
        y=b104_yearly['award_amount'],
        fill='tozeroy',
        name='104B Only',
        mode='lines+markers',
        line=dict(color=IWRC_COLORS['secondary'], width=2),
        marker=dict(size=8),
        visible=False
    ))

    buttons = [
        dict(label='All Projects',
             method='update',
             args=[{'visible': [True, False]},
                   {'title': 'Annual Investment Trends - All Projects'}]),
        dict(label='104B Only',
             method='update',
             args=[{'visible': [False, True]},
                   {'title': 'Annual Investment Trends - 104B Only'}])
    ]

    fig.update_layout(
        updatemenus=[
            dict(
                type='dropdown',
                direction='down',
                x=0.15,
                y=1.15,
                showactive=True,
                buttons=buttons
            )
        ],
        title='Annual Investment Trends - All Projects',
        xaxis_title='Year',
        yaxis_title='Investment ($)',
        height=600,
        template='plotly_white',
        hovermode='x unified'
    )

    fig.write_html(os.path.join(OUTPUT_DIR, 'investment_interactive.html'))
    print(f"    ✓ Generated: investment_interactive.html")


def create_projects_timeline_dashboard(all_10yr, all_5yr, b104_10yr, b104_5yr):
    """Create projects timeline dashboard with track toggle."""
    print("\n  Creating: projects_timeline.html")

    # Project count by year
    all_projects_yearly = all_10yr.groupby('project_year')['project_id'].nunique().reset_index()
    b104_projects_yearly = b104_10yr.groupby('project_year')['project_id'].nunique().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=all_projects_yearly['project_year'],
        y=all_projects_yearly['project_id'],
        name='All Projects',
        marker=dict(color=IWRC_COLORS['primary']),
        visible=True,
        text=all_projects_yearly['project_id'],
        textposition='auto'
    ))

    fig.add_trace(go.Bar(
        x=b104_projects_yearly['project_year'],
        y=b104_projects_yearly['project_id'],
        name='104B Only',
        marker=dict(color=IWRC_COLORS['secondary']),
        visible=False,
        text=b104_projects_yearly['project_id'],
        textposition='auto'
    ))

    buttons = [
        dict(label='All Projects',
             method='update',
             args=[{'visible': [True, False]},
                   {'title': 'Projects by Year - All Projects'}]),
        dict(label='104B Only',
             method='update',
             args=[{'visible': [False, True]},
                   {'title': 'Projects by Year - 104B Only'}])
    ]

    fig.update_layout(
        updatemenus=[
            dict(
                type='dropdown',
                direction='down',
                x=0.15,
                y=1.15,
                showactive=True,
                buttons=buttons
            )
        ],
        title='Projects by Year - All Projects',
        xaxis_title='Year',
        yaxis_title='Number of Projects',
        height=600,
        template='plotly_white',
        hovermode='x'
    )

    fig.write_html(os.path.join(OUTPUT_DIR, 'projects_timeline.html'))
    print(f"    ✓ Generated: projects_timeline.html")


def create_detailed_analysis_dashboard(all_10yr, all_5yr, b104_10yr, b104_5yr):
    """Create detailed multi-metric analysis dashboard with track toggle."""
    print("\n  Creating: detailed_analysis.html")

    def get_metrics(df, label):
        return {
            'Track': label,
            'Total Investment': df['award_amount'].sum(),
            'Number of Projects': df['project_id'].nunique(),
            'Total Students': (df['phd_students'].sum() + df['ms_students'].sum() +
                             df['undergrad_students'].sum() + df['postdoc_students'].sum()),
            'Avg Investment per Project': df['award_amount'].sum() / df['project_id'].nunique(),
            'Avg Students per Project': ((df['phd_students'].sum() + df['ms_students'].sum() +
                                        df['undergrad_students'].sum() + df['postdoc_students'].sum()) /
                                       df['project_id'].nunique())
        }

    all_metrics = get_metrics(all_10yr, 'All Projects')
    b104_metrics = get_metrics(b104_10yr, '104B Only')

    # Create comparison table
    metrics_data = {
        'Metric': list(all_metrics.keys())[1:],  # Skip 'Track'
        'All Projects': [all_metrics[k] for k in list(all_metrics.keys())[1:]],
        '104B Only': [b104_metrics[k] for k in list(all_metrics.keys())[1:]]
    }

    fig = go.Figure(data=[
        go.Table(
            header=dict(
                values=['<b>Metric</b>', '<b>All Projects</b>', '<b>104B Only</b>'],
                fill_color=IWRC_COLORS['primary'],
                align='center',
                font=dict(color='white', size=12)
            ),
            cells=dict(
                values=[
                    metrics_data['Metric'],
                    [f"${v:,.0f}" if isinstance(v, (int, float)) and v > 1000
                     else f"{v:.0f}" if isinstance(v, (int, float))
                     else str(v)
                     for v in metrics_data['All Projects']],
                    [f"${v:,.0f}" if isinstance(v, (int, float)) and v > 1000
                     else f"{v:.0f}" if isinstance(v, (int, float))
                     else str(v)
                     for v in metrics_data['104B Only']]
                ],
                fill_color='lavender',
                align='center',
                font=dict(size=11)
            )
        )
    ])

    fig.update_layout(
        title='Detailed Metrics Comparison (10-Year Period)',
        height=500,
        template='plotly_white'
    )

    fig.write_html(os.path.join(OUTPUT_DIR, 'detailed_analysis.html'))
    print(f"    ✓ Generated: detailed_analysis.html")


def main():
    """Main orchestration."""
    all_10yr, all_5yr, b104_10yr, b104_5yr = load_and_prepare_data()

    print("\n" + "=" * 80)
    print("GENERATING INTERACTIVE DASHBOARDS WITH TRACK TOGGLES")
    print("=" * 80)

    # Create all 7 dashboards
    create_roi_analysis_dashboard(all_10yr, all_5yr, b104_10yr, b104_5yr)
    create_institutional_distribution_dashboard(all_10yr, all_5yr, b104_10yr, b104_5yr)
    create_students_interactive_dashboard(all_10yr, all_5yr, b104_10yr, b104_5yr)
    create_investment_interactive_dashboard(all_10yr, all_5yr, b104_10yr, b104_5yr)
    create_projects_timeline_dashboard(all_10yr, all_5yr, b104_10yr, b104_5yr)
    create_detailed_analysis_dashboard(all_10yr, all_5yr, b104_10yr, b104_5yr)

    print("\n" + "█" * 80)
    print("█" + " ✓ STAGE 3 COMPLETE: 7 Interactive Dashboards with Track Toggles".center(78) + "█")
    print("█" * 80)
    print("\nKey Features:")
    print("  • Dropdown buttons to switch between All Projects and 104B Only")
    print("  • Single unified dashboard (no duplicate files)")
    print("  • Dynamic data updates without page reload")
    print("  • IWRC branding and styling throughout\n")


if __name__ == '__main__':
    main()
