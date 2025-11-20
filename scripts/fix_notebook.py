"""
Script to fix the IWRC ROI Analysis notebook with improved data extraction.
This addresses:
1. Grant amounts in multiple columns (swapped data)
2. Non-numeric values in student columns
3. Comprehensive monetary value extraction
"""

import json

# Read the current notebook
with open('Seed_Fund_Tracking_Analysis NEW.ipynb', 'r') as f:
    notebook = json.load(f)

# Find and update the column mapping cell (cell 3, index 3)
col_map_cell_code = '''# Create simplified column name mappings for easier reference
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
    "Award, Achievement, or Grant\\n (This may include awards and achievements for projects from the previous year to this 5-year cycle, so long as they were not already included in last year's report)": 'awards_grants',
    "Description of Award, Achievement, or Grant\\n (This may include awards and achievements for projects from the previous year to this 5-year cycle, so long as they were not already included in last year's report)": 'award_description',
    'Monetary Benefit of Award or Achievement (if applicable; use NA if not applicable)': 'monetary_benefit',
    'WRRI Science Priority that Best Aligns with this Project': 'science_priority',
    'Keyword (Primary)': 'keyword_primary'
}

# Rename columns for easier access
df_work = df.rename(columns=col_map)

# Clean student columns - convert non-numeric values to NaN
student_cols = ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']
for col in student_cols:
    df_work[col] = pd.to_numeric(df_work[col], errors='coerce')

print('✓ Column names simplified for analysis')
print('✓ Student columns cleaned (non-numeric values converted to NaN)')'''

notebook['cells'][3]['source'] = col_map_cell_code

# Update the monetary value extraction cell (cell 13, index 13)
monetary_cell_code = '''def clean_monetary_value(value):
    """
    Clean and convert monetary values to float with comprehensive extraction.
    Handles: $X,XXX, NA, embedded amounts, text descriptions, etc.
    """
    if pd.isna(value):
        return 0.0

    value_str = str(value).strip().upper()

    # Handle NA or N/A
    if value_str in ['NA', 'N/A', 'NONE', '']:
        return 0.0

    # Try to extract ALL dollar amounts from text and sum them
    # Pattern: $X,XXX.XX or $XXXX or XXXX (with optional commas and decimals)
    dollar_pattern = r'\\$?\\s*([\\d,]+(?:\\.\\d{2})?)'
    matches = re.findall(dollar_pattern, value_str)

    if matches:
        total = 0.0
        for match in matches:
            try:
                # Remove commas and convert to float
                amount = float(match.replace(',', ''))
                total += amount
            except (ValueError, TypeError):
                continue
        return total if total > 0 else 0.0

    return 0.0

def extract_grant_amount_comprehensive(row):
    """
    Extract grant monetary value from multiple possible columns.
    Handles data entry inconsistencies where amounts appear in different columns.

    Priority order:
    1. monetary_benefit column
    2. award_description column (for swapped data)
    3. Extract from awards_grants text (e.g., "$250,000" in description)
    """
    # Priority 1: Check monetary_benefit column
    if pd.notna(row['monetary_benefit']):
        amount = clean_monetary_value(row['monetary_benefit'])
        if amount > 0:
            return amount

    # Priority 2: Check award_description column (swapped data)
    if pd.notna(row['award_description']):
        amount = clean_monetary_value(row['award_description'])
        if amount > 0:
            return amount

    # Priority 3: Extract from awards_grants text
    if pd.notna(row['awards_grants']):
        amount = clean_monetary_value(row['awards_grants'])
        if amount > 0:
            return amount

    return 0.0

# Apply comprehensive extraction to both datasets
df_10yr['monetary_benefit_clean'] = df_10yr.apply(extract_grant_amount_comprehensive, axis=1)
df_5yr['monetary_benefit_clean'] = df_5yr.apply(extract_grant_amount_comprehensive, axis=1)

# Calculate total monetary benefit by award category
def calculate_monetary_by_category(df):
    # Only include rows with valid award categories
    df_with_awards = df[df['award_category'].notna()].copy()

    if len(df_with_awards) == 0:
        return pd.DataFrame(columns=['Count', 'Total Value'])

    monetary_summary = df_with_awards.groupby('award_category')['monetary_benefit_clean'].agg([
        ('Count', 'count'),
        ('Total Value', 'sum')
    ]).round(2)

    return monetary_summary

monetary_10yr = calculate_monetary_by_category(df_10yr)
monetary_5yr = calculate_monetary_by_category(df_5yr)

# Add data quality report
total_with_amounts_10yr = (df_10yr['monetary_benefit_clean'] > 0).sum()
total_with_amounts_5yr = (df_5yr['monetary_benefit_clean'] > 0).sum()

print('\\n' + '='*70)
print('FOLLOW-ON FUNDING: MONETARY VALUE BY TYPE')
print('='*70)
print('\\n10-Year Period (2015-2024):')
print(monetary_10yr)
print(f'\\n  TOTAL FOLLOW-ON FUNDING: ${monetary_10yr["Total Value"].sum():,.2f}')
print(f'  (Based on {total_with_amounts_10yr} entries with monetary values)')
print('\\n5-Year Period (2020-2024):')
print(monetary_5yr)
print(f'\\n  TOTAL FOLLOW-ON FUNDING: ${monetary_5yr["Total Value"].sum():,.2f}')
print(f'  (Based on {total_with_amounts_5yr} entries with monetary values)')
print('\\n' + '='*70)
print('\\nNOTE: Some grant/award amounts may not be reported in the dataset.')
print('These figures represent confirmed follow-on funding with documented values.')
print('='*70)'''

notebook['cells'][13]['source'] = monetary_cell_code

# Save the updated notebook
with open('Seed_Fund_Tracking_Analysis NEW.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)

print("✓ Notebook updated successfully!")
print("  - Added award_description column mapping")
print("  - Added student column cleaning (converts non-numeric to NaN)")
print("  - Enhanced monetary value extraction (checks 3 columns)")
print("  - Added data quality notes to output")
