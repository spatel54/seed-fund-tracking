import pandas as pd
from pathlib import Path

project_root = Path(__file__).parent.parent
data_file = project_root / "data" / "consolidated" / "fact sheet data.xlsx"

# Load the data
df = pd.read_excel(data_file, sheet_name="2025 data")

# Extract year from PI column
df['Year'] = None
current_year = None
for idx, row in df.iterrows():
    pi_val = row['PI']
    try:
        year_num = int(pi_val)
        if 2015 <= year_num <= 2026:
            current_year = year_num
    except (ValueError, TypeError):
        pass
    df.loc[idx, 'Year'] = current_year

# Clean data
df_clean = df[(df['Award Amount'].notna()) & (df['Institution'].notna()) & (df['Year'].notna())].copy()
df_clean['Award Amount'] = pd.to_numeric(df_clean['Award Amount'], errors='coerce')
df_clean['Year'] = pd.to_numeric(df_clean['Year'], errors='coerce')
df_clean = df_clean[(df_clean['Award Amount'] > 0) & (df_clean['Year'].notna())]

# Consolidate institutions
def consolidate_institution(inst):
    if pd.isna(inst):
        return None
    inst = str(inst).strip()
    if 'urbana' in inst.lower() or 'uiuc' in inst.lower():
        return 'University of Illinois Urbana-Champaign'
    elif 'southern illinois' in inst.lower():
        return 'Southern Illinois University'
    elif 'chicago' in inst.lower():
        return 'University of Illinois Chicago'
    else:
        return inst

df_clean['Institution_Clean'] = df_clean['Institution'].apply(consolidate_institution)

print("=" * 80)
print("DETAILED FUNDING VERIFICATION BY INSTITUTION AND YEAR")
print("=" * 80)

# Get all unique institutions
institutions = sorted(df_clean['Institution_Clean'].unique())

for inst in institutions:
    inst_data = df_clean[df_clean['Institution_Clean'] == inst]
    print(f"\n{inst}")
    print("-" * 80)

    # Show breakdown by year
    yearly = inst_data.groupby('Year')['Award Amount'].agg(['sum', 'count'])
    print(yearly)

    # Calculate periods
    five_yr = inst_data[inst_data['Year'] >= 2020]['Award Amount'].sum()
    ten_yr = inst_data['Award Amount'].sum()

    print(f"  5-Year (2020-2024): ${five_yr:,.0f}")
    print(f"  10-Year (2015-2024): ${ten_yr:,.0f}")

print("\n" + "=" * 80)
print("SUMMARY TABLE")
print("=" * 80)

summary = []
for inst in institutions:
    inst_data = df_clean[df_clean['Institution_Clean'] == inst]
    five_yr = inst_data[inst_data['Year'] >= 2020]['Award Amount'].sum()
    ten_yr = inst_data['Award Amount'].sum()
    summary.append({
        'Institution': inst,
        '5-Year (2020-2024)': five_yr,
        '10-Year (2015-2024)': ten_yr,
        'Difference': ten_yr - five_yr,
        '5-Yr Count': len(inst_data[inst_data['Year'] >= 2020]),
        '10-Yr Count': len(inst_data)
    })

summary_df = pd.DataFrame(summary).sort_values('10-Year (2015-2024)', ascending=False)
print(summary_df.to_string(index=False))

print(f"\nTotal 5-Year: ${summary_df['5-Year (2020-2024)'].sum():,.0f}")
print(f"Total 10-Year: ${summary_df['10-Year (2015-2024)'].sum():,.0f}")

print("\n" + "=" * 80)
print("INSTITUTIONS WITH ZERO 5-YEAR FUNDING (2015-2019 ONLY)")
print("=" * 80)
zero_5yr = summary_df[summary_df['5-Year (2020-2024)'] == 0]
if len(zero_5yr) > 0:
    print(zero_5yr[['Institution', '10-Year (2015-2024)', '10-Yr Count']].to_string(index=False))
else:
    print("None - all institutions have some 2020-2024 funding")
