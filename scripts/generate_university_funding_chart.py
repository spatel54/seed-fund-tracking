import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up paths
project_root = Path(__file__).parent.parent
data_file = project_root / "data" / "consolidated" / "fact sheet data.xlsx"
output_dir = project_root / "visualizations" / "static"
output_dir.mkdir(parents=True, exist_ok=True)

# Load the data
df = pd.read_excel(data_file, sheet_name="2025 data")

# Extract year from PI column (rows with years are marked in PI column)
# Create a year column by forward-filling
df['Year'] = None
current_year = None
for idx, row in df.iterrows():
    pi_val = row['PI']
    # Check if PI is numeric (year marker)
    try:
        year_num = int(pi_val)
        if 2015 <= year_num <= 2026:
            current_year = year_num
    except (ValueError, TypeError):
        pass

    df.loc[idx, 'Year'] = current_year

# Remove rows without awards or institutions
df_clean = df[(df['Award Amount'].notna()) & (df['Institution'].notna()) & (df['Year'].notna())].copy()
df_clean['Award Amount'] = pd.to_numeric(df_clean['Award Amount'], errors='coerce')
df_clean['Year'] = pd.to_numeric(df_clean['Year'], errors='coerce')
df_clean = df_clean[(df_clean['Award Amount'] > 0) & (df_clean['Year'].notna())]

print(f"Cleaned data: {len(df_clean)} records")
print("\nData sample:")
print(df_clean[['PI', 'Year', 'Award Amount', 'Institution']].head(15))

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

print("\nInstitutions after consolidation:")
print(df_clean['Institution_Clean'].value_counts())

# Calculate funding by institution and period
def calculate_funding(df, start_year, end_year, label):
    period_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    funding_by_inst = period_df.groupby('Institution_Clean')['Award Amount'].sum().sort_values(ascending=False)
    return funding_by_inst

funding_5yr = calculate_funding(df_clean, 2020, 2024, "5-Year (2020-2024)")
funding_10yr = calculate_funding(df_clean, 2015, 2024, "10-Year (2015-2024)")

print("\n5-Year Funding (2020-2024):")
print(funding_5yr)
print(f"Total: ${funding_5yr.sum():,.0f}")

print("\n10-Year Funding (2015-2024):")
print(funding_10yr)
print(f"Total: ${funding_10yr.sum():,.0f}")

# Combine data for overlapped visualization
# Create a dataframe with both periods
combined_data = pd.DataFrame({
    '10-Year (2015-2024)': funding_10yr,
    '5-Year (2020-2024)': funding_5yr
}).fillna(0)

# Sort by 10-year funding (descending)
combined_data = combined_data.sort_values('10-Year (2015-2024)', ascending=True)

print("\nCombined funding data:")
print(combined_data)

# Create overlapped visualization
fig = plt.figure(figsize=(18, 13))
ax = fig.add_subplot(111)

# Prepare data
institutions = combined_data.index.tolist()
x_pos = np.arange(len(institutions))
width = 0.35

# Create bars
bars1 = ax.barh(x_pos - width/2, combined_data['10-Year (2015-2024)'].values,
               width, label='10-Year (2015-2024)', color='#001a4d')
bars2 = ax.barh(x_pos + width/2, combined_data['5-Year (2020-2024)'].values,
               width, label='5-Year (2020-2024)', color='#4a5f8f')

# Add amount labels for 10-year bars
for i, (bar, amount) in enumerate(zip(bars1, combined_data['10-Year (2015-2024)'].values)):
    if amount > 0:
        label_text = f'${amount:,.0f}'
        ax.text(amount, bar.get_y() + bar.get_height()/2, f'  {label_text}',
                va='center', ha='left', fontsize=9, color='#e85d04', fontweight='bold',
                family='sans-serif')

# Add amount labels for 5-year bars
for i, (bar, amount) in enumerate(zip(bars2, combined_data['5-Year (2020-2024)'].values)):
    if amount > 0:
        label_text = f'${amount:,.0f}'
        ax.text(amount, bar.get_y() + bar.get_height()/2, f'  {label_text}',
                va='center', ha='left', fontsize=9, color='#cc6633', fontweight='bold',
                family='sans-serif')

# Set y-axis labels
ax.set_yticks(x_pos)
ax.set_yticklabels(institutions, fontsize=11, color='#001a4d')

# Style the axis
ax.set_xlabel('')
ax.set_title('INSTITUTIONAL FUNDING SUPPORT PROVIDED BY THE IWRC',
             fontsize=14, fontweight='bold', pad=20, color='#001a4d', loc='left')

# Set x-axis limits and formatting
max_val = combined_data['10-Year (2015-2024)'].max()
ax.set_xlim(0, max_val * 1.15)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))

# Style the axis
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.grid(axis='x', alpha=0.2, linestyle='-', linewidth=0.5, color='#e0e0e0')
ax.set_axisbelow(True)

# Style ticks
ax.tick_params(axis='y', labelsize=11, colors='#001a4d', pad=8)
ax.tick_params(axis='x', labelsize=10, colors='#666666')

# Add legend
legend = ax.legend(loc='lower right', fontsize=11, frameon=True, fancybox=False,
                   edgecolor='#001a4d', framealpha=0.95)
legend.get_frame().set_linewidth(1.5)
for text in legend.get_texts():
    text.set_color('#001a4d')
    text.set_fontweight('bold')

# Add a border around the figure
rect = plt.Rectangle((0.02, 0.02), 0.96, 0.96, fill=False, transform=fig.transFigure,
                      edgecolor='#001a4d', linewidth=2.5)
fig.patches.append(rect)

plt.tight_layout(rect=[0.05, 0.04, 0.96, 0.98])

# Save as PNG
output_file = output_dir / "university_funding_comparison.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"\nChart saved to: {output_file}")

plt.close()
print("Done!")
