#!/usr/bin/env python3
"""
Generate Illinois Institutions Map PDF with visual markers
Updated: November 24, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, Polygon, Wedge
import matplotlib.patches as mpatches
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

OUTPUT_DIR = Path('/Users/shivpat/Downloads/Seed Fund Tracking/visualizations/pdfs')
DATA_FILE = Path('/Users/shivpat/Downloads/Seed Fund Tracking/data/consolidated/IWRC Seed Fund Tracking.xlsx')

# ============================================================================
# DATA LOADING
# ============================================================================

def load_data():
    """Load and prepare institution data."""
    print("Loading data...")
    df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')

    # Rename columns
    col_map = {
        'Academic Institution of PI': 'institution',
        'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount'
    }

    df = df.rename(columns=col_map)

    # Get 10-year period data
    df_10yr = df[df.index > 0].copy()  # Use all data

    # Aggregate by institution
    inst_summary = df_10yr.groupby('institution').agg({
        'award_amount': ['sum', 'count']
    }).reset_index()

    inst_summary.columns = ['institution', 'total_funding', 'project_count']

    return inst_summary

# ============================================================================
# INSTITUTION COORDINATES
# ============================================================================

INSTITUTION_COORDS = {
    'University of Illinois Urbana-Champaign': (40.1020, -88.2272, 'Urbana-Champaign'),
    'University of Illinois at Urbana-Champaign': (40.1020, -88.2272, 'Urbana-Champaign'),
    'Univeristy of Illinois': (40.1020, -88.2272, 'Urbana-Champaign'),
    'Illinois Institute of Technology': (41.8348, -87.6266, 'Chicago'),
    'Southern Illinois University Carbondale': (37.7213, -89.2167, 'Carbondale'),
    'Southern Illinois University at Carbondale': (37.7213, -89.2167, 'Carbondale'),
    'Illinois State University': (40.5142, -88.9907, 'Normal'),
    'Illinois State Water Survey': (40.1164, -88.2434, 'Champaign'),
    'University of Illinois Chicago': (41.8708, -87.6470, 'Chicago'),
    'University of Illinois at Chicago': (41.8708, -87.6470, 'Chicago'),
    'Northwestern University': (42.0565, -87.6753, 'Evanston'),
    'Illinois Sustainable Technology Center': (40.1164, -88.2434, 'Champaign'),
    'Lewis and Clark Community College': (38.9742, -90.1840, 'Godfrey'),
    'National Great Rivers Research & Education Center': (38.8881, -90.1068, 'East Alton'),
    'Loyola University Chicago': (41.9989, -87.6576, 'Chicago'),
    'Eastern Illinois University': (39.4817, -88.2039, 'Charleston'),
    'Northern Illinois University': (41.9306, -88.7712, 'DeKalb'),
    'Lewis University': (41.6070, -88.0892, 'Romeoville'),
    'Basil\'s Harvest': (40.0, -89.0, 'Central Illinois'),
}

# ============================================================================
# MAP GENERATION
# ============================================================================

def generate_map_pdf():
    """Generate Illinois institutions map PDF."""
    print("Generating map PDF...")

    # Load data
    inst_data = load_data()

    # Add coordinates
    inst_data['lat'] = inst_data['institution'].apply(
        lambda x: INSTITUTION_COORDS.get(x, (40.0, -89.0, 'Unknown'))[0]
    )
    inst_data['lon'] = inst_data['institution'].apply(
        lambda x: INSTITUTION_COORDS.get(x, (40.0, -89.0, 'Unknown'))[1]
    )
    inst_data['city'] = inst_data['institution'].apply(
        lambda x: INSTITUTION_COORDS.get(x, (40.0, -89.0, 'Unknown'))[2]
    )

    pdf_path = OUTPUT_DIR / '2025_illinois_institutions_map.pdf'

    with PdfPages(pdf_path) as pdf:
        # Page 1: Map with markers
        fig = plt.figure(figsize=(11, 8.5))
        fig.suptitle('2025 IWRC Seed Fund - Funded Institutions Across Illinois',
                    fontsize=16, fontweight='bold', y=0.98)

        ax = fig.add_subplot(111)

        # Set map bounds for Illinois (with padding)
        ax.set_xlim(-92.5, -86.5)
        ax.set_ylim(36.5, 42.8)

        # Set background color (beige/tan like GIS Geography)
        ax.set_facecolor('#E8DCC8')

        # Draw simplified Illinois outline
        illinois_outline = [
            (37.0, -91.5), (37.2, -91.2), (37.5, -90.8), (37.8, -90.5),
            (38.0, -90.2), (38.2, -89.8), (38.4, -89.5), (38.5, -89.0),
            (38.7, -88.8), (38.9, -88.5), (39.1, -88.2), (39.3, -87.8),
            (39.5, -87.5), (39.7, -87.2), (39.9, -87.0), (40.1, -87.0),
            (40.3, -87.2), (40.5, -87.0), (40.7, -86.9), (41.0, -87.0),
            (41.5, -87.2), (42.0, -87.3), (42.3, -87.5), (42.5, -88.0),
            (42.3, -88.5), (42.0, -89.0), (41.5, -89.5), (41.0, -89.8),
            (40.5, -90.2), (40.0, -90.8), (39.5, -91.0), (39.0, -91.2),
            (38.5, -91.3), (38.0, -91.2), (37.5, -91.0), (37.0, -91.5)
        ]

        outline_poly = Polygon(illinois_outline, closed=True, fill=False,
                              edgecolor='black', linewidth=2)
        ax.add_patch(outline_poly)

        # Draw major rivers
        rivers = {
            'Mississippi': [(42.5, -91.0), (42.0, -91.2), (41.0, -91.5), (40.0, -91.4),
                           (39.0, -91.3), (38.5, -91.2), (37.5, -91.0)],
            'Illinois': [(42.3, -89.8), (41.5, -89.2), (40.5, -88.5), (39.5, -88.8),
                        (39.0, -88.9), (38.5, -89.2)],
            'Rock': [(42.5, -89.0), (42.0, -88.8), (41.2, -88.5), (40.5, -88.3)],
            'Fox': [(42.2, -88.8), (41.8, -88.4), (41.5, -88.2), (41.0, -88.0)],
        }

        for river_name, coords in rivers.items():
            lons = [c[1] for c in coords]
            lats = [c[0] for c in coords]
            ax.plot(lons, lats, color='#4A90E2', linewidth=1.5, alpha=0.7)

        # Draw lakes
        lakes = {
            'Carlyle Lake': (38.4, -89.3, 0.35),
            'Lake Shelbyville': (39.8, -88.5, 0.25),
            'Lake Springfield': (39.8, -89.6, 0.2),
            'Upper Peoria Lake': (40.8, -89.6, 0.2),
            'Rend Lake': (38.2, -89.0, 0.2),
            'Crab Orchard Lake': (37.8, -88.8, 0.2),
        }

        for lake_name, (lat, lon, radius) in lakes.items():
            circle = Circle((lon, lat), radius, facecolor='#4A90E2', alpha=0.5,
                           edgecolor='#4A90E2', linewidth=1)
            ax.add_patch(circle)

        # Sort institutions by funding for star sizing
        inst_data = inst_data.sort_values('total_funding', ascending=False)

        # Plot institution markers
        for idx, row in inst_data.iterrows():
            # Size based on funding
            funding = row['total_funding']
            if funding > 1000000:
                size = 300
                color = '#d62728'  # Red for largest
                label_size = 9
            elif funding > 500000:
                size = 200
                color = '#ff7f0e'  # Orange
                label_size = 8
            elif funding > 100000:
                size = 150
                color = '#1f77b4'  # Blue
                label_size = 7
            else:
                size = 100
                color = '#2ca02c'  # Green
                label_size = 6

            # Plot star marker
            ax.scatter(row['lon'], row['lat'], marker='*', s=size*3, color=color,
                      edgecolors='darkblue', linewidths=1, zorder=5, alpha=0.9)

            # Add label
            short_name = row['institution'].split()[0] if len(row['institution']) > 15 else row['institution'][:12]
            ax.text(row['lon'] + 0.2, row['lat'] + 0.15, short_name,
                   fontsize=label_size, fontweight='bold', zorder=6,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                            alpha=0.7, edgecolor='none'))

        # Add legend
        legend_elements = [
            plt.scatter([], [], marker='*', s=900, color='#d62728',
                       label='$1M+ funding', edgecolors='darkblue'),
            plt.scatter([], [], marker='*', s=600, color='#ff7f0e',
                       label='$500K-$1M', edgecolors='darkblue'),
            plt.scatter([], [], marker='*', s=450, color='#1f77b4',
                       label='$100K-$500K', edgecolors='darkblue'),
            plt.scatter([], [], marker='*', s=300, color='#2ca02c',
                       label='<$100K', edgecolors='darkblue')
        ]

        ax.legend(handles=legend_elements, loc='lower left', fontsize=9,
                 framealpha=0.95, title='Funding Level', title_fontsize=10)

        # Add river and lake labels
        ax.text(-90.5, 41.5, 'Mississippi\nRiver', fontsize=8, style='italic', color='#4A90E2', alpha=0.7)
        ax.text(-88.5, 40.0, 'Illinois River', fontsize=8, style='italic', color='#4A90E2', alpha=0.7)
        ax.text(-89.3, 38.4, 'Carlyle\nLake', fontsize=7, style='italic', color='#4A90E2', alpha=0.7)
        ax.text(-88.5, 39.8, 'Lake\nShelbyville', fontsize=7, style='italic', color='#4A90E2', alpha=0.7)

        # Add attribution
        ax.text(0.99, 0.01, 'Source: GISGeography.com | Data: November 24, 2025',
               transform=ax.transAxes, fontsize=8, ha='right', va='bottom',
               style='italic', color='gray')

        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

        # Page 2: Institution listing with details
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_subplot(111)
        ax.axis('off')

        ax.text(0.5, 0.97, 'IWRC Funded Institutions', ha='center', fontsize=14,
               fontweight='bold', transform=ax.transAxes)
        ax.text(0.5, 0.94, '10-Year Period (2015-2024)', ha='center', fontsize=11,
               style='italic', transform=ax.transAxes, color='gray')

        # Sort by funding
        inst_data_sorted = inst_data.sort_values('total_funding', ascending=False)

        # Create listing
        listing_text = "Institution                                    Funding        Projects\n"
        listing_text += "─" * 75 + "\n"

        for idx, row in inst_data_sorted.iterrows():
            inst_short = row['institution'][:44] if len(row['institution']) > 44 else row['institution']
            listing_text += f"{inst_short:<45} ${row['total_funding']:>10,.0f}   {int(row['project_count']):>3d}\n"

        listing_text += "─" * 75 + "\n"
        listing_text += f"{'TOTAL':<45} ${inst_data_sorted['total_funding'].sum():>10,.0f}   {int(inst_data_sorted['project_count'].sum()):>3d}"

        ax.text(0.05, 0.90, listing_text, ha='left', va='top', fontsize=7.5,
               transform=ax.transAxes, family='monospace',
               bbox=dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.5))

        ax.text(0.5, 0.02, f"Generated: {datetime.now().strftime('%B %d, %Y')}",
               ha='center', fontsize=8, style='italic', color='gray', transform=ax.transAxes)

        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

    print(f"✓ Saved: {pdf_path}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print("GENERATING ILLINOIS INSTITUTIONS MAP PDF")
    print("="*70)

    generate_map_pdf()

    print("\n" + "="*70)
    print("✓ MAP PDF GENERATED SUCCESSFULLY")
    print("="*70)
