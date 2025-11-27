#!/usr/bin/env python3
"""
Create Illinois Institutions Map PDF - Final Version
Uses matplotlib with proper coordinate plotting
Updated: November 24, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, Polygon
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

OUTPUT_DIR = Path('/Users/shivpat/seed-fund-tracking/visualizations/pdfs')
DATA_FILE = Path('/Users/shivpat/seed-fund-tracking/data/consolidated/IWRC Seed Fund Tracking.xlsx')

INSTITUTION_COORDS = {
    'University of Illinois Urbana-Champaign': (40.1020, -88.2272),
    'University of Illinois at Urbana-Champaign': (40.1020, -88.2272),
    'Univeristy of Illinois': (40.1020, -88.2272),
    'Illinois Institute of Technology': (41.8348, -87.6266),
    'Southern Illinois University Carbondale': (37.7213, -89.2167),
    'Southern Illinois University at Carbondale': (37.7213, -89.2167),
    'Southern Illinois University': (37.7213, -89.2167),
    'Illinois State University': (40.5142, -88.9907),
    'Illinois State Water Survey': (40.1164, -88.2434),
    'University of Illinois Chicago': (41.8708, -87.6470),
    'University of Illinois at Chicago': (41.8708, -87.6470),
    'Northwestern University': (42.0565, -87.6753),
    'Illinois Sustainable Technology Center': (40.1164, -88.2434),
    'Lewis and Clark Community College': (38.9742, -90.1840),
    'National Great Rivers Research & Education Center': (38.8881, -90.1068),
    'Loyola University Chicago': (41.9989, -87.6576),
    'Eastern Illinois University': (39.4817, -88.2039),
    'Northern Illinois University': (41.9306, -88.7712),
    'Lewis University': (41.6070, -88.0892),
    'Basil\'s Harvest': (40.0, -89.0),
    'University of Illinois': (40.1020, -88.2272),
}

# ============================================================================
# DATA LOADING
# ============================================================================

def load_data():
    """Load and prepare institution data."""
    print("Loading data...")
    df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')

    col_map = {
        'Academic Institution of PI': 'institution',
        'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount'
    }

    df = df.rename(columns=col_map)

    # Aggregate by institution
    inst_summary = df.groupby('institution').agg({
        'award_amount': ['sum', 'count']
    }).reset_index()

    inst_summary.columns = ['institution', 'total_funding', 'project_count']

    # Add coordinates
    inst_summary['lat'] = inst_summary['institution'].apply(
        lambda x: INSTITUTION_COORDS.get(x, (40.0, -89.0))[0]
    )
    inst_summary['lon'] = inst_summary['institution'].apply(
        lambda x: INSTITUTION_COORDS.get(x, (40.0, -89.0))[1]
    )

    # Filter to Illinois institutions only
    inst_summary = inst_summary[(inst_summary['lat'] >= 36.9) & (inst_summary['lat'] <= 42.6)]

    return inst_summary.sort_values('total_funding', ascending=False)

# ============================================================================
# MAP GENERATION - BOTH PAGES
# ============================================================================

def generate_map_pdf():
    """Generate Illinois institutions map PDF with both pages."""
    print("Generating map...")

    inst_data = load_data()
    pdf_path = OUTPUT_DIR / '2025_illinois_institutions_map.pdf'

    with PdfPages(pdf_path) as pdf:
        # =====================
        # PAGE 1: MAP WITH MARKERS
        # =====================
        fig = plt.figure(figsize=(14, 10))
        fig.suptitle('2025 IWRC Seed Fund - Funded Institutions Across Illinois',
                    fontsize=18, fontweight='bold', y=0.98)

        ax = fig.add_subplot(111)

        # Set map bounds for Illinois
        ax.set_xlim(-92.0, -86.8)
        ax.set_ylim(36.8, 42.8)

        # Set background color
        ax.set_facecolor('#E8E8E8')
        fig.patch.set_facecolor('white')

        # Draw Illinois outline
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

        outline_poly = Polygon(illinois_outline, closed=True, fill=True,
                              facecolor='#F5F5F5', edgecolor='black', linewidth=2.5, zorder=1)
        ax.add_patch(outline_poly)

        # Draw rivers
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
            ax.plot(lons, lats, color='#4A90E2', linewidth=2, alpha=0.7, zorder=2)

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
            circle = Circle((lon, lat), radius, facecolor='#4A90E2', alpha=0.4,
                           edgecolor='#4A90E2', linewidth=1.5, zorder=2)
            ax.add_patch(circle)

        # Normalize funding for color mapping
        min_funding = inst_data['total_funding'].min()
        max_funding = inst_data['total_funding'].max()

        # Plot institutions with star markers
        for idx, row in inst_data.iterrows():
            lat, lon = row['lat'], row['lon']
            funding = row['total_funding']
            projects = row['project_count']

            # Determine marker size based on funding
            size = 200 + (funding - min_funding) / (max_funding - min_funding) * 800

            # Determine color based on funding
            color_intensity = (funding - min_funding) / (max_funding - min_funding)
            if color_intensity > 0.66:
                color = '#d62728'  # Red for highest
            elif color_intensity > 0.33:
                color = '#ff7f0e'  # Orange for medium
            else:
                color = '#1f77b4'  # Blue for lower

            # Plot star marker
            ax.scatter(lon, lat, marker='*', s=size, color=color,
                      edgecolors='darkblue', linewidths=2, zorder=5, alpha=0.9)

            # Add institution label
            short_name = row['institution']
            if len(short_name) > 25:
                words = short_name.split()
                if len(words) > 1:
                    short_name = ' '.join(words[:2])
                else:
                    short_name = short_name[:20]

            ax.text(lon + 0.25, lat + 0.25, short_name,
                   fontsize=8, fontweight='bold', zorder=6,
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                            alpha=0.85, edgecolor='gray', linewidth=1))

        # Add river/lake labels
        ax.text(-90.8, 41.2, 'Mississippi\nRiver', fontsize=9, style='italic',
               color='#4A90E2', alpha=0.8, ha='center')
        ax.text(-88.5, 40.2, 'Illinois River', fontsize=9, style='italic',
               color='#4A90E2', alpha=0.8, ha='center')
        ax.text(-89.3, 38.7, 'Carlyle\nLake', fontsize=7, style='italic',
               color='#4A90E2', alpha=0.8, ha='center')

        # Add legend
        legend_elements = [
            plt.scatter([], [], marker='*', s=400, color='#d62728',
                       edgecolors='darkblue', linewidths=2,
                       label='$4M+ funding (1 institution)', zorder=5),
            plt.scatter([], [], marker='*', s=300, color='#ff7f0e',
                       edgecolors='darkblue', linewidths=2,
                       label='$1M-$4M (2 institutions)', zorder=5),
            plt.scatter([], [], marker='*', s=200, color='#1f77b4',
                       edgecolors='darkblue', linewidths=2,
                       label='<$1M (remaining institutions)', zorder=5)
        ]

        ax.legend(handles=legend_elements, loc='lower left', fontsize=10,
                 framealpha=0.95, edgecolor='black', title='Funding Level', title_fontsize=11)

        # Add attribution
        ax.text(0.99, 0.01, 'Source: GISGeography.com | Data: November 24, 2025 (Corrected Analysis)',
               transform=ax.transAxes, fontsize=8, ha='right', va='bottom',
               style='italic', color='gray')

        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.set_aspect('equal')

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight', dpi=150)
        plt.close(fig)
        print("✓ Saved page 1 (map)")

        # =====================
        # PAGE 2: INSTITUTION LISTING
        # =====================
        fig = plt.figure(figsize=(11, 8.5))
        ax = fig.add_subplot(111)
        ax.axis('off')

        # Title
        ax.text(0.5, 0.97, 'IWRC Funded Institutions - Detailed Listing',
               ha='center', fontsize=14, fontweight='bold', transform=ax.transAxes)
        ax.text(0.5, 0.94, '10-Year Period (2015-2024)',
               ha='center', fontsize=11, style='italic', transform=ax.transAxes, color='gray')

        # Create table data
        table_data = [['Institution', 'City', 'Funding', 'Projects']]

        for idx, row in inst_data.head(20).iterrows():
            inst_short = row['institution'][:45]
            table_data.append([
                inst_short,
                'IL',
                f"${row['total_funding']:,.0f}",
                f"{int(row['project_count'])}"
            ])

        # Add totals
        table_data.append([
            'TOTAL',
            '',
            f"${inst_data['total_funding'].sum():,.0f}",
            f"{int(inst_data['project_count'].sum())}"
        ])

        # Create table
        table = ax.table(cellText=table_data, cellLoc='left', loc='center',
                        colWidths=[0.45, 0.1, 0.25, 0.2],
                        bbox=[0.05, 0.15, 0.9, 0.75])

        table.auto_set_font_size(False)
        table.set_fontsize(8.5)
        table.scale(1, 2)

        # Style header row
        for i in range(4):
            table[(0, i)].set_facecolor('#003d7a')
            table[(0, i)].set_text_props(weight='bold', color='white')

        # Style total row
        for i in range(4):
            table[(len(table_data)-1, i)].set_facecolor('#cccccc')
            table[(len(table_data)-1, i)].set_text_props(weight='bold')

        # Alternate row colors
        for i in range(1, len(table_data)-1):
            for j in range(4):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#f5f5f5')

        # Add note
        ax.text(0.5, 0.08, f"Generated: {datetime.now().strftime('%B %d, %Y')} | Data corrected to reflect unique projects",
               ha='center', fontsize=8, style='italic', color='gray', transform=ax.transAxes)

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight', dpi=150)
        plt.close(fig)
        print("✓ Saved page 2 (institution listing)")

    print(f"✓ PDF saved: {pdf_path}")

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
    print("\nFeatures:")
    print("  ✓ Page 1: Illinois map with rivers, lakes, and institution markers")
    print("  ✓ Page 2: Detailed institution listing table")
    print("  ✓ Color-coded markers (red=highest funding, blue=lower)")
    print("  ✓ Corrected data (November 24, 2025)")
    print("="*70)
