
import sys
import os
import pandas as pd

# Add analysis/scripts to path
sys.path.append(os.path.join(os.getcwd(), 'analysis/scripts'))

from iwrc_data_loader import IWRCDataLoader
from award_type_filters import filter_all_projects, filter_104b_only

loader = IWRCDataLoader()
df = loader.load_master_data(deduplicate=True)

if 'project_year' in df.columns:
    df['year'] = df['project_year']

# Filter 1: All Projects, 2020-2024
df_all = filter_all_projects(df)
df_all_5yr = df_all[(df_all['year'] >= 2020) & (df_all['year'] <= 2024)]

# Filter 2: 104B Only, 2020-2024
df_104b = filter_104b_only(df)
df_104b_5yr = df_104b[(df_104b['year'] >= 2020) & (df_104b['year'] <= 2024)]

# Find the difference
df_diff = df_all_5yr[~df_all_5yr.index.isin(df_104b_5yr.index)]

print(f"Difference Count: {len(df_diff)}")
print("Award Types in Difference:")
print(df_diff['award_type'].value_counts(dropna=False))

print("\nFull rows of difference:")
print(df_diff[['project_year', 'award_type', 'project_title']])
