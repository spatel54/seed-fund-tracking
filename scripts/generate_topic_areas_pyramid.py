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
print("Loading fact sheet data...")
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

# Function to assign topics based on keywords
def assign_topics(row):
    keywords = []
    for col in ['Keyword 1', 'Keyword 2', 'Keyword 3']:
        if col in df_clean.columns and pd.notna(row[col]):
            kw = str(row[col]).strip().upper()
            if kw:
                keywords.append(kw)

    if not keywords:
        return {}

    matched_topics = {}
    for topic, topic_kws in topic_keywords.items():
        for kw in keywords:
            if any(tkw in kw or kw in tkw for tkw in topic_kws):
                if topic not in matched_topics:
                    matched_topics[topic] = 0
                matched_topics[topic] += 1

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
# Sort by 10-year (descending, so highest at top in pyramid)
df_funding = df_funding.sort_values('10-Year (2015-2024)', ascending=False)

print("\nTopic Areas Funding Comparison:")
print(df_funding.to_string(index=False))
print(f"\nTotal 5-Year: ${df_funding['5-Year (2020-2024)'].sum():,.0f}")
print(f"Total 10-Year: ${df_funding['10-Year (2015-2024)'].sum():,.0f}")

# ============================================================================
# VERSION 1: STACKED PYRAMID BARS
# ============================================================================
print("\nGenerating stacked pyramid bar chart...")
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)

topics = df_funding['Topic'].tolist()
y_pos = np.arange(len(topics))

# For pyramid: 5-year as negative (left), 10-year as positive (right)
amounts_5yr_neg = -df_funding['5-Year (2020-2024)'].values
amounts_10yr = df_funding['10-Year (2015-2024)'].values

# Create bars (5-year on left as negative, 10-year on right as positive)
bars1 = ax.barh(y_pos, amounts_5yr_neg, color='#e8a76a', label='5-Year (2020-2024)', height=0.65)
bars2 = ax.barh(y_pos, amounts_10yr, color='#c95d34', label='10-Year (2015-2024)', height=0.65)

# Add labels for 5-year amounts (left side)
for bar, amount in zip(bars1, df_funding['5-Year (2020-2024)'].values):
    if amount > 0:
        label_text = f'${amount:,.0f}'
        ax.text(amount * -0.5, bar.get_y() + bar.get_height()/2, label_text,
                va='center', ha='right', fontsize=9, color='#001a4d', fontweight='bold')

# Add labels for 10-year amounts (right side)
for bar, amount in zip(bars2, df_funding['10-Year (2015-2024)'].values):
    if amount > 0:
        label_text = f'${amount:,.0f}'
        ax.text(amount * 0.5, bar.get_y() + bar.get_height()/2, label_text,
                va='center', ha='left', fontsize=9, color='#001a4d', fontweight='bold')

# Style the axis
ax.set_xlabel('')
ax.set_title('TOPIC AREAS OF CONCERN IN ILLINOIS - PYRAMID COMPARISON',
             fontsize=14, fontweight='bold', pad=20, color='#001a4d', loc='center')

# Set x-axis limits symmetrically
max_val = max(df_funding['5-Year (2020-2024)'].max(), df_funding['10-Year (2015-2024)'].max())
ax.set_xlim(-max_val * 1.2, max_val * 1.2)

# Format x-axis labels as absolute values
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${abs(x)/1e3:.0f}K' if abs(x) < 1e6 else f'${abs(x)/1e6:.1f}M'))

# Add vertical line at center
ax.axvline(x=0, color='#001a4d', linewidth=1.5, linestyle='-', alpha=0.3)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.grid(axis='x', alpha=0.2, linestyle='-', linewidth=0.5, color='#e0e0e0')
ax.set_axisbelow(True)

ax.set_yticks(y_pos)
ax.set_yticklabels(topics, fontsize=11, color='#001a4d')
ax.tick_params(axis='y', labelsize=11, colors='#001a4d', pad=8)
ax.tick_params(axis='x', labelsize=10, colors='#666666')

# Add legend
legend = ax.legend(loc='lower right', fontsize=11, frameon=True, fancybox=False,
                   edgecolor='#001a4d', framealpha=0.95)
legend.get_frame().set_linewidth(1.5)
for text in legend.get_texts():
    text.set_color('#001a4d')
    text.set_fontweight('bold')

# Add border
rect = plt.Rectangle((0.02, 0.02), 0.96, 0.96, fill=False, transform=fig.transFigure,
                      edgecolor='#001a4d', linewidth=2.5)
fig.patches.append(rect)

plt.tight_layout(rect=[0.05, 0.04, 0.96, 0.98])

output_file = output_dir / "topic_areas_pyramid_stacked.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"Stacked pyramid chart saved to: {output_file}")
plt.close()

# ============================================================================
# VERSION 2: OVERLAPPING PYRAMID BARS
# ============================================================================
print("Generating overlapping pyramid bar chart...")
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)

# Create overlapping pyramid bars with transparency
bars1 = ax.barh(y_pos - 0.15, amounts_5yr_neg, 0.3, color='#e8a76a',
                label='5-Year (2020-2024)', alpha=0.8, edgecolor='none')
bars2 = ax.barh(y_pos + 0.15, amounts_10yr, 0.3, color='#c95d34',
                label='10-Year (2015-2024)', alpha=0.9, edgecolor='none')

# Add labels for 5-year amounts (left side)
for bar, amount in zip(bars1, df_funding['5-Year (2020-2024)'].values):
    if amount > 0:
        label_text = f'${amount:,.0f}'
        ax.text(amount * -0.6, bar.get_y() + bar.get_height()/2, label_text,
                va='center', ha='right', fontsize=9, color='#cc3300', fontweight='bold')

# Add labels for 10-year amounts (right side)
for bar, amount in zip(bars2, df_funding['10-Year (2015-2024)'].values):
    if amount > 0:
        label_text = f'${amount:,.0f}'
        ax.text(amount * 0.6, bar.get_y() + bar.get_height()/2, label_text,
                va='center', ha='left', fontsize=9, color='#001a4d', fontweight='bold')

# Style the axis
ax.set_xlabel('')
ax.set_title('TOPIC AREAS OF CONCERN IN ILLINOIS - PYRAMID COMPARISON',
             fontsize=14, fontweight='bold', pad=20, color='#001a4d', loc='center')

# Set x-axis limits symmetrically
max_val = max(df_funding['5-Year (2020-2024)'].max(), df_funding['10-Year (2015-2024)'].max())
ax.set_xlim(-max_val * 1.2, max_val * 1.2)

# Format x-axis labels as absolute values
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${abs(x)/1e3:.0f}K' if abs(x) < 1e6 else f'${abs(x)/1e6:.1f}M'))

# Add vertical line at center
ax.axvline(x=0, color='#001a4d', linewidth=1.5, linestyle='-', alpha=0.3)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.grid(axis='x', alpha=0.2, linestyle='-', linewidth=0.5, color='#e0e0e0')
ax.set_axisbelow(True)

ax.set_yticks(y_pos)
ax.set_yticklabels(topics, fontsize=11, color='#001a4d')
ax.tick_params(axis='y', labelsize=11, colors='#001a4d', pad=8)
ax.tick_params(axis='x', labelsize=10, colors='#666666')

# Add legend
legend = ax.legend(loc='lower right', fontsize=11, frameon=True, fancybox=False,
                   edgecolor='#001a4d', framealpha=0.95)
legend.get_frame().set_linewidth(1.5)
for text in legend.get_texts():
    text.set_color('#001a4d')
    text.set_fontweight('bold')

# Add border
rect = plt.Rectangle((0.02, 0.02), 0.96, 0.96, fill=False, transform=fig.transFigure,
                      edgecolor='#001a4d', linewidth=2.5)
fig.patches.append(rect)

plt.tight_layout(rect=[0.05, 0.04, 0.96, 0.98])

output_file = output_dir / "topic_areas_pyramid_overlapping.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"Overlapping pyramid chart saved to: {output_file}")
plt.close()

print("\nBoth pyramid visualizations created successfully!")
print("Files:")
print("  - topic_areas_pyramid_stacked.png")
print("  - topic_areas_pyramid_overlapping.png")
