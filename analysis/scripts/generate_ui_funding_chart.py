
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add scripts to path
sys.path.insert(0, '/Users/shivpat/seed-fund-tracking/analysis/scripts')
from iwrc_brand_style import IWRC_COLORS, configure_matplotlib_iwrc, apply_iwrc_matplotlib_style, add_logo_to_matplotlib_figure
from iwrc_data_loader import IWRCDataLoader

def generate_ui_funding_chart():
    print("Loading data...")
    loader = IWRCDataLoader()
    df = loader.load_master_data(deduplicate=True)
    
    # Filter 2015-2024
    df = df[df['project_year'].between(2015, 2024, inclusive='both')]
    
    # Filter for UI Affiliated Only
    ui_keywords = ['University of Illinois', 'Southern Illinois University']
    df_ui = df[
        (df['institution'].str.contains('|'.join(ui_keywords), case=False, na=False)) & 
        (df['institution'] != "Basil's Harvest")
    ]
    
    # Group by institution
    inst_funding = df_ui.groupby('institution')['award_amount'].sum().sort_values(ascending=True) # Ascending for barh
    
    print("\nFunding Data:")
    print(inst_funding)
    
    # Create Chart
    configure_matplotlib_iwrc()
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot bars
    bars = ax.barh(inst_funding.index, inst_funding.values, color=IWRC_COLORS['primary'])
    
    # Add labels with FULL numbers
    for bar in bars:
        width = bar.get_width()
        label_x_pos = width + (inst_funding.max() * 0.01)
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'${width:,.0f}',
                va='center', fontsize=11, fontweight='bold', color=IWRC_COLORS['text'])
    
    # Styling
    ax.set_title('Top University of Illinois Affiliated Institutions by Funding (2015-2024)', 
                 fontsize=14, fontweight='bold', color=IWRC_COLORS['dark_teal'], pad=20)
    ax.set_xlabel('Total Funding ($)', fontsize=12, fontweight='bold')
    ax.set_ylabel('') # Institution names are self-explanatory
    
    # Remove spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Expand x-axis to fit labels
    ax.set_xlim(0, inst_funding.max() * 1.2)
    
    # Add logo
    add_logo_to_matplotlib_figure(fig, position='bottom-right')
    
    # Save
    output_dir = Path('/Users/shivpat/seed-fund-tracking/deliverables_final/visualizations/static/institutions')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'ui_affiliated_funding.png'
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nChart saved to: {output_file}")

if __name__ == "__main__":
    generate_ui_funding_chart()
