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
DATA_FILE = '/Users/shivpat/seed-fund-tracking/data/consolidated/IWRC Seed Fund Tracking.xlsx'

# Base output directory
# Base output directory
BASE_OUTPUT_DIR = '/Users/shivpat/seed-fund-tracking/deliverables_final/visualizations'

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
        """Load and preprocess data using IWRCDataLoader."""
        try:
            from iwrc_data_loader import IWRCDataLoader
            loader = IWRCDataLoader()
            # Load with deduplication to ensure accurate counts
            df = loader.load_master_data(deduplicate=True)
            
            # Ensure year column exists (loader might name it 'project_year')
            if 'project_year' in df.columns:
                df['year'] = df['project_year']
            
            # Ensure award_type column exists
            if 'award_type' in df.columns:
                df['award_type'] = df['award_type']
                
            return df
        except ImportError:
            print("Warning: Could not import IWRCDataLoader. Using manual loading.")
            return self._manual_load_data(data_path)

    def _manual_load_data(self, data_path):
        """Fallback manual loading."""
        df = pd.read_excel(data_path, sheet_name='Project Overview')
        # ... (existing manual loading logic)
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

        df['year'] = df['Project ID '].apply(extract_year)
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
                num_projects = len(df_filtered['project_id'].dropna().unique()) if 'project_id' in df_filtered.columns else len(df_filtered)
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
        num_projects = len(df['project_id'].dropna().unique()) if 'project_id' in df.columns else len(df)

        award_col = 'award_amount'
        if award_col in df.columns:
            total_investment = df[award_col].fillna(0).sum()
        else:
            total_investment = 0

        # Student columns
        student_cols = [
            'phd_students',
            'ms_students',
            'undergrad_students',
            'postdoc_students'
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
        # Generate interactive HTMLs
        self.generate_interactive_htmls()

    def generate_interactive_htmls(self):
        """Generate interactive HTML dashboards for each track."""
        print("\n" + "=" * 80)
        print("GENERATING INTERACTIVE HTML DASHBOARDS")
        print("=" * 80)

        for track_key in TRACKS.keys():
            print(f"\nGenerating dashboard for {TRACKS[track_key]['label']}...")
            
            # Prepare data for both periods
            df_10yr = self.get_filtered_data('2015-2024', track_key)
            df_5yr = self.get_filtered_data('2020-2024', track_key)
            
            # Create dashboard
            self.create_interactive_dashboard(df_10yr, df_5yr, track_key)
            
    def create_interactive_dashboard(self, df_10yr, df_5yr, track_key):
        """Create interactive dashboard with period selection."""
        
        # Calculate metrics
        def get_metrics(df):
            projects = len(df['project_title'].unique()) if 'project_title' in df.columns else len(df)
            investment = df['award_amount'].sum() if 'award_amount' in df.columns else 0
            students = 0
            student_cols = ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']
            for col in student_cols:
                if col in df.columns:
                    students += df[col].fillna(0).sum()
            return projects, investment, students

        p10, i10, s10 = get_metrics(df_10yr)
        p5, i5, s5 = get_metrics(df_5yr)
        
        # Create figure
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "bar"}, {"type": "scatter"}]],
            subplot_titles=("Key Metrics", "Student Impact", "Investment Distribution", "Projects by Year"),
            vertical_spacing=0.15
        )
        
        # Add indicators (using 10-year as default)
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=i10,
            title={"text": "Total Investment"},
            number={'prefix': "$", 'valueformat': ",.0f"},
            delta={'reference': i5, 'relative': False, 'valueformat': ",.0f", 'position': "bottom"},
            domain={'row': 0, 'column': 0}
        ))
        
        fig.add_trace(go.Indicator(
            mode="number+delta",
            value=s10,
            title={"text": "Students Trained"},
            delta={'reference': s5, 'relative': False, 'position': "bottom"},
            domain={'row': 0, 'column': 1}
        ))
        
        # Add charts (using 10-year data initially)
        # Investment by Year
        if 'year' in df_10yr.columns:
            yearly_10 = df_10yr.groupby('year')['award_amount'].sum().reset_index()
            fig.add_trace(go.Bar(
                x=yearly_10['year'], y=yearly_10['award_amount'],
                name='Investment', marker_color=IWRC_COLORS['primary']
            ), row=2, col=1)
            
            projects_10 = df_10yr.groupby('year')['project_title'].count().reset_index()
            fig.add_trace(go.Scatter(
                x=projects_10['year'], y=projects_10['project_title'],
                name='Projects', mode='lines+markers', line=dict(color=IWRC_COLORS['secondary'])
            ), row=2, col=2)

        # Apply styling
        apply_iwrc_plotly_style(fig)
        
        # Update layout
        fig.update_layout(
            title_text=f"<b>{TRACKS[track_key]['label']} Dashboard</b><br><sub>{TRACKS[track_key]['description']}</sub>",
            height=800
        )
        
        # Save
        filename = f"project_type_breakdown_{track_key.lower()}.html"
        # Output to interactive/project_type_breakdown/
        output_dir = Path(BASE_OUTPUT_DIR) / 'interactive' / 'project_type_breakdown'
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        fig.write_html(output_path)
        print(f"✓ Created: {output_path}")




# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    visualizer = ProjectTypeVisualizer()
    visualizer.run()
