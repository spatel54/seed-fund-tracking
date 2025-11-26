# IWRC Award Type Analysis Guide

**Purpose:** Understanding the dual-track analysis structure and how to work with award type filters.

## Award Type Overview

The IWRC Seed Fund Tracking dataset includes five award types that support water research across Illinois:

| Award Type | Code | Description | Use Case |
|-----------|------|-------------|----------|
| Base Grant | 104b | Core seed funding for water research | Foundation support |
| AIS Research | 104g-AIS | Aquatic Invasive Species research | Specialized research track |
| General Water | 104g-General | General water resource research | Broad water research |
| PFAS Research | 104g-PFAS | PFAS contamination research | Emerging pollutant focus |
| Coordination | Coord | Administrative & strategic projects | Program management |

## Dual-Track Analysis Structure

### Track 1: All Projects (104B + 104G + Coordination)

**Purpose:** Comprehensive view of entire IWRC seed funding portfolio

**Includes:**
- Base Grants (104b) - 60 projects (10-year)
- All 104g variants - 17+ projects (10-year)
- Coordination Grants - strategic projects

**Key Metrics (10-Year: 2015-2024):**
- **Unique Projects:** 77
- **Total Investment:** $8,516,278
- **Students Trained:** 304
- **Institutions:** 16
- **Average Award:** $110,605 per project

**Typical Use Cases:**
- Demonstrate IWRC's full impact
- Show comprehensive institutional reach
- Report total research portfolio
- Present overall ROI and outcomes
- Federal agency reporting requirements

### Track 2: 104B Only (Seed Funding Specific)

**Purpose:** Focus on foundational seed funding that forms the backbone of IWRC support

**Includes:**
- Base Grants (104b) ONLY - 60 projects (10-year)
- Excludes all 104g variants and coordination

**Key Metrics (10-Year: 2015-2024):**
- **Unique Projects:** 60
- **Total Investment:** $1,675,465
- **Students Trained:** 202
- **Institutions:** 16
- **Average Award:** $27,924 per project

**Typical Use Cases:**
- Report on seed funding effectiveness
- Analyze foundational support impact
- Target smaller research grants
- Show accessibility to diverse institutions
- Highlight entry-level funding opportunities

## Comparing the Two Tracks

### Investment Comparison
```
10-Year Period (2015-2024):
┌─────────────────────┬──────────────┬──────────────┐
│ Track               │ Projects     │ Investment   │
├─────────────────────┼──────────────┼──────────────┤
│ All Projects        │ 77           │ $8,516,278   │
│ 104B Only           │ 60           │ $1,675,465   │
│ Difference (104G)   │ 17+          │ $6,840,813   │
└─────────────────────┴──────────────┴──────────────┘
```

### Key Insights
- **104B represents 19.7%** of total investment but supports **77.9%** of projects
- **104G represents 80.3%** of investment but only **22.1%** of projects
- **104B reaches more institutions** with smaller, foundational awards
- **104G enables specialized research** with larger, focused funding

## Using the Filtering Functions

### Python Implementation

#### Load and Filter Data
```python
import pandas as pd
from award_type_filters import (
    filter_all_projects,
    filter_104b_only,
    get_award_type_label,
    get_award_type_short_label
)

# Load data
df = pd.read_excel('data/consolidated/IWRC Seed Fund Tracking.xlsx',
                   sheet_name='Project Overview')

# Filter by award type
df_all = filter_all_projects(df)      # All projects (no filter)
df_104b = filter_104b_only(df)        # Only 104b projects

# Get labels for reporting
label_all = get_award_type_label('all')        # "All Projects (104B + 104G + Coordination)"
label_104b = get_award_type_label('104b')      # "104B Only (Base Grant - Seed Funding)"

short_all = get_award_type_short_label('all')  # "All_Projects"
short_104b = get_award_type_short_label('104b') # "104B_Only"
```

#### Analyze Filtered Data
```python
# Get 10-year period data
df_all_10yr = df_all[df_all['project_year'].between(2015, 2024, inclusive='both')]
df_104b_10yr = df_104b[df_104b['project_year'].between(2015, 2024, inclusive='both')]

# Calculate metrics
projects_all = df_all_10yr['project_id'].nunique()      # 77
projects_104b = df_104b_10yr['project_id'].nunique()    # 60

investment_all = df_all_10yr['award_amount'].sum()      # $8,516,278
investment_104b = df_104b_10yr['award_amount'].sum()    # $1,675,465

students_all = df_all_10yr[['phd_students', 'ms_students',
                             'undergrad_students', 'postdoc_students']].sum().sum()  # 304
students_104b = df_104b_10yr[['phd_students', 'ms_students',
                               'undergrad_students', 'postdoc_students']].sum().sum() # 202
```

### Using in Visualizations

#### Generate Dual-Track Charts
```python
import matplotlib.pyplot as plt
from iwrc_brand_style import IWRC_COLORS, apply_iwrc_matplotlib_style

# Create figure with dual-track data
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# All Projects chart
categories_all = df_all_10yr.groupby('project_year')['project_id'].nunique()
ax1.bar(categories_all.index, categories_all.values, color=IWRC_COLORS['primary'])
ax1.set_title('All Projects (104B + 104G + Coordination)')
ax1.set_ylabel('Projects per Year')

# 104B Only chart
categories_104b = df_104b_10yr.groupby('project_year')['project_id'].nunique()
ax2.bar(categories_104b.index, categories_104b.values, color=IWRC_COLORS['secondary'])
ax2.set_title('104B Only (Seed Funding)')
ax2.set_ylabel('Projects per Year')

apply_iwrc_matplotlib_style(fig, [ax1, ax2])
plt.tight_layout()
plt.savefig('dual_track_comparison.png', dpi=300, bbox_inches='tight')
```

## Award Type Data Quality

### Award Type Distribution
```python
from award_type_filters import get_award_type_distribution

distribution = get_award_type_distribution(df)
print(distribution)

# Output:
# award_type
# Base Grant (104b)      93  ← 93 rows (60 unique projects with multiple entries)
# 104g - General         125
# 104g - AIS             78
# 104g - PFAS            42
# Coordination Grant     16
```

### Data Coverage
- **Award Type Coverage:** 100% of rows have award type classification
- **Project ID Coverage:** 100% of rows identifiable
- **Year Coverage:** 95%+ of rows have valid project years
- **Amount Coverage:** 100% of rows have award amounts

## Reporting Guidelines

### When to Use "All Projects" Track
✓ Federal/state funding reports
✓ Total portfolio impact statements
✓ Comprehensive institution lists
✓ Broad stakeholder presentations
✓ Overall effectiveness demonstrations

### When to Use "104B Only" Track
✓ Seed funding efficacy reports
✓ Entry-level opportunity analysis
✓ Focused funding impact studies
✓ Small grant program reviews
✓ Foundation support demonstrations

## Common Analysis Patterns

### Time Period Filtering
```python
# Common periods
periods = {
    '10year': (2015, 2024),  # 10-year: 77 projects (all), 60 (104b)
    '5year': (2020, 2024),   # 5-year: 47 projects (all), 33 (104b)
    'recent': (2023, 2024),  # Recent 2-year
    'fiscal': (2024, 2024),  # Current fiscal year
}

for period_name, (start, end) in periods.items():
    df_period = df[df['project_year'].between(start, end, inclusive='both')]
    print(f"{period_name}: {df_period['project_id'].nunique()} unique projects")
```

### Institution Analysis
```python
# Top institutions by project count
top_by_projects = df_104b_10yr.groupby('institution')['project_id'].nunique().nlargest(5)
print("Top 5 Institutions by Project Count (104B):")
print(top_by_projects)

# Top institutions by funding
top_by_funding = df_104b_10yr.groupby('institution')['award_amount'].sum().nlargest(5)
print("Top 5 Institutions by Total Funding (104B):")
print(top_by_funding)
```

### Student Impact Analysis
```python
# Students by degree level
student_breakdown = {
    'PhD': df_104b_10yr['phd_students'].sum(),
    'Masters': df_104b_10yr['ms_students'].sum(),
    'Undergraduate': df_104b_10yr['undergrad_students'].sum(),
    'Postdoc': df_104b_10yr['postdoc_students'].sum(),
}

total_students = sum(student_breakdown.values())
print(f"Total Students Trained (104B, 10-year): {int(total_students)}")
for level, count in student_breakdown.items():
    pct = (count / total_students * 100) if total_students > 0 else 0
    print(f"  {level}: {int(count)} ({pct:.1f}%)")
```

## Expected Counts Reference

### 10-Year Analysis (2015-2024)
```
All Projects:     77 unique projects
104B Only:        60 unique projects
104G Total:       17+ additional projects
Coordination:     Projects included in "All" count
```

### 5-Year Analysis (2020-2024)
```
All Projects:     47 unique projects
104B Only:        33 unique projects
Growth since 2015: 30% reduction from 10-year (natural)
```

## Troubleshooting

### Issue: Unexpected Project Counts
**Cause:** Using `len(df)` instead of `df['project_id'].nunique()`
**Solution:** Always use `.nunique()` on project_id for accurate counts
```python
# WRONG: Returns row count
projects = len(df)

# CORRECT: Returns unique project count
projects = df['project_id'].nunique()
```

### Issue: Missing Award Type Filter
**Cause:** Column named "Award Type" instead of "award_type"
**Solution:** Use filter functions which handle normalization
```python
# Will handle both raw and normalized column names
df_104b = filter_104b_only(df)
```

### Issue: Year Extraction Fails
**Cause:** Project ID format not matching regex patterns
**Solution:** Supports multiple formats (2024, FY24, FY2024, etc.)
```python
# Supported formats:
# - 2024 (4-digit year)
# - FY24 (fiscal year 2-digit)
# - FY2024 (fiscal year 4-digit)
# - 2024-104B (year with suffix)
```

## FAQ

**Q: Why is 104B called "Seed Funding"?**
A: 104b grants are smaller, foundational awards designed to seed new research initiatives across a broad range of institutions.

**Q: Can a project appear in both tracks?**
A: Only if it has multiple rows with different award types. However, unique project counts prevent double-counting.

**Q: How do I know which track to use for my report?**
A: Use "All Projects" for comprehensive impact. Use "104B Only" to isolate foundational funding effect.

**Q: What's the difference between projects and rows?**
A: One project can have multiple rows (e.g., for different award components). We count unique projects using `nunique()`.

**Q: Are the metrics validated?**
A: Yes - expected project counts are hardcoded in `award_type_filters.py` and verified during execution.

## References

- Filter Module: `scripts/award_type_filters.py`
- Branding Module: `scripts/iwrc_brand_style.py`
- Master Script: `scripts/generate_final_deliverables.py`
- Data File: `data/consolidated/IWRC Seed Fund Tracking.xlsx`

---

**Last Updated:** November 25, 2025
**Version:** 1.0
**Maintainer:** Claude Code
