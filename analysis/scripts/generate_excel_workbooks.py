#!/usr/bin/env python3
"""
IWRC Seed Fund Tracking - Excel Comparison Workbook - CORRECTED VERSION

This script replaces stage5_excel_and_documentation.py which had double-counting errors.

Key Improvements:
- Uses IWRCDataLoader for proper deduplication
- Calculates all metrics correctly (no double-counting)
- Uses groupby('project_id').first() before aggregations
- Generates corrected Excel comparison workbook

Generates:
- Dual_Track_Metrics_Comparison.xlsx (CORRECTED)

Author: IWRC Data Quality Team
Date: November 27, 2025
Version: 1.0 (CORRECTED)
"""

import pandas as pd
import os
import sys
from datetime import datetime
from pathlib import Path

# Setup
sys.path.insert(0, str(Path(__file__).parent))

# Import IWRC data loader
from iwrc_data_loader import IWRCDataLoader

PROJECT_ROOT = '/Users/shivpat/seed-fund-tracking'
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'FINAL_DELIVERABLES 2/data_exports')

print(f"\n{'█' * 80}")
print(f"█ EXCEL COMPARISON WORKBOOK (CORRECTED VERSION)".center(80) + "█")
print(f"{'█' * 80}\n")


def create_excel_comparison_corrected(all_10yr, b104_10yr, loader):
    """Create Excel comparison workbook with CORRECTED metrics."""
    print("  Creating: Dual_Track_Metrics_Comparison.xlsx (CORRECTED)")
    
    # Calculate metrics using corrected loader
    all_metrics = loader.calculate_metrics(all_10yr, period='10yr')
    b104_metrics = loader.calculate_metrics(b104_10yr, period='10yr')
    
    # Create comparison DataFrame
    comparison_data = {
        'Metric': [
            'Time Period',
            'Total Investment',
            'Number of Projects',
            'Total Students',
            'PhD Students',
            'Masters Students',
            'Undergraduate Students',
            'Postdoc Students',
            'Cost per Project',
            'Cost per Student',
            'Students per Project',
            'Projects per $1M',
            'Students per $1M',
        ],
        'All Projects': [
            '2015-2024',
            f"${all_metrics['investment']:,.2f}",
            f"{all_metrics['projects']}",
            f"{all_metrics['students']}",
            f"{all_metrics['phd']}",
            f"{all_metrics['masters']}",
            f"{all_metrics['undergrad']}",
            f"{all_metrics['postdoc']}",
            f"${all_metrics['investment_per_project']:,.2f}",
            f"${all_metrics['investment_per_student']:,.2f}",
            f"{all_metrics['students_per_project']:.2f}",
            f"{(all_metrics['projects']/all_metrics['investment']*1_000_000):.2f}",
            f"{(all_metrics['students']/all_metrics['investment']*1_000_000):.2f}",
        ],
        '104B Only': [
            '2015-2024',
            f"${b104_metrics['investment']:,.2f}",
            f"{b104_metrics['projects']}",
            f"{b104_metrics['students']}",
            f"{b104_metrics['phd']}",
            f"{b104_metrics['masters']}",
            f"{b104_metrics['undergrad']}",
            f"{b104_metrics['postdoc']}",
            f"${b104_metrics['investment_per_project']:,.2f}",
            f"${b104_metrics['investment_per_student']:,.2f}",
            f"{b104_metrics['students_per_project']:.2f}",
            f"{(b104_metrics['projects']/b104_metrics['investment']*1_000_000):.2f}",
            f"{(b104_metrics['students']/b104_metrics['investment']*1_000_000):.2f}",
        ]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Create Excel workbook with multiple sheets
    with pd.ExcelWriter(os.path.join(OUTPUT_DIR, 'Dual_Track_Metrics_Comparison.xlsx'),
                       engine='openpyxl') as writer:
        # Summary comparison sheet
        comparison_df.to_excel(writer, sheet_name='Summary Comparison', index=False)
        
        # All Projects detailed breakdown (yearly)
        # Use deduplicated data - groupby project_id first, then by year
        all_deduped = all_10yr.groupby('project_id').first().reset_index()
        all_yearly = all_deduped.groupby('project_year').agg({
            'award_amount_numeric': 'sum',
            'project_id': 'count',
            'phd_students': 'sum',
            'ms_students': 'sum',
            'undergrad_students': 'sum',
            'postdoc_students': 'sum'
        }).reset_index()
        all_yearly.columns = ['Year', 'Total Investment', 'Projects', 'PhD', 'Masters', 'Undergrad', 'Postdoc']
        all_yearly.to_excel(writer, sheet_name='All Projects - Yearly', index=False)
        
        # 104B detailed breakdown (yearly)
        b104_deduped = b104_10yr.groupby('project_id').first().reset_index()
        b104_yearly = b104_deduped.groupby('project_year').agg({
            'award_amount_numeric': 'sum',
            'project_id': 'count',
            'phd_students': 'sum',
            'ms_students': 'sum',
            'undergrad_students': 'sum',
            'postdoc_students': 'sum'
        }).reset_index()
        b104_yearly.columns = ['Year', 'Total Investment', 'Projects', 'PhD', 'Masters', 'Undergrad', 'Postdoc']
        b104_yearly.to_excel(writer, sheet_name='104B - Yearly', index=False)
        
        # Award type breakdown for all projects
        all_by_award = all_deduped.groupby('award_type').agg({
            'award_amount_numeric': 'sum',
            'project_id': 'count',
            'phd_students': 'sum',
            'ms_students': 'sum',
            'undergrad_students': 'sum',
            'postdoc_students': 'sum'
        }).reset_index()
        all_by_award.columns = ['Award Type', 'Total Investment', 'Projects', 'PhD', 'Masters', 'Undergrad', 'Postdoc']
        all_by_award = all_by_award.sort_values('Total Investment', ascending=False)
        all_by_award.to_excel(writer, sheet_name='Award Type Breakdown', index=False)
        
        # Institution breakdown
        all_by_inst = all_deduped.groupby('institution').agg({
            'award_amount_numeric': 'sum',
            'project_id': 'count'
        }).reset_index()
        all_by_inst.columns = ['Institution', 'Total Investment', 'Projects']
        all_by_inst = all_by_inst.sort_values('Total Investment', ascending=False)
        all_by_inst.to_excel(writer, sheet_name='Institutions', index=False)
    
    print(f"    ✓ Generated: Dual_Track_Metrics_Comparison.xlsx")
    print(f"\n  Metrics included:")
    print(f"    All Projects - Investment: ${all_metrics['investment']:,.2f}, Students: {all_metrics['students']}")
    print(f"    104B Only - Investment: ${b104_metrics['investment']:,.2f}, Students: {b104_metrics['students']}")


def main():
    """Main orchestration."""
    print("="*80)
    print("LOADING DATA WITH PROPER DEDUPLICATION")
    print("="*80)
    
    # Initialize loader
    loader = IWRCDataLoader()
    df = loader.load_master_data(deduplicate=True)
    
    # Filter for 2015-2024
    df_10yr = df[df['project_year'].between(2015, 2024, inclusive='both')]
    
    # Split into tracks
    all_10yr = df_10yr
    b104_10yr = df_10yr[df_10yr['award_type'] == 'Base Grant (104b)']
    
    print(f"✓ All Projects (2015-2024): {all_10yr['project_id'].nunique()} projects")
    print(f"✓ 104B Only (2015-2024): {b104_10yr['project_id'].nunique()} projects\n")
    
    print("="*80)
    print("CREATING EXCEL WORKBOOK")
    print("="*80 + "\n")
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate Excel file
    create_excel_comparison_corrected(all_10yr, b104_10yr, loader)
    
    print("\n" + "█" * 80)
    print("█" + " ✓ EXCEL WORKBOOK GENERATED (CORRECTED)".center(78) + "█")
    print("█" * 80)
    print("\nGenerated File:")
    print("  • data_exports/Dual_Track_Metrics_Comparison.xlsx")
    print("\n✅ All metrics use CORRECTED values (no double-counting)")
    print("="*80)


if __name__ == '__main__':
    main()
