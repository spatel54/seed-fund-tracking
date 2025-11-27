#!/usr/bin/env python3
"""
Dual-Track Analysis Orchestrator

Runs complete analysis pipeline for both "All Projects" and "104B Only" award types.
This is the master script for IWRC rebranding and award type analysis.

Execution Order:
1. Load and prepare data with award type filtering
2. Run analysis for "All Projects" track
3. Run analysis for "104B Only" track
4. Generate dual outputs
5. Organize into FINAL_DELIVERABLES
"""

import pandas as pd
import numpy as np
import os
import sys
import subprocess
import shutil
from datetime import datetime

# Add scripts to path
sys.path.insert(0, '/Users/shivpat/seed-fund-tracking/scripts')

# Import filtering modules
from award_type_filters import (
    filter_all_projects, filter_104b_only,
    get_award_type_label, get_award_type_short_label,
    EXPECTED_COUNTS
)

# Constants
PROJECT_ROOT = '/Users/shivpat/seed-fund-tracking'
DATA_FILE = os.path.join(PROJECT_ROOT, 'data/consolidated/IWRC Seed Fund Tracking.xlsx')
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, 'scripts')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'FINAL_DELIVERABLES')
ARCHIVE_DIR = os.path.join(PROJECT_ROOT, 'PROJECT_ARCHIVES')

# Award type tracks
AWARD_TYPES = {
    'all': ('All Projects', filter_all_projects),
    '104b': ('104B Only (Seed Funding)', filter_104b_only),
}


def load_and_prepare_data():
    """Load and prepare core dataset."""
    print("\n" + "="*80)
    print("STEP 1: LOADING AND PREPARING DATA")
    print("="*80)

    try:
        df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')
        print(f"✓ Data loaded: {len(df):,} rows, {len(df.columns)} columns")

        # Normalize column names and extract project year
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
        student_cols = ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']
        for col in student_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Extract year from Project ID
        def extract_year_from_project_id(project_id):
            """Extract year from Project ID."""
            import re
            if pd.isna(project_id):
                return None

            project_id_str = str(project_id).strip()

            # Try 4-digit year
            year_match = re.search(r'(20\d{2}|19\d{2})', project_id_str)
            if year_match:
                return int(year_match.group(1))

            # Try FY format
            fy_match = re.search(r'FY(\d{2})', project_id_str, re.IGNORECASE)
            if fy_match:
                fy_year = int(fy_match.group(1))
                return 2000 + fy_year if fy_year < 100 else fy_year

            return None

        df['project_year'] = df['project_id'].apply(extract_year_from_project_id)
        print(f"✓ Extracted project years")

        return df
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def verify_award_type_filtering(df):
    """Verify filtering works correctly."""
    print("\n" + "="*80)
    print("STEP 2: VERIFYING AWARD TYPE FILTERING")
    print("="*80)

    print(f"\nOriginal dataset: {df.shape[0]} rows")

    all_df = filter_all_projects(df)
    b104_df = filter_104b_only(df)

    print(f"  All Projects filter:    {all_df.shape[0]} rows, {all_df['project_id'].nunique()} unique projects")
    print(f"  104B Only filter:       {b104_df.shape[0]} rows, {b104_df['project_id'].nunique()} unique projects")

    # Verify counts match expected
    for track in ['all', '104b']:
        filter_name = '104b' if track == '104b' else 'all'
        expected_10yr = EXPECTED_COUNTS['10year'].get(track, {}).get('projects')

        if track == 'all':
            actual_10yr = all_df[all_df['project_year'].between(2015, 2024, inclusive='both')]['project_id'].nunique()
        else:
            actual_10yr = b104_df[b104_df['project_year'].between(2015, 2024, inclusive='both')]['project_id'].nunique()

        match = "✓" if actual_10yr == expected_10yr else "✗"
        print(f"  {match} {get_award_type_label(track)}: {actual_10yr} projects (expected {expected_10yr})")


def run_analysis_for_track(award_type, df):
    """Run core analysis for a specific award type track."""
    print(f"\n" + "="*80)
    print(f"STEP 3: RUNNING ANALYSIS FOR {award_type.upper()}")
    print(f"Track: {get_award_type_label(award_type)}")
    print("="*80)

    # Apply filter
    if award_type == 'all':
        df_filtered = filter_all_projects(df)
    elif award_type == '104b':
        df_filtered = filter_104b_only(df)
    else:
        raise ValueError(f"Unknown award type: {award_type}")

    print(f"\n✓ Filtered to {df_filtered.shape[0]} rows")
    print(f"✓ {df_filtered['project_id'].nunique()} unique projects")

    # Time periods
    df_10yr = df_filtered[df_filtered['project_year'].between(2015, 2024, inclusive='both')].copy()
    df_5yr = df_filtered[df_filtered['project_year'].between(2020, 2024, inclusive='both')].copy()

    print(f"\nTime periods:")
    print(f"  10-Year (2015-2024): {df_10yr['project_id'].nunique()} unique projects")
    print(f"  5-Year (2020-2024): {df_5yr['project_id'].nunique()} unique projects")

    # Calculate key metrics
    metrics = {
        'award_type': award_type,
        'label': get_award_type_label(award_type),
        'short_label': get_award_type_short_label(award_type),
        '10yr': {
            'projects': df_10yr['project_id'].nunique(),
            'investment': df_10yr['award_amount'].sum(),
            'institutions': df_10yr['institution'].nunique(),
            'students': df_10yr[['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']].sum().sum(),
        },
        '5yr': {
            'projects': df_5yr['project_id'].nunique(),
            'investment': df_5yr['award_amount'].sum(),
            'institutions': df_5yr['institution'].nunique(),
            'students': df_5yr[['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']].sum().sum(),
        },
    }

    print(f"\nKey Metrics:")
    print(f"  10-Year:")
    print(f"    Investment: ${metrics['10yr']['investment']:,.0f}")
    print(f"    Institutions: {metrics['10yr']['institutions']}")
    print(f"    Students: {int(metrics['10yr']['students'])}")
    print(f"  5-Year:")
    print(f"    Investment: ${metrics['5yr']['investment']:,.0f}")
    print(f"    Institutions: {metrics['5yr']['institutions']}")
    print(f"    Students: {int(metrics['5yr']['students'])}")

    return metrics


def create_final_deliverables_structure():
    """Create organized FINAL_DELIVERABLES directory structure."""
    print("\n" + "="*80)
    print("STEP 4: CREATING FINAL_DELIVERABLES STRUCTURE")
    print("="*80)

    # Create subdirectories
    subdirs = [
        'reports/all_projects',
        'reports/104b_only',
        'pdfs/all_projects',
        'pdfs/104b_only',
        'visualizations/static/all_projects',
        'visualizations/static/104b_only',
        'visualizations/interactive/all_projects',
        'visualizations/interactive/104b_only',
        'visualizations/interactive/award_type_comparison',
        'data_exports',
    ]

    for subdir in subdirs:
        dir_path = os.path.join(OUTPUT_DIR, subdir)
        os.makedirs(dir_path, exist_ok=True)
        print(f"  ✓ Created: {subdir}")

    print(f"\n✓ FINAL_DELIVERABLES structure created at: {OUTPUT_DIR}")


def generate_summary_report(all_metrics, b104_metrics):
    """Generate summary report of dual-track analysis."""
    print("\n" + "="*80)
    print("DUAL-TRACK ANALYSIS SUMMARY")
    print("="*80)

    print(f"\n{'Metric':<40} {'All Projects':<20} {'104B Only':<20}")
    print("-" * 80)
    print(f"{'10-Year Projects':<40} {all_metrics['10yr']['projects']:<20} {b104_metrics['10yr']['projects']:<20}")
    print(f"{'10-Year Investment':<40} ${all_metrics['10yr']['investment']:>18,.0f} ${b104_metrics['10yr']['investment']:>18,.0f}")
    print(f"{'10-Year Institutions':<40} {all_metrics['10yr']['institutions']:<20} {b104_metrics['10yr']['institutions']:<20}")
    print(f"{'10-Year Students':<40} {int(all_metrics['10yr']['students']):<20} {int(b104_metrics['10yr']['students']):<20}")

    print("\n" + "-" * 80)
    print(f"{'5-Year Projects':<40} {all_metrics['5yr']['projects']:<20} {b104_metrics['5yr']['projects']:<20}")
    print(f"{'5-Year Investment':<40} ${all_metrics['5yr']['investment']:>18,.0f} ${b104_metrics['5yr']['investment']:>18,.0f}")
    print(f"{'5-Year Institutions':<40} {all_metrics['5yr']['institutions']:<20} {b104_metrics['5yr']['institutions']:<20}")
    print(f"{'5-Year Students':<40} {int(all_metrics['5yr']['students']):<20} {int(b104_metrics['5yr']['students']):<20}")

    print("\n" + "="*80)


def main():
    """Main orchestration function."""
    start_time = datetime.now()

    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + "  IWRC SEED FUND TRACKING - DUAL-TRACK ANALYSIS ORCHESTRATOR".center(78) + "█")
    print("█" + "  With IWRC Branding and Award Type Breakdown".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)

    # Step 1: Load data
    df = load_and_prepare_data()

    # Step 2: Verify filtering
    verify_award_type_filtering(df)

    # Step 3: Run analysis for both tracks
    all_metrics = run_analysis_for_track('all', df)
    b104_metrics = run_analysis_for_track('104b', df)

    # Step 4: Create final structure
    create_final_deliverables_structure()

    # Step 5: Summary report
    generate_summary_report(all_metrics, b104_metrics)

    # Complete
    elapsed_time = (datetime.now() - start_time).total_seconds() / 60

    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + f"  ✓ ORCHESTRATION COMPLETE - {elapsed_time:.1f} minutes".ljust(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)

    print(f"\nNext Steps:")
    print(f"  1. Run individual analysis scripts for each track")
    print(f"  2. Generate static and interactive visualizations")
    print(f"  3. Create PDF reports")
    print(f"  4. Run final validation")
    print(f"  5. Push to GitHub")


if __name__ == '__main__':
    main()
