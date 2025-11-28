
import pandas as pd
from pathlib import Path
import sys

# Add scripts to path to import loader
sys.path.insert(0, '/Users/shivpat/seed-fund-tracking/analysis/scripts')
from iwrc_data_loader import IWRCDataLoader

def verify_counts():
    print("Loading data...")
    loader = IWRCDataLoader()
    # Load with deduplication as used in the new reports
    df = loader.load_master_data(deduplicate=True)
    
    print(f"\nTotal rows in dataframe: {len(df)}")
    print(f"Total unique project_ids: {df['project_id'].nunique()}")
    
    # Filter 2015-2024 (10-year period used in reports)
    df_10yr = df[df['project_year'].between(2015, 2024, inclusive='both')]
    print(f"\n--- 10-Year Period (2015-2024) ---")
    print(f"All Projects (Unique IDs): {df_10yr['project_id'].nunique()}")
    
    # Filter 104B Only
    df_104b = df_10yr[df_10yr['award_type'] == 'Base Grant (104b)']
    print(f"104B Only (Unique IDs): {df_104b['project_id'].nunique()}")
    
    # Check for the "87" number
    # Maybe it's the total without year filter?
    print(f"\n--- Other Potential Counts ---")
    print(f"Total All Projects (No Year Filter): {df['project_id'].nunique()}")
    
    # Maybe it includes 2025?
    df_plus_2025 = df[df['project_year'].between(2015, 2025, inclusive='both')]
    print(f"All Projects (2015-2025): {df_plus_2025['project_id'].nunique()}")

    # Maybe it's rows instead of unique projects?
    # Check 2014-2024
    df_14_24 = df[df['project_year'].between(2014, 2024, inclusive='both')]
    print(f"All Projects (2014-2024): {df_14_24['project_id'].nunique()}")

if __name__ == "__main__":
    verify_counts()
