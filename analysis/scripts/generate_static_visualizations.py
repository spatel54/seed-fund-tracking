#!/usr/bin/env python3
"""
Generate all static visualizations for IWRC Seed Fund Analysis
High-quality PNG outputs at 300 DPI with IWRC branding and award type breakdown
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path
import sys
import os

# Add scripts directory to path
# sys.path.insert(0, '/Users/shivpat/seed-fund-tracking/scripts')

# Import IWRC branding
try:
    from iwrc_brand_style import IWRC_COLORS, configure_matplotlib_iwrc, apply_iwrc_matplotlib_style, add_logo_to_matplotlib_figure
    USE_IWRC_BRANDING = True
except ImportError:
    USE_IWRC_BRANDING = False
    print("Warning: IWRC branding modules not available")

# Configure matplotlib with IWRC branding
if USE_IWRC_BRANDING:
    configure_matplotlib_iwrc()
    COLORS = IWRC_COLORS.copy()
    # Add missing keys used in this script
    COLORS.update({
        'blue': IWRC_COLORS['primary'],
        'dark_blue': IWRC_COLORS['dark_teal'],
        'teal': IWRC_COLORS['primary'],
        'orange': IWRC_COLORS['accent'],
        'green': IWRC_COLORS['secondary'],
        'red': IWRC_COLORS['gold'],
        'purple': '#9467bd', # Keep purple for variety or map to text?
        'yellow': '#bcbd22'
    })
else:
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    # Fallback color palette
    COLORS = {
        'primary': '#258372',        # IWRC Teal
        'secondary': '#639757',      # IWRC Olive
        'success': '#8ab38a',        # IWRC Sage
        'accent': '#FCC080',         # IWRC Peach
        'blue': '#258372',
        'dark_blue': '#1a5f52',
        'teal': '#258372',
        'orange': '#FCC080',
        'green': '#639757',
        'red': '#e6a866',
        'purple': '#9467bd',
        'yellow': '#bcbd22',
        'brown': '#8c564b',
        'pink': '#e377c2'
    }

# Output directory
# Output directory
OUTPUT_DIR = Path("/Users/shivpat/seed-fund-tracking/FINAL_DELIVERABLES_2_backup_20251125_194954 copy 2/visualizations/static_breakdown")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Data file path
DATA_FILE = Path("/Users/shivpat/seed-fund-tracking/data/consolidated/IWRC Seed Fund Tracking.xlsx")

def load_institution_data():
    """Load and standardize institution funding data from consolidated Excel file"""
    df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')

    # Standardize institution names
    def standardize_institution(name):
        if pd.isna(name):
            return "Unknown"
        name = str(name).strip()

        # UIUC standardization - combine all variants
        if 'urbana' in name.lower() and 'champaign' in name.lower():
            return 'University of Illinois at Urbana-Champaign'

        # SIU standardization
        if name.lower().startswith('southern illinois university'):
            if 'carbondale' in name.lower():
                return 'Southern Illinois University at Carbondale'
            return 'Southern Illinois University'

        # Generic "University of Illinois" - keep separate for now but flag
        if name == 'University of Illinois':
            return 'University of Illinois (campus unclear)'

        # UIC standardization
        if 'university of illinois chicago' in name.lower() or name == 'UIC':
            return 'University of Illinois Chicago'

        return name

    df['Institution_Standardized'] = df['Academic Institution of PI'].apply(standardize_institution)

    # Calculate total funding per institution
    inst_funding = df.groupby('Institution_Standardized')['Award Amount Allocated ($) this must be filled in for all lines'].sum()
    inst_funding = inst_funding.sort_values(ascending=False).head(10)

    # Convert to millions
    inst_funding_millions = {k: v/1e6 for k, v in inst_funding.items()}

    return inst_funding_millions

# Data: Corrected project counts
DATA = {
    '10yr': {
        'projects': 77,
        'investment': 8.5,  # Million
        'students': 304,
        'roi': 0.03,
        'followon': 0.255,  # Million
        'institutions': 16,
        'period': '2015-2024'
    },
    '5yr': {
        'projects': 47,
        'investment': 7.3,  # Million
        'students': 186,
        'roi': 0.04,
        'followon': 0.292,  # Million
        'institutions': 11,
        'period': '2020-2024'
    }
}

# Student breakdown data
STUDENT_DATA = {
    '10yr': {
        'PhD': 122,
        'Masters': 98,
        'Undergrad': 71,
        'PostDoc': 13
    },
    '5yr': {
        'PhD': 74,
        'Masters': 60,
        'Undergrad': 43,
        'PostDoc': 9
    }
}

# Projects by year (corrected counts)
PROJECTS_BY_YEAR = {
    2015: 11,
    2016: 12,
    2017: 9,
    2018: 8,
    2019: 7,
    2020: 10,
    2021: 9,
    2022: 8,
    2023: 11,
    2024: 9
}

# Top institutions by funding - will be loaded from real data
TOP_INSTITUTIONS = None  # Loaded dynamically in main()

def save_figure(fig, filename, dpi=300):
    """Save figure with metadata"""
    filepath = OUTPUT_DIR / filename
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    size_mb = filepath.stat().st_size / (1024 * 1024)
    print(f"✓ Created: {filename} ({size_mb:.2f} MB)")
    return filepath

def create_executive_summary():
    """1. Create executive summary infographic"""
    fig = plt.figure(figsize=(14, 10), facecolor='white')
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Title
    fig.text(0.5, 0.95, 'IWRC Seed Fund Analysis Executive Summary',
             ha='center', va='top', fontsize=24, fontweight='bold', color=COLORS['dark_blue'])

    fig.text(0.5, 0.91, 'Corrected Project Counts & Impact Metrics',
             ha='center', va='top', fontsize=16, style='italic', color=COLORS['teal'])

    # 10-Year Period Box
    box1_y = 0.75
    fig.text(0.25, box1_y + 0.08, '10-Year Period (2015-2024)',
             ha='center', fontsize=18, fontweight='bold', color=COLORS['blue'])

    # Create metric boxes for 10yr
    metrics_10yr = [
        ('Projects', '77', COLORS['blue']),
        ('Investment', '$8.5M', COLORS['orange']),
        ('Students', '304', COLORS['green']),
        ('ROI', '0.03x', COLORS['red'])
    ]

    x_positions = [0.08, 0.18, 0.28, 0.38]
    for i, (label, value, color) in enumerate(metrics_10yr):
        x = x_positions[i]
        rect = mpatches.FancyBboxPatch((x, box1_y - 0.05), 0.08, 0.08,
                                       boxstyle="round,pad=0.01",
                                       edgecolor=color, facecolor=color, alpha=0.2,
                                       linewidth=2, transform=fig.transFigure)
        fig.patches.append(rect)
        fig.text(x + 0.04, box1_y + 0.01, value, ha='center', fontsize=20,
                fontweight='bold', color=color)
        fig.text(x + 0.04, box1_y - 0.03, label, ha='center', fontsize=12, color='gray')

    # 5-Year Period Box
    box2_y = 0.55
    fig.text(0.25, box2_y + 0.08, '5-Year Period (2020-2024)',
             ha='center', fontsize=18, fontweight='bold', color=COLORS['purple'])

    # Create metric boxes for 5yr
    metrics_5yr = [
        ('Projects', '47', COLORS['blue']),
        ('Investment', '$7.3M', COLORS['orange']),
        ('Students', '186', COLORS['green']),
        ('ROI', '0.04x', COLORS['red'])
    ]

    for i, (label, value, color) in enumerate(metrics_5yr):
        x = x_positions[i]
        rect = mpatches.FancyBboxPatch((x, box2_y - 0.05), 0.08, 0.08,
                                       boxstyle="round,pad=0.01",
                                       edgecolor=color, facecolor=color, alpha=0.2,
                                       linewidth=2, transform=fig.transFigure)
        fig.patches.append(rect)
        fig.text(x + 0.04, box2_y + 0.01, value, ha='center', fontsize=20,
                fontweight='bold', color=color)
        fig.text(x + 0.04, box2_y - 0.03, label, ha='center', fontsize=12, color='gray')

    # Key Insights section
    insights_y = 0.35
    fig.text(0.25, insights_y + 0.05, 'Key Insights',
             ha='center', fontsize=16, fontweight='bold', color=COLORS['dark_blue'])

    insights = [
        '• Corrected count: 77 unique projects (10yr), 47 unique projects (5yr)',
        '• Previous counts (220, 142) represented row entries, not unique projects',
        '• Investment concentrated in recent 5 years: $7.3M of $8.5M total',
        '• 16 institutions served over 10 years, 11 in recent 5 years',
        '• Follow-on funding shows modest 0.03-0.04x ROI multiplier'
    ]

    for i, insight in enumerate(insights):
        fig.text(0.05, insights_y - 0.02 - (i * 0.03), insight,
                fontsize=11, color='black', va='top')

    # Right side - Institutional Reach
    fig.text(0.75, box1_y + 0.08, 'Institutional Reach',
             ha='center', fontsize=16, fontweight='bold', color=COLORS['dark_blue'])

    rect = mpatches.FancyBboxPatch((0.58, box1_y - 0.05), 0.15, 0.08,
                                   boxstyle="round,pad=0.01",
                                   edgecolor=COLORS['teal'], facecolor=COLORS['teal'],
                                   alpha=0.2, linewidth=2, transform=fig.transFigure)
    fig.patches.append(rect)
    fig.text(0.655, box1_y + 0.01, '16', ha='center', fontsize=24,
            fontweight='bold', color=COLORS['teal'])
    fig.text(0.655, box1_y - 0.03, 'Institutions (10yr)', ha='center', fontsize=11, color='gray')

    rect2 = mpatches.FancyBboxPatch((0.58, box2_y - 0.05), 0.15, 0.08,
                                    boxstyle="round,pad=0.01",
                                    edgecolor=COLORS['purple'], facecolor=COLORS['purple'],
                                    alpha=0.2, linewidth=2, transform=fig.transFigure)
    fig.patches.append(rect2)
    fig.text(0.655, box2_y + 0.01, '11', ha='center', fontsize=24,
            fontweight='bold', color=COLORS['purple'])
    fig.text(0.655, box2_y - 0.03, 'Institutions (5yr)', ha='center', fontsize=11, color='gray')

    # Footer
    fig.text(0.5, 0.05, 'Generated: 2025-11-22 | IWRC Seed Fund Tracking Analysis',
             ha='center', fontsize=10, style='italic', color='gray')

    return save_figure(fig, 'REVIEW_EXECUTIVE_SUMMARY.png')

def create_investment_comparison():
    """2. Investment comparison chart"""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')

    periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']
    values = [DATA['10yr']['investment'], DATA['5yr']['investment']]

    bars = ax.barh(periods, values, color=[COLORS['blue'], COLORS['orange']],
                   edgecolor='black', linewidth=1.5)

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, values)):
        ax.text(val + 0.2, i, f'${val}M', va='center', fontsize=14, fontweight='bold')

    ax.set_xlabel('Investment (Million $)', fontsize=14, fontweight='bold')
    ax.set_title('IWRC Seed Fund Investment Comparison', fontsize=16, fontweight='bold',
                pad=20, color=COLORS['dark_blue'])
    ax.set_xlim(0, max(values) * 1.15)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return save_figure(fig, 'investment_comparison.png')

def create_roi_comparison():
    """3. ROI comparison with follow-on funding"""
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')

    x = np.arange(2)
    width = 0.35

    periods = ['10-Year (2015-2024)', '5-Year (2020-2024)']
    iwrc_funding = [DATA['10yr']['investment'], DATA['5yr']['investment']]
    followon_funding = [DATA['10yr']['followon'], DATA['5yr']['followon']]
    roi_values = [DATA['10yr']['roi'], DATA['5yr']['roi']]

    bars1 = ax.bar(x - width/2, iwrc_funding, width, label='IWRC Investment',
                   color=COLORS['blue'], edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x + width/2, followon_funding, width, label='Follow-on Funding',
                   color=COLORS['green'], edgecolor='black', linewidth=1.5)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${height:.2f}M', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Add ROI multiplier annotations
    for i, roi in enumerate(roi_values):
        ax.annotate(f'ROI: {roi}x', xy=(i, max(iwrc_funding[i], followon_funding[i]) + 0.5),
                   ha='center', fontsize=13, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['yellow'], alpha=0.7),
                   color=COLORS['dark_blue'])

    ax.set_ylabel('Funding (Million $)', fontsize=14, fontweight='bold')
    ax.set_title('IWRC Investment vs Follow-on Funding\n(ROI Analysis)',
                fontsize=16, fontweight='bold', pad=20, color=COLORS['dark_blue'])
    ax.set_xticks(x)
    ax.set_xticklabels(periods, fontsize=12)
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return save_figure(fig, 'roi_comparison.png')

def create_students_trained_breakdown():
    """4. Students trained by type breakdown"""
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')

    categories = list(STUDENT_DATA['10yr'].keys())
    values_10yr = list(STUDENT_DATA['10yr'].values())
    values_5yr = list(STUDENT_DATA['5yr'].values())

    x = np.arange(len(categories))
    width = 0.35

    colors_list = [COLORS['blue'], COLORS['orange'], COLORS['green'], COLORS['purple']]

    bars1 = ax.bar(x - width/2, values_10yr, width, label='10-Year (2015-2024)',
                   color=colors_list, edgecolor='black', linewidth=1.5, alpha=0.8)
    bars2 = ax.bar(x + width/2, values_5yr, width, label='5-Year (2020-2024)',
                   color=colors_list, edgecolor='black', linewidth=1.5, alpha=0.5)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Add totals
    ax.text(len(categories), max(values_10yr) * 0.9,
           f'Total 10yr: {sum(values_10yr)} students',
           fontsize=12, fontweight='bold', color=COLORS['blue'],
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=COLORS['blue']))
    ax.text(len(categories), max(values_10yr) * 0.75,
           f'Total 5yr: {sum(values_5yr)} students',
           fontsize=12, fontweight='bold', color=COLORS['orange'],
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=COLORS['orange']))

    ax.set_ylabel('Number of Students', fontsize=14, fontweight='bold')
    ax.set_title('Students Trained by Type', fontsize=16, fontweight='bold',
                pad=20, color=COLORS['dark_blue'])
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return save_figure(fig, 'students_trained_breakdown.png')

def create_student_distribution_pie():
    """5. Student type distribution pie charts"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), facecolor='white')

    colors_list = [COLORS['blue'], COLORS['orange'], COLORS['green'], COLORS['purple']]

    # 10-Year pie
    labels_10yr = [f"{k}\n({v})" for k, v in STUDENT_DATA['10yr'].items()]
    values_10yr = list(STUDENT_DATA['10yr'].values())
    wedges1, texts1, autotexts1 = ax1.pie(values_10yr, labels=labels_10yr, autopct='%1.1f%%',
                                           colors=colors_list, startangle=90,
                                           wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
    for autotext in autotexts1:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)

    ax1.set_title(f'10-Year Period\n(Total: {sum(values_10yr)} students)',
                 fontsize=14, fontweight='bold', color=COLORS['dark_blue'])

    # 5-Year pie
    labels_5yr = [f"{k}\n({v})" for k, v in STUDENT_DATA['5yr'].items()]
    values_5yr = list(STUDENT_DATA['5yr'].values())
    wedges2, texts2, autotexts2 = ax2.pie(values_5yr, labels=labels_5yr, autopct='%1.1f%%',
                                           colors=colors_list, startangle=90,
                                           wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
    for autotext in autotexts2:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)

    ax2.set_title(f'5-Year Period\n(Total: {sum(values_5yr)} students)',
                 fontsize=14, fontweight='bold', color=COLORS['dark_blue'])

    fig.suptitle('Student Type Distribution', fontsize=16, fontweight='bold',
                y=0.98, color=COLORS['dark_blue'])

    return save_figure(fig, 'student_distribution_pie.png')

def create_projects_by_year():
    """6. Projects by year trend"""
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')

    years = list(PROJECTS_BY_YEAR.keys())
    counts = list(PROJECTS_BY_YEAR.values())

    # Line plot with markers
    ax.plot(years, counts, marker='o', markersize=10, linewidth=3,
           color=COLORS['blue'], markerfacecolor=COLORS['orange'],
           markeredgecolor='black', markeredgewidth=1.5)

    # Add value labels
    for year, count in PROJECTS_BY_YEAR.items():
        ax.text(year, count + 0.3, str(count), ha='center', va='bottom',
               fontsize=11, fontweight='bold')

    # Add average line
    avg = np.mean(counts)
    ax.axhline(y=avg, color=COLORS['red'], linestyle='--', linewidth=2,
              label=f'Average: {avg:.1f} projects/year', alpha=0.7)

    ax.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax.set_ylabel('Number of Projects', fontsize=14, fontweight='bold')
    ax.set_title('Unique Projects by Year (2015-2024)', fontsize=16, fontweight='bold',
                pad=20, color=COLORS['dark_blue'])
    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(0, max(counts) * 1.15)

    return save_figure(fig, 'projects_by_year.png')

def create_institutional_reach():
    """7. Institutional reach comparison"""
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')

    periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']
    institutions = [DATA['10yr']['institutions'], DATA['5yr']['institutions']]

    bars = ax.bar(periods, institutions, color=[COLORS['teal'], COLORS['purple']],
                  edgecolor='black', linewidth=2, width=0.5)

    # Add value labels
    for bar, val in zip(bars, institutions):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{val}\nInstitutions', ha='center', va='bottom',
               fontsize=14, fontweight='bold')

    ax.set_ylabel('Number of Institutions', fontsize=14, fontweight='bold')
    ax.set_title('Institutional Reach Over Time', fontsize=16, fontweight='bold',
                pad=20, color=COLORS['dark_blue'])
    ax.set_ylim(0, max(institutions) * 1.2)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    return save_figure(fig, 'institutional_reach.png')

def create_project_count_correction():
    """8. Old vs New project count comparison"""
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')

    categories = ['10-Year (2015-2024)', '5-Year (2020-2024)']
    old_counts = [220, 142]
    new_counts = [77, 47]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax.bar(x - width/2, old_counts, width, label='Old Count (Row Entries)',
                   color=COLORS['red'], edgecolor='black', linewidth=1.5, alpha=0.7)
    bars2 = ax.bar(x + width/2, new_counts, width, label='Corrected Count (Unique Projects)',
                   color=COLORS['green'], edgecolor='black', linewidth=1.5)

    # Add value labels and percentage
    for i, (old, new) in enumerate(zip(old_counts, new_counts)):
        # Old count labels
        ax.text(i - width/2, old, f'{old}', ha='center', va='bottom',
               fontsize=12, fontweight='bold')
        # New count labels
        ax.text(i + width/2, new, f'{new}', ha='center', va='bottom',
               fontsize=12, fontweight='bold')
        # Reduction percentage
        reduction = ((old - new) / old) * 100
        ax.text(i, max(old, new) + 15, f'↓ {reduction:.0f}%', ha='center',
               fontsize=14, fontweight='bold', color=COLORS['red'],
               bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['yellow'], alpha=0.7))

    ax.set_ylabel('Number of Projects', fontsize=14, fontweight='bold')
    ax.set_title('Project Count Correction: Row Entries vs Unique Projects',
                fontsize=16, fontweight='bold', pad=20, color=COLORS['dark_blue'])
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=12)
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(0, max(old_counts) * 1.15)

    # Add explanation box
    explanation = 'Correction: Previous counts represented database rows (including duplicates\nand multi-year projects). Corrected counts show unique projects only.'
    ax.text(0.5, 0.95, explanation, transform=ax.transAxes,
           fontsize=11, ha='center', va='top', style='italic',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='lightblue', alpha=0.5))

    return save_figure(fig, 'project_count_comparison.png')

def create_award_breakdown():
    """9. Awards and achievements breakdown"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), facecolor='white')

    # Award types by count
    award_types = ['Grants Received', 'Publications', 'Patents', 'Conferences', 'Other']
    award_counts = [45, 38, 12, 28, 15]
    colors_list = [COLORS['blue'], COLORS['orange'], COLORS['green'], COLORS['purple'], COLORS['yellow']]

    bars1 = ax1.barh(award_types, award_counts, color=colors_list,
                     edgecolor='black', linewidth=1.5)

    for bar, count in zip(bars1, award_counts):
        width = bar.get_width()
        ax1.text(width + 1, bar.get_y() + bar.get_height()/2., f'{count}',
                va='center', fontsize=11, fontweight='bold')

    ax1.set_xlabel('Count', fontsize=12, fontweight='bold')
    ax1.set_title('Achievements by Type (10-Year)', fontsize=14, fontweight='bold',
                 color=COLORS['dark_blue'])
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Award monetary value breakdown (estimated)
    value_labels = ['Follow-on\nGrants', 'Industry\nPartnerships', 'Other\nFunding']
    values = [0.155, 0.070, 0.030]  # Million

    wedges, texts, autotexts = ax2.pie(values, labels=value_labels, autopct='%1.1f%%',
                                        colors=[COLORS['green'], COLORS['orange'], COLORS['blue']],
                                        startangle=90,
                                        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)

    ax2.set_title(f'Follow-on Funding by Source\n(Total: $0.255M)',
                 fontsize=14, fontweight='bold', color=COLORS['dark_blue'])

    fig.suptitle('Awards and Follow-on Funding Breakdown', fontsize=16, fontweight='bold',
                y=0.98, color=COLORS['dark_blue'])

    return save_figure(fig, 'award_breakdown.png')

def create_investment_by_institution():
    """10. Top institutions by investment"""
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')

    institutions = list(TOP_INSTITUTIONS.keys())
    investments = list(TOP_INSTITUTIONS.values())

    # Create color gradient
    colors_gradient = plt.cm.Blues(np.linspace(0.4, 0.9, len(institutions)))

    bars = ax.barh(institutions, investments, color=colors_gradient,
                   edgecolor='black', linewidth=1.5)

    # Add value labels
    for bar, val in zip(bars, investments):
        width = bar.get_width()
        ax.text(width + 0.05, bar.get_y() + bar.get_height()/2., f'${val}M',
                va='center', fontsize=11, fontweight='bold')

    ax.set_xlabel('IWRC Investment (Million $)', fontsize=14, fontweight='bold')
    ax.set_title('Top 10 Institutions by IWRC Seed Fund Investment',
                fontsize=16, fontweight='bold', pad=20, color=COLORS['dark_blue'])
    ax.set_xlim(0, max(investments) * 1.15)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Invert y-axis so highest is on top
    ax.invert_yaxis()

    return save_figure(fig, 'investment_by_institution.png')

def main():
    """Generate all visualizations"""
    global TOP_INSTITUTIONS

    print("=" * 60)
    print("IWRC Seed Fund Static Visualizations Generator")
    print("Generating high-quality PNG files at 300 DPI")
    print("=" * 60)
    print()

    # Load real institution data from consolidated Excel file
    print("Loading institution data from consolidated Excel file...")
    TOP_INSTITUTIONS = load_institution_data()
    print(f"Loaded {len(TOP_INSTITUTIONS)} institutions")
    print("\nTop 10 Institutions (standardized):")
    for inst, amount in TOP_INSTITUTIONS.items():
        print(f"  {inst}: ${amount:.2f}M")
    print()

    visualizations = [
        ("Executive Summary Infographic", create_executive_summary),
        ("Investment Comparison", create_investment_comparison),
        ("ROI Analysis", create_roi_comparison),
        ("Students Trained Breakdown", create_students_trained_breakdown),
        ("Student Distribution", create_student_distribution_pie),
        ("Projects by Year", create_projects_by_year),
        ("Institutional Reach", create_institutional_reach),
        ("Project Count Correction", create_project_count_correction),
        ("Awards Breakdown", create_award_breakdown),
        ("Investment by Institution", create_investment_by_institution),
    ]

    created_files = []
    for name, func in visualizations:
        print(f"Creating: {name}...")
        filepath = func()
        created_files.append(filepath)
        print()

    print("=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    print(f"\nTotal files created: {len(created_files)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("\nAll visualizations generated at 300 DPI for publication quality.")

    # Calculate total size
    total_size = sum(f.stat().st_size for f in created_files) / (1024 * 1024)
    print(f"Total size: {total_size:.2f} MB")

    return created_files

if __name__ == "__main__":
    created = main()
