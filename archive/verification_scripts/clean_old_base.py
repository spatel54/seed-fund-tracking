import pandas as pd
import numpy as np
import os

INPUT_FILE = '/Users/shivpat/seed-fund-tracking/data/consolidated/IWRC Seed Fund Tracking.xlsx'
OUTPUT_FILE = '/Users/shivpat/seed-fund-tracking/data/processed/clean_iwrc_tracking.xlsx'
REPORT_FILE = '/Users/shivpat/seed-fund-tracking/analysis/reports/clean_report.txt'

def clean_id(s):
    if pd.isna(s): return np.nan
    s = str(s).strip()
    if s.lower() in ['nan', 'total', '']: return np.nan
    return s

def main():
    print(f"Cleaning {INPUT_FILE}...")
    
    try:
        df = pd.read_excel(INPUT_FILE, sheet_name='Project Overview')
        print(f"Original Rows: {len(df)}")
        
        # 1. Clean Project IDs
        # Identify the column
        pid_col = next((c for c in df.columns if 'project id' in c.lower()), 'Project ID ')
        print(f"Project ID Column: {pid_col}")
        
        df['clean_pid'] = df[pid_col].apply(clean_id)
        
        # Remove invalid IDs
        df = df.dropna(subset=['clean_pid'])
        print(f"Rows after removing invalid IDs: {len(df)}")
        
        # 2. Deduplicate
        # Keep first occurrence
        df = df.drop_duplicates(subset=['clean_pid'], keep='first')
        print(f"Rows after deduplication: {len(df)}")
        
        # 3. Fix Data Types
        # Identify numeric columns
        # Award Amount
        amt_col = next((c for c in df.columns if 'Award Amount' in c), None)
        if amt_col:
            print(f"Fixing numeric column: {amt_col}")
            df[amt_col] = pd.to_numeric(df[amt_col], errors='coerce')
            
        # Student Counts
        student_cols = [c for c in df.columns if 'Number of' in c and 'Supported' in c]
        for c in student_cols:
            print(f"Fixing numeric column: {c}")
            df[c] = pd.to_numeric(df[c], errors='coerce')
            
        # USGS Staff / Student co-authors
        author_cols = [c for c in df.columns if 'How many' in c and 'co-authors' in c]
        for c in author_cols:
            print(f"Fixing numeric column: {c}")
            df[c] = pd.to_numeric(df[c], errors='coerce')

        # 4. Handle Unnamed Columns (User Request)
        u34 = 'Unnamed: 34'
        u33 = 'Unnamed: 33'
        ben_col = next((c for c in df.columns if 'Monetary Benefit' in c), None)
        
        if u34 in df.columns and ben_col:
            print(f"Merging {u34} into {ben_col}...")
            # Exclude specific ID from merge
            mask_exclude = df[pid_col] == '2019IL089B'
            
            # Merge for others
            # If benefit is NaN, take Unnamed: 34
            df.loc[~mask_exclude & df[ben_col].isna(), ben_col] = df.loc[~mask_exclude, u34]
            
        # Drop Unnamed columns
        cols_to_drop = [c for c in [u33, u34, 'clean_pid'] if c in df.columns]
        print(f"Dropping columns: {cols_to_drop}")
        df = df.drop(columns=cols_to_drop)
        
        # 5. Save
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        df.to_excel(OUTPUT_FILE, index=False, sheet_name='Project Overview')
        print(f"Saved cleaned data to {OUTPUT_FILE}")
        
        # 5. Generate Report
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
        with open(REPORT_FILE, 'w') as r:
            r.write("Cleaning Report\n")
            r.write("===============\n\n")
            r.write(f"Input File: {INPUT_FILE}\n")
            r.write(f"Output File: {OUTPUT_FILE}\n")
            r.write(f"Final Row Count: {len(df)}\n")
            r.write(f"Unique Project IDs: {df[pid_col].nunique()}\n\n")
            r.write("Columns and Data Types:\n")
            for c in df.columns:
                r.write(f"{c}: {df[c].dtype}\n")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
