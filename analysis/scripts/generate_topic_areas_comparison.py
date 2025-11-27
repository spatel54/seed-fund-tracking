import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up paths
# Set up paths
project_root = Path('/Users/shivpat/seed-fund-tracking')
data_file = project_root / "data/consolidated/IWRC Seed Fund Tracking.xlsx"
output_dir = project_root / "FINAL_DELIVERABLES_2_backup_20251125_194954 copy 2/visualizations/static_breakdown"
output_dir.mkdir(parents=True, exist_ok=True)

# Import IWRC branding
try:
    from iwrc_brand_style import IWRC_COLORS, configure_matplotlib_iwrc
    configure_matplotlib_iwrc()
    USE_IWRC = True
except ImportError:
    print("Warning: iwrc_brand_style not found. Using default style.")
    USE_IWRC = False
    IWRC_COLORS = {
        'primary': '#258372',
        'secondary': '#639757',
        'accent': '#FCC080',
        'gold': '#e6a866',
        'text': '#54595F',
        'dark_teal': '#1a5f52'
    }

# Load the data
print("Loading fact sheet data...")
df = pd.read_excel(data_file, sheet_name="Project Overview")

# Rename columns to match script expectations
column_mapping = {
    'Project PI': 'PI',
    'Award Amount Allocated ($) this must be filled in for all lines': 'Award Amount',
    'Keyword (Primary)': 'Keyword 1',
    'Keyword (Secondary, if applicable)': 'Keyword 2',
    'Keyword (Tertiary, if applicable)': 'Keyword 3'
}
df.rename(columns=column_mapping, inplace=True)

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
df_clean = df[(df['Award Amount'].notna()) & (df['Year'].notna())].copy()
df_clean['Award Amount'] = pd.to_numeric(df_clean['Award Amount'], errors='coerce')
df_clean['Year'] = pd.to_numeric(df_clean['Year'], errors='coerce')
df_clean = df_clean[(df_clean['Award Amount'] > 0) & (df_clean['Year'].notna())]

print(f"Cleaned data: {len(df_clean)} records")

# Define keyword-to-topic mappings
topic_keywords = {
    'Stormwater': ['FLOODS', 'SURFACE WATER'],
    'Agriculture': ['AGRICULTURE', 'NON POINT POLLUTION', 'NONPOINT POLLUTION'],
    'Groundwater': ['GROUNDWATER', 'GEOCHEMICAL PROCESSES', 'NITRATE CONTAMINATION'],
    'Nutrients': ['NUTRIENTS', 'PHOSPHORUS'],
    'Hydrology': ['HYDROLOGY', 'DROUGHT'],
    'Modeling': ['MODELS', 'METHODS', 'GEOMORPOLOGICAL PROCESSES'],
    'PFAS': ['PFAS', 'TOXIC SUBSTANCES'],
    'Invasive Species': ['AQUATIC INVASIVE SPECIES', 'INVASIVE SPECIES'],
}

# Function to assign topic based on keywords
def assign_topics(row):
    """Assign topics to a row based on its keywords, using proportional allocation"""
    keywords = []
    for col in ['Keyword 1', 'Keyword 2', 'Keyword 3']:
        if col in df_clean.columns and pd.notna(row[col]):
            kw = str(row[col]).strip().upper()
            if kw:
                keywords.append(kw)

    if not keywords:
        return {}

    # Find which topics match
    matched_topics = {}
    for topic, topic_kws in topic_keywords.items():
        for kw in keywords:
            if any(tkw in kw or kw in tkw for tkw in topic_kws):
                if topic not in matched_topics:
                    matched_topics[topic] = 0
                matched_topics[topic] += 1

    # Proportional allocation: split award by number of keywords
    if matched_topics:
        total_matches = sum(matched_topics.values())
        return {topic: count / total_matches for topic, count in matched_topics.items()}

    return {}

# Apply topic assignment
print("Assigning topics to projects...")
topic_allocations = []
for idx, row in df_clean.iterrows():
    topics = assign_topics(row)
    for topic, proportion in topics.items():
        topic_allocations.append({
            'Topic': topic,
            'Amount': row['Award Amount'] * proportion,
            'Year': row['Year'],
            'Proportion': proportion
        })

if topic_allocations:
    df_topics = pd.DataFrame(topic_allocations)
else:
    print("Warning: No topics assigned. Creating empty dataframe with all topics.")
    df_topics = pd.DataFrame({
        'Topic': list(topic_keywords.keys()),
        'Amount': [0] * len(topic_keywords),
        'Year': [2020] * len(topic_keywords),
        'Proportion': [1.0] * len(topic_keywords)
    })

# Calculate funding by topic and period
print("Calculating funding by topic and period...")
funding_data = []

for topic in topic_keywords.keys():
    topic_data = df_topics[df_topics['Topic'] == topic]

    if len(topic_data) > 0:
        amount_5yr = topic_data[topic_data['Year'] >= 2020]['Amount'].sum()
        amount_10yr = topic_data['Amount'].sum()
    else:
        amount_5yr = 0
        amount_10yr = 0

    funding_data.append({
        'Topic': topic,
        '5-Year (2020-2024)': amount_5yr,
        '10-Year (2015-2024)': amount_10yr
    })

df_funding = pd.DataFrame(funding_data)
df_funding = df_funding.sort_values('10-Year (2015-2024)', ascending=True)

print("\nTopic Areas Funding Comparison:")
print(df_funding.to_string(index=False))
print(f"\nTotal 5-Year: ${df_funding['5-Year (2020-2024)'].sum():,.0f}")
print(f"Total 10-Year: ${df_funding['10-Year (2015-2024)'].sum():,.0f}")

# ============================================================================
# VERSION 1: STACKED BARS
# ============================================================================
print("\nGenerating stacked bar chart...")
fig = plt.figure(figsize=(16, 11))
ax = fig.add_subplot(111)

topics = df_funding['Topic'].tolist()
x_pos = np.arange(len(topics))

# Create stacked bars
bars1 = ax.barh(x_pos, df_funding['10-Year (2015-2024)'].values,
               label='10-Year (2015-2024)', color=IWRC_COLORS['primary'], height=0.6)
bars2 = ax.barh(x_pos, df_funding['5-Year (2020-2024)'].values,
               left=0, label='5-Year (2020-2024)', color=IWRC_COLORS['secondary'], height=0.6)

# Add labels for 10-year amounts
for bar, amount in zip(bars1, df_funding['10-Year (2015-2024)'].values):
    if amount > 0:
        label_text = f'${amount:,.0f}'
        ax.text(amount, bar.get_y() + bar.get_height()/2, f'  {label_text}',
                va='center', ha='left', fontsize=10, color=IWRC_COLORS['dark_teal'], fontweight='bold')

# Style the axis
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_title('TOPIC AREAS OF CONCERN IN ILLINOIS - FUNDING COMPARISON',
             fontsize=14, fontweight='bold', pad=20, color=IWRC_COLORS['dark_teal'], loc='left')

max_val = df_funding['10-Year (2015-2024)'].max()
ax.set_xlim(0, max_val * 1.15)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K' if x < 1e6 else f'${x/1e6:.1f}M'))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.grid(axis='x', alpha=0.2, linestyle='-', linewidth=0.5, color='#e0e0e0')
ax.set_axisbelow(True)

ax.set_yticks(x_pos)
ax.set_yticklabels(topics, fontsize=11, color=IWRC_COLORS['dark_teal'])
ax.tick_params(axis='y', labelsize=11, colors=IWRC_COLORS['dark_teal'], pad=8)
ax.tick_params(axis='x', labelsize=10, colors=IWRC_COLORS['text'])

# Add legend
legend = ax.legend(loc='lower right', fontsize=11, frameon=True, fancybox=False,
                   edgecolor=IWRC_COLORS['dark_teal'], framealpha=0.95)
legend.get_frame().set_linewidth(1.5)
for text in legend.get_texts():
    text.set_color=IWRC_COLORS['dark_teal']
    text.set_fontweight('bold')

# Add border
rect = plt.Rectangle((0.02, 0.02), 0.96, 0.96, fill=False, transform=fig.transFigure,
                      edgecolor=IWRC_COLORS['dark_teal'], linewidth=2.5)
fig.patches.append(rect)

plt.tight_layout(rect=[0.05, 0.04, 0.96, 0.98])

output_file = output_dir / "topic_areas_stacked.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"Stacked chart saved to: {output_file}")
plt.close()

# ============================================================================
# VERSION 2: OVERLAPPING BARS (TRUE OVERLAY)
# ============================================================================
print("Generating overlapping bar chart...")
fig = plt.figure(figsize=(16, 11))
ax = fig.add_subplot(111)

# Create 10-year bars (darker, opaque)
bars1 = ax.barh(x_pos - 0.1, df_funding['10-Year (2015-2024)'].values,
               0.2, label='10-Year (2015-2024)', color=IWRC_COLORS['primary'], alpha=0.9)

# Create 5-year bars (lighter, semi-transparent, overlaid)
bars2 = ax.barh(x_pos + 0.1, df_funding['5-Year (2020-2024)'].values,
               0.2, label='5-Year (2020-2024)', color=IWRC_COLORS['secondary'], alpha=0.7)

# Add labels for 10-year amounts
for bar, amount in zip(bars1, df_funding['10-Year (2015-2024)'].values):
    if amount > 0:
        label_text = f'${amount:,.0f}'
        ax.text(amount, bar.get_y() + bar.get_height()/2, f'  {label_text}',
                va='center', ha='left', fontsize=9, color=IWRC_COLORS['dark_teal'], fontweight='bold')

# Add labels for 5-year amounts
for bar, amount in zip(bars2, df_funding['5-Year (2020-2024)'].values):
    if amount > 0:
        label_text = f'${amount:,.0f}'
        ax.text(amount, bar.get_y() + bar.get_height()/2, f'  {label_text}',
                va='center', ha='left', fontsize=9, color=IWRC_COLORS['secondary'], fontweight='bold')

# Style the axis
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_title('TOPIC AREAS OF CONCERN IN ILLINOIS - FUNDING COMPARISON',
             fontsize=14, fontweight='bold', pad=20, color=IWRC_COLORS['dark_teal'], loc='left')

max_val = df_funding['10-Year (2015-2024)'].max()
ax.set_xlim(0, max_val * 1.15)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K' if x < 1e6 else f'${x/1e6:.1f}M'))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.grid(axis='x', alpha=0.2, linestyle='-', linewidth=0.5, color='#e0e0e0')
ax.set_axisbelow(True)

ax.set_yticks(x_pos)
ax.set_yticklabels(topics, fontsize=11, color=IWRC_COLORS['dark_teal'])
ax.tick_params(axis='y', labelsize=11, colors=IWRC_COLORS['dark_teal'], pad=8)
ax.tick_params(axis='x', labelsize=10, colors=IWRC_COLORS['text'])

# Add legend
legend = ax.legend(loc='lower right', fontsize=11, frameon=True, fancybox=False,
                   edgecolor=IWRC_COLORS['dark_teal'], framealpha=0.95)
legend.get_frame().set_linewidth(1.5)
for text in legend.get_texts():
    text.set_color=IWRC_COLORS['dark_teal']
    text.set_fontweight('bold')

# Add border
rect = plt.Rectangle((0.02, 0.02), 0.96, 0.96, fill=False, transform=fig.transFigure,
                      edgecolor=IWRC_COLORS['dark_teal'], linewidth=2.5)
fig.patches.append(rect)

plt.tight_layout(rect=[0.05, 0.04, 0.96, 0.98])

output_file = output_dir / "topic_areas_overlapping.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"Overlapping chart saved to: {output_file}")
plt.close()

print("\nBoth visualizations created successfully!")
print("Files:")
print("  - topic_areas_stacked.png")
print("  - topic_areas_overlapping.png")
