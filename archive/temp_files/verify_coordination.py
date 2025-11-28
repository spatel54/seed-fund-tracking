
import sys
import os
import pandas as pd

# Add analysis/scripts to path
sys.path.append(os.path.join(os.getcwd(), 'analysis/scripts'))

from iwrc_data_loader import IWRCDataLoader

loader = IWRCDataLoader()
df = loader.load_master_data(deduplicate=True)

# Ensure year column
if 'project_year' in df.columns:
    df['year'] = df['project_year']

# Standardize award type for filtering
df['award_type_clean'] = df['award_type'].fillna('Unknown').astype(str).str.lower().str.strip()

# Filter for Coordination Grants
coordination_df = df[df['award_type_clean'].str.contains('coordination', na=False)]

total_count = len(coordination_df)
recent_count = len(coordination_df[(coordination_df['year'] >= 2020) & (coordination_df['year'] <= 2024)])
older_count = len(coordination_df[(coordination_df['year'] >= 2015) & (coordination_df['year'] <= 2019)])

print(f"\nVERIFICATION OF COORDINATION GRANTS:")
print(f"==================================================")
print(f"Total Coordination Grants (2015-2024): {total_count}")
print(f" - Recent (2020-2024): {recent_count}")
print(f" - Older (2015-2019): {older_count}")

print(f"\nDetailed List (Recent):")
print(coordination_df[(coordination_df['year'] >= 2020)][['project_year', 'award_type', 'award_amount']])
