"""
Execute the ROI analysis notebook and save results
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import warnings
warnings.filterwarnings('ignore')

# Configure settings
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:,.2f}'.format)

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'accent': '#d62728',
    'purple': '#9467bd',
}

print('='*80)
print('IWRC SEED FUND ROI ANALYSIS - EXECUTING...')
print('='*80)

# Load data
print('\n1. Loading data...')
df = pd.read_excel('IWRC Seed Fund Tracking.xlsx', sheet_name='Project Overview')
print(f'   ✓ Loaded {len(df):,} rows, {len(df.columns)} columns')

# Column mapping
col_map = {
    'Project ID ': 'project_id',
    'Award Type': 'award_type',
    'Project Title': 'project_title',
    'Project PI': 'pi_name',
    'Academic Institution of PI': 'institution',
    'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount',
    'Number of PhD Students Supported by WRRA $': 'phd_students',
    'Number of MS Students Supported by WRRA $': 'ms_students',
    'Number of Undergraduate Students Supported by WRRA $': 'undergrad_students',
    'Number of Post Docs Supported by WRRA $': 'postdoc_students',
    "Award, Achievement, or Grant\n (This may include awards and achievements for projects from the previous year to this 5-year cycle, so long as they were not already included in last year's report)": 'awards_grants',
    "Description of Award, Achievement, or Grant\n (This may include awards and achievements for projects from the previous year to this 5-year cycle, so long as they were not already included in last year's report)": 'award_description',
    'Monetary Benefit of Award or Achievement (if applicable; use NA if not applicable)': 'monetary_benefit',
    'WRRI Science Priority that Best Aligns with this Project': 'science_priority',
    'Keyword (Primary)': 'keyword_primary'
}

df_work = df.rename(columns=col_map)

# Clean student columns
student_cols = ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']
for col in student_cols:
    df_work[col] = pd.to_numeric(df_work[col], errors='coerce')

print('   ✓ Columns mapped and cleaned')

# Extract years
print('\n2. Extracting project years...')

def extract_year_from_project_id(project_id):
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

df_work['project_year'] = df_work['project_id'].apply(extract_year_from_project_id)

# Filter datasets
df_10yr = df_work[df_work['project_year'].between(2015, 2024, inclusive='both')].copy()
df_5yr = df_work[df_work['project_year'].between(2020, 2024, inclusive='both')].copy()

print(f'   ✓ 10-Year dataset: {len(df_10yr):,} projects')
print(f'   ✓ 5-Year dataset: {len(df_5yr):,} projects')

# Calculate investment
print('\n3. Calculating investment totals...')
investment_10yr = df_10yr['award_amount'].sum()
investment_5yr = df_5yr['award_amount'].sum()

print(f'   ✓ 10-Year investment: ${investment_10yr:,.2f}')
print(f'   ✓ 5-Year investment: ${investment_5yr:,.2f}')

# Categorize awards
print('\n4. Categorizing awards/grants...')

def categorize_award_type(text):
    if pd.isna(text):
        return None
    text_lower = str(text).lower()
    if 'grant' in text_lower:
        return 'Grant'
    elif 'award' in text_lower:
        return 'Award'
    elif 'achievement' in text_lower:
        return 'Achievement'
    return None

df_10yr['award_category'] = df_10yr['awards_grants'].apply(categorize_award_type)
df_5yr['award_category'] = df_5yr['awards_grants'].apply(categorize_award_type)

awards_10yr = df_10yr['award_category'].value_counts()
awards_5yr = df_5yr['award_category'].value_counts()

print(f'   ✓ 10-Year: {awards_10yr.sum()} total awards/grants')
print(f'   ✓ 5-Year: {awards_5yr.sum()} total awards/grants')

# Extract monetary values
print('\n5. Extracting monetary values from multiple columns...')

def clean_monetary_value(value):
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

def extract_grant_amount_comprehensive(row):
    if pd.notna(row['monetary_benefit']):
        amount = clean_monetary_value(row['monetary_benefit'])
        if amount > 0:
            return amount
    if 'award_description' in row.index and pd.notna(row['award_description']):
        amount = clean_monetary_value(row['award_description'])
        if amount > 0:
            return amount
    if pd.notna(row['awards_grants']):
        amount = clean_monetary_value(row['awards_grants'])
        if amount > 0:
            return amount
    return 0.0

df_10yr['monetary_benefit_clean'] = df_10yr.apply(extract_grant_amount_comprehensive, axis=1)
df_5yr['monetary_benefit_clean'] = df_5yr.apply(extract_grant_amount_comprehensive, axis=1)

followon_10yr = df_10yr['monetary_benefit_clean'].sum()
followon_5yr = df_5yr['monetary_benefit_clean'].sum()

print(f'   ✓ 10-Year follow-on funding: ${followon_10yr:,.2f}')
print(f'   ✓ 5-Year follow-on funding: ${followon_5yr:,.2f}')

# Calculate ROI
print('\n6. Calculating ROI...')
roi_10yr = followon_10yr / investment_10yr if investment_10yr > 0 else 0
roi_5yr = followon_5yr / investment_5yr if investment_5yr > 0 else 0

print(f'   ✓ 10-Year ROI: {roi_10yr:.3f}x')
print(f'   ✓ 5-Year ROI: {roi_5yr:.3f}x')

# Calculate students
print('\n7. Calculating student totals...')
students_10yr = {
    'phd': df_10yr['phd_students'].sum(),
    'ms': df_10yr['ms_students'].sum(),
    'undergrad': df_10yr['undergrad_students'].sum(),
    'postdoc': df_10yr['postdoc_students'].sum()
}
students_10yr['total'] = sum(students_10yr.values())

students_5yr = {
    'phd': df_5yr['phd_students'].sum(),
    'ms': df_5yr['ms_students'].sum(),
    'undergrad': df_5yr['undergrad_students'].sum(),
    'postdoc': df_5yr['postdoc_students'].sum()
}
students_5yr['total'] = sum(students_5yr.values())

print(f'   ✓ 10-Year students: {int(students_10yr["total"])}')
print(f'   ✓ 5-Year students: {int(students_5yr["total"])}')

# Generate visualizations
print('\n8. Generating visualizations...')

# 1. Investment comparison
fig, ax = plt.subplots(figsize=(10, 6))
periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']
investments = [investment_10yr, investment_5yr]
bars = ax.barh(periods, investments, color=[COLORS['primary'], COLORS['secondary']], height=0.6)
for i, (bar, value) in enumerate(zip(bars, investments)):
    ax.text(value + max(investments)*0.02, i, f'${value:,.0f}',
            va='center', fontsize=12, fontweight='bold')
ax.set_xlabel('Total Investment ($)', fontsize=12, fontweight='bold')
ax.set_title('IWRC Seed Funding Investment by Time Period', fontsize=14, fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('iwrc_investment_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print('   ✓ Created: iwrc_investment_comparison.png')

# 2. ROI Comparison
fig, ax = plt.subplots(figsize=(12, 7))
x = np.arange(len(periods))
width = 0.35
bars1 = ax.bar(x - width/2, [investment_10yr, investment_5yr], width,
               label='IWRC Investment', color=COLORS['primary'])
bars2 = ax.bar(x + width/2, [followon_10yr, followon_5yr], width,
               label='Follow-on Funding Secured', color=COLORS['success'])
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
for i, (period, roi) in enumerate(zip(periods, [roi_10yr, roi_5yr])):
    ax.text(i, max(investment_10yr, investment_5yr, followon_10yr, followon_5yr) * 1.15,
            f'ROI: {roi:.3f}x',
            ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
ax.set_ylabel('Funding Amount ($)', fontsize=12, fontweight='bold')
ax.set_title('IWRC Seed Funding Return on Investment', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(periods, fontsize=11)
ax.legend(fontsize=11, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('roi_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print('   ✓ Created: roi_comparison.png')

# 3. Students trained
fig, ax = plt.subplots(figsize=(10, 6))
categories = ['PhD', "Master's", 'Undergraduate', 'Post-Doctoral']
data_10yr = [students_10yr['phd'], students_10yr['ms'], students_10yr['undergrad'], students_10yr['postdoc']]
data_5yr = [students_5yr['phd'], students_5yr['ms'], students_5yr['undergrad'], students_5yr['postdoc']]
x = np.arange(len(categories))
width = 0.35
bars1 = ax.bar(x - width/2, data_10yr, width, label='10-Year (2015-2024)', color=COLORS['primary'])
bars2 = ax.bar(x + width/2, data_5yr, width, label='5-Year (2020-2024)', color=COLORS['secondary'])
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_ylabel('Number of Students', fontsize=12, fontweight='bold')
ax.set_title('Students Trained Through IWRC Seed Funding', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11)
ax.legend(fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('students_trained.png', dpi=300, bbox_inches='tight')
plt.close()
print('   ✓ Created: students_trained.png')

# 4. Student distribution pie charts
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
colors_pie = [COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['purple']]
if students_10yr['total'] > 0:
    ax1.pie(data_10yr, labels=categories, autopct='%1.1f%%', startangle=90,
            colors=colors_pie, textprops={'fontsize': 11})
    ax1.set_title('10-Year Period (2015-2024)\nTotal Students: {:,.0f}'.format(students_10yr['total']),
                  fontsize=13, fontweight='bold')
if students_5yr['total'] > 0:
    ax2.pie(data_5yr, labels=categories, autopct='%1.1f%%', startangle=90,
            colors=colors_pie, textprops={'fontsize': 11})
    ax2.set_title('5-Year Period (2020-2024)\nTotal Students: {:,.0f}'.format(students_5yr['total']),
                  fontsize=13, fontweight='bold')
fig.suptitle('Distribution of Students Trained by Type', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('student_distribution_pie.png', dpi=300, bbox_inches='tight')
plt.close()
print('   ✓ Created: student_distribution_pie.png')

# Create Excel summary
print('\n9. Creating Excel summary...')

executive_summary = pd.DataFrame({
    'Metric': [
        'Total IWRC Investment',
        'Total Follow-on Funding Secured',
        'Return on Investment (ROI)',
        'Total Students Trained',
        'PhD Students',
        "Master's Students",
        'Undergraduate Students',
        'Post-Doctoral Researchers',
        'Number of Projects'
    ],
    '10-Year (2015-2024)': [
        f'${investment_10yr:,.2f}',
        f'${followon_10yr:,.2f}',
        f'{roi_10yr:.3f}x',
        int(students_10yr['total']),
        int(students_10yr['phd']),
        int(students_10yr['ms']),
        int(students_10yr['undergrad']),
        int(students_10yr['postdoc']),
        len(df_10yr)
    ],
    '5-Year (2020-2024)': [
        f'${investment_5yr:,.2f}',
        f'${followon_5yr:,.2f}',
        f'{roi_5yr:.3f}x',
        int(students_5yr['total']),
        int(students_5yr['phd']),
        int(students_5yr['ms']),
        int(students_5yr['undergrad']),
        int(students_5yr['postdoc']),
        len(df_5yr)
    ]
})

with pd.ExcelWriter('IWRC_ROI_Analysis_Summary.xlsx', engine='openpyxl') as writer:
    executive_summary.to_excel(writer, sheet_name='Executive Summary', index=False)

print('   ✓ Created: IWRC_ROI_Analysis_Summary.xlsx')

# Print summary
print('\n' + '='*80)
print('EXECUTIVE SUMMARY')
print('='*80)
print('\n10-YEAR PERIOD (2015-2024):')
print(f'  Investment:         ${investment_10yr:,.2f}')
print(f'  Follow-on Funding:  ${followon_10yr:,.2f}')
print(f'  ROI:                {roi_10yr:.3f}x')
print(f'  Students Trained:   {int(students_10yr["total"])}')

print('\n5-YEAR PERIOD (2020-2024):')
print(f'  Investment:         ${investment_5yr:,.2f}')
print(f'  Follow-on Funding:  ${followon_5yr:,.2f}')
print(f'  ROI:                {roi_5yr:.3f}x')
print(f'  Students Trained:   {int(students_5yr["total"])}')

print('\n' + '='*80)
print('✓ ANALYSIS COMPLETE!')
print('='*80)
print('\nGenerated files:')
print('  • IWRC_ROI_Analysis_Summary.xlsx')
print('  • iwrc_investment_comparison.png')
print('  • roi_comparison.png')
print('  • students_trained.png')
print('  • student_distribution_pie.png')
print('\n' + '='*80)
