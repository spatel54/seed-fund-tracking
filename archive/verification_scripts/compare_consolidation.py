import pandas as pd
import numpy as np

OLD_FILE = '/Users/shivpat/seed-fund-tracking/data/consolidated/IWRC Seed Fund Tracking.xlsx'
NEW_FILE = '/Users/shivpat/seed-fund-tracking/data/processed/combined_data_v2.xlsx'

def clean_id(s):
    return str(s).strip()

def compare_files():
    print(f"Comparing:\nOld: {OLD_FILE}\nNew: {NEW_FILE}\n")
    
    try:
        old_df = pd.read_excel(OLD_FILE, sheet_name='Project Overview')
        new_df = pd.read_excel(NEW_FILE)
        
        # Normalize IDs
        old_df['pid_clean'] = old_df['Project ID '].apply(clean_id)
        new_df['pid_clean'] = new_df['Project ID'].apply(clean_id)
        
        # 1. Row Counts
        print(f"--- Row Counts ---")
        print(f"Old: {len(old_df)}")
        print(f"New: {len(new_df)}")
        
        # 2. Unique IDs
        old_ids = set(old_df['pid_clean'])
        new_ids = set(new_df['pid_clean'])
        print(f"\n--- Unique Project IDs ---")
        print(f"Old: {len(old_ids)}")
        print(f"New: {len(new_ids)}")
        
        common = old_ids.intersection(new_ids)
        print(f"Common: {len(common)}")
        
        only_old = old_ids - new_ids
        print(f"Only in Old: {len(only_old)}")
        if only_old:
            print(f"Sample Only in Old: {list(only_old)[:5]}")
            
        only_new = new_ids - old_ids
        print(f"Only in New: {len(only_new)}")
        if only_new:
            print(f"Sample Only in New: {list(only_new)[:5]}")
            
        # 3. Column Comparison
        print(f"\n--- Columns ---")
        old_cols = set(old_df.columns)
        new_cols = set(new_df.columns)
        
        # Normalize column names for comparison (strip spaces)
        old_cols_norm = {c.strip() for c in old_cols}
        new_cols_norm = {c.strip() for c in new_cols}
        
        print(f"Common Columns: {len(old_cols_norm.intersection(new_cols_norm))}")
        print(f"Only in Old: {len(old_cols_norm - new_cols_norm)}")
        # print(f"Sample Only in Old: {list(old_cols_norm - new_cols_norm)[:5]}")
        print(f"Only in New: {len(new_cols_norm - old_cols_norm)}")
        # print(f"Sample Only in New: {list(new_cols_norm - old_cols_norm)[:5]}")
        
        # 4. Financial Comparison (Award Amount)
        # Find column with 'Amount'
        old_amt_col = next((c for c in old_df.columns if 'Amount' in c), None)
        new_amt_col = next((c for c in new_df.columns if 'Amount' in c), None)
        
        if old_amt_col and new_amt_col:
            print(f"\n--- Financials (Award Amount) ---")
            # Filter to common IDs
            old_common = old_df[old_df['pid_clean'].isin(common)].copy()
            new_common = new_df[new_df['pid_clean'].isin(common)].copy()
            
            # Handle duplicates in old (take sum or first? Old file has duplicates)
            # Let's take sum for Old to see total allocated vs New (which is deduped)
            # Actually, if Old has duplicates, are they same project split or just copy-paste errors?
            # Let's check one ID with duplicates in Old
            dup_id = old_df['pid_clean'].mode()[0]
            print(f"Checking duplicates for ID '{dup_id}' in Old file:")
            print(old_df[old_df['pid_clean'] == dup_id][old_amt_col].values)
            
            # Summing might be misleading if they are exact duplicates.
            # Let's assume they are duplicates and take the first non-null.
            
            # Coerce to numeric
            old_common[old_amt_col] = pd.to_numeric(old_common[old_amt_col], errors='coerce').fillna(0)
            new_common[new_amt_col] = pd.to_numeric(new_common[new_amt_col], errors='coerce').fillna(0)
            
            old_sums = old_common.groupby('pid_clean')[old_amt_col].sum()
            new_sums = new_common.groupby('pid_clean')[new_amt_col].sum()
            
            print(f"Total Amount (Old, Sum of Common): ${old_sums.sum():,.2f}")
            print(f"Total Amount (New, Sum of Common): ${new_sums.sum():,.2f}")
            
            diff = new_sums.sum() - old_sums.sum()
            print(f"Difference: ${diff:,.2f}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    compare_files()
