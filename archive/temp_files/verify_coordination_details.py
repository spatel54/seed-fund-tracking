
import sys
import os
import pandas as pd

# Add analysis/scripts to path
sys.path.append(os.path.join(os.getcwd(), 'analysis/scripts'))

from iwrc_data_loader import IWRCDataLoader

loader = IWRCDataLoader()
df = loader.load_master_data(deduplicate=True)

if 'project_year' in df.columns:
    df['year'] = df['project_year']

df['award_type_clean'] = df['award_type'].fillna('Unknown').astype(str).str.lower().str.strip()
coordination_df = df[df['award_type_clean'].str.contains('coordination', na=False)]

print(f"\nALL COORDINATION GRANTS:")
print(coordination_df[['project_year', 'award_type', 'award_amount']].sort_values('project_year'))
