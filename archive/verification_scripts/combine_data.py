import pandas as pd
import os
import numpy as np

# File Paths
BASE_FILE = '/Users/shivpat/seed-fund-tracking/data/source/IWRC Seed Fund Tracking August 2025 Update.xlsx'
SOURCE_FILES = [
    '/Users/shivpat/seed-fund-tracking/data/source/FY23_reporting_IL.xlsx',
    '/Users/shivpat/seed-fund-tracking/data/source/FY24_reporting_IL.xlsx',
    '/Users/shivpat/seed-fund-tracking/data/source/IL_5yr_FY16_20_2.xlsx',
    '/Users/shivpat/seed-fund-tracking/data/source/IWRC-2022-WRRA-Annual-Report-v.101923.xlsx'
]
OUTPUT_FILE = '/Users/shivpat/seed-fund-tracking/data/processed/combined_data_v2.xlsx'
REPORT_FILE = '/Users/shivpat/seed-fund-tracking/analysis/reports/merge_report.txt'

def normalize_columns(df):
    """Normalize column names to lowercase and stripped."""
    df.columns = df.columns.astype(str).str.strip()
    return df

def rename_grant_column(df):
    """Rename the specific award description column to 'grant'."""
    # Find column that contains "Description of Award"
    for col in df.columns:
        if "Description of Award" in col:
            df = df.rename(columns={col: 'grant'})
            return df
    return df

def load_and_process_grants(file_path):
    """Load Awards sheet and return a dictionary mapping Project ID to grants summary."""
    try:
        xl = pd.ExcelFile(file_path)
        # Create map of lower -> original
        sheet_map = {s.lower(): s for s in xl.sheet_names}
        
        target_sheet = None
        for s_lower, s_original in sheet_map.items():
            if 'award' in s_lower and 'grant' in s_lower:
                target_sheet = s_original
                break
        
        if target_sheet:
            df = pd.read_excel(file_path, sheet_name=target_sheet)
            df = normalize_columns(df)
            
            # Identify Project ID column
            pid_col = next((c for c in df.columns if 'project id' in c.lower()), None)
            # Identify Description column specifically first
            desc_col = next((c for c in df.columns if 'description' in c.lower()), None)
            if not desc_col:
                 # Fallback to something with 'award' but be careful not to pick 'Award Type' if possible, 
                 # though in the Awards sheet it's usually 'Award, Achievement...'
                 desc_col = next((c for c in df.columns if 'award' in c.lower() and 'type' not in c.lower()), None)
            
            if pid_col and desc_col:
                df[pid_col] = df[pid_col].astype(str).str.strip()
                # Aggregate grants per project
                grants_map = df.groupby(pid_col)[desc_col].apply(lambda x: '; '.join(x.dropna().astype(str))).to_dict()
                return grants_map
    except Exception as e:
        print(f"Warning processing grants for {file_path}: {e}")
    return {}

def main():
    print("Starting data combination...")
    
    # 1. Load Base File
    print(f"Loading base file: {BASE_FILE}")
    base_df = pd.read_excel(BASE_FILE, sheet_name='Project Overview')
    base_df = normalize_columns(base_df)
    base_df = rename_grant_column(base_df)
    
    # Standardize Project ID in Base
    base_pid_col = next((c for c in base_df.columns if 'project id' in c.lower()), 'Project ID')
    base_df[base_pid_col] = base_df[base_pid_col].astype(str).str.strip()
    
    # Ensure 'grant' column exists
    if 'grant' not in base_df.columns:
        base_df['grant'] = ""
    
    all_projects = base_df.copy()
    
    # 2. Process Source Files
    for f in SOURCE_FILES:
        print(f"Processing {f}...")
        try:
            # Load Project Overview
            df = pd.read_excel(f, sheet_name='Project Overview')
            df = normalize_columns(df)
            df = rename_grant_column(df)
            
            pid_col = next((c for c in df.columns if 'project id' in c.lower()), None)
            if not pid_col:
                print(f"Skipping {f}: No Project ID column found in Project Overview.")
                continue
                
            df[pid_col] = df[pid_col].astype(str).str.strip()
            
            # Load Grants for this file (from separate sheet)
            grants_map = load_and_process_grants(f)
            
            # Add/Update grants info
            # If 'grant' column exists (renamed from Description...), use it.
            # Also append info from the separate sheet if available.
            
            if 'grant' not in df.columns:
                df['grant'] = ""
            
            # Map from separate sheet
            sheet_grants = df[pid_col].map(grants_map).fillna("")
            
            # Combine existing 'grant' column with sheet grants
            # If both exist, concatenate? Or prefer one? 
            # Let's concatenate if not empty.
            
            def combine_grants(row):
                parts = []
                if pd.notna(row['grant']) and str(row['grant']).strip():
                    parts.append(str(row['grant']).strip())
                if pd.notna(sheet_grants[row.name]) and str(sheet_grants[row.name]).strip():
                    parts.append(str(sheet_grants[row.name]).strip())
                return "; ".join(list(set(parts))) # Dedupe strings simply
            
            # We need to align indices for the map to work or use apply
            # Easier:
            for idx, row in df.iterrows():
                pid = row[pid_col]
                g_sheet = grants_map.get(pid, "")
                g_col = row['grant'] if pd.notna(row['grant']) else ""
                
                parts = [str(p).strip() for p in [g_col, g_sheet] if str(p).strip()]
                df.at[idx, 'grant'] = "; ".join(list(set(parts)))

            # Rename Project ID to match Base
            df = df.rename(columns={pid_col: base_pid_col})
            
            all_projects = pd.concat([all_projects, df], ignore_index=True)
            
        except Exception as e:
            print(f"Error processing {f}: {e}")

    # 3. Deduplicate
    print("Deduplicating...")
    initial_count = len(all_projects)
    all_projects = all_projects.drop_duplicates(subset=[base_pid_col], keep='first')
    final_count = len(all_projects)
    print(f"Rows before dedupe: {initial_count}, after: {final_count}")
    
    # 4. Final Polish - Re-aggregate grants from all sources for the kept IDs
    # Because drop_duplicates kept the first one (Base), but other files might have had grant info for that ID.
    
    print("Re-aggregating grants info...")
    master_grants = {}
    
    # We need to re-scan files to build a master grants map for every ID
    # This is slightly inefficient but robust.
    
    # Helper to extract grants from a file
    def extract_grants_from_file(f_path, is_base=False):
        g_map = {}
        try:
            # From Project Overview column
            df = pd.read_excel(f_path, sheet_name='Project Overview')
            df = normalize_columns(df)
            df = rename_grant_column(df)
            pid_col = next((c for c in df.columns if 'project id' in c.lower()), None)
            if pid_col:
                df[pid_col] = df[pid_col].astype(str).str.strip()
                if 'grant' in df.columns:
                    for _, row in df.iterrows():
                        if pd.notna(row['grant']) and str(row['grant']).strip():
                            pid = row[pid_col]
                            if pid not in g_map: g_map[pid] = []
                            g_map[pid].append(str(row['grant']).strip())
            
            # From separate sheet (only for source files usually, but check all)
            sheet_g_map = load_and_process_grants(f_path)
            for pid, val in sheet_g_map.items():
                if pid not in g_map: g_map[pid] = []
                g_map[pid].append(val)
                
        except Exception as e:
            print(f"Error extracting grants from {f_path}: {e}")
        return g_map

    # Collect from Base
    base_grants = extract_grants_from_file(BASE_FILE, is_base=True)
    for pid, vals in base_grants.items():
        if pid not in master_grants: master_grants[pid] = set()
        master_grants[pid].update(vals)
        
    # Collect from Sources
    for f in SOURCE_FILES:
        src_grants = extract_grants_from_file(f)
        for pid, vals in src_grants.items():
            if pid not in master_grants: master_grants[pid] = set()
            master_grants[pid].update(vals)
            
    # Apply master grants to final df
    for idx, row in all_projects.iterrows():
        pid = row[base_pid_col]
        if pid in master_grants:
            # Join unique non-empty strings
            combined = "; ".join(sorted(list(master_grants[pid])))
            all_projects.at[idx, 'grant'] = combined
    
    # 5. Save Output
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    all_projects.to_excel(OUTPUT_FILE, index=False)
    print(f"Saved combined data to {OUTPUT_FILE}")
    
    # 6. Generate Report
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, 'w') as r:
        r.write("Consolidation Report\n")
        r.write("====================\n\n")
        r.write(f"Base File: {BASE_FILE}\n")
        r.write(f"Total Rows in Combined Data: {len(all_projects)}\n")
        r.write(f"Unique Project IDs: {all_projects[base_pid_col].nunique()}\n")
        r.write(f"Projects with Grant Info: {all_projects['grant'].replace('', np.nan).count()}\n")
        r.write("\nSource Files Merged:\n")
        for f in SOURCE_FILES:
            r.write(f"- {f}\n")

if __name__ == "__main__":
    main()
