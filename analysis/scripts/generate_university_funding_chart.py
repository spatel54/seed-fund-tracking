import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up paths
# Set up paths
project_root = Path(__file__).parent.parent
data_file = project_root / "data/consolidated/fact sheet data.xlsx"
output_dir = project_root / "FINAL_DELIVERABLES_2_backup_20251125_194954 copy 2/visualizations/static"
output_dir.mkdir(parents=True, exist_ok=True)

# Import IWRC branding
try:
    from iwrc_brand_style import IWRC_COLORS, configure_matplotlib_iwrc
    configure_matplotlib_iwrc()
    USE_IWRC = True
except ImportError:
    print("Warning: IWRC branding not available")
    USE_IWRC = False

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
               width, label='10-Year (2015-2024)', color=IWRC_COLORS['primary'])
bars2 = ax.barh(x_pos + width/2, combined_data['5-Year (2020-2024)'].values,
               width, label='5-Year (2020-2024)', color=IWRC_COLORS['secondary'])

# Add amount labels for 10-year bars
for i, (bar, amount) in enumerate(zip(bars1, combined_data['10-Year (2015-2024)'].values)):
    if amount > 0:
        label_text = f'${amount:,.0f}'
        ax.text(amount, bar.get_y() + bar.get_height()/2, f'  {label_text}',
                va='center', ha='left', fontsize=9, color=IWRC_COLORS['text'], fontweight='bold')

# Add amount labels for 5-year bars
for i, (bar, amount) in enumerate(zip(bars2, combined_data['5-Year (2020-2024)'].values)):
    if amount > 0:
        label_text = f'${amount:,.0f}'
        ax.text(amount, bar.get_y() + bar.get_height()/2, f'  {label_text}',
                va='center', ha='left', fontsize=9, color=IWRC_COLORS['text'], fontweight='bold')

# Set y-axis labels
ax.set_yticks(x_pos)
ax.set_yticklabels(institutions, fontsize=11, color=IWRC_COLORS['text'])

# Style the axis
ax.set_xlabel('')
ax.set_title('INSTITUTIONAL FUNDING SUPPORT PROVIDED BY THE IWRC',
             fontsize=14, fontweight='bold', pad=20, color=IWRC_COLORS['dark_teal'], loc='left')

# Set x-axis limits and formatting
max_val = combined_data['10-Year (2015-2024)'].max()
ax.set_xlim(0, max_val * 1.15)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))

# Apply IWRC style
from iwrc_brand_style import apply_iwrc_matplotlib_style, add_logo_to_matplotlib_figure
apply_iwrc_matplotlib_style(fig, ax)

# Add legend
legend = ax.legend(loc='lower right', fontsize=11, frameon=True, fancybox=False,
                   edgecolor=IWRC_COLORS['neutral_light'], framealpha=0.95)
legend.get_frame().set_linewidth(1.5)
for text in legend.get_texts():
    text.set_color(IWRC_COLORS['text'])
    text.set_fontweight('bold')

# Add logo
add_logo_to_matplotlib_figure(fig, position='bottom-right', size=0.1)

plt.tight_layout()

# Save as PNG
output_file = output_dir / "university_funding_comparison.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"\nChart saved to: {output_file}")

plt.close()
print("Done!")
