import pandas as pd
import numpy as np

# Load data
df = pd.read_excel('data/consolidated/IWRC Seed Fund Tracking.xlsx', sheet_name='Project Overview')

# Rename columns
col_map = {
    'Project ID ': 'project_id',
    'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount'
}
df = df.rename(columns=col_map)

# Focus on one project
pid = '2020IL103AIS'
subset = df[df['project_id'] == pid]

print(f"--- Analysis for Project {pid} ---")
print(f"Number of rows: {len(subset)}")
print("Award Amounts in rows:")
print(subset['award_amount'].tolist())

# Flawed Logic
flawed_sum = subset['award_amount'].sum()
print(f"\n[FLAWED] Simple Sum: ${flawed_sum:,.2f}")

# Corrected Logic
subset['award_amount_numeric'] = pd.to_numeric(subset['award_amount'], errors='coerce')
corrected_sum = subset.groupby('project_id')['award_amount_numeric'].first().sum()
print(f"[CORRECTED] Deduplicated Sum: ${corrected_sum:,.2f}")

print(f"\nDifference: ${flawed_sum - corrected_sum:,.2f}")
print(f"Inflation Factor: {flawed_sum / corrected_sum:.2f}x")
