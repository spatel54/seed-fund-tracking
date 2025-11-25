#!/usr/bin/env python3
"""
Award Type Filtering Module

Provides filtering functions for IWRC Seed Fund Tracking analysis.
Creates separate analysis tracks for "All Projects" vs "104B Only" (seed funding).

Award Types in Dataset:
- Base Grant (104b): 60 projects, ~$1.7M investment (seed funding backbone)
- 104g-AIS: Aquatic Invasive Species research
- 104g-General: General water research
- 104g-PFAS: PFAS contamination research
- Coordination Grant: Strategic coordination projects

Analysis Tracks:
1. "All Projects": 104B + all 104G variants + Coordination (comprehensive view)
2. "104B Only": Base Grant only (seed funding specific)
"""

import pandas as pd


# ============================================================================
# AWARD TYPE DEFINITIONS
# ============================================================================

AWARD_TYPES = {
    'base_grant': 'Base Grant (104b)',
    '104g_ais': '104g - AIS',
    '104g_general': '104g - General',
    '104g_pfas': '104g - PFAS',
    'coordination': 'Coordination Grant',
}

AWARD_TYPE_DESCRIPTIONS = {
    'Base Grant (104b)': 'Seed funding - base grants for water research',
    '104g - AIS': 'Aquatic Invasive Species research',
    '104g - General': 'General water research',
    '104g - PFAS': 'PFAS contamination research',
    'Coordination Grant': 'Strategic coordination and administrative projects',
}

AWARD_TYPE_ABBREVIATIONS = {
    'Base Grant (104b)': '104B',
    '104g - AIS': '104G-AIS',
    '104g - General': '104G-General',
    '104g - PFAS': '104G-PFAS',
    'Coordination Grant': 'Coord',
}


# ============================================================================
# FILTER FUNCTIONS
# ============================================================================

def _normalize_award_type_column(df):
    """
    Normalize award type column - handle both raw and processed names.

    Raw column name: 'Award Type'
    Processed column name: 'award_type'
    """
    df = df.copy()
    if 'Award Type' in df.columns and 'award_type' not in df.columns:
        df = df.rename(columns={'Award Type': 'award_type'})
    return df


def filter_all_projects(df):
    """
    Returns all projects (no filtering).

    Includes: 104B + all 104G variants (AIS, General, PFAS) + Coordination
    This is the comprehensive view of all IWRC Seed Fund projects.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe with award type column

    Returns:
    --------
    pandas.DataFrame
        All projects (unchanged dataframe)
    """
    df = _normalize_award_type_column(df)
    return df


def filter_104b_only(df):
    """
    Returns only Base Grant (104b) projects.

    This represents the "seed funding" component specifically - smaller grants
    that form the foundational support for water research across institutions.

    Expected 10-year count: 60 unique projects
    Expected 5-year count: 33 unique projects

    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe with award type column

    Returns:
    --------
    pandas.DataFrame
        Filtered dataframe with only 104B projects
    """
    df = _normalize_award_type_column(df)
    return df[df['award_type'] == 'Base Grant (104b)'].copy()


def filter_104g_all(df):
    """
    Returns all 104g grants (all variants: AIS, General, PFAS).

    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe with award type column

    Returns:
    --------
    pandas.DataFrame
        Filtered dataframe with only 104g projects
    """
    return df[df['award_type'].str.contains('104g', case=False, na=False)].copy()


def filter_104g_ais(df):
    """Returns only 104g-AIS (Aquatic Invasive Species) projects."""
    return df[df['award_type'] == '104g - AIS'].copy()


def filter_104g_general(df):
    """Returns only 104g-General (General water research) projects."""
    return df[df['award_type'] == '104g - General'].copy()


def filter_104g_pfas(df):
    """Returns only 104g-PFAS (PFAS contamination) projects."""
    return df[df['award_type'] == '104g - PFAS'].copy()


def filter_coordination(df):
    """Returns only Coordination Grant projects."""
    return df[df['award_type'] == 'Coordination Grant'].copy()


# ============================================================================
# FILTER MAPPING & UTILITIES
# ============================================================================

FILTER_FUNCTIONS = {
    'all': filter_all_projects,
    'all_projects': filter_all_projects,
    '104b': filter_104b_only,
    '104b_only': filter_104b_only,
    '104g': filter_104g_all,
    '104g_all': filter_104g_all,
    '104g_ais': filter_104g_ais,
    '104g_general': filter_104g_general,
    '104g_pfas': filter_104g_pfas,
    'coordination': filter_coordination,
}


def get_filter_function(filter_type):
    """
    Get filter function by name.

    Parameters:
    -----------
    filter_type : str
        Filter name: 'all', '104b', '104g', '104g_ais', '104g_general',
        '104g_pfas', 'coordination'

    Returns:
    --------
    callable
        Filter function that takes DataFrame and returns filtered DataFrame

    Raises:
    -------
    ValueError
        If filter_type is not recognized
    """
    filter_key = filter_type.lower().strip()

    if filter_key not in FILTER_FUNCTIONS:
        available = ', '.join(FILTER_FUNCTIONS.keys())
        raise ValueError(f"Unknown filter type: {filter_type}\n"
                        f"Available filters: {available}")

    return FILTER_FUNCTIONS[filter_key]


def apply_filter(df, filter_type):
    """
    Apply filter to dataframe.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe
    filter_type : str
        Filter name

    Returns:
    --------
    pandas.DataFrame
        Filtered dataframe
    """
    filter_func = get_filter_function(filter_type)
    return filter_func(df)


# ============================================================================
# LABEL & DESCRIPTION FUNCTIONS
# ============================================================================

def get_award_type_label(filter_type):
    """
    Get display label for award type filter.

    Parameters:
    -----------
    filter_type : str
        Filter name: 'all' or '104b'

    Returns:
    --------
    str
        Display label for reports/charts
    """
    labels = {
        'all': 'All Projects (104B + 104G + Coordination)',
        'all_projects': 'All Projects (104B + 104G + Coordination)',
        '104b': '104B Only (Base Grant - Seed Funding)',
        '104b_only': '104B Only (Base Grant - Seed Funding)',
        '104g': '104G Programs (AIS, General, PFAS)',
        '104g_all': '104G Programs (AIS, General, PFAS)',
        '104g_ais': '104G-AIS (Aquatic Invasive Species)',
        '104g_general': '104G-General (General Water Research)',
        '104g_pfas': '104G-PFAS (PFAS Contamination)',
        'coordination': 'Coordination Grants',
    }

    filter_key = filter_type.lower().strip()
    return labels.get(filter_key, f'Unknown Filter: {filter_type}')


def get_award_type_short_label(filter_type):
    """
    Get short label for award type filter (for filenames, charts).

    Parameters:
    -----------
    filter_type : str
        Filter name

    Returns:
    --------
    str
        Short label
    """
    labels = {
        'all': 'All_Projects',
        'all_projects': 'All_Projects',
        '104b': '104B_Only',
        '104b_only': '104B_Only',
        '104g': '104G_All',
        '104g_all': '104G_All',
        '104g_ais': '104G_AIS',
        '104g_general': '104G_General',
        '104g_pfas': '104G_PFAS',
        'coordination': 'Coordination',
    }

    filter_key = filter_type.lower().strip()
    return labels.get(filter_key, filter_type)


def get_award_type_description(award_type):
    """
    Get description of award type.

    Parameters:
    -----------
    award_type : str
        Award type name (e.g., 'Base Grant (104b)')

    Returns:
    --------
    str
        Description of award type
    """
    return AWARD_TYPE_DESCRIPTIONS.get(award_type, 'Unknown award type')


# ============================================================================
# ANALYSIS METADATA
# ============================================================================

EXPECTED_COUNTS = {
    '10year': {
        'all': {'projects': 77, 'description': '10-year all projects'},
        '104b': {'projects': 60, 'description': '10-year 104B only'},
    },
    '5year': {
        'all': {'projects': 47, 'description': '5-year all projects'},
        '104b': {'projects': 33, 'description': '5-year 104B only'},
    },
}


def get_expected_project_count(time_period, filter_type):
    """
    Get expected project count for given time period and filter.

    Parameters:
    -----------
    time_period : str
        '10year' or '5year'
    filter_type : str
        'all' or '104b'

    Returns:
    --------
    int or None
        Expected number of unique projects, or None if unknown
    """
    period_key = time_period.lower().strip().replace('-', '').replace(' ', '')
    filter_key = filter_type.lower().strip()

    if period_key not in EXPECTED_COUNTS:
        return None

    if filter_key not in EXPECTED_COUNTS[period_key]:
        return None

    return EXPECTED_COUNTS[period_key][filter_key].get('projects')


# ============================================================================
# DISTRIBUTION & ANALYSIS FUNCTIONS
# ============================================================================

def get_award_type_distribution(df):
    """
    Get distribution of projects across award types.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe

    Returns:
    --------
    pandas.Series
        Count of unique projects by award type
    """
    return df.groupby('award_type')['project_id'].nunique().sort_values(ascending=False)


def get_award_type_investment_distribution(df):
    """
    Get investment distribution across award types.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe

    Returns:
    --------
    pandas.DataFrame
        Investment metrics by award type
    """
    return df.groupby('award_type').agg({
        'project_id': 'nunique',
        'award_amount': 'sum',
    }).rename(columns={'project_id': 'projects'})


def verify_award_type_data_quality(df):
    """
    Verify data quality for award type filtering.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe

    Returns:
    --------
    dict
        Quality metrics
    """
    total_rows = len(df)
    rows_with_award_type = df['award_type'].notna().sum()
    coverage_pct = (rows_with_award_type / total_rows * 100) if total_rows > 0 else 0

    return {
        'total_rows': total_rows,
        'rows_with_award_type': rows_with_award_type,
        'rows_missing_award_type': total_rows - rows_with_award_type,
        'coverage_percent': coverage_pct,
        'award_type_values': df['award_type'].value_counts().to_dict(),
    }


# ============================================================================
# REPORTING FUNCTIONS
# ============================================================================

def print_filter_summary(df, filter_type):
    """
    Print summary of filtered data.

    Parameters:
    -----------
    df : pandas.DataFrame
        Original dataframe
    filter_type : str
        Filter to apply
    """
    filtered_df = apply_filter(df, filter_type)
    label = get_award_type_label(filter_type)

    print(f"\n{'='*70}")
    print(f"FILTER: {label}")
    print(f"{'='*70}")
    print(f"  Rows (outputs):        {len(filtered_df):,}")
    print(f"  Unique Projects:       {filtered_df['project_id'].nunique():,}")
    print(f"  Total Investment:      ${filtered_df['award_amount'].sum():,.0f}")
    print(f"  Total Students:        {filtered_df[['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']].sum().sum():.0f}")
    print(f"  Institutions:          {filtered_df['institution'].nunique():,}")


def compare_filters(df, filter_type_1, filter_type_2):
    """
    Compare metrics between two filters.

    Parameters:
    -----------
    df : pandas.DataFrame
        Original dataframe
    filter_type_1 : str
        First filter name
    filter_type_2 : str
        Second filter name

    Returns:
    --------
    pandas.DataFrame
        Comparison table
    """
    df1 = apply_filter(df, filter_type_1)
    df2 = apply_filter(df, filter_type_2)

    label1 = get_award_type_label(filter_type_1)
    label2 = get_award_type_label(filter_type_2)

    projects1 = df1['project_id'].nunique()
    projects2 = df2['project_id'].nunique()

    investment1 = df1['award_amount'].sum()
    investment2 = df2['award_amount'].sum()

    students1 = df1[['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']].sum().sum()
    students2 = df2[['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']].sum().sum()

    institutions1 = df1['institution'].nunique()
    institutions2 = df2['institution'].nunique()

    comparison = pd.DataFrame({
        label1: [projects1, investment1, students1, institutions1],
        label2: [projects2, investment2, students2, institutions2],
    }, index=['Projects', 'Investment ($)', 'Students', 'Institutions'])

    return comparison


if __name__ == '__main__':
    # Test the award type filters module
    print("Award Type Filters Module Test")
    print("=" * 70)

    print("\nAvailable Filters:")
    for name, func in FILTER_FUNCTIONS.items():
        label = get_award_type_label(name)
        print(f"  {name:20} → {label}")

    print("\nAward Types in Dataset:")
    for name, desc in AWARD_TYPE_DESCRIPTIONS.items():
        abbrev = AWARD_TYPE_ABBREVIATIONS[name]
        print(f"  {name:30} ({abbrev:15}) - {desc}")

    print("\nExpected Project Counts:")
    for period in ['10year', '5year']:
        print(f"\n  {period}:")
        for filter_type in ['all', '104b']:
            count = get_expected_project_count(period, filter_type)
            label = get_award_type_label(filter_type)
            print(f"    {label:50} {count}")

    print("\n" + "=" * 70)
    print("✓ Module test complete")
