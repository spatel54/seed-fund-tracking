import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up paths
# Set up paths
project_root = Path(__file__).parent.parent.parent
data_file = project_root / "data/consolidated/fact sheet data.xlsx"
output_dir = project_root / "deliverables_final/visualizations/static/topics"
output_dir.mkdir(parents=True, exist_ok=True)

# Import IWRC branding
try:
    from iwrc_brand_style import IWRC_COLORS, configure_matplotlib_iwrc
    configure_matplotlib_iwrc()
    USE_IWRC = True
except ImportError:
    print("Warning: IWRC branding not available")
    USE_IWRC = False

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
bars = ax.barh(topics, amounts, color=IWRC_COLORS['primary'], height=0.6)

# Add amount labels
for bar, amount in zip(bars, amounts):
    label_text = f'${amount:,.0f}'
    ax.text(amount, bar.get_y() + bar.get_height()/2, f'  {label_text}',
            va='center', ha='left', fontsize=11, color=IWRC_COLORS['text'], fontweight='bold')

# Style the axis
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_title('TOPIC AREAS OF CONCERN IN ILLINOIS',
             fontsize=15, fontweight='bold', pad=20, color=IWRC_COLORS['dark_teal'], loc='left')

# Set x-axis limits and formatting
max_val = amounts.max()
ax.set_xlim(0, max_val * 1.15)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K' if x < 1e6 else f'${x/1e6:.1f}M'))

# Apply IWRC style
from iwrc_brand_style import apply_iwrc_matplotlib_style, add_logo_to_matplotlib_figure
apply_iwrc_matplotlib_style(fig, ax)

# Add legend box
legend_text = 'Funding\nmanaged\nby the\nIWRC'
props = dict(boxstyle='round,pad=0.8', facecolor=IWRC_COLORS['secondary'], edgecolor='none', alpha=0.9)
ax.text(0.98, 0.97, legend_text, transform=ax.transAxes,
        fontsize=11, verticalalignment='top', horizontalalignment='right',
        bbox=props, color='white', fontweight='bold', linespacing=1.5)

# Add logo
add_logo_to_matplotlib_figure(fig, position='bottom-right', size=0.1)

plt.tight_layout()

# Save as PNG
output_file = output_dir / "topic_areas_funding.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
print(f"\nChart saved to: {output_file}")

plt.close()
print("Done!")
