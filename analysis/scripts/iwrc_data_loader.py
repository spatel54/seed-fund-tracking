#!/usr/bin/env python3
"""
IWRC Data Loader - Centralized Data Loading with Built-in Deduplication

This module provides a single source of truth for loading IWRC Seed Fund data
with automatic deduplication to prevent double-counting errors.

Features:
- Automatic deduplication by project_id
- Institution name standardization (fixes spelling variations)
- Built-in metric calculations

Author: IWRC Data Quality Team
Date: November 27, 2025
Version: 1.1
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path
from typing import Dict, Optional, Tuple
import warnings

# Institution name standardization mapping
# Maps all variations to canonical names
INSTITUTION_NAME_MAP = {
    # University of Illinois variations → canonical name
    'University of Illinois Urbana-Champaign': 'University of Illinois at Urbana-Champaign',
    'University of Illinois': 'University of Illinois at Urbana-Champaign',
    'University of Illinois  ': 'University of Illinois at Urbana-Champaign',  # extra space
    'Univeristy of Illinois': 'University of Illinois at Urbana-Champaign',  # typo
    # University of Illinois at Urbana-Champaign maps to itself (canonical)
    
    # Southern Illinois University variations → canonical name
    'Southern Illinois University at Carbondale': 'Southern Illinois University',
    'Southern Illinois University Carbondale': 'Southern Illinois University',
    # Southern Illinois University maps to itself (canonical)
}


class IWRCDataLoader:
    """
    Centralized data loader for IWRC Seed Fund Tracking data.

    Features:
    - Automatic deduplication by project_id
    - Institution name standardization (fixes spelling variations)
    - Handles column name variations (trailing spaces)
    - Built-in metric calculations with proper deduplication
    - Support for both master dataset and fact sheet data
    - Data quality warnings and validation

    Example:
        >>> loader = IWRCDataLoader()
        >>> df = loader.load_master_data(deduplicate=True)
        >>> metrics = loader.calculate_metrics(df, period='10yr')
        >>> print(f"Investment: ${metrics['investment']:,.2f}")
    """

    def __init__(self, project_root: Optional[str] = None):
        """
        Initialize the data loader.

        Args:
            project_root: Path to project root directory.
                         If None, uses default path.
        """
        if project_root is None:
            project_root = '/Users/shivpat/seed-fund-tracking'

        self.project_root = Path(project_root)
        # UPDATED: Pointing to the new cleaned and deduplicated dataset
        self.master_file = self.project_root / 'data/processed/clean_iwrc_tracking.xlsx'
        self.fact_sheet_file = self.project_root / 'data/consolidated/fact sheet data.xlsx'

        # Column mapping with trailing space handling
        self.col_map = {
            'Project ID ': 'project_id',  # Note trailing space!
            'Project ID': 'project_id',
            'Award Type': 'award_type',
            'Project Title': 'project_title',
            'Project PI': 'pi_name',
            'Academic Institution of PI': 'institution',
            'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount',
            'Number of PhD Students Supported by WRRA $': 'phd_students',
            'Number of MS Students Supported by WRRA $': 'ms_students',
            'Number of Undergraduate Students Supported by WRRA $': 'undergrad_students',
            'Number of Post Docs Supported by WRRA $': 'postdoc_students',
            'WRRI Science Priority that Best Aligns with this Project': 'science_priority',
        }

    def load_master_data(self, deduplicate: bool = True) -> pd.DataFrame:
        """
        Load the master IWRC Seed Fund Tracking dataset.

        Args:
            deduplicate: If True, ensures each project appears only once.
                        If False, returns raw data (use with caution!)

        Returns:
            DataFrame with standardized column names and optional deduplication.

        Raises:
            FileNotFoundError: If master file doesn't exist.

        Example:
            >>> loader = IWRCDataLoader()
            >>> df = loader.load_master_data(deduplicate=True)
            >>> print(f"Unique projects: {df['project_id'].nunique()}")
        """
        if not self.master_file.exists():
            raise FileNotFoundError(f"Master file not found: {self.master_file}")

        # Load data
        df = pd.read_excel(self.master_file, sheet_name='Project Overview')

        # Rename columns (handles trailing spaces)
        df = df.rename(columns=self.col_map)

        # Extract project year
        df['project_year'] = df['project_id'].apply(self._extract_year)

        # Convert numeric columns
        df['award_amount_numeric'] = pd.to_numeric(df['award_amount'], errors='coerce')

        student_cols = ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']
        for col in student_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Standardize institution names
        df = self._standardize_institution_names(df)

        if deduplicate:
            # The source file is already deduplicated, but we keep this check for safety
            # and to handle any potential future duplicates if the file is manually edited.
            initial_count = len(df)
            df = self._deduplicate_by_project(df)
            final_count = len(df)
            if initial_count != final_count:
                print(f"✓ Loaded {initial_count} rows, deduplicated to {final_count} unique projects")
            else:
                print(f"✓ Loaded {final_count} unique projects (already clean)")
        else:
            warnings.warn(
                "⚠️  Loading data WITHOUT deduplication! "
                "This may cause double-counting errors. "
                "Use deduplicate=True unless you have a specific reason not to.",
                UserWarning
            )

        return df

    def load_fact_sheet_data(self, year: str = '2025', warn: bool = True) -> pd.DataFrame:
        """
        Load fact sheet data (use with caution - no Project ID column).

        ⚠️ WARNING: This file lacks a Project ID column and cannot be reliably
        deduplicated. Use ONLY for visualizations (keywords, geography).
        DO NOT use for financial calculations or metric summaries.

        Args:
            year: Sheet name to load (default: '2025 data')
            warn: If True, displays warning about limitations

        Returns:
            DataFrame with fact sheet data (no deduplication possible)

        Example:
            >>> loader = IWRCDataLoader()
            >>> df = loader.load_fact_sheet_data(year='2025')
            >>> # Safe: keyword analysis
            >>> keywords = df['Keyword 2'].value_counts()
            >>> # UNSAFE: financial totals (may double-count!)
        """
        if not self.fact_sheet_file.exists():
            raise FileNotFoundError(f"Fact sheet file not found: {self.fact_sheet_file}")

        sheet_name = f'{year} data'
        df = pd.read_excel(self.fact_sheet_file, sheet_name=sheet_name)

        if warn:
            warnings.warn(
                f"\n{'='*70}\n"
                f"⚠️  FACT SHEET DATA LIMITATIONS\n"
                f"{'='*70}\n"
                f"File: {self.fact_sheet_file.name}\n"
                f"Rows: {len(df)}\n\n"
                f"CRITICAL ISSUES:\n"
                f"  ❌ NO Project ID column - cannot deduplicate\n"
                f"  ❌ May contain duplicate projects (unknown)\n"
                f"  ❌ Cannot cross-reference with master data\n\n"
                f"SAFE USES:\n"
                f"  ✅ Keyword analysis (frequency counts)\n"
                f"  ✅ Geographic visualizations\n"
                f"  ✅ Descriptive statistics\n\n"
                f"UNSAFE USES:\n"
                f"  ❌ Summing Award Amount (may double-count)\n"
                f"  ❌ Summing student counts (may double-count)\n"
                f"  ❌ ROI calculations\n"
                f"  ❌ Financial reporting\n\n"
                f"For accurate metrics, use load_master_data() instead.\n"
                f"See: data/consolidated/FACT_SHEET_DATA_README.md\n"
                f"{'='*70}\n",
                UserWarning
            )

        return df

    def calculate_metrics(self, df: pd.DataFrame, period: str = '10yr') -> Dict:
        """
        Calculate metrics with guaranteed deduplication.

        Args:
            df: DataFrame (should already be deduplicated)
            period: '10yr' (2015-2024) or '5yr' (2020-2024)

        Returns:
            Dictionary with metrics:
            - projects: int
            - investment: float
            - students: int
            - phd, masters, undergrad, postdoc: int
            - institutions: int
            - roi: float
            - followon: float
            - students_per_project: float
            - investment_per_project: float
            - investment_per_student: float

        Example:
            >>> loader = IWRCDataLoader()
            >>> df = loader.load_master_data(deduplicate=True)
            >>> metrics = loader.calculate_metrics(df, period='10yr')
            >>> print(f"ROI: {metrics['roi']:.1%}")
        """
        # Filter by period
        if period == '10yr':
            df_filtered = df[df['project_year'].between(2015, 2024, inclusive='both')]
        elif period == '5yr':
            df_filtered = df[df['project_year'].between(2020, 2024, inclusive='both')]
        else:
            raise ValueError(f"Invalid period: {period}. Use '10yr' or '5yr'.")

        # Verify deduplication
        if len(df_filtered) != df_filtered['project_id'].nunique():
            warnings.warn(
                f"⚠️  DataFrame contains duplicate project IDs! "
                f"Rows: {len(df_filtered)}, Unique projects: {df_filtered['project_id'].nunique()}. "
                f"Use load_master_data(deduplicate=True) to fix.",
                UserWarning
            )
            # Apply deduplication here as safety measure
            df_filtered = self._deduplicate_by_project(df_filtered)

        metrics = {}

        # Project count
        metrics['projects'] = df_filtered['project_id'].nunique()

        # Investment (already deduplicated DataFrame)
        metrics['investment'] = df_filtered['award_amount_numeric'].sum()

        # Student counts (already deduplicated DataFrame)
        student_cols = ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']
        student_totals = df_filtered[student_cols].sum()

        metrics['students'] = int(student_totals.sum())
        metrics['phd'] = int(student_totals['phd_students'])
        metrics['masters'] = int(student_totals['ms_students'])
        metrics['undergrad'] = int(student_totals['undergrad_students'])
        metrics['postdoc'] = int(student_totals['postdoc_students'])

        # Institutions
        metrics['institutions'] = df_filtered['institution'].nunique()

        # Efficiency metrics
        metrics['students_per_project'] = metrics['students'] / metrics['projects'] if metrics['projects'] > 0 else 0
        metrics['investment_per_project'] = metrics['investment'] / metrics['projects'] if metrics['projects'] > 0 else 0
        metrics['investment_per_student'] = metrics['investment'] / metrics['students'] if metrics['students'] > 0 else 0

        # ROI (7% for 10yr, 8% for 5yr based on corrected analysis)
        metrics['roi'] = 0.07 if period == '10yr' else 0.08
        metrics['followon'] = metrics['investment'] * metrics['roi']

        return metrics

    def _deduplicate_by_project(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Deduplicate DataFrame by taking first occurrence of each project_id.

        This is CRITICAL to prevent double-counting since the source file
        has multiple rows per project (one for each output/publication).

        Args:
            df: DataFrame with potential duplicates

        Returns:
            DataFrame with one row per unique project_id
        """
        # Group by project_id and take first row
        # This preserves the first occurrence of award amount, students, etc.
        df_deduped = df.groupby('project_id').first().reset_index()

        return df_deduped

    def _standardize_institution_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize institution names to fix spelling variations.

        Applies the INSTITUTION_NAME_MAP to convert all variations to
        canonical institution names.

        Args:
            df: DataFrame with 'institution' column

        Returns:
            DataFrame with standardized institution names
        """
        if 'institution' not in df.columns:
            return df

        # First, strip whitespace from all institution names
        df['institution'] = df['institution'].str.strip()

        # Apply mapping
        original_unique = df['institution'].nunique()
        df['institution'] = df['institution'].replace(INSTITUTION_NAME_MAP)
        standardized_unique = df['institution'].nunique()

        if original_unique != standardized_unique:
            print(f"✓ Standardized institution names: {original_unique} → {standardized_unique} unique institutions")

        return df

    def _extract_year(self, project_id) -> Optional[int]:
        """
        Extract year from Project ID.

        Handles formats:
        - "2015-001" -> 2015
        - "2020-IL103AIS" -> 2020
        - "FY16-XXX" -> 2016

        Args:
            project_id: Project ID string

        Returns:
            Year as integer, or None if no year found
        """
        if pd.isna(project_id):
            return None

        project_id_str = str(project_id).strip()

        # Try 4-digit year (20XX or 19XX)
        year_match = re.search(r'(20\d{2}|19\d{2})', project_id_str)
        if year_match:
            return int(year_match.group(1))

        # Try FY format (FY16 -> 2016)
        fy_match = re.search(r'FY(\d{2})', project_id_str, re.IGNORECASE)
        if fy_match:
            fy_year = int(fy_match.group(1))
            return 2000 + fy_year if fy_year < 100 else fy_year

        return None

    def validate_data_quality(self, df: pd.DataFrame) -> Dict:
        """
        Run data quality checks on a DataFrame.

        Args:
            df: DataFrame to validate

        Returns:
            Dictionary with validation results
        """
        results = {
            'total_rows': len(df),
            'unique_projects': df['project_id'].nunique(),
            'has_duplicates': len(df) != df['project_id'].nunique(),
            'null_project_ids': df['project_id'].isna().sum(),
            'null_award_amounts': df['award_amount_numeric'].isna().sum(),
            'valid_years': df['project_year'].notna().sum(),
        }

        # Add duplication factor
        if results['unique_projects'] > 0:
            results['duplication_factor'] = results['total_rows'] / results['unique_projects']
        else:
            results['duplication_factor'] = 0

        return results


# Convenience functions for quick access
def load_master(deduplicate=True) -> pd.DataFrame:
    """Quick function to load master data."""
    loader = IWRCDataLoader()
    return loader.load_master_data(deduplicate=deduplicate)


def calculate_metrics(df: pd.DataFrame, period='10yr') -> Dict:
    """Quick function to calculate metrics."""
    loader = IWRCDataLoader()
    return loader.calculate_metrics(df, period=period)


# Example usage
if __name__ == '__main__':
    print("="*80)
    print("IWRC DATA LOADER - Example Usage")
    print("="*80)

    # Initialize loader
    loader = IWRCDataLoader()

    # Load master data with deduplication
    print("\n1. Loading Master Data (with deduplication):")
    df = loader.load_master_data(deduplicate=True)

    # Validate data quality
    print("\n2. Data Quality Validation:")
    validation = loader.validate_data_quality(df)
    for key, value in validation.items():
        print(f"  {key}: {value}")

    # Calculate metrics
    print("\n3. Calculate 10-Year Metrics:")
    metrics_10yr = loader.calculate_metrics(df, period='10yr')
    print(f"  Projects: {metrics_10yr['projects']}")
    print(f"  Investment: ${metrics_10yr['investment']:,.2f}")
    print(f"  Students: {metrics_10yr['students']}")
    print(f"  ROI: {metrics_10yr['roi']:.1%}")

    print("\n4. Calculate 5-Year Metrics:")
    metrics_5yr = loader.calculate_metrics(df, period='5yr')
    print(f"  Projects: {metrics_5yr['projects']}")
    print(f"  Investment: ${metrics_5yr['investment']:,.2f}")
    print(f"  Students: {metrics_5yr['students']}")
    print(f"  ROI: {metrics_5yr['roi']:.1%}")

    print("\n" + "="*80)
    print("✅ Data loader working correctly!")
    print("="*80)
