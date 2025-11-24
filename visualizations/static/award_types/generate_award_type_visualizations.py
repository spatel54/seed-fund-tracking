import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib import rcParams
import os

# Set professional styling
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
rcParams['font.size'] = 12

# Define color palette
COLORS = {
    '104g': '#1f77b4',  # Blue
    '104b': '#ff7f0e',  # Orange
    'Coordination': '#2ca02c'  # Green
}

# Data
data_10yr = {
    '104g': {'projects': 2, 'investment': 1700000},
    '104b': {'projects': 33, 'investment': 728000},
    'Coordination': {'projects': 2, 'investment': 98000}
}

data_5yr = {
    '104g': {'projects': 1, 'investment': 1203120},
    '104b': {'projects': 6, 'investment': 127134},
    'Coordination': {'projects': 0, 'investment': 0}
}

# 104g subtypes data
subtypes_104g = {
    '104g-AIS': {'projects': 7, 'investment': 3800000},
    '104g-General': {'projects': 8, 'investment': 1300000},
    '104g-PFAS': {'projects': 2, 'investment': 1000000}
}

output_dir = '/Users/shivpat/Downloads/Seed Fund Tracking/visualizations/static/award_types/'

def format_currency(value):
    """Format value as currency in millions or thousands"""
    if value >= 1000000:
        return f'${value/1000000:.1f}M'
    elif value >= 1000:
        return f'${value/1000:.0f}K'
    else:
        return f'${value:,.0f}'

# 1. Award Type Overview
print("Generating 1/8: award_type_overview.png")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8), dpi=300)
fig.suptitle('Award Type Overview: 10-Year vs 5-Year Comparison', fontsize=16, fontweight='bold', y=0.98)

# 10-Year panel
award_types = list(data_10yr.keys())
x = np.arange(len(award_types))
width = 0.35

projects_10yr = [data_10yr[at]['projects'] for at in award_types]
investments_10yr = [data_10yr[at]['investment']/1000000 for at in award_types]

bars1 = ax1.bar(x - width/2, projects_10yr, width, label='Projects', color='#7570b3', alpha=0.8)
ax1_twin = ax1.twinx()
bars2 = ax1_twin.bar(x + width/2, investments_10yr, width, label='Investment ($M)', color='#d95f02', alpha=0.8)

ax1.set_xlabel('Award Type', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Projects', fontsize=12, fontweight='bold', color='#7570b3')
ax1_twin.set_ylabel('Investment ($ Millions)', fontsize=12, fontweight='bold', color='#d95f02')
ax1.set_title('10-Year Period (2015-2024)', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(award_types, fontsize=11)
ax1.tick_params(axis='y', labelcolor='#7570b3')
ax1_twin.tick_params(axis='y', labelcolor='#d95f02')
ax1.grid(True, alpha=0.3, axis='y')

# Add value labels
for i, (p, inv) in enumerate(zip(projects_10yr, investments_10yr)):
    ax1.text(i - width/2, p + 1, f'{p}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax1_twin.text(i + width/2, inv + 0.05, f'${inv:.1f}M', ha='center', va='bottom', fontsize=10, fontweight='bold')

# 5-Year panel
projects_5yr = [data_5yr[at]['projects'] for at in award_types]
investments_5yr = [data_5yr[at]['investment']/1000000 for at in award_types]

bars3 = ax2.bar(x - width/2, projects_5yr, width, label='Projects', color='#7570b3', alpha=0.8)
ax2_twin = ax2.twinx()
bars4 = ax2_twin.bar(x + width/2, investments_5yr, width, label='Investment ($M)', color='#d95f02', alpha=0.8)

ax2.set_xlabel('Award Type', fontsize=12, fontweight='bold')
ax2.set_ylabel('Number of Projects', fontsize=12, fontweight='bold', color='#7570b3')
ax2_twin.set_ylabel('Investment ($ Millions)', fontsize=12, fontweight='bold', color='#d95f02')
ax2.set_title('5-Year Period (2020-2024)', fontsize=14, fontweight='bold', pad=15)
ax2.set_xticks(x)
ax2.set_xticklabels(award_types, fontsize=11)
ax2.tick_params(axis='y', labelcolor='#7570b3')
ax2_twin.tick_params(axis='y', labelcolor='#d95f02')
ax2.grid(True, alpha=0.3, axis='y')

# Add value labels
for i, (p, inv) in enumerate(zip(projects_5yr, investments_5yr)):
    if p > 0:
        ax2.text(i - width/2, p + 0.05, f'{p}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    if inv > 0:
        ax2_twin.text(i + width/2, inv + 0.03, f'${inv:.1f}M', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Create combined legend
handles = [bars1, bars2]
labels = ['Projects', 'Investment ($M)']
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.95), ncol=2, fontsize=11)

plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig(os.path.join(output_dir, 'award_type_overview.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 2. Award Type Investment 10-Year
print("Generating 2/8: award_type_investment_10yr.png")
fig, ax = plt.subplots(figsize=(10, 8), dpi=300)

total_10yr = sum([data_10yr[at]['investment'] for at in award_types])
sizes_10yr = [data_10yr[at]['investment'] for at in award_types]
percentages_10yr = [s/total_10yr*100 for s in sizes_10yr]
colors_list = [COLORS[at] for at in award_types]

wedges, texts, autotexts = ax.pie(sizes_10yr, labels=award_types, colors=colors_list,
                                    autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})

# Enhance text
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(13)

for text in texts:
    text.set_fontsize(12)
    text.set_fontweight('bold')

ax.set_title('Award Type Investment Distribution\n10-Year Period (2015-2024)',
             fontsize=16, fontweight='bold', pad=20)

# Add legend with dollar amounts
legend_labels = [f'{at}: {format_currency(data_10yr[at]["investment"])} ({percentages_10yr[i]:.1f}%)'
                 for i, at in enumerate(award_types)]
ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=11)

# Add total in center
total_text = f'Total:\n{format_currency(total_10yr)}'
ax.text(0, 0, total_text, ha='center', va='center', fontsize=14, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray', alpha=0.9))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'award_type_investment_10yr.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 3. Award Type Investment 5-Year
print("Generating 3/8: award_type_investment_5yr.png")
fig, ax = plt.subplots(figsize=(10, 8), dpi=300)

total_5yr = sum([data_5yr[at]['investment'] for at in award_types if data_5yr[at]['investment'] > 0])
# Filter out zero values
award_types_5yr = [at for at in award_types if data_5yr[at]['investment'] > 0]
sizes_5yr = [data_5yr[at]['investment'] for at in award_types_5yr]
percentages_5yr = [s/total_5yr*100 for s in sizes_5yr]
colors_list_5yr = [COLORS[at] for at in award_types_5yr]

wedges, texts, autotexts = ax.pie(sizes_5yr, labels=award_types_5yr, colors=colors_list_5yr,
                                    autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})

# Enhance text
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(13)

for text in texts:
    text.set_fontsize(12)
    text.set_fontweight('bold')

ax.set_title('Award Type Investment Distribution\n5-Year Period (2020-2024)',
             fontsize=16, fontweight='bold', pad=20)

# Add legend with dollar amounts
legend_labels = [f'{at}: {format_currency(data_5yr[at]["investment"])} ({percentages_5yr[i]:.1f}%)'
                 for i, at in enumerate(award_types_5yr)]
ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=11)

# Add total in center
total_text = f'Total:\n{format_currency(total_5yr)}'
ax.text(0, 0, total_text, ha='center', va='center', fontsize=14, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray', alpha=0.9))

# Add note about Coordination
ax.text(0, -1.5, 'Note: Coordination award type had $0 investment in this period',
        ha='center', fontsize=10, style='italic', color='gray')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'award_type_investment_5yr.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 4. Award Type Project Counts
print("Generating 4/8: award_type_project_counts.png")
fig, ax = plt.subplots(figsize=(12, 7), dpi=300)

x = np.arange(len(award_types))
width = 0.35

projects_10yr = [data_10yr[at]['projects'] for at in award_types]
projects_5yr = [data_5yr[at]['projects'] for at in award_types]

bars1 = ax.bar(x - width/2, projects_10yr, width, label='10-Year (2015-2024)',
               color='#1f77b4', alpha=0.8, edgecolor='black', linewidth=0.5)
bars2 = ax.bar(x + width/2, projects_5yr, width, label='5-Year (2020-2024)',
               color='#ff7f0e', alpha=0.8, edgecolor='black', linewidth=0.5)

ax.set_xlabel('Award Type', fontsize=13, fontweight='bold')
ax.set_ylabel('Number of Projects', fontsize=13, fontweight='bold')
ax.set_title('Project Count Comparison by Award Type\n10-Year vs 5-Year Period',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(award_types, fontsize=12)
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
ax.set_axisbelow(True)

# Add value labels on bars
for i, v in enumerate(projects_10yr):
    ax.text(i - width/2, v + 0.5, str(v), ha='center', va='bottom', fontsize=11, fontweight='bold')
for i, v in enumerate(projects_5yr):
    if v > 0:
        ax.text(i + width/2, v + 0.5, str(v), ha='center', va='bottom', fontsize=11, fontweight='bold')
    else:
        ax.text(i + width/2, v, '0', ha='center', va='bottom', fontsize=11, fontweight='bold', color='gray')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'award_type_project_counts.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 5. 104g Subtypes Breakdown
print("Generating 5/8: 104g_subtypes_breakdown.png")
fig, ax = plt.subplots(figsize=(11, 7), dpi=300)

subtypes = list(subtypes_104g.keys())
y_pos = np.arange(len(subtypes))
projects = [subtypes_104g[st]['projects'] for st in subtypes]
investments = [subtypes_104g[st]['investment']/1000000 for st in subtypes]

# Create horizontal bars
colors_subtypes = ['#084594', '#2171b5', '#6baed6']
bars = ax.barh(y_pos, investments, color=colors_subtypes, alpha=0.8, edgecolor='black', linewidth=0.5)

ax.set_yticks(y_pos)
ax.set_yticklabels(subtypes, fontsize=12)
ax.set_xlabel('Investment ($ Millions)', fontsize=13, fontweight='bold')
ax.set_title('104g Award Subtypes Breakdown\nAll-Time Data', fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x', linestyle='--')
ax.set_axisbelow(True)

# Add value labels
for i, (inv, proj) in enumerate(zip(investments, projects)):
    label = f'${inv:.1f}M ({proj} projects)'
    ax.text(inv + 0.1, i, label, va='center', fontsize=11, fontweight='bold')

# Add average per project
ax.text(0.98, 0.02, 'Note: Data shows comprehensive 104g subtype distribution',
        transform=ax.transAxes, ha='right', va='bottom', fontsize=10, style='italic', color='gray')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '104g_subtypes_breakdown.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 6. Award Type Per Project Average
print("Generating 6/8: award_type_per_project_avg.png")
fig, ax = plt.subplots(figsize=(11, 7), dpi=300)

# Calculate averages
avg_10yr = [data_10yr[at]['investment']/data_10yr[at]['projects'] if data_10yr[at]['projects'] > 0 else 0
            for at in award_types]
avg_5yr = [data_5yr[at]['investment']/data_5yr[at]['projects'] if data_5yr[at]['projects'] > 0 else 0
           for at in award_types]

x = np.arange(len(award_types))
width = 0.35

bars1 = ax.bar(x - width/2, [a/1000 for a in avg_10yr], width, label='10-Year (2015-2024)',
               color='#1f77b4', alpha=0.8, edgecolor='black', linewidth=0.5)
bars2 = ax.bar(x + width/2, [a/1000 for a in avg_5yr], width, label='5-Year (2020-2024)',
               color='#ff7f0e', alpha=0.8, edgecolor='black', linewidth=0.5)

ax.set_xlabel('Award Type', fontsize=13, fontweight='bold')
ax.set_ylabel('Average Investment per Project ($K)', fontsize=13, fontweight='bold')
ax.set_title('Average Investment per Project by Award Type\n10-Year vs 5-Year Comparison',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(award_types, fontsize=12)
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
ax.set_axisbelow(True)

# Add value labels on bars
for i, v in enumerate(avg_10yr):
    if v > 0:
        ax.text(i - width/2, v/1000 + 20, f'${v/1000:.0f}K', ha='center', va='bottom',
                fontsize=10, fontweight='bold')

for i, v in enumerate(avg_5yr):
    if v > 0:
        ax.text(i + width/2, v/1000 + 20, f'${v/1000:.0f}K', ha='center', va='bottom',
                fontsize=10, fontweight='bold')
    else:
        ax.text(i + width/2, 0, 'N/A', ha='center', va='bottom', fontsize=10,
                fontweight='bold', color='gray')

# Add insight text
ax.text(0.98, 0.98, '104g projects are ~40x larger than 104b projects on average',
        transform=ax.transAxes, ha='right', va='top', fontsize=11,
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3), fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'award_type_per_project_avg.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 7. Award Type Coverage
print("Generating 7/8: award_type_coverage.png")
fig, ax = plt.subplots(figsize=(11, 7), dpi=300)

# Coverage data
projects_with_data_10yr = 37
projects_missing_10yr = 40
projects_with_data_5yr = 7
projects_missing_5yr = 40

total_10yr_projects = projects_with_data_10yr + projects_missing_10yr
total_5yr_projects = projects_with_data_5yr + projects_missing_5yr

coverage_10yr = projects_with_data_10yr / total_10yr_projects * 100
coverage_5yr = projects_with_data_5yr / total_5yr_projects * 100

x = np.array([0, 1])
width = 0.5

# Stacked bars
bars1 = ax.bar(x, [projects_with_data_10yr, projects_with_data_5yr], width,
               label='Projects with Award Type Data', color='#2ca02c', alpha=0.8, edgecolor='black', linewidth=0.5)
bars2 = ax.bar(x, [projects_missing_10yr, projects_missing_5yr], width,
               bottom=[projects_with_data_10yr, projects_with_data_5yr],
               label='Projects Missing Award Type Data', color='#d62728', alpha=0.8, edgecolor='black', linewidth=0.5)

ax.set_ylabel('Number of Projects', fontsize=13, fontweight='bold')
ax.set_title('Award Type Data Coverage Analysis\nData Quality Assessment',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(['10-Year Period\n(2015-2024)', '5-Year Period\n(2020-2024)'], fontsize=12)
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
ax.set_axisbelow(True)

# Add value labels
ax.text(0, projects_with_data_10yr/2, f'{projects_with_data_10yr}', ha='center', va='center',
        fontsize=12, fontweight='bold', color='white')
ax.text(0, projects_with_data_10yr + projects_missing_10yr/2, f'{projects_missing_10yr}',
        ha='center', va='center', fontsize=12, fontweight='bold', color='white')
ax.text(1, projects_with_data_5yr/2, f'{projects_with_data_5yr}', ha='center', va='center',
        fontsize=12, fontweight='bold', color='white')
ax.text(1, projects_with_data_5yr + projects_missing_5yr/2, f'{projects_missing_5yr}',
        ha='center', va='center', fontsize=12, fontweight='bold', color='white')

# Add coverage percentages
ax.text(0, total_10yr_projects + 2, f'{coverage_10yr:.0f}% Coverage', ha='center', va='bottom',
        fontsize=13, fontweight='bold', color='#2ca02c')
ax.text(1, total_5yr_projects + 2, f'{coverage_5yr:.0f}% Coverage', ha='center', va='bottom',
        fontsize=13, fontweight='bold', color='#d62728')

# Add warning box
warning_text = 'WARNING: Low data coverage indicates significant missing award type information\nData quality improvements needed for comprehensive analysis'
ax.text(0.5, 0.02, warning_text, transform=ax.transAxes, ha='center', va='bottom',
        fontsize=10, bbox=dict(boxstyle='round', facecolor='#ffcccc', edgecolor='#d62728', linewidth=2),
        fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'award_type_coverage.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

# 8. Award Type Comparison 10yr vs 5yr
print("Generating 8/8: award_type_comparison_10yr_vs_5yr.png")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 7), dpi=300)
fig.suptitle('Award Type Distribution: 10-Year vs 5-Year Detailed Comparison',
             fontsize=16, fontweight='bold', y=0.98)

# Left panel - 10-Year
y_pos = np.arange(len(award_types))
investments_10yr_millions = [data_10yr[at]['investment']/1000000 for at in award_types]
colors_list = [COLORS[at] for at in award_types]

bars1 = ax1.barh(y_pos, investments_10yr_millions, color=colors_list, alpha=0.8,
                 edgecolor='black', linewidth=0.5)

ax1.set_yticks(y_pos)
ax1.set_yticklabels(award_types, fontsize=11)
ax1.set_xlabel('Investment ($ Millions)', fontsize=12, fontweight='bold')
ax1.set_title('10-Year Period (2015-2024)', fontsize=14, fontweight='bold', pad=15)
ax1.grid(True, alpha=0.3, axis='x', linestyle='--')
ax1.set_axisbelow(True)

# Add value labels with project counts
for i, (inv, at) in enumerate(zip(investments_10yr_millions, award_types)):
    label = f'${inv:.1f}M ({data_10yr[at]["projects"]} proj)'
    ax1.text(inv + 0.05, i, label, va='center', fontsize=10, fontweight='bold')

# Right panel - 5-Year
investments_5yr_millions = [data_5yr[at]['investment']/1000000 for at in award_types]

bars2 = ax2.barh(y_pos, investments_5yr_millions, color=colors_list, alpha=0.8,
                 edgecolor='black', linewidth=0.5)

ax2.set_yticks(y_pos)
ax2.set_yticklabels(award_types, fontsize=11)
ax2.set_xlabel('Investment ($ Millions)', fontsize=12, fontweight='bold')
ax2.set_title('5-Year Period (2020-2024)', fontsize=14, fontweight='bold', pad=15)
ax2.grid(True, alpha=0.3, axis='x', linestyle='--')
ax2.set_axisbelow(True)

# Add value labels with project counts
for i, (inv, at) in enumerate(zip(investments_5yr_millions, award_types)):
    if inv > 0:
        label = f'${inv:.1f}M ({data_5yr[at]["projects"]} proj)'
        ax2.text(inv + 0.05, i, label, va='center', fontsize=10, fontweight='bold')
    else:
        ax2.text(0.05, i, '$0.0M (0 proj)', va='center', fontsize=10,
                fontweight='bold', color='gray')

# Match x-axis limits for fair comparison
max_x = max(max(investments_10yr_millions), max(investments_5yr_millions))
ax1.set_xlim(0, max_x * 1.15)
ax2.set_xlim(0, max_x * 1.15)

# Add summary statistics
total_10yr_text = f'Total: {format_currency(sum([data_10yr[at]["investment"] for at in award_types]))}'
total_5yr_text = f'Total: {format_currency(sum([data_5yr[at]["investment"] for at in award_types]))}'

ax1.text(0.5, -0.15, total_10yr_text, transform=ax1.transAxes, ha='center',
         fontsize=11, fontweight='bold', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
ax2.text(0.5, -0.15, total_5yr_text, transform=ax2.transAxes, ha='center',
         fontsize=11, fontweight='bold', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(output_dir, 'award_type_comparison_10yr_vs_5yr.png'), dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print("\nAll 8 visualizations generated successfully!")
