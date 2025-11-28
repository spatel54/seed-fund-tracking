#!/usr/bin/env python3
"""
Generate Interactive HTML Dashboards - CORRECTED VERSION

This script replaces deprecated notebook 06_interactive_breakdown.ipynb
which had systematic double-counting errors.

Generates:
- interactive_roi_dashboard.html: ROI metrics with 10yr/5yr toggle
- interactive_topic_distribution.html: Topic distribution pie charts

Key Improvements:
- Uses IWRCDataLoader for automatic deduplication
- Proper metric calculations (no double-counting)
- IWRC branding applied
- Outputs to deliverables directory

Author: IWRC Data Quality Team
Date: November 27, 2025
Version: 1.0 (CORRECTED)
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import base64
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import centralized data loader
from iwrc_data_loader import IWRCDataLoader

# IWRC Branding
COLORS = {
    'primary': '#258372',    # Teal
    'secondary': '#639757',  # Olive
    'text': '#54595F',       # Dark Gray
    'accent': '#FCC080',     # Peach/Orange
    'bg': '#F6F6F6'          # Light Gray
}

FONT_FAMILY = "Montserrat, Arial, sans-serif"

# Paths
BASE_DIR = Path("/Users/shivpat/seed-fund-tracking")
OUTPUT_DIR = BASE_DIR / "deliverables_final/visualizations/interactive/project_types"
LOGO_PATH = BASE_DIR / "IWRC Logo - Full Color.svg"

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load logo
logo_base64 = ""
try:
    with open(LOGO_PATH, "rb") as f:
        logo_base64 = "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode('utf-8')
    print("✓ Logo loaded successfully")
except Exception as e:
    print(f"⚠ Could not load logo: {e}")


def create_roi_dashboard(loader, df):
    """
    Create interactive ROI dashboard with 10yr/5yr toggle.
    
    Shows:
    - Investment ($)
    - Follow-on Funding ($)
    - ROI Multiplier
    - Students Trained
    
    Args:
        loader: IWRCDataLoader instance
        df: Deduplicated DataFrame
    """
    print("\nGenerating ROI Dashboard...")
    
    # Calculate metrics for both periods using CORRECTED loader
    metrics_10yr = loader.calculate_metrics(df, period='10yr')
    metrics_5yr = loader.calculate_metrics(df, period='5yr')
    
    # Create figure with subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Investment ($)", "Follow-on Funding ($)", "ROI Multiplier", "Students Trained"),
        vertical_spacing=0.15
    )
    
    # Helper function to add bar traces
    def add_bar_traces(row, col, val_10yr, val_5yr, fmt_func):
        # 10-Year trace (visible by default)
        fig.add_trace(go.Bar(
            x=['10-Year (2015-2024)'],
            y=[val_10yr],
            name='10-Year',
            marker_color=COLORS['primary'],
            text=[fmt_func(val_10yr)],
            textposition='auto',
            showlegend=False
        ), row=row, col=col)
        
        # 5-Year trace (hidden by default)
        fig.add_trace(go.Bar(
            x=['5-Year (2020-2024)'],
            y=[val_5yr],
            name='5-Year',
            marker_color=COLORS['secondary'],
            text=[fmt_func(val_5yr)],
            textposition='auto',
            showlegend=False,
            visible=False
        ), row=row, col=col)
    
    # Add all metrics
    add_bar_traces(1, 1, metrics_10yr['investment'], metrics_5yr['investment'], 
                   lambda v: f'${v:,.0f}')
    add_bar_traces(1, 2, metrics_10yr['followon'], metrics_5yr['followon'], 
                   lambda v: f'${v:,.0f}')
    add_bar_traces(2, 1, metrics_10yr['roi'], metrics_5yr['roi'], 
                   lambda v: f'{v:.1%}')
    add_bar_traces(2, 2, metrics_10yr['students'], metrics_5yr['students'], 
                   lambda v: f'{v:,.0f}')
    
    # Update layout with toggle buttons
    fig.update_layout(
        title=dict(
            text="<b>IWRC Impact Dashboard: Corrected Metrics</b>",
            font=dict(size=24, family=FONT_FAMILY, color=COLORS['primary']),
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        updatemenus=[dict(
            type="buttons",
            direction="left",
            x=0.0, y=1.15,
            xanchor='left', yanchor='top',
            showactive=True,
            buttons=list([
                dict(label="10-Year (2015-2024)",
                     method="update",
                     args=[{"visible": [True, False, True, False, True, False, True, False]}]),
                dict(label="5-Year (2020-2024)",
                     method="update",
                     args=[{"visible": [False, True, False, True, False, True, False, True]}])
            ]),
            bgcolor=COLORS['bg'],
            font=dict(color=COLORS['text'], family=FONT_FAMILY)
        )],
        template="plotly_white",
        font=dict(family=FONT_FAMILY, color=COLORS['text']),
        height=800,
        margin=dict(t=160, l=50, r=50, b=50)
    )
    
    # Add logo if available
    if logo_base64:
        fig.add_layout_image(
            dict(
                source=logo_base64,
                xref="paper", yref="paper",
                x=1, y=1.18,
                sizex=0.18, sizey=0.18,
                xanchor="right", yanchor="top"
            )
        )
    
    # Save
    output_file = OUTPUT_DIR / "interactive_roi_dashboard.html"
    fig.write_html(str(output_file))
    print(f"✓ Saved: {output_file}")
    
    # Print metrics for verification
    print(f"\n  10-Year Metrics:")
    print(f"    Investment: ${metrics_10yr['investment']:,.2f}")
    print(f"    Students: {metrics_10yr['students']}")
    print(f"    ROI: {metrics_10yr['roi']:.1%}")
    print(f"\n  5-Year Metrics:")
    print(f"    Investment: ${metrics_5yr['investment']:,.2f}")
    print(f"    Students: {metrics_5yr['students']}")
    print(f"    ROI: {metrics_5yr['roi']:.1%}")


def create_topic_distribution(df):
    """
    Create interactive topic distribution pie charts.
    
    Shows science priority distribution for 2015-2024 period.
    Uses value_counts which is safe (doesn't sum duplicates).
    
    Args:
        df: Deduplicated DataFrame
    """
    print("\nGenerating Topic Distribution Chart...")
    
    # Filter for 2015-2024
    df_filtered = df[df['project_year'].between(2015, 2024, inclusive='both')]
    
    # Get topic distribution (value_counts is safe - no summing)
    topic_counts = df_filtered['science_priority'].value_counts().reset_index()
    topic_counts.columns = ['Topic', 'Count']
    
    # Create pie chart
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=topic_counts['Topic'],
        values=topic_counts['Count'],
        marker=dict(colors=px.colors.qualitative.Prism),
        hole=0.4,
        textinfo='label+percent',
        textfont=dict(family=FONT_FAMILY)
    ))
    
    fig.update_layout(
        title=dict(
            text="<b>Research Topic Distribution (2015-2024)</b>",
            font=dict(size=24, family=FONT_FAMILY, color=COLORS['primary']),
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        font=dict(family=FONT_FAMILY, color=COLORS['text']),
        height=700,
        margin=dict(t=140, l=50, r=50, b=50)
    )
    
    # Add logo if available
    if logo_base64:
        fig.add_layout_image(
            dict(
                source=logo_base64,
                xref="paper", yref="paper",
                x=1, y=1.12,
                sizex=0.15, sizey=0.15,
                xanchor="right", yanchor="top"
            )
        )
    
    # Save
    output_file = OUTPUT_DIR / "interactive_topic_distribution.html"
    fig.write_html(str(output_file))
    print(f"✓ Saved: {output_file}")
    print(f"\n  Total Projects: {topic_counts['Count'].sum()}")
    print(f"  Unique Topics: {len(topic_counts)}")


def main():
    """Main execution function."""
    print("="*80)
    print("GENERATE INTERACTIVE DASHBOARDS - CORRECTED VERSION")
    print("="*80)
    print("\nThis script uses IWRCDataLoader for proper deduplication.")
    print("Replacing deprecated notebook 06 which had double-counting errors.")
    
    # Initialize loader
    print("\n" + "="*80)
    print("STEP 1: Load Data with Deduplication")
    print("="*80)
    loader = IWRCDataLoader()
    df = loader.load_master_data(deduplicate=True)
    
    # Validate data quality
    print("\n" + "="*80)
    print("STEP 2: Validate Data Quality")
    print("="*80)
    validation = loader.validate_data_quality(df)
    print(f"  Total rows: {validation['total_rows']}")
    print(f"  Unique projects: {validation['unique_projects']}")
    print(f"  Has duplicates: {validation['has_duplicates']}")
    
    if validation['has_duplicates']:
        print("  ⚠️  WARNING: Data still has duplicates!")
        return
    
    # Generate dashboards
    print("\n" + "="*80)
    print("STEP 3: Generate Interactive Dashboards")
    print("="*80)
    
    create_roi_dashboard(loader, df)
    create_topic_distribution(df)
    
    print("\n" + "="*80)
    print("✅ DASHBOARDS GENERATED SUCCESSFULLY")
    print("="*80)
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print(f"  - interactive_roi_dashboard.html")
    print(f"  - interactive_topic_distribution.html")
    print("\n✅ All metrics use CORRECTED values (no double-counting)")
    print("="*80)


if __name__ == '__main__':
    main()
