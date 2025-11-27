#!/usr/bin/env python3
"""
Convert interactive HTML visualizations to static PNG images.
Uses plotly to render HTML charts as static images.
"""

import os
import sys
import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Try to import plotly for HTML rendering
try:
    import plotly.io as pio
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("⚠ Warning: plotly not available, will use kaleido fallback")

# Try to import kaleido for HTML rendering
try:
    import kaleido
    KALEIDO_AVAILABLE = True
except ImportError:
    KALEIDO_AVAILABLE = False

print("=" * 80)
print("CONVERT INTERACTIVE VISUALIZATIONS TO STATIC PNG")
print("=" * 80)

# Define paths
BASE_PATH = Path('/Users/shivpat/seed-fund-tracking')
INTERACTIVE_DIR = BASE_PATH / 'visualizations' / 'interactive'
STATIC_VERSION_DIR = INTERACTIVE_DIR / 'static_versions'

# Create output directory
STATIC_VERSION_DIR.mkdir(parents=True, exist_ok=True)
print(f'\n✓ Output directory: {STATIC_VERSION_DIR}')

# Load data for regenerating visualizations from scratch
print('\n📊 Loading data for visualization regeneration...')
consolidated_file = BASE_PATH / 'data' / 'consolidated' / 'IWRC Seed Fund Tracking.xlsx'
df = pd.read_excel(consolidated_file, sheet_name='Project Overview')

# Column mapping
col_map = {
    'Project ID ': 'project_id',
    'Award Type': 'award_type',
    'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount',
    'Number of Undergraduate Students Supported by WRRA $': 'undergrad_students',
    'Number of MS Students Supported by WRRA $': 'grad_students',
    'Number of PhD Students Supported by WRRA $': 'phd_students',
    'Academic Institution of PI': 'institution',
    'Project PI': 'pi_name',
    'PI Email': 'pi_email',
}

# Rename columns
for old, new in col_map.items():
    if old in df.columns:
        df.rename(columns={old: new}, inplace=True)

# Create combined grad students column (MS + PhD)
if 'grad_students' in df.columns and 'phd_students' in df.columns:
    df['grad_students'] = pd.to_numeric(df['grad_students'], errors='coerce').fillna(0) + pd.to_numeric(df['phd_students'], errors='coerce').fillna(0)
    df.drop('phd_students', axis=1, inplace=True)

print(f'✓ Data loaded: {len(df)} rows')

# Helper function to extract year from project ID
def extract_year_from_project_id(project_id):
    import re
    if pd.isna(project_id):
        return None
    project_id_str = str(project_id).strip()
    year_match = re.search(r'(20\d{2}|19\d{2})', project_id_str)
    if year_match:
        return int(year_match.group(1))
    fy_match = re.search(r'FY(\d{2})', project_id_str, re.IGNORECASE)
    if fy_match:
        fy_year = int(fy_match.group(1))
        return 2000 + fy_year if fy_year < 100 else fy_year
    return None

df['year'] = df['project_id'].apply(extract_year_from_project_id)
df['award_amount'] = pd.to_numeric(df['award_amount'], errors='coerce')
df['undergrad_students'] = pd.to_numeric(df['undergrad_students'], errors='coerce').fillna(0)
df['grad_students'] = pd.to_numeric(df['grad_students'], errors='coerce').fillna(0)
# HS students not tracked in this dataset, but keep for compatibility
if 'hs_students' not in df.columns:
    df['hs_students'] = 0
else:
    df['hs_students'] = pd.to_numeric(df['hs_students'], errors='coerce').fillna(0)

# Setup matplotlib style
sns.set_style('whitegrid')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['font.size'] = 10

COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'accent': '#d62728',
    'purple': '#9467bd',
    'brown': '#8c564b',
    'pink': '#e377c2'
}

# Add award category before filtering
def categorize_award_type(award_type):
    if pd.isna(award_type):
        return None
    award_str = str(award_type).lower().strip()
    if '104g' in award_str:
        if 'ais' in award_str:
            return '104g-AIS'
        elif 'pfas' in award_str:
            return '104g-PFAS'
        else:
            return '104g-General'
    elif '104b' in award_str:
        return '104b'
    elif 'coordination' in award_str:
        return 'Coordination'
    return None

df['award_category'] = df['award_type'].apply(categorize_award_type)

# ============================================================================
# STATIC VERSION 1: ROI Analysis Dashboard
# ============================================================================
print('\n📊 Creating static version: roi_analysis_dashboard.png')

df_10yr = df[df['year'] >= 2015].copy()
df_5yr = df[df['year'] >= 2020].copy()

num_projects_10yr = df_10yr['project_id'].nunique()
num_projects_5yr = df_5yr['project_id'].nunique()
total_investment_10yr = df_10yr['award_amount'].sum()
total_investment_5yr = df_5yr['award_amount'].sum()
students_10yr = (df_10yr['undergrad_students'] + df_10yr['grad_students'] + df_10yr['hs_students']).sum()
students_5yr = (df_5yr['undergrad_students'] + df_5yr['grad_students'] + df_5yr['hs_students']).sum()

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('IWRC Seed Fund ROI Analysis - Summary Metrics', fontsize=16, fontweight='bold', y=0.98)

# 1. Projects comparison
ax = axes[0, 0]
periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']
projects = [num_projects_10yr, num_projects_5yr]
bars = ax.bar(periods, projects, color=[COLORS['primary'], COLORS['secondary']], alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Number of Projects', fontweight='bold')
ax.set_title('Project Count', fontweight='bold', fontsize=12)
ax.set_ylim(0, max(projects) * 1.2)
for bar, val in zip(bars, projects):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(val)}', ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.grid(axis='y', alpha=0.3)

# 2. Investment comparison
ax = axes[0, 1]
investments = [total_investment_10yr / 1e6, total_investment_5yr / 1e6]
bars = ax.bar(periods, investments, color=[COLORS['primary'], COLORS['secondary']], alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Investment ($ Millions)', fontweight='bold')
ax.set_title('Total Investment', fontweight='bold', fontsize=12)
ax.set_ylim(0, max(investments) * 1.2)
for bar, val in zip(bars, investments):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height, f'${val:.1f}M', ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.grid(axis='y', alpha=0.3)

# 3. Students comparison
ax = axes[0, 2]
student_counts = [students_10yr, students_5yr]
bars = ax.bar(periods, student_counts, color=[COLORS['primary'], COLORS['secondary']], alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Number of Students', fontweight='bold')
ax.set_title('Students Trained', fontweight='bold', fontsize=12)
ax.set_ylim(0, max(student_counts) * 1.2)
for bar, val in zip(bars, student_counts):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(val)}', ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.grid(axis='y', alpha=0.3)

# 4. Investment by year
ax = axes[1, 0]
investment_by_year = df[df['year'] >= 2015].groupby('year')['award_amount'].sum() / 1e6
ax.bar(investment_by_year.index, investment_by_year.values, color=COLORS['primary'], alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Investment ($ Millions)', fontweight='bold')
ax.set_title('Annual Investment Trend', fontweight='bold', fontsize=12)
ax.set_xticks(investment_by_year.index)
ax.grid(axis='y', alpha=0.3)

# 5. Student breakdown 10-year
ax = axes[1, 1]
student_types = ['Undergrad', 'Graduate', 'High School']
student_values = [
    df_10yr['undergrad_students'].sum(),
    df_10yr['grad_students'].sum(),
    df_10yr['hs_students'].sum()
]
colors_list = [COLORS['primary'], COLORS['secondary'], COLORS['accent']]
wedges, texts, autotexts = ax.pie(student_values, labels=student_types, autopct='%1.1f%%',
                                     colors=colors_list, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
ax.set_title('Student Type Distribution\n(10-Year)', fontweight='bold', fontsize=12)

# 6. Student breakdown 5-year
ax = axes[1, 2]
student_values_5yr = [
    df_5yr['undergrad_students'].sum(),
    df_5yr['grad_students'].sum(),
    df_5yr['hs_students'].sum()
]
wedges, texts, autotexts = ax.pie(student_values_5yr, labels=student_types, autopct='%1.1f%%',
                                     colors=colors_list, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
ax.set_title('Student Type Distribution\n(5-Year)', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig(STATIC_VERSION_DIR / 'roi_analysis_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()
print('✓ Created: roi_analysis_dashboard.png')

# ============================================================================
# STATIC VERSION 2: Detailed Analysis
# ============================================================================
print('\n📊 Creating static version: detailed_analysis.png')

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('IWRC Seed Fund - Detailed Analysis', fontsize=16, fontweight='bold', y=0.995)

# 1. Projects by institution (top 10)
ax = axes[0, 0]
top_institutions = df_10yr.groupby('institution')['project_id'].nunique().nlargest(10)
ax.barh(range(len(top_institutions)), top_institutions.values, color=COLORS['primary'], alpha=0.8, edgecolor='black', linewidth=1)
ax.set_yticks(range(len(top_institutions)))
ax.set_yticklabels([inst[:30] for inst in top_institutions.index], fontsize=9)
ax.set_xlabel('Number of Projects', fontweight='bold')
ax.set_title('Top 10 Institutions by Project Count (10-Year)', fontweight='bold', fontsize=11)
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)

# 2. Investment by institution (top 10)
ax = axes[0, 1]
top_funding = df_10yr.groupby('institution')['award_amount'].sum().nlargest(10) / 1e6
ax.barh(range(len(top_funding)), top_funding.values, color=COLORS['secondary'], alpha=0.8, edgecolor='black', linewidth=1)
ax.set_yticks(range(len(top_funding)))
ax.set_yticklabels([inst[:30] for inst in top_funding.index], fontsize=9)
ax.set_xlabel('Award Amount ($ Millions)', fontweight='bold')
ax.set_title('Top 10 Institutions by Funding (10-Year)', fontweight='bold', fontsize=11)
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)

# 3. Average award per project
ax = axes[1, 0]
avg_award = df_10yr.groupby('institution')['award_amount'].mean().nlargest(10) / 1e3
ax.barh(range(len(avg_award)), avg_award.values, color=COLORS['success'], alpha=0.8, edgecolor='black', linewidth=1)
ax.set_yticks(range(len(avg_award)))
ax.set_yticklabels([inst[:30] for inst in avg_award.index], fontsize=9)
ax.set_xlabel('Avg Award per Project ($ Thousands)', fontweight='bold')
ax.set_title('Top 10 Institutions by Avg Award (10-Year)', fontweight='bold', fontsize=11)
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)

# 4. Project timeline
ax = axes[1, 1]
projects_by_year = df[df['year'] >= 2015].groupby('year')['project_id'].nunique()
ax.plot(projects_by_year.index, projects_by_year.values, marker='o', linewidth=2.5, markersize=8,
        color=COLORS['accent'], markerfacecolor=COLORS['accent'], markeredgecolor='black', markeredgewidth=1.5)
ax.fill_between(projects_by_year.index, projects_by_year.values, alpha=0.3, color=COLORS['accent'])
ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Number of Projects', fontweight='bold')
ax.set_title('Annual Project Count Trend (2015-2024)', fontweight='bold', fontsize=11)
ax.set_xticks(projects_by_year.index)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(STATIC_VERSION_DIR / 'detailed_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print('✓ Created: detailed_analysis.png')

# ============================================================================
# STATIC VERSION 3: Investment Analysis
# ============================================================================
print('\n📊 Creating static version: investment_interactive.png')

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('IWRC Seed Fund - Investment Analysis', fontsize=16, fontweight='bold', y=0.995)

# 1. Investment by year
ax = axes[0, 0]
inv_by_year = df[df['year'] >= 2015].groupby('year')['award_amount'].sum() / 1e6
colors_gradient = plt.cm.Blues(np.linspace(0.4, 0.8, len(inv_by_year)))
ax.bar(inv_by_year.index, inv_by_year.values, color=COLORS['primary'], alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Investment ($ Millions)', fontweight='bold')
ax.set_title('Annual Investment', fontweight='bold', fontsize=11)
ax.set_xticks(inv_by_year.index)
ax.grid(axis='y', alpha=0.3)

# 2. Cumulative investment
ax = axes[0, 1]
cumulative = inv_by_year.cumsum()
ax.plot(cumulative.index, cumulative.values, marker='o', linewidth=2.5, markersize=8,
        color=COLORS['accent'], markerfacecolor=COLORS['accent'], markeredgecolor='black', markeredgewidth=1.5)
ax.fill_between(cumulative.index, cumulative.values, alpha=0.3, color=COLORS['accent'])
ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Cumulative Investment ($ Millions)', fontweight='bold')
ax.set_title('Cumulative Investment Over Time', fontweight='bold', fontsize=11)
ax.set_xticks(cumulative.index)
ax.grid(True, alpha=0.3)

# 3. Investment distribution by institution
ax = axes[1, 0]
top_10_inst = df_10yr.groupby('institution')['award_amount'].sum().nlargest(10)
other_amount = df_10yr[~df_10yr['institution'].isin(top_10_inst.index)]['award_amount'].sum()
pie_data = list(top_10_inst.values / 1e6) + [other_amount / 1e6]
pie_labels = [inst[:20] for inst in top_10_inst.index] + ['Others']
colors_pie = plt.cm.Set3(np.linspace(0, 1, len(pie_data)))
ax.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', colors=colors_pie, startangle=90, textprops={'fontsize': 8})
ax.set_title('Investment Distribution by Institution\n(10-Year)', fontweight='bold', fontsize=11)

# 4. Award amount distribution
ax = axes[1, 1]
award_ranges = pd.cut(df_10yr['award_amount'] / 1000, bins=[0, 50, 100, 150, 200, np.inf],
                       labels=['<$50K', '$50-100K', '$100-150K', '$150-200K', '>$200K'])
award_counts = award_ranges.value_counts().sort_index()
ax.bar(range(len(award_counts)), award_counts.values, color=COLORS['success'], alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(award_counts)))
ax.set_xticklabels(award_counts.index, rotation=45, ha='right')
ax.set_ylabel('Number of Projects', fontweight='bold')
ax.set_title('Award Amount Distribution (10-Year)', fontweight='bold', fontsize=11)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(STATIC_VERSION_DIR / 'investment_interactive.png', dpi=300, bbox_inches='tight')
plt.close()
print('✓ Created: investment_interactive.png')

# ============================================================================
# STATIC VERSION 4: Students Analysis
# ============================================================================
print('\n📊 Creating static version: students_interactive.png')

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('IWRC Seed Fund - Student Training Analysis', fontsize=16, fontweight='bold', y=0.995)

# 1. Students by type (10-year)
ax = axes[0, 0]
student_totals_10yr = {
    'Undergraduate': df_10yr['undergrad_students'].sum(),
    'Graduate': df_10yr['grad_students'].sum(),
    'High School': df_10yr['hs_students'].sum()
}
colors_list = [COLORS['primary'], COLORS['secondary'], COLORS['accent']]
ax.bar(student_totals_10yr.keys(), student_totals_10yr.values(), color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Number of Students', fontweight='bold')
ax.set_title('Students by Type (10-Year)', fontweight='bold', fontsize=11)
ax.tick_params(axis='x', rotation=45)
for i, (k, v) in enumerate(student_totals_10yr.items()):
    ax.text(i, v, str(int(v)), ha='center', va='bottom', fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# 2. Students by type (5-year)
ax = axes[0, 1]
student_totals_5yr = {
    'Undergraduate': df_5yr['undergrad_students'].sum(),
    'Graduate': df_5yr['grad_students'].sum(),
    'High School': df_5yr['hs_students'].sum()
}
ax.bar(student_totals_5yr.keys(), student_totals_5yr.values(), color=colors_list, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_ylabel('Number of Students', fontweight='bold')
ax.set_title('Students by Type (5-Year)', fontweight='bold', fontsize=11)
ax.tick_params(axis='x', rotation=45)
for i, (k, v) in enumerate(student_totals_5yr.items()):
    ax.text(i, v, str(int(v)), ha='center', va='bottom', fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# 3. Students per project (10-year)
ax = axes[1, 0]
df_10yr['total_students'] = df_10yr['undergrad_students'] + df_10yr['grad_students'] + df_10yr['hs_students']
students_per_project = df_10yr[df_10yr['total_students'] > 0].groupby('institution')['total_students'].mean().nlargest(10)
ax.barh(range(len(students_per_project)), students_per_project.values, color=COLORS['purple'], alpha=0.8, edgecolor='black', linewidth=1)
ax.set_yticks(range(len(students_per_project)))
ax.set_yticklabels([inst[:30] for inst in students_per_project.index], fontsize=9)
ax.set_xlabel('Avg Students per Project', fontweight='bold')
ax.set_title('Top 10 Institutions by Avg Students/Project (10-Year)', fontweight='bold', fontsize=11)
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)

# 4. Student training trend
ax = axes[1, 1]
students_by_year = df[df['year'] >= 2015].copy()
students_by_year['total_students'] = students_by_year['undergrad_students'] + students_by_year['grad_students'] + students_by_year['hs_students']
students_annual = students_by_year.groupby('year')[['undergrad_students', 'grad_students', 'hs_students']].sum()
ax.bar(students_annual.index, students_annual['undergrad_students'], label='Undergraduate', color=COLORS['primary'], alpha=0.8, edgecolor='black', linewidth=0.5)
ax.bar(students_annual.index, students_annual['grad_students'], bottom=students_annual['undergrad_students'],
       label='Graduate', color=COLORS['secondary'], alpha=0.8, edgecolor='black', linewidth=0.5)
ax.bar(students_annual.index, students_annual['hs_students'],
       bottom=students_annual['undergrad_students'] + students_annual['grad_students'],
       label='High School', color=COLORS['accent'], alpha=0.8, edgecolor='black', linewidth=0.5)
ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Number of Students', fontweight='bold')
ax.set_title('Annual Student Training (2015-2024)', fontweight='bold', fontsize=11)
ax.set_xticks(students_annual.index)
ax.legend(loc='upper left', fontsize=9)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(STATIC_VERSION_DIR / 'students_interactive.png', dpi=300, bbox_inches='tight')
plt.close()
print('✓ Created: students_interactive.png')

# ============================================================================
# STATIC VERSION 5: Award Type Analysis Dashboard
# ============================================================================
print('\n📊 Creating static version: award_type_dashboard.png')

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('IWRC Seed Fund - Award Type Analysis', fontsize=16, fontweight='bold', y=0.98)

# 1. Project count by award type (10-year)
ax = axes[0, 0]
award_projects_10yr = df_10yr[df_10yr['award_category'].notna()].groupby('award_category')['project_id'].nunique()
colors_award = [COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['accent']][:len(award_projects_10yr)]
ax.bar(range(len(award_projects_10yr)), award_projects_10yr.values, color=colors_award, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(award_projects_10yr)))
ax.set_xticklabels(award_projects_10yr.index, rotation=45, ha='right')
ax.set_ylabel('Number of Projects', fontweight='bold')
ax.set_title('Projects by Award Type (10-Year)', fontweight='bold', fontsize=11)
for i, v in enumerate(award_projects_10yr.values):
    ax.text(i, v, str(int(v)), ha='center', va='bottom', fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# 2. Investment by award type (10-year)
ax = axes[0, 1]
award_funding_10yr = df_10yr[df_10yr['award_category'].notna()].groupby('award_category')['award_amount'].sum() / 1e6
ax.bar(range(len(award_funding_10yr)), award_funding_10yr.values, color=colors_award, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(award_funding_10yr)))
ax.set_xticklabels(award_funding_10yr.index, rotation=45, ha='right')
ax.set_ylabel('Award Amount ($ Millions)', fontweight='bold')
ax.set_title('Funding by Award Type (10-Year)', fontweight='bold', fontsize=11)
for i, v in enumerate(award_funding_10yr.values):
    ax.text(i, v, f'${v:.1f}M', ha='center', va='bottom', fontweight='bold', fontsize=9)
ax.grid(axis='y', alpha=0.3)

# 3. Avg award per project
ax = axes[0, 2]
award_avg_10yr = (df_10yr[df_10yr['award_category'].notna()].groupby('award_category')['award_amount'].sum() /
                   df_10yr[df_10yr['award_category'].notna()].groupby('award_category')['project_id'].nunique()) / 1e3
ax.bar(range(len(award_avg_10yr)), award_avg_10yr.values, color=colors_award, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(award_avg_10yr)))
ax.set_xticklabels(award_avg_10yr.index, rotation=45, ha='right')
ax.set_ylabel('Avg Award ($ Thousands)', fontweight='bold')
ax.set_title('Avg Award per Project (10-Year)', fontweight='bold', fontsize=11)
for i, v in enumerate(award_avg_10yr.values):
    ax.text(i, v, f'${v:.0f}K', ha='center', va='bottom', fontweight='bold', fontsize=9)
ax.grid(axis='y', alpha=0.3)

# 4. Project count comparison (5yr vs 10yr)
ax = axes[1, 0]
award_projects_5yr = df_5yr[df_5yr['award_category'].notna()].groupby('award_category')['project_id'].nunique()
# Align indices
all_awards = sorted(set(award_projects_10yr.index) | set(award_projects_5yr.index))
x = np.arange(len(all_awards))
width = 0.35
ax.bar(x - width/2, [award_projects_10yr.get(a, 0) for a in all_awards], width, label='10-Year', color=COLORS['primary'], alpha=0.8, edgecolor='black', linewidth=1)
ax.bar(x + width/2, [award_projects_5yr.get(a, 0) for a in all_awards], width, label='5-Year', color=COLORS['secondary'], alpha=0.8, edgecolor='black', linewidth=1)
ax.set_xticks(x)
ax.set_xticklabels(all_awards, rotation=45, ha='right')
ax.set_ylabel('Number of Projects', fontweight='bold')
ax.set_title('Project Count: 10-Year vs 5-Year', fontweight='bold', fontsize=11)
ax.legend()
ax.grid(axis='y', alpha=0.3)

# 5. Investment comparison (5yr vs 10yr)
ax = axes[1, 1]
award_funding_5yr = df_5yr[df_5yr['award_category'].notna()].groupby('award_category')['award_amount'].sum() / 1e6
x = np.arange(len(all_awards))
ax.bar(x - width/2, [award_funding_10yr.get(a, 0) for a in all_awards], width, label='10-Year', color=COLORS['primary'], alpha=0.8, edgecolor='black', linewidth=1)
ax.bar(x + width/2, [award_funding_5yr.get(a, 0) for a in all_awards], width, label='5-Year', color=COLORS['secondary'], alpha=0.8, edgecolor='black', linewidth=1)
ax.set_xticks(x)
ax.set_xticklabels(all_awards, rotation=45, ha='right')
ax.set_ylabel('Award Amount ($ Millions)', fontweight='bold')
ax.set_title('Funding: 10-Year vs 5-Year', fontweight='bold', fontsize=11)
ax.legend()
ax.grid(axis='y', alpha=0.3)

# 6. Award type distribution pie (10-year)
ax = axes[1, 2]
pie_data = award_projects_10yr.values
pie_labels = award_projects_10yr.index
colors_pie = [COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['accent']][:len(pie_data)]
wedges, texts, autotexts = ax.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', colors=colors_pie, startangle=90, textprops={'fontsize': 9, 'fontweight': 'bold'})
ax.set_title('Award Type Distribution\n(10-Year)', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig(STATIC_VERSION_DIR / 'award_type_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()
print('✓ Created: award_type_dashboard.png')

# ============================================================================
# Create an index file
# ============================================================================
print('\n📋 Creating index file for static versions...')

index_content = """# Interactive Visualizations - Static Versions

This folder contains **static PNG versions** of all interactive visualizations.
These are high-resolution (300 DPI) snapshots suitable for presentations, reports, and printing.

## Files Overview

### 1. roi_analysis_dashboard.png
**Source**: `roi_analysis_dashboard.html`
- 6-panel summary of key ROI metrics
- Project counts (10-year vs 5-year comparison)
- Total investment comparison
- Students trained comparison
- Annual investment trend (2015-2024)
- Student type distribution (pie charts)

### 2. detailed_analysis.png
**Source**: `detailed_analysis.html`
- Top 10 institutions by project count
- Top 10 institutions by funding
- Top 10 institutions by average award per project
- Annual project count trend (2015-2024)

### 3. investment_interactive.png
**Source**: `investment_interactive.html`
- Annual investment trend
- Cumulative investment over time
- Investment distribution by institution (pie chart)
- Award amount distribution by ranges

### 4. students_interactive.png
**Source**: `students_interactive.html`
- Students by type (10-year period)
- Students by type (5-year period)
- Top 10 institutions by average students per project
- Annual student training trend (2015-2024)

### 5. award_type_dashboard.png
**Source**: `award_type_dashboard.html`
- Projects by award type (10-year)
- Funding by award type (10-year)
- Average award per project by type
- Project count comparison (10-year vs 5-year)
- Funding comparison (10-year vs 5-year)
- Award type distribution pie chart

## Specifications

- **Resolution**: 300 DPI (print-quality)
- **Format**: PNG (lossless compression)
- **Color**: Full color with professional palette
- **Dimensions**: Optimized for standard presentations and reports

## Usage

These static images are ideal for:
- PowerPoint/Keynote presentations
- PDF reports
- Printed materials
- Email attachments
- Web content (when interactive features not needed)

## Relationship to Interactive Versions

Each PNG file corresponds to an interactive HTML dashboard in the parent directory.
The static versions show the same data and analysis, but without the interactive filtering,
zooming, and hover tooltips available in the HTML versions.

For dynamic exploration, use the HTML files. For fixed presentations and printing, use the PNG files.

---

**Generated**: November 24, 2025
**Data Source**: IWRC Seed Fund Tracking Consolidated Spreadsheet
**Analysis Methodology**: Unique Project ID counting (not row counting)
"""

index_file = STATIC_VERSION_DIR / 'README.md'
with open(index_file, 'w') as f:
    f.write(index_content)
print(f'✓ Created: README.md')

# ============================================================================
# Summary
# ============================================================================
print('\n' + '=' * 80)
print('✅ CONVERSION COMPLETE')
print('=' * 80)

files_created = list(STATIC_VERSION_DIR.glob('*.png')) + list(STATIC_VERSION_DIR.glob('*.md'))
print(f'\n📊 Files created: {len(files_created)}')
for f in sorted(files_created):
    size_mb = f.stat().st_size / (1024 * 1024)
    print(f'  • {f.name:<40} ({size_mb:>6.2f} MB)' if size_mb > 0.1 else f'  • {f.name:<40} ({f.stat().st_size / 1024:>6.1f} KB)')

print(f'\n📁 Output directory: {STATIC_VERSION_DIR}')
print('\n✨ All interactive visualizations now have static PNG counterparts!')
