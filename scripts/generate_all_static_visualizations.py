#!/usr/bin/env python3
"""
Generate all static visualization files for IWRC Seed Fund Analysis
Publication-ready PNG files at 300 DPI with corrected project counts
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import re
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set publication-ready style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Define paths
BASE_DIR = Path('/Users/shivpat/Downloads/Seed Fund Tracking')
DATA_FILE = BASE_DIR / 'data/consolidated/IWRC Seed Fund Tracking.xlsx'
OUTPUT_DIR = BASE_DIR / 'visualizations/static'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Color scheme
COLORS = {
    'blue': '#1f77b4',
    'orange': '#ff7f0e',
    'green': '#2ca02c',
    'red': '#d62728',
    'purple': '#9467bd',
    'brown': '#8c564b',
    'pink': '#e377c2',
    'gray': '#7f7f7f',
    'olive': '#bcbd22',
    'cyan': '#17becf'
}

# Load and prepare data
print("Loading data from Excel...")
df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')

# Column mapping - using actual column names from the Excel file
column_mapping = {
    'Project ID ': 'Project_ID',
    'Project Title': 'Project_Title',
    'Project PI': 'PI',
    'Academic Institution of PI': 'Institution',
    'Award Amount Allocated ($) this must be filled in for all lines': 'IWRC_Investment',
    'Number of PhD Students Supported by WRRA $': 'PhD_Students',
    'Number of MS Students Supported by WRRA $': 'Masters_Students',
    'Number of Undergraduate Students Supported by WRRA $': 'Undergraduate_Students',
    'Number of Post Docs Supported by WRRA $': 'Post_Doctoral_Students',
    'Monetary Benefit of Award or Achievement (if applicable; use NA if not applicable)': 'Follow_on_Funding'
}

df.rename(columns=column_mapping, inplace=True)

# Extract year from Project ID (format: 2015IL123B or similar)
def extract_year(project_id):
    if pd.isna(project_id):
        return None

    project_id_str = str(project_id).strip()

    # Try 4-digit year pattern
    year_match = re.search(r'(20\d{2}|19\d{2})', project_id_str)
    if year_match:
        return int(year_match.group(1))

    # Try FY format
    fy_match = re.search(r'FY(\d{2})', project_id_str, re.IGNORECASE)
    if fy_match:
        fy_year = int(fy_match.group(1))
        return 2000 + fy_year if fy_year < 100 else fy_year

    return None

df['Year'] = df['Project_ID'].apply(extract_year)
df = df[df['Year'].notna()]

# Clean numeric columns
numeric_cols = ['IWRC_Investment', 'Follow_on_Funding', 'PhD_Students',
                'Masters_Students', 'Undergraduate_Students', 'Post_Doctoral_Students']

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Add award/grant type column
award_grant_col = "Award, Achievement, or Grant\n (This may include awards and achievements for projects from the previous year to this 5-year cycle, so long as they were not already included in last year's report)"
if award_grant_col in df.columns:
    df['Award_Type_Cat'] = df[award_grant_col]
else:
    df['Award_Type_Cat'] = None

# Filter time periods
df_10yr = df[df['Year'].between(2015, 2024)].copy()
df_5yr = df[df['Year'].between(2020, 2024)].copy()

# Calculate key metrics
# Count awards by type
def count_awards_by_type(df_subset):
    """Count grants, awards, and achievements from Award_Type_Cat column."""
    counts = {'grants': 0, 'awards': 0, 'achievements': 0, 'other': 0}

    for val in df_subset['Award_Type_Cat'].dropna():
        val_lower = str(val).lower()
        if 'grant' in val_lower:
            counts['grants'] += 1
        elif 'award' in val_lower:
            counts['awards'] += 1
        elif 'achievement' in val_lower:
            counts['achievements'] += 1
        else:
            counts['other'] += 1

    return counts

# Helper function to extract monetary values from text
def clean_monetary_value(value):
    """Extract numeric dollar amounts from text."""
    if pd.isna(value):
        return 0.0
    value_str = str(value).strip().upper()
    if value_str in ['NA', 'N/A', 'NONE', '']:
        return 0.0
    dollar_pattern = r'\$?\s*([\d,]+(?:\.\d{2})?)'
    matches = re.findall(dollar_pattern, value_str)
    if matches:
        total = 0.0
        for match in matches:
            try:
                amount = float(match.replace(',', ''))
                total += amount
            except (ValueError, TypeError):
                continue
        return total if total > 0 else 0.0
    return 0.0

# Add description column for monetary extraction
desc_col = "Description of Award, Achievement, or Grant\n (This may include awards and achievements for projects from the previous year to this 5-year cycle, so long as they were not already included in last year's report)"
if desc_col in df.columns:
    df['Award_Description'] = df[desc_col]
else:
    df['Award_Description'] = None

# Re-filter after adding new column
df_10yr = df[df['Year'].between(2015, 2024)].copy()
df_5yr = df[df['Year'].between(2020, 2024)].copy()

# Extract follow-on funding from multiple sources
def extract_follow_on_funding(row):
    """Extract follow-on funding from all available columns."""
    # Check monetary benefit column
    if pd.notna(row['Follow_on_Funding']):
        amount = clean_monetary_value(row['Follow_on_Funding'])
        if amount > 0:
            return amount
    # Check award description
    if pd.notna(row.get('Award_Description')):
        amount = clean_monetary_value(row['Award_Description'])
        if amount > 0:
            return amount
    # Check award type column
    if pd.notna(row.get('Award_Type_Cat')):
        amount = clean_monetary_value(row['Award_Type_Cat'])
        if amount > 0:
            return amount
    return 0.0

df_10yr['Follow_on_Funding_Clean'] = df_10yr.apply(extract_follow_on_funding, axis=1)
df_5yr['Follow_on_Funding_Clean'] = df_5yr.apply(extract_follow_on_funding, axis=1)

awards_10yr = count_awards_by_type(df_10yr)
awards_5yr = count_awards_by_type(df_5yr)

metrics_10yr = {
    'projects': df_10yr['Project_ID'].nunique(),
    'investment': df_10yr['IWRC_Investment'].sum(),
    'follow_on': df_10yr['Follow_on_Funding_Clean'].sum(),
    'students': int(df_10yr[['PhD_Students', 'Masters_Students', 'Undergraduate_Students', 'Post_Doctoral_Students']].sum().sum()),
    'institutions': df_10yr['Institution'].nunique(),
    'phd': int(df_10yr['PhD_Students'].sum()),
    'masters': int(df_10yr['Masters_Students'].sum()),
    'undergrad': int(df_10yr['Undergraduate_Students'].sum()),
    'postdoc': int(df_10yr['Post_Doctoral_Students'].sum()),
    'grants': awards_10yr['grants'],
    'awards': awards_10yr['awards'],
    'achievements': awards_10yr['achievements'],
    'other': awards_10yr['other']
}
metrics_10yr['roi'] = metrics_10yr['follow_on'] / metrics_10yr['investment'] if metrics_10yr['investment'] > 0 else 0

metrics_5yr = {
    'projects': df_5yr['Project_ID'].nunique(),
    'investment': df_5yr['IWRC_Investment'].sum(),
    'follow_on': df_5yr['Follow_on_Funding_Clean'].sum(),
    'students': int(df_5yr[['PhD_Students', 'Masters_Students', 'Undergraduate_Students', 'Post_Doctoral_Students']].sum().sum()),
    'institutions': df_5yr['Institution'].nunique(),
    'phd': int(df_5yr['PhD_Students'].sum()),
    'masters': int(df_5yr['Masters_Students'].sum()),
    'undergrad': int(df_5yr['Undergraduate_Students'].sum()),
    'postdoc': int(df_5yr['Post_Doctoral_Students'].sum()),
    'grants': awards_5yr['grants'],
    'awards': awards_5yr['awards'],
    'achievements': awards_5yr['achievements'],
    'other': awards_5yr['other']
}
metrics_5yr['roi'] = metrics_5yr['follow_on'] / metrics_5yr['investment'] if metrics_5yr['investment'] > 0 else 0

print(f"\n10-Year Metrics (2015-2024):")
print(f"  Projects: {metrics_10yr['projects']}")
print(f"  Investment: ${metrics_10yr['investment']/1e6:.1f}M")
print(f"  Students: {metrics_10yr['students']}")
print(f"  ROI: {metrics_10yr['roi']:.2f}x")

print(f"\n5-Year Metrics (2020-2024):")
print(f"  Projects: {metrics_5yr['projects']}")
print(f"  Investment: ${metrics_5yr['investment']/1e6:.1f}M")
print(f"  Students: {metrics_5yr['students']}")
print(f"  ROI: {metrics_5yr['roi']:.2f}x")

# ==============================================================================
# 1. EXECUTIVE SUMMARY
# ==============================================================================
print("\n\nGenerating 1/10: REVIEW_EXECUTIVE_SUMMARY.png...")

fig = plt.figure(figsize=(14, 10), dpi=300)
fig.patch.set_facecolor('white')

# Title
fig.text(0.5, 0.95, 'IWRC Seed Fund Analysis - Executive Summary',
         ha='center', va='top', fontsize=18, fontweight='bold')

# Create grid for layout
gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3,
                      left=0.1, right=0.9, top=0.88, bottom=0.08)

# 10-Year Section (Left)
ax1 = fig.add_subplot(gs[0:2, 0])
ax1.axis('off')
ax1.text(0.5, 0.95, '10-Year Period (2015-2024)',
         ha='center', va='top', fontsize=16, fontweight='bold',
         transform=ax1.transAxes)

# Metric boxes for 10-year
metrics_10_display = [
    ('Projects', metrics_10yr['projects'], COLORS['blue']),
    ('Investment', f"${metrics_10yr['investment']/1e6:.1f}M", COLORS['orange']),
    ('Students', metrics_10yr['students'], COLORS['green']),
    ('ROI', f"{metrics_10yr['roi']:.2f}x", COLORS['red'])
]

y_pos = 0.75
for label, value, color in metrics_10_display:
    # Box
    rect = mpatches.FancyBboxPatch((0.1, y_pos-0.08), 0.8, 0.12,
                                    boxstyle="round,pad=0.01",
                                    linewidth=2, edgecolor=color,
                                    facecolor=color, alpha=0.15,
                                    transform=ax1.transAxes)
    ax1.add_patch(rect)

    # Label and value
    ax1.text(0.15, y_pos, label, ha='left', va='center',
             fontsize=12, fontweight='bold', transform=ax1.transAxes)
    ax1.text(0.85, y_pos, str(value), ha='right', va='center',
             fontsize=14, fontweight='bold', color=color, transform=ax1.transAxes)
    y_pos -= 0.18

# Institutions count
ax1.text(0.5, 0.05, f'Institutions Served: {metrics_10yr["institutions"]}',
         ha='center', va='center', fontsize=11, style='italic',
         transform=ax1.transAxes)

# 5-Year Section (Right)
ax2 = fig.add_subplot(gs[0:2, 1])
ax2.axis('off')
ax2.text(0.5, 0.95, '5-Year Period (2020-2024)',
         ha='center', va='top', fontsize=16, fontweight='bold',
         transform=ax2.transAxes)

# Metric boxes for 5-year
metrics_5_display = [
    ('Projects', metrics_5yr['projects'], COLORS['blue']),
    ('Investment', f"${metrics_5yr['investment']/1e6:.1f}M", COLORS['orange']),
    ('Students', metrics_5yr['students'], COLORS['green']),
    ('ROI', f"{metrics_5yr['roi']:.2f}x", COLORS['red'])
]

y_pos = 0.75
for label, value, color in metrics_5_display:
    # Box
    rect = mpatches.FancyBboxPatch((0.1, y_pos-0.08), 0.8, 0.12,
                                    boxstyle="round,pad=0.01",
                                    linewidth=2, edgecolor=color,
                                    facecolor=color, alpha=0.15,
                                    transform=ax2.transAxes)
    ax2.add_patch(rect)

    # Label and value
    ax2.text(0.15, y_pos, label, ha='left', va='center',
             fontsize=12, fontweight='bold', transform=ax2.transAxes)
    ax2.text(0.85, y_pos, str(value), ha='right', va='center',
             fontsize=14, fontweight='bold', color=color, transform=ax2.transAxes)
    y_pos -= 0.18

# Institutions count
ax2.text(0.5, 0.05, f'Institutions Served: {metrics_5yr["institutions"]}',
         ha='center', va='center', fontsize=11, style='italic',
         transform=ax2.transAxes)

# Bottom section - Project count correction
ax3 = fig.add_subplot(gs[2, :])
ax3.axis('off')
ax3.text(0.5, 0.9, 'Project Count Correction: Row Count vs Unique Project IDs',
         ha='center', va='top', fontsize=14, fontweight='bold',
         transform=ax3.transAxes)

# Correction bars
bar_width = 0.15
x_10yr = 0.25
x_5yr = 0.65

# 10-year correction
rect_old_10 = mpatches.FancyBboxPatch((x_10yr-bar_width/2, 0.3), bar_width, 0.35,
                                       linewidth=2, edgecolor=COLORS['red'],
                                       facecolor=COLORS['red'], alpha=0.3,
                                       transform=ax3.transAxes)
ax3.add_patch(rect_old_10)
ax3.text(x_10yr, 0.7, '220', ha='center', va='bottom', fontsize=12,
         fontweight='bold', color=COLORS['red'], transform=ax3.transAxes)
ax3.text(x_10yr, 0.25, 'Old Count', ha='center', va='top', fontsize=10,
         transform=ax3.transAxes)

rect_new_10 = mpatches.FancyBboxPatch((x_10yr+bar_width*0.7, 0.3), bar_width, 0.35,
                                       linewidth=2, edgecolor=COLORS['green'],
                                       facecolor=COLORS['green'], alpha=0.3,
                                       transform=ax3.transAxes)
ax3.add_patch(rect_new_10)
ax3.text(x_10yr+bar_width*0.7+bar_width/2, 0.7, '77', ha='center', va='bottom',
         fontsize=12, fontweight='bold', color=COLORS['green'], transform=ax3.transAxes)
ax3.text(x_10yr+bar_width*0.7+bar_width/2, 0.25, 'Corrected', ha='center', va='top',
         fontsize=10, transform=ax3.transAxes)

ax3.text(x_10yr+bar_width*0.7/2, 0.15, '10-Year: 65% reduction',
         ha='center', va='top', fontsize=11, style='italic',
         transform=ax3.transAxes)

# 5-year correction
rect_old_5 = mpatches.FancyBboxPatch((x_5yr-bar_width/2, 0.3), bar_width, 0.35,
                                      linewidth=2, edgecolor=COLORS['red'],
                                      facecolor=COLORS['red'], alpha=0.3,
                                      transform=ax3.transAxes)
ax3.add_patch(rect_old_5)
ax3.text(x_5yr, 0.7, '142', ha='center', va='bottom', fontsize=12,
         fontweight='bold', color=COLORS['red'], transform=ax3.transAxes)
ax3.text(x_5yr, 0.25, 'Old Count', ha='center', va='top', fontsize=10,
         transform=ax3.transAxes)

rect_new_5 = mpatches.FancyBboxPatch((x_5yr+bar_width*0.7, 0.3), bar_width, 0.35,
                                      linewidth=2, edgecolor=COLORS['green'],
                                      facecolor=COLORS['green'], alpha=0.3,
                                      transform=ax3.transAxes)
ax3.add_patch(rect_new_5)
ax3.text(x_5yr+bar_width*0.7+bar_width/2, 0.7, '47', ha='center', va='bottom',
         fontsize=12, fontweight='bold', color=COLORS['green'], transform=ax3.transAxes)
ax3.text(x_5yr+bar_width*0.7+bar_width/2, 0.25, 'Corrected', ha='center', va='top',
         fontsize=10, transform=ax3.transAxes)

ax3.text(x_5yr+bar_width*0.7/2, 0.15, '5-Year: 67% reduction',
         ha='center', va='top', fontsize=11, style='italic',
         transform=ax3.transAxes)

plt.savefig(OUTPUT_DIR / 'REVIEW_EXECUTIVE_SUMMARY.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

# ==============================================================================
# 2. INVESTMENT COMPARISON
# ==============================================================================
print("Generating 2/10: investment_comparison.png...")

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
fig.patch.set_facecolor('white')

periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']
investments = [metrics_10yr['investment']/1e6, metrics_5yr['investment']/1e6]

bars = ax.barh(periods, investments, color=[COLORS['blue'], COLORS['orange']], alpha=0.7)

# Value labels
for i, (bar, inv) in enumerate(zip(bars, investments)):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
            f'${inv:.1f}M', va='center', fontsize=12, fontweight='bold')

ax.set_xlabel('Investment (Millions USD)', fontsize=12, fontweight='bold')
ax.set_title('IWRC Seed Fund Investment by Period', fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)
ax.set_xlim(0, max(investments) * 1.2)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'investment_comparison.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

# ==============================================================================
# 3. ROI COMPARISON
# ==============================================================================
print("Generating 3/10: roi_comparison.png...")

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
fig.patch.set_facecolor('white')

x = np.arange(2)
width = 0.35

iwrc_values = [metrics_10yr['investment']/1e6, metrics_5yr['investment']/1e6]
follow_on_values = [metrics_10yr['follow_on']/1e6, metrics_5yr['follow_on']/1e6]
roi_values = [metrics_10yr['roi'], metrics_5yr['roi']]

bars1 = ax.bar(x - width/2, iwrc_values, width, label='IWRC Investment',
               color=COLORS['blue'], alpha=0.7)
bars2 = ax.bar(x + width/2, follow_on_values, width, label='Follow-on Funding',
               color=COLORS['green'], alpha=0.7)

# Value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.1,
                f'${height:.1f}M', ha='center', va='bottom', fontsize=10, fontweight='bold')

# ROI annotations above bars
for i, roi in enumerate(roi_values):
    ax.text(i, max(iwrc_values[i], follow_on_values[i]) + 0.5,
            f'ROI: {roi:.2f}x', ha='center', va='bottom',
            fontsize=11, fontweight='bold', color=COLORS['red'])

ax.set_ylabel('Funding (Millions USD)', fontsize=12, fontweight='bold')
ax.set_title('Return on Investment (ROI) Analysis', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(['10-Year\n(2015-2024)', '5-Year\n(2020-2024)'])
ax.legend(loc='upper left', fontsize=11)
ax.grid(axis='y', alpha=0.3)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'roi_comparison.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

# ==============================================================================
# 4. STUDENTS TRAINED
# ==============================================================================
print("Generating 4/10: students_trained.png...")

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
fig.patch.set_facecolor('white')

categories = ['PhD', "Master's", 'Undergraduate', 'Post-Doctoral']
x = np.arange(len(categories))
width = 0.35

values_10yr = [metrics_10yr['phd'], metrics_10yr['masters'],
               metrics_10yr['undergrad'], metrics_10yr['postdoc']]
values_5yr = [metrics_5yr['phd'], metrics_5yr['masters'],
              metrics_5yr['undergrad'], metrics_5yr['postdoc']]

bars1 = ax.bar(x - width/2, values_10yr, width, label='10-Year (2015-2024)',
               color=COLORS['blue'], alpha=0.7)
bars2 = ax.bar(x + width/2, values_5yr, width, label='5-Year (2020-2024)',
               color=COLORS['orange'], alpha=0.7)

# Value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2, height + 2,
                    f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Total labels
ax.text(-width/2, max(values_10yr) + 15, f'Total: {metrics_10yr["students"]}',
        ha='center', va='bottom', fontsize=11, fontweight='bold', color=COLORS['blue'])
ax.text(len(categories) - 1 + width/2, max(values_5yr) + 15,
        f'Total: {metrics_5yr["students"]}',
        ha='center', va='bottom', fontsize=11, fontweight='bold', color=COLORS['orange'])

ax.set_ylabel('Number of Students', fontsize=12, fontweight='bold')
ax.set_title('Students Trained by Type and Period', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend(loc='upper right', fontsize=11)
ax.grid(axis='y', alpha=0.3)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'students_trained.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

# ==============================================================================
# 5. STUDENT DISTRIBUTION PIE
# ==============================================================================
print("Generating 5/10: student_distribution_pie.png...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
fig.patch.set_facecolor('white')

# 10-Year pie
sizes_10yr = [metrics_10yr['phd'], metrics_10yr['masters'],
              metrics_10yr['undergrad'], metrics_10yr['postdoc']]
labels = ['PhD', "Master's", 'Undergraduate', 'Post-Doctoral']
colors_pie = [COLORS['blue'], COLORS['orange'], COLORS['green'], COLORS['purple']]

# Filter out zero values
sizes_10yr_filtered = []
labels_10yr_filtered = []
colors_10yr_filtered = []
for size, label, color in zip(sizes_10yr, labels, colors_pie):
    if size > 0:
        sizes_10yr_filtered.append(size)
        labels_10yr_filtered.append(label)
        colors_10yr_filtered.append(color)

wedges1, texts1, autotexts1 = ax1.pie(sizes_10yr_filtered, labels=None, autopct='%1.1f%%',
                                        colors=colors_10yr_filtered, startangle=90,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'})
ax1.set_title('10-Year Period (2015-2024)\nTotal Students: 304',
              fontsize=13, fontweight='bold', pad=15)

# Legend with counts
legend_labels_10 = [f'{label}: {int(size)}' for label, size in zip(labels_10yr_filtered, sizes_10yr_filtered)]
ax1.legend(legend_labels_10, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)

# 5-Year pie
sizes_5yr = [metrics_5yr['phd'], metrics_5yr['masters'],
             metrics_5yr['undergrad'], metrics_5yr['postdoc']]

# Filter out zero values
sizes_5yr_filtered = []
labels_5yr_filtered = []
colors_5yr_filtered = []
for size, label, color in zip(sizes_5yr, labels, colors_pie):
    if size > 0:
        sizes_5yr_filtered.append(size)
        labels_5yr_filtered.append(label)
        colors_5yr_filtered.append(color)

wedges2, texts2, autotexts2 = ax2.pie(sizes_5yr_filtered, labels=None, autopct='%1.1f%%',
                                        colors=colors_5yr_filtered, startangle=90,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'})
ax2.set_title('5-Year Period (2020-2024)\nTotal Students: 186',
              fontsize=13, fontweight='bold', pad=15)

# Legend with counts
legend_labels_5 = [f'{label}: {int(size)}' for label, size in zip(labels_5yr_filtered, sizes_5yr_filtered)]
ax2.legend(legend_labels_5, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)

plt.suptitle('Student Distribution by Type', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'student_distribution_pie.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

# ==============================================================================
# 6. PROJECTS BY YEAR
# ==============================================================================
print("Generating 6/10: projects_by_year.png...")

# Count unique projects per year
projects_by_year_10 = df_10yr.groupby('Year')['Project_ID'].nunique().sort_index()
projects_by_year_5 = df_5yr.groupby('Year')['Project_ID'].nunique().sort_index()

fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
fig.patch.set_facecolor('white')

# Plot lines
ax.plot(projects_by_year_10.index, projects_by_year_10.values,
        marker='o', linewidth=2, markersize=8, label='10-Year (2015-2024)',
        color=COLORS['blue'], alpha=0.7)
ax.plot(projects_by_year_5.index, projects_by_year_5.values,
        marker='s', linewidth=2, markersize=8, label='5-Year (2020-2024)',
        color=COLORS['orange'], alpha=0.7)

# Value labels
for year, count in projects_by_year_10.items():
    ax.text(year, count + 0.3, str(int(count)), ha='center', va='bottom',
            fontsize=9, fontweight='bold', color=COLORS['blue'])

for year, count in projects_by_year_5.items():
    ax.text(year, count - 0.3, str(int(count)), ha='center', va='top',
            fontsize=9, fontweight='bold', color=COLORS['orange'])

ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Unique Projects', fontsize=12, fontweight='bold')
ax.set_title('Unique Project Count Trend Over Time', fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper left', fontsize=11)
ax.grid(alpha=0.3)
ax.set_xticks(range(2015, 2025))

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'projects_by_year.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

# ==============================================================================
# 7. INSTITUTIONAL REACH
# ==============================================================================
print("Generating 7/10: institutional_reach.png...")

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
fig.patch.set_facecolor('white')

periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']
institutions = [metrics_10yr['institutions'], metrics_5yr['institutions']]

bars = ax.barh(periods, institutions, color=[COLORS['purple'], COLORS['cyan']], alpha=0.7)

# Value labels
for bar, inst in zip(bars, institutions):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            str(int(inst)), va='center', fontsize=12, fontweight='bold')

ax.set_xlabel('Number of Institutions', fontsize=12, fontweight='bold')
ax.set_title('Institutional Reach by Period', fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)
ax.set_xlim(0, max(institutions) * 1.2)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'institutional_reach.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

# ==============================================================================
# 8. AWARD BREAKDOWN
# ==============================================================================
print("Generating 8/10: award_breakdown.png...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
fig.patch.set_facecolor('white')

# 10-Year breakdown
categories_10 = ['Grants', 'Awards', 'Achievements', 'Other']
sizes_10 = [metrics_10yr['grants'], metrics_10yr['awards'],
            metrics_10yr['achievements'], metrics_10yr['other']]
colors_award = [COLORS['blue'], COLORS['green'], COLORS['orange'], COLORS['gray']]

# Filter non-zero values
sizes_10_filtered = []
categories_10_filtered = []
colors_10_filtered = []
for size, cat, color in zip(sizes_10, categories_10, colors_award):
    if size > 0:
        sizes_10_filtered.append(size)
        categories_10_filtered.append(cat)
        colors_10_filtered.append(color)

if sizes_10_filtered:
    wedges1, texts1, autotexts1 = ax1.pie(sizes_10_filtered, labels=None, autopct='%1.1f%%',
                                            colors=colors_10_filtered, startangle=90,
                                            textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax1.set_title(f'10-Year Period (2015-2024)\nTotal: {sum(sizes_10_filtered):.0f}',
                  fontsize=13, fontweight='bold', pad=15)
    legend_labels = [f'{cat}: {int(size)}' for cat, size in zip(categories_10_filtered, sizes_10_filtered)]
    ax1.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
else:
    ax1.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=14, transform=ax1.transAxes)
    ax1.set_title('10-Year Period (2015-2024)', fontsize=13, fontweight='bold', pad=15)

# 5-Year breakdown
sizes_5 = [metrics_5yr['grants'], metrics_5yr['awards'],
           metrics_5yr['achievements'], metrics_5yr['other']]

# Filter non-zero values
sizes_5_filtered = []
categories_5_filtered = []
colors_5_filtered = []
for size, cat, color in zip(sizes_5, categories_10, colors_award):
    if size > 0:
        sizes_5_filtered.append(size)
        categories_5_filtered.append(cat)
        colors_5_filtered.append(color)

if sizes_5_filtered:
    wedges2, texts2, autotexts2 = ax2.pie(sizes_5_filtered, labels=None, autopct='%1.1f%%',
                                            colors=colors_5_filtered, startangle=90,
                                            textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax2.set_title(f'5-Year Period (2020-2024)\nTotal: {sum(sizes_5_filtered):.0f}',
                  fontsize=13, fontweight='bold', pad=15)
    legend_labels = [f'{cat}: {int(size)}' for cat, size in zip(categories_5_filtered, sizes_5_filtered)]
    ax2.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
else:
    ax2.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=14, transform=ax2.transAxes)
    ax2.set_title('5-Year Period (2020-2024)', fontsize=13, fontweight='bold', pad=15)

plt.suptitle('Grants, Awards, and Achievements Distribution', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'award_breakdown.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

# ==============================================================================
# 9. TOP INSTITUTIONS
# ==============================================================================
print("Generating 9/10: top_institutions.png...")

# Get top 10 institutions by funding (10-year period)
institution_funding = df_10yr.groupby('Institution')['IWRC_Investment'].sum().sort_values(ascending=True).tail(10)

fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
fig.patch.set_facecolor('white')

bars = ax.barh(range(len(institution_funding)), institution_funding.values/1e6,
               color=COLORS['blue'], alpha=0.7)

# Value labels
for i, (bar, value) in enumerate(zip(bars, institution_funding.values/1e6)):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
            f'${value:.2f}M', va='center', fontsize=10, fontweight='bold')

ax.set_yticks(range(len(institution_funding)))
ax.set_yticklabels(institution_funding.index, fontsize=10)
ax.set_xlabel('IWRC Investment (Millions USD)', fontsize=12, fontweight='bold')
ax.set_title('Top 10 Institutions by IWRC Funding (2015-2024)', fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='x', alpha=0.3)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'top_institutions.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

# ==============================================================================
# 10. PROJECT COUNT CORRECTION
# ==============================================================================
print("Generating 10/10: project_count_correction.png...")

fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
fig.patch.set_facecolor('white')

# Data
old_counts = [220, 142]
new_counts = [77, 47]
periods = ['10-Year (2015-2024)', '5-Year (2020-2024)']
reductions = [(old-new)/old*100 for old, new in zip(old_counts, new_counts)]

x = np.arange(len(periods))
width = 0.35

bars1 = ax.bar(x - width/2, old_counts, width, label='Old Count (Row Count)',
               color=COLORS['red'], alpha=0.6)
bars2 = ax.bar(x + width/2, new_counts, width, label='Corrected (Unique Project IDs)',
               color=COLORS['green'], alpha=0.6)

# Value labels on bars
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 5,
            f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold',
            color=COLORS['red'])

for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 5,
            f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold',
            color=COLORS['green'])

# Reduction percentage labels
for i, reduction in enumerate(reductions):
    ax.text(i, max(old_counts[i], new_counts[i]) + 15,
            f'{reduction:.0f}% reduction', ha='center', va='bottom',
            fontsize=11, fontweight='bold', style='italic', color='black')

ax.set_ylabel('Number of Projects', fontsize=12, fontweight='bold')
ax.set_title('Project Count Correction: Row Count vs Unique Project IDs',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(periods)
ax.legend(loc='upper right', fontsize=11)
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, max(old_counts) * 1.15)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'project_count_correction.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

# ==============================================================================
# GENERATE SUMMARY REPORT
# ==============================================================================
print("\n" + "="*80)
print("VISUALIZATION GENERATION COMPLETE")
print("="*80)

import os

file_info = []
for filename in sorted(OUTPUT_DIR.glob('*.png')):
    if filename.name.startswith('.'):
        continue
    size_kb = filename.stat().st_size / 1024
    file_info.append((filename.name, size_kb))

print(f"\nGenerated {len(file_info)} visualization files in:")
print(f"  {OUTPUT_DIR}")
print(f"\nFiles created:")
for name, size in file_info:
    print(f"  - {name:45s} ({size:7.1f} KB)")

print(f"\nTotal size: {sum(s for _, s in file_info):.1f} KB")
print(f"\nAll files generated at 300 DPI with publication-ready quality.")
print("\n" + "="*80)
