import pandas as pd
from pathlib import Path

project_root = Path(__file__).parent.parent
data_file = project_root / "data" / "consolidated" / "fact sheet data.xlsx"

df = pd.read_excel(data_file, sheet_name="2025 data")

print("First 20 rows of PI and Award Amount columns:")
print(df[['PI', 'Award Amount', 'Institution']].head(20))

print("\nUnique PI values (first 30):")
print(df['PI'].unique()[:30])

print("\nRows with numeric PI values:")
numeric_rows = df[pd.to_numeric(df['PI'], errors='coerce').notna()]
print(numeric_rows[['PI', 'Award Amount', 'Institution']].head(10))
