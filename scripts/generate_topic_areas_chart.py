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

# Load data from Sheet1, columns CA-CB, rows 34-43
print("Loading topic areas data from Sheet1...")
df = pd.read_excel(
    data_file,
    sheet_name='Sheet1',
    usecols=[78, 79],  # Columns CA (78) and CB (79) in 0-based indexing
    skiprows=33,       # Skip first 33 rows to start at row 34
    nrows=10,          # Read 10 rows (rows 34-43)
    header=None        # No header row
)

# Rename columns
df.columns = ['Topic', 'Funding']

# Clean up data
df = df.dropna()
df['Funding'] = pd.to_numeric(df['Funding'], errors='coerce')
df = df[df['Funding'] > 0]

# Sort by funding amount (ascending for bottom-to-top bar chart)
df_sorted = df.sort_values('Funding', ascending=True)

print(f"Loaded {len(df_sorted)} topics")
print("\nTopic Areas Data:")
print(df_sorted.to_string(index=False))
print(f"\nTotal Funding: ${df_sorted['Funding'].sum():,.0f}")

# Create visualization
fig = plt.figure(figsize=(16, 11))
ax = fig.add_subplot(111)

# Prepare data
topics = df_sorted['Topic'].tolist()
amounts = df_sorted['Funding'].values

# Create bars
bars = ax.barh(topics, amounts, color='#c95d34', height=0.6)

# Add amount labels
for bar, amount in zip(bars, amounts):
    label_text = f'${amount:,.0f}'
    ax.text(amount, bar.get_y() + bar.get_height()/2, f'  {label_text}',
            va='center', ha='left', fontsize=11, color='#001a4d', fontweight='bold',
            family='sans-serif')

# Style the axis
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_title('TOPIC AREAS OF CONCERN IN ILLINOIS',
             fontsize=15, fontweight='bold', pad=20, color='#001a4d', loc='left')

# Set x-axis limits and formatting
max_val = amounts.max()
ax.set_xlim(0, max_val * 1.15)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K' if x < 1e6 else f'${x/1e6:.1f}M'))

# Style the plot
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#cccccc')
ax.spines['bottom'].set_color('#cccccc')
ax.grid(axis='x', alpha=0.2, linestyle='-', linewidth=0.5, color='#e0e0e0')
ax.set_axisbelow(True)

# Style ticks
ax.tick_params(axis='y', labelsize=11, colors='#001a4d', pad=8)
ax.tick_params(axis='x', labelsize=10, colors='#666666')

# Add legend box
legend_text = 'Funding\nmanaged\nby the\nIWRC'
props = dict(boxstyle='round,pad=0.8', facecolor='#c95d34', edgecolor='none', alpha=0.9)
ax.text(0.98, 0.97, legend_text, transform=ax.transAxes,
        fontsize=11, verticalalignment='top', horizontalalignment='right',
        bbox=props, color='white', fontweight='bold', linespacing=1.5)

# Add a border around the figure
rect = plt.Rectangle((0.02, 0.02), 0.96, 0.96, fill=False, transform=fig.transFigure,
                      edgecolor='#001a4d', linewidth=2.5)
fig.patches.append(rect)

plt.tight_layout(rect=[0.05, 0.04, 0.96, 0.98])

# Save as PNG
output_file = output_dir / "topic_areas_funding.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"\nChart saved to: {output_file}")

plt.close()
print("Done!")
