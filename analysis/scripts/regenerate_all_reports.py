#!/usr/bin/env python3
"""
Regenerate ROI analysis with PROPER DEDUPLICATION using centralized data loader.

This script replaces the deprecated regenerate_analysis.py which had double-counting errors.

Key Improvements:
- Uses IWRCDataLoader for automatic deduplication
- Prevents double-counting of investment and student metrics
- Maintains IWRC branding and styling
- Generates accurate visualizations and reports

See: docs/MIGRATION_FROM_FACT_SHEET.md for methodology details
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / 'analysis' / 'scripts'))

# Import centralized data loader and IWRC branding
from iwrc_data_loader import IWRCDataLoader

try:
    from iwrc_brand_style import IWRC_COLORS, configure_matplotlib_iwrc
    from award_type_filters import filter_all_projects, filter_104b_only, get_award_type_label
    USE_IWRC_BRANDING = True
except ImportError as e:
    print(f"Warning: Could not import IWRC modules ({e}). Using fallback colors.")
    USE_IWRC_BRANDING = False

# Configure visualization settings
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 11

if USE_IWRC_BRANDING:
    configure_matplotlib_iwrc()
    COLORS = IWRC_COLORS
else:
    COLORS = {
        'primary': '#258372',
        'secondary': '#639757',
        'success': '#8ab38a',
        'accent': '#FCC080'
    }

print("=" * 80)
print("IWRC SEED FUND ANALYSIS - CORRECTED VERSION")
print("Using centralized data loader with automatic deduplication")
print("=" * 80)

# Initialize data loader
loader = IWRCDataLoader()

# Load master data with deduplication
df = loader.load_master_data(deduplicate=True)
print(f'\n✓ Data loaded and deduplicated: {len(df):,} unique projects from master file')

# Create time period filters
df_10yr = df[df['project_year'].between(2015, 2024)].copy()
df_5yr = df[df['project_year'].between(2020, 2024)].copy()

print(f'✓ Time period filters created:')
print(f'  10-Year (2015-2024): {len(df_10yr):,} projects')
print(f'  5-Year (2020-2024): {len(df_5yr):,} projects')

# ============================================================================
# Calculate Metrics Using Data Loader
# ============================================================================
print('\n' + '='*70)
print('CALCULATING METRICS (DEDUPLICATED)')
print('='*70)

metrics_10yr = loader.calculate_metrics(df_10yr, period='10yr')
metrics_5yr = loader.calculate_metrics(df_5yr, period='5yr')

print(f'\n✓ 10-Year Metrics (2015-2024):')
print(f'  Projects: {metrics_10yr["projects"]}')
print(f'  Investment: ${metrics_10yr["investment"]:,.2f}')
print(f'  Students: {metrics_10yr["students"]}')
print(f'  Follow-on: ${metrics_10yr["followon"]:,.2f}')
print(f'  ROI: {metrics_10yr["roi"]:.1%}')

print(f'\n✓ 5-Year Metrics (2020-2024):')
print(f'  Projects: {metrics_5yr["projects"]}')
print(f'  Investment: ${metrics_5yr["investment"]:,.2f}')
print(f'  Students: {metrics_5yr["students"]}')
print(f'  Follow-on: ${metrics_5yr["followon"]:,.2f}')
print(f'  ROI: {metrics_5yr["roi"]:.1%}')

# ============================================================================
# Investment Summary
# ============================================================================
investment_summary = pd.DataFrame({
    'Time Period': ['10-Year (2015-2024)', '5-Year (2020-2024)'],
    'Total IWRC Investment': [
        f'${metrics_10yr["investment"]:,.2f}',
        f'${metrics_5yr["investment"]:,.2f}'
    ],
    'Number of Projects': [metrics_10yr['projects'], metrics_5yr['projects']]
})

print('\n' + '='*70)
print('IWRC SEED FUNDING INVESTMENT SUMMARY')
print('='*70)
print(investment_summary.to_string(index=False))
print('='*70)

# ============================================================================
# ROI Summary
# ============================================================================
roi_summary = pd.DataFrame({
    'Time Period': ['10-Year (2015-2024)', '5-Year (2020-2024)'],
    'IWRC Investment': [
        f'${metrics_10yr["investment"]:,.2f}',
        f'${metrics_5yr["investment"]:,.2f}'
    ],
    'Follow-on Funding': [
        f'${metrics_10yr["followon"]:,.2f}',
        f'${metrics_5yr["followon"]:,.2f}'
    ],
    'ROI Multiplier': [
        f'{metrics_10yr["roi"]:.2f}x',
        f'{metrics_5yr["roi"]:.2f}x'
    ]
})

print('\n' + '='*80)
print('RETURN ON INVESTMENT (ROI) SUMMARY')
print('='*80)
print(roi_summary.to_string(index=False))
print('='*80)

# ============================================================================
# Student Summary
# ============================================================================
student_summary = pd.DataFrame({
    'Student Type': ['PhD', "Master's", 'Undergraduate', 'Post-Doctoral', 'TOTAL'],
    '10-Year (2015-2024)': [
        metrics_10yr['phd'],
        metrics_10yr['masters'],
        metrics_10yr['undergrad'],
        metrics_10yr['postdoc'],
        metrics_10yr['students']
    ],
    '5-Year (2020-2024)': [
        metrics_5yr['phd'],
        metrics_5yr['masters'],
        metrics_5yr['undergrad'],
        metrics_5yr['postdoc'],
        metrics_5yr['students']
    ]
})

print('\n' + '='*70)
print('STUDENTS TRAINED THROUGH IWRC SEED FUNDING')
print('='*70)
print(student_summary.to_string(index=False))
print('='*70)

# ============================================================================
# Executive Summary
# ============================================================================
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
        'Number of Projects',
        'Institutions Served'
    ],
    '10-Year (2015-2024)': [
        f'${metrics_10yr["investment"]:,.2f}',
        f'${metrics_10yr["followon"]:,.2f}',
        f'{metrics_10yr["roi"]:.2f}x',
        metrics_10yr['students'],
        metrics_10yr['phd'],
        metrics_10yr['masters'],
        metrics_10yr['undergrad'],
        metrics_10yr['postdoc'],
        metrics_10yr['projects'],
        metrics_10yr['institutions']
    ],
    '5-Year (2020-2024)': [
        f'${metrics_5yr["investment"]:,.2f}',
        f'${metrics_5yr["followon"]:,.2f}',
        f'{metrics_5yr["roi"]:.2f}x',
        metrics_5yr['students'],
        metrics_5yr['phd'],
        metrics_5yr['masters'],
        metrics_5yr['undergrad'],
        metrics_5yr['postdoc'],
        metrics_5yr['projects'],
        metrics_5yr['institutions']
    ]
})

print('\n' + '='*80)
print('EXECUTIVE SUMMARY: IWRC SEED FUND ROI ANALYSIS')
print('='*80)
print(executive_summary.to_string(index=False))
print('='*80)

print('\n✓ KEY TAKEAWAYS:')
print(f'  • IWRC serves {metrics_10yr["institutions"]} institutions across Illinois')
print(f'  • For every $1 invested, IWRC generates ${metrics_10yr["roi"]:.2f} in follow-on funding (10-year)')
print(f'  • {metrics_10yr["students"]} students trained over 10 years')
print(f'  • All metrics properly deduplicated - no double-counting')
print('='*80)

# ============================================================================
# Generate Visualizations
# ============================================================================
output_dir = project_root / 'deliverables' / 'visualizations' / 'static' / 'overview'
output_dir.mkdir(parents=True, exist_ok=True)

# 1. Investment Comparison
fig, ax = plt.subplots(figsize=(10, 6))
periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']
investments = [metrics_10yr['investment'], metrics_5yr['investment']]
bars = ax.barh(periods, investments, color=[COLORS['primary'], COLORS['secondary']], height=0.6)
for i, (bar, value) in enumerate(zip(bars, investments)):
    ax.text(value + max(investments)*0.02, i, f'${value:,.0f}', va='center', fontsize=12, fontweight='bold')
ax.set_xlabel('Total Investment ($)', fontsize=12, fontweight='bold')
ax.set_title('IWRC Seed Funding Investment by Time Period', fontsize=14, fontweight='bold', pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(output_dir / 'iwrc_investment_comparison_CORRECTED.png', dpi=300, bbox_inches='tight')
print(f'\n✓ Chart saved: iwrc_investment_comparison_CORRECTED.png')
plt.close()

# 2. ROI Comparison
fig, ax = plt.subplots(figsize=(12, 7))
x = np.arange(len(periods))
width = 0.35
bars1 = ax.bar(x - width/2, [metrics_10yr['investment'], metrics_5yr['investment']], width,
               label='IWRC Investment', color=COLORS['primary'])
bars2 = ax.bar(x + width/2, [metrics_10yr['followon'], metrics_5yr['followon']], width,
               label='Follow-on Funding Secured', color=COLORS['success'])
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
for i, (period, roi) in enumerate(zip(periods, [metrics_10yr['roi'], metrics_5yr['roi']])):
    max_value = max(metrics_10yr['investment'], metrics_5yr['investment'],
                    metrics_10yr['followon'], metrics_5yr['followon'])
    ax.text(i, max_value * 1.15,
            f'ROI: {roi:.2f}x',
            ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
ax.set_ylabel('Funding Amount ($)', fontsize=12, fontweight='bold')
ax.set_title('IWRC Seed Funding Return on Investment (CORRECTED)', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(periods, fontsize=11)
ax.legend(fontsize=11, loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(output_dir / 'roi_comparison_CORRECTED.png', dpi=300, bbox_inches='tight')
print(f'✓ Chart saved: roi_comparison_CORRECTED.png')
plt.close()

# 3. Students Trained
fig, ax = plt.subplots(figsize=(10, 6))
categories = ['PhD', "Master's", 'Undergraduate', 'Post-Doctoral']
data_10yr = [
    metrics_10yr['phd'],
    metrics_10yr['masters'],
    metrics_10yr['undergrad'],
    metrics_10yr['postdoc']
]
data_5yr = [
    metrics_5yr['phd'],
    metrics_5yr['masters'],
    metrics_5yr['undergrad'],
    metrics_5yr['postdoc']
]
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
ax.set_title('Students Trained Through IWRC Seed Funding (CORRECTED)', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11)
ax.legend(fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(output_dir / 'students_trained_CORRECTED.png', dpi=300, bbox_inches='tight')
print(f'✓ Chart saved: students_trained_CORRECTED.png')
plt.close()

# ============================================================================
# Export to Excel
# ============================================================================
output_file = project_root / 'data' / 'outputs' / 'IWRC_ROI_Analysis_Summary_CORRECTED.xlsx'
output_file.parent.mkdir(parents=True, exist_ok=True)

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    executive_summary.to_excel(writer, sheet_name='Executive Summary', index=False)
    investment_summary.to_excel(writer, sheet_name='Investment', index=False)
    roi_summary.to_excel(writer, sheet_name='ROI Analysis', index=False)
    student_summary.to_excel(writer, sheet_name='Students Trained', index=False)

print(f'\n✓ Excel file saved: IWRC_ROI_Analysis_Summary_CORRECTED.xlsx')

print('\n' + '='*80)
print('✓ ANALYSIS COMPLETE WITH PROPER DEDUPLICATION')
print('='*80)
print(f'\nCORRECTED METRICS USING IWRC DATA LOADER:')
print(f'  10-Year Investment: ${metrics_10yr["investment"]:,.2f} (deduplicated)')
print(f'  10-Year Students: {metrics_10yr["students"]} (deduplicated)')
print(f'  10-Year ROI: {metrics_10yr["roi"]:.1%}')
print(f'\n  5-Year Investment: ${metrics_5yr["investment"]:,.2f} (deduplicated)')
print(f'  5-Year Students: {metrics_5yr["students"]} (deduplicated)')
print(f'  5-Year ROI: {metrics_5yr["roi"]:.1%}')
print(f'\n  All visualizations and outputs regenerated with accurate metrics.')
print('='*80)
