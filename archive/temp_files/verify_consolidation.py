#!/usr/bin/env python3
"""
Verification script to check data consolidation quality
Checks for column mapping, unknown values, and data integrity
"""

import pandas as pd
import numpy as np
from pathlib import Path

# File paths
PROJECT_ROOT = Path('/Users/shivpat/seed-fund-tracking')
SOURCE_DIR = PROJECT_ROOT / 'data/source'
CONSOLIDATED_FILE = PROJECT_ROOT / 'data/consolidated/IWRC Seed Fund Tracking.xlsx'

source_files = {
    'WRRA_2022': SOURCE_DIR / 'IWRC-2022-WRRA-Annual-Report-v.101923.xlsx',
    'FY16-20': SOURCE_DIR / 'IL_5yr_FY16_20_2.xlsx',
    'FY23': SOURCE_DIR / 'FY23_reporting_IL.xlsx',
    'FY24': SOURCE_DIR / 'FY24_reporting_IL.xlsx',
}

print("="*100)
print("DATA CONSOLIDATION VERIFICATION REPORT")
print("="*100)

# Load consolidated data
print("\n1. LOADING CONSOLIDATED DATA")
print("-"*100)
try:
    consolidated_df = pd.read_excel(CONSOLIDATED_FILE, sheet_name='Project Overview')
    print(f"✓ Loaded consolidated file: {len(consolidated_df)} rows, {len(consolidated_df.columns)} columns")
    print(f"\nConsolidated columns:")
    for i, col in enumerate(consolidated_df.columns, 1):
        print(f"  {i:2d}. {col}")
except Exception as e:
    print(f"✗ Error loading consolidated file: {e}")
    exit(1)

# Load each source file
print("\n\n2. LOADING SOURCE FILES")
print("-"*100)
source_data = {}
for name, filepath in source_files.items():
    print(f"\n{name}: {filepath.name}")
    try:
        df = pd.read_excel(filepath, sheet_name='Project Overview')
        source_data[name] = df
        print(f"  ✓ Loaded: {len(df)} rows, {len(df.columns)} columns")

        # Show first few column names
        print(f"  Columns (first 10):")
        for i, col in enumerate(df.columns[:10], 1):
            print(f"    {i:2d}. {col}")
        if len(df.columns) > 10:
            print(f"    ... and {len(df.columns) - 10} more columns")

    except Exception as e:
        print(f"  ✗ Error: {e}")

# Check for column mapping issues
print("\n\n3. COLUMN MAPPING VERIFICATION")
print("-"*100)
consolidated_cols = set(consolidated_df.columns)

for name, df in source_data.items():
    print(f"\n{name}:")
    source_cols = set(df.columns)

    # Check which columns are in source but not in consolidated
    unmapped_cols = []
    for col in source_cols:
        col_clean = str(col).strip().lower()
        # Check if there's any similar column in consolidated
        found = False
        for cons_col in consolidated_cols:
            cons_clean = str(cons_col).strip().lower()
            if col_clean == cons_clean or col_clean in cons_clean or cons_clean in col_clean:
                found = True
                break
        if not found and 'unnamed' not in col_clean:
            unmapped_cols.append(col)

    if unmapped_cols:
        print(f"  ⚠️  Potentially unmapped columns ({len(unmapped_cols)}):")
        for col in unmapped_cols[:10]:
            print(f"    - {col}")
        if len(unmapped_cols) > 10:
            print(f"    ... and {len(unmapped_cols) - 10} more")
    else:
        print(f"  ✓ All columns appear mapped")

# Check for unknown/ambiguous values
print("\n\n4. UNKNOWN/AMBIGUOUS VALUES CHECK")
print("-"*100)

# Define key columns to check
key_columns = [
    'Project ID ',
    'Award Type',
    'Academic Institution of PI',
    'Award Amount Allocated ($) this must be filled in for all lines',
    'WRRI Science Priority that Best Aligns with this Project',
]

for col in key_columns:
    if col in consolidated_df.columns:
        print(f"\n{col}:")

        # Check for null/empty values
        null_count = consolidated_df[col].isna().sum()
        empty_count = (consolidated_df[col].astype(str).str.strip() == '').sum()
        total_issues = null_count + empty_count

        if total_issues > 0:
            print(f"  ⚠️  {total_issues} missing/empty values ({null_count} null, {empty_count} empty)")
        else:
            print(f"  ✓ No missing values")

        # Show unique values if categorical (and not too many)
        unique_values = consolidated_df[col].dropna().unique()
        if len(unique_values) < 50 and 'Amount' not in col:
            print(f"  Unique values ({len(unique_values)}):")
            for val in sorted([str(v) for v in unique_values])[:20]:
                count = (consolidated_df[col].astype(str) == val).sum()
                print(f"    - {val} ({count} rows)")
            if len(unique_values) > 20:
                print(f"    ... and {len(unique_values) - 20} more values")
    else:
        print(f"\n{col}:")
        print(f"  ✗ Column not found in consolidated data!")

# Check for data quality issues
print("\n\n5. DATA QUALITY CHECKS")
print("-"*100)

# Check Project IDs
print("\nProject ID Analysis:")
if 'Project ID ' in consolidated_df.columns:
    project_ids = consolidated_df['Project ID '].dropna()
    print(f"  Total Project IDs: {len(project_ids)}")
    print(f"  Unique Project IDs: {project_ids.nunique()}")

    duplicates = project_ids[project_ids.duplicated()].unique()
    if len(duplicates) > 0:
        print(f"  ⚠️  Duplicate Project IDs found ({len(duplicates)}):")
        for pid in list(duplicates)[:10]:
            count = (project_ids == pid).sum()
            print(f"    - {pid} (appears {count} times)")
        if len(duplicates) > 10:
            print(f"    ... and {len(duplicates) - 10} more")
    else:
        print(f"  ✓ No duplicate Project IDs")

    # Check ID formats
    print(f"\n  Project ID Formats:")
    formats = {}
    for pid in project_ids.head(20):
        pid_str = str(pid).strip()
        if '-' in pid_str:
            year_part = pid_str.split('-')[0]
            format_key = f"{year_part}-XXX"
        else:
            format_key = "Other format"
        formats[format_key] = formats.get(format_key, 0) + 1

    for fmt, count in sorted(formats.items()):
        print(f"    - {fmt}: ~{count} examples")

# Check Award Amounts
print("\nAward Amount Analysis:")
award_col = 'Award Amount Allocated ($) this must be filled in for all lines'
if award_col in consolidated_df.columns:
    amounts = pd.to_numeric(consolidated_df[award_col], errors='coerce')
    valid_amounts = amounts.dropna()

    print(f"  Total rows: {len(consolidated_df)}")
    print(f"  Valid amounts: {len(valid_amounts)}")
    print(f"  Missing/invalid: {len(amounts) - len(valid_amounts)}")

    if len(valid_amounts) > 0:
        print(f"\n  Amount Statistics:")
        print(f"    Min: ${valid_amounts.min():,.2f}")
        print(f"    Max: ${valid_amounts.max():,.2f}")
        print(f"    Mean: ${valid_amounts.mean():,.2f}")
        print(f"    Median: ${valid_amounts.median():,.2f}")
        print(f"    Total: ${valid_amounts.sum():,.2f}")

        # Check for suspicious values
        zero_amounts = (valid_amounts == 0).sum()
        if zero_amounts > 0:
            print(f"  ⚠️  {zero_amounts} rows with $0 amount")

        very_large = (valid_amounts > 1000000).sum()
        if very_large > 0:
            print(f"  ⚠️  {very_large} rows with amount > $1M")

# Check Institution Names
print("\nInstitution Analysis:")
inst_col = 'Academic Institution of PI'
if inst_col in consolidated_df.columns:
    institutions = consolidated_df[inst_col].dropna()
    unique_insts = institutions.unique()

    print(f"  Total institutions: {len(unique_insts)}")
    print(f"\n  All institutions:")
    for inst in sorted([str(i) for i in unique_insts]):
        count = (consolidated_df[inst_col].astype(str) == inst).sum()
        print(f"    - {inst} ({count} rows)")

    # Check for potential duplicates (spelling variations)
    print(f"\n  Potential spelling variations to check:")
    inst_lower = {str(i).lower().strip(): str(i) for i in unique_insts}
    checked = set()
    for inst in unique_insts:
        inst_str = str(inst).lower().strip()
        if inst_str in checked:
            continue

        # Find similar names
        similar = []
        for other in unique_insts:
            other_str = str(other).lower().strip()
            if other_str != inst_str and (inst_str in other_str or other_str in inst_str):
                similar.append(str(other))
                checked.add(other_str)

        if similar:
            print(f"    - '{inst}' similar to: {similar}")
            checked.add(inst_str)

# Summary
print("\n\n6. SUMMARY")
print("-"*100)
print(f"Consolidated file has {len(consolidated_df)} total rows")
print(f"Source files combined have:")
for name, df in source_data.items():
    print(f"  - {name}: {len(df)} rows")

total_source_rows = sum(len(df) for df in source_data.values())
print(f"\nTotal source rows: {total_source_rows}")
print(f"Consolidated rows: {len(consolidated_df)}")
if len(consolidated_df) >= total_source_rows:
    print(f"✓ Consolidated data includes all source data (possible duplicates for multi-output projects)")
else:
    print(f"⚠️  Consolidated has fewer rows than source total - some data may be missing")

print("\n" + "="*100)
print("VERIFICATION COMPLETE")
print("="*100)
