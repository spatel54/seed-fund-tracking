#!/usr/bin/env python3
"""
Project Type Breakdown Visualization Generator

Generates comprehensive visualizations broken down by project type (All Projects vs 104B Only)
for both 10-year (2015-2024) and 5-year (2020-2024) periods.

Output: 156 total files
- 52 static PNGs (13 types × 2 tracks × 2 periods)
- 26 comparison PNGs (side-by-side All Projects vs 104B Only)
- 52 interactive HTMLs (13 types × 2 tracks × 2 periods)  
- 26 comparison HTML dashboards

Directory Structure: track-first hierarchy
  visualizations/{static,interactive}/project_type_breakdown/
  ├── All_Projects/{2015-2024, 2020-2024}/
  ├── 104B_Only/{2015-2024, 2020-2024}/
  └── comparison/{2015-2024, 2020-2024}/
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import sys
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
sys.path.append(os.path.dirname(__file__))
from iwrc_brand_style import (
    IWRC_COLORS, IWRC_PALETTE,
    configure_matplotlib_iwrc,
    apply_iwrc_matplotlib_style,
    add_logo_to_matplotlib_figure,
    get_iwrc_plotly_template,
    apply_iwrc_plotly_style,
    format_currency
)
from award_type_filters import (
    filter_all_projects,
    filter_104b_only,
    AWARD_TYPE_DESCRIPTIONS,
    AWARD_TYPE_ABBREVIATIONS
)

# ============================================================================
# CONFIGURATION
# ============================================================================

# Data file path
DATA_FILE = '/Users/shivpat/Downloads/Seed Fund Tracking/data/consolidated/IWRC Seed Fund Tracking.xlsx'

# Base output directory
BASE_OUTPUT_DIR = '/Users/shivpat/Downloads/Seed Fund Tracking/visualizations'

# Period definitions
PERIODS = {
    '2015-2024': {'start': 2015, 'end': 2024, 'label': '10-Year Period (2015-2024)'},
    '2020-2024': {'start': 2020, 'end': 2024, 'label': '5-Year Period (2020-2024)'}
}

# Track definitions
TRACKS = {
    'All_Projects': {
        'filter_func': filter_all_projects,
        'label': 'All Projects',
        'description': '104B + 104G + Coordination'
    },
    '104B_Only': {
        'filter_func': filter_104b_only,
        'label': '104B Only',
        'description': 'Seed Funding Only'
    }
}

# Visualization types to generate (simplified list for initial implementation)
VISUALIZATION_TYPES = [
    'award_breakdown',
    'institutional_reach',
    'investment_comparison',
    'projects_by_year',
    'student_distribution_pie',
    'students_trained',
    'university_funding_comparison'
]


# ============================================================================
# MAIN VISUALIZER CLASS
# ============================================================================

class ProjectTypeVisualizer:
    """
    Main class for generating project type breakdown visualizations.
    """

    def __init__(self, data_path=DATA_FILE):
        """Initialize visualizer with data loading."""
        print("=" * 80)
        print("PROJECT TYPE BREAKDOWN VISUALIZATION GENERATOR")
        print("=" * 80)
        print(f"\nLoading data from: {data_path}")

        self.df = self.load_data(data_path)
        self.output_dirs = self._create_output_directories()

        # Configure matplotlib
        configure_matplotlib_iwrc()

        print(f"✓ Data loaded: {len(self.df)} rows")
        print(f"✓ Output directories created")

    def load_data(self, data_path):
        """Load and preprocess data from Excel file."""
        df = pd.read_excel(data_path, sheet_name='Project Overview')

        # Extract year from Project ID
        def extract_year(project_id):
            if pd.isna(project_id):
                return None
            project_id_str = str(project_id)
            if len(project_id_str) >= 4:
                try:
                    year = int(project_id_str[:4])
                    if 1999 <= year <= 2030:
                        return year
                except (ValueError, TypeError):
                    pass
            return None

        df['year'] = df['Project ID'].apply(extract_year)

        # Normalize column names for award type
        if 'Award Type' in df.columns:
            df['award_type'] = df['Award Type']

        return df

    def _create_output_directories(self):
        """Create output directory structure."""
        dirs = {}

        for output_type in ['static', 'interactive']:
            base = Path(BASE_OUTPUT_DIR) / output_type / 'project_type_breakdown'

            for track in TRACKS.keys():
                for period in PERIODS.keys():
                    dir_path = base / track / period
                    dir_path.mkdir(parents=True, exist_ok=True)
                    dirs[f"{output_type}_{track}_{period}"] = dir_path

            # Comparison directories
            for period in PERIODS.keys():
                dir_path = base / 'comparison' / period
                dir_path.mkdir(parents=True, exist_ok=True)
                dirs[f"{output_type}_comparison_{period}"] = dir_path

        return dirs

    def filter_by_period(self, period_key):
        """Filter data by time period."""
        period = PERIODS[period_key]
        df_period = self.df[
            (self.df['year'] >= period['start']) &
            (self.df['year'] <= period['end'])
        ].copy()
        return df_period

    def filter_by_track(self, df, track_key):
        """Apply track filter to dataframe."""
        filter_func = TRACKS[track_key]['filter_func']
        return filter_func(df)

    def get_filtered_data(self, period_key, track_key):
        """Get data filtered by both period and track."""
        df_period = self.filter_by_period(period_key)
        df_filtered = self.filter_by_track(df_period, track_key)
        return df_filtered

    def get_output_path(self, output_type, track_key, period_key, viz_name, extension):
        """Generate output file path."""
        dir_key = f"{output_type}_{track_key}_{period_key}"
        filename = f"{viz_name}_{track_key}_{period_key}.{extension}"
        return self.output_dirs[dir_key] / filename

    def generate_all_static_pngs(self):
        """Generate all static PNG visualizations (simplified version)."""
        print("\n" + "=" * 80)
        print("GENERATING STATIC PNG VISUALIZATIONS")
        print("=" * 80)

        total_files = 0

        for period_key in PERIODS.keys():
            for track_key in TRACKS.keys():
                print(f"\n{TRACKS[track_key]['label']} - {period_key}:")

                # Get filtered data
                df_filtered = self.get_filtered_data(period_key, track_key)
                num_projects = len(df_filtered['Project ID'].dropna().unique())
                print(f"  Data: {len(df_filtered)} rows, {num_projects} unique projects")

                # For now, create a simple summary visualization
                self.generate_summary_png(df_filtered, period_key, track_key)

                total_files += 1

        print(f"\n✓ Generated {total_files} static PNG files")

    def generate_summary_png(self, df, period_key, track_key):
        """Generate a summary visualization combining key metrics."""
        output_path = self.get_output_path('static', track_key, period_key,
                                          'summary', 'png')

        # Calculate metrics
        num_projects = len(df['Project ID'].dropna().unique())

        award_col = 'Award Amount Allocated ($)'
        if award_col in df.columns:
            total_investment = df[award_col].fillna(0).sum()
        else:
            total_investment = 0

        # Student columns
        student_cols = [
            'Number of PhD Students Supported by WRRA $',
            'Number of MS Students Supported by WRRA $',
            'Number of Undergraduate Students Supported by WRRA $',
            'Number of Post Docs Supported by WRRA $'
        ]
        total_students = 0
        for col in student_cols:
            if col in df.columns:
                total_students += df[col].fillna(0).sum()

        # Create figure
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

        # Panel 1: Project count
        ax1.bar([0], [num_projects], color=IWRC_COLORS['primary'], width=0.5)
        ax1.set_xlim(-0.5, 0.5)
        ax1.set_xticks([0])
        ax1.set_xticklabels(['Projects'])
        ax1.set_ylabel('Count', fontsize=11, weight='semibold')
        ax1.set_title('Total Projects', fontsize=12, weight='semibold')
        ax1.text(0, num_projects, f'{int(num_projects)}', ha='center', va='bottom',
                fontsize=14, weight='bold')

        # Panel 2: Investment
        ax2.bar([0], [total_investment], color=IWRC_COLORS['secondary'], width=0.5)
        ax2.set_xlim(-0.5, 0.5)
        ax2.set_xticks([0])
        ax2.set_xticklabels(['Investment'])
        ax2.set_ylabel('Amount ($)', fontsize=11, weight='semibold')
        ax2.set_title('Total Investment', fontsize=12, weight='semibold')
        ax2.text(0, total_investment, format_currency(total_investment),
                ha='center', va='bottom', fontsize=12, weight='bold')

        # Panel 3: Students
        ax3.bar([0], [total_students], color=IWRC_COLORS['accent'], width=0.5)
        ax3.set_xlim(-0.5, 0.5)
        ax3.set_xticks([0])
        ax3.set_xticklabels(['Students'])
        ax3.set_ylabel('Count', fontsize=11, weight='semibold')
        ax3.set_title('Students Trained', fontsize=12, weight='semibold')
        ax3.text(0, total_students, f'{int(total_students)}', ha='center', va='bottom',
                fontsize=14, weight='bold')

        # Panel 4: Year distribution
        if 'year' in df.columns and df['year'].notna().sum() > 0:
            year_counts = df['year'].value_counts().sort_index()
            ax4.bar(year_counts.index, year_counts.values, color=IWRC_COLORS['primary'])
            ax4.set_xlabel('Year', fontsize=11, weight='semibold')
            ax4.set_ylabel('Projects', fontsize=11, weight='semibold')
            ax4.set_title('Projects by Year', fontsize=12, weight='semibold')

        # Overall title
        fig.suptitle(f'{TRACKS[track_key]["label"]} Summary - {period_key}',
                    fontsize=16, weight='bold', color=IWRC_COLORS['dark_teal'])

        # Apply IWRC styling
        for ax in [ax1, ax2, ax3, ax4]:
            apply_iwrc_matplotlib_style(fig, ax)

        add_logo_to_matplotlib_figure(fig)

        # Save
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        print(f"  ✓ Generated summary visualization")

    def run(self):
        """Run the complete visualization generation pipeline."""
        start_time = datetime.now()

        print(f"\nStart time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Generate static PNGs
        self.generate_all_static_pngs()

        # TODO: Add more visualization types
        # TODO: Generate comparison PNGs
        # TODO: Generate interactive HTMLs
        # TODO: Generate comparison HTMLs
        # TODO: Generate documentation

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print("\n" + "=" * 80)
        print("GENERATION COMPLETE")
        print("=" * 80)
        print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {duration:.1f} seconds")
        print(f"\nOutput location: {BASE_OUTPUT_DIR}/{{static,interactive}}/project_type_breakdown/")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    visualizer = ProjectTypeVisualizer()
    visualizer.run()
