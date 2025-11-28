import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import warnings
warnings.filterwarnings('ignore')

# Target file
target_file = 'IWRC Seed Fund Tracking.xlsx'

# Source files
source_files = [
    'FY23_reporting_IL.xlsx',
    'FY24_reporting_IL.xlsx',
    'IL_5yr_FY16_20_2.xlsx',
    'IWRC-2022-WRRA-Annual-Report-v.101923.xlsx'
]

# Read the target file
print(f"Reading target file: {target_file}")
target_df = pd.read_excel(target_file, sheet_name='Project Overview')
print(f"Target file has {len(target_df)} rows")
print(f"Target has {len(target_df.columns)} columns")

# Get target columns for matching
target_columns = list(target_df.columns)

def clean_column_name(col):
    """Clean column name for comparison"""
    return str(col).strip().lower().replace('\n', ' ').replace('  ', ' ').replace('\t', ' ')

# Process each source file
all_new_rows = []

for source_file in source_files:
    print(f"\n{'='*80}")
    print(f"Processing: {source_file}")

    try:
        # Try reading with multi-level headers first
        try:
            source_df_multi = pd.read_excel(source_file, sheet_name='Project Overview', header=[0,1,2])
            # Extract the actual column names from level 1 (middle level has the real names)
            column_names = [col[1] if isinstance(col, tuple) else col for col in source_df_multi.columns]
            # Get the data (first row is actual data)
            data_rows = source_df_multi.values
            source_df = pd.DataFrame(data_rows, columns=column_names)
        except:
            # Fallback to single header
            source_df = pd.read_excel(source_file, sheet_name='Project Overview')

        print(f"  Found {len(source_df)} rows")
        print(f"  Found {len(source_df.columns)} columns")

        # Remove completely empty rows
        source_df = source_df.dropna(how='all')
        print(f"  After removing empty rows: {len(source_df)} rows")

        # Create a mapping of source columns to target columns
        column_mapping = {}
        target_cols_clean = {clean_column_name(col): col for col in target_columns}

        matched_count = 0
        for source_col in source_df.columns:
            source_clean = clean_column_name(source_col)

            # Skip unnamed columns
            if 'unnamed' in source_clean:
                continue

            # Try exact match first
            if source_clean in target_cols_clean:
                column_mapping[source_col] = target_cols_clean[source_clean]
                matched_count += 1
            else:
                # Try partial match - check if key parts match
                for target_clean, target_col in target_cols_clean.items():
                    # Extract key words (longer than 4 chars)
                    source_words = set([w for w in source_clean.split() if len(w) > 4])
                    target_words = set([w for w in target_clean.split() if len(w) > 4])

                    # If there's significant overlap, consider it a match
                    if source_words and target_words:
                        overlap = source_words & target_words
                        if len(overlap) >= min(2, len(source_words)):
                            column_mapping[source_col] = target_col
                            matched_count += 1
                            break

        print(f"  Mapped {matched_count} columns")

        # Show some examples of mapped columns
        if matched_count > 0:
            print("  Sample mappings:")
            for i, (src, tgt) in enumerate(list(column_mapping.items())[:5]):
                print(f"    '{src[:50]}' -> '{tgt[:50]}'")

        # Create new rows with mapped columns
        rows_added = 0
        for idx, row in source_df.iterrows():
            # Skip rows where first column looks like a header
            first_val = str(row.iloc[0]).strip().lower()
            if first_val in ['nan', '', 'project id', 'project identifiers']:
                continue

            new_row = pd.Series(index=target_columns, dtype=object)

            # Map values from source to target columns
            for source_col, target_col in column_mapping.items():
                value = row[source_col]
                # Don't copy NaN or empty values
                if pd.notna(value) and str(value).strip() not in ['', 'nan']:
                    new_row[target_col] = value

            # Only add row if it has at least some non-empty data
            non_empty = sum(1 for v in new_row if pd.notna(v) and str(v).strip() not in ['', 'nan'])
            if non_empty > 0:
                all_new_rows.append(new_row)
                rows_added += 1

        print(f"  Added {rows_added} rows from {source_file}")

    except Exception as e:
        print(f"  Error processing {source_file}: {e}")
        import traceback
        traceback.print_exc()

# Combine target data with new rows
print(f"\n{'='*80}")
print(f"Combining data...")
print(f"Original target rows: {len(target_df)}")
print(f"New rows to add: {len(all_new_rows)}")

if all_new_rows:
    new_rows_df = pd.DataFrame(all_new_rows)
    combined_df = pd.concat([target_df, new_rows_df], ignore_index=True)
    print(f"Total rows after combining: {len(combined_df)}")

    # Save to the target file
    output_file = target_file

    # Simple approach: just save the combined data
    # This will only save the Project Overview sheet, but preserves the data
    combined_df.to_excel(output_file, sheet_name='Project Overview', index=False)

    print(f"\nSuccessfully saved combined data to: {output_file}")
    print(f"Total rows in output: {len(combined_df)}")

else:
    print("No new rows to add!")

print("\nDone!")
