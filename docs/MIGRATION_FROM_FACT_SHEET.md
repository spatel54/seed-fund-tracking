# Migrating from Fact Sheet Data to Master Data

**Date:** November 27, 2025
**Purpose:** Guide for migrating analysis from `fact sheet data.xlsx` to master dataset
**Status:** Recommended for all financial calculations

---

## Why Migrate?

### Problem with Fact Sheet Data

`fact sheet data.xlsx` has **critical limitations**:

1. ❌ **No Project ID column** - Cannot deduplicate
2. ❌ **Unknown duplicates** - May contain same project multiple times
3. ❌ **Cannot cross-reference** - No way to match with master data
4. ❌ **Unreliable totals** - Financial sums may be inflated

### Benefits of Master Data

`IWRC Seed Fund Tracking.xlsx` (master) provides:

1. ✅ **Project ID column** - Reliable deduplication
2. ✅ **Verified unique projects** - 122 unique projects total
3. ✅ **Cross-reference capability** - Can match records
4. ✅ **Accurate totals** - Proper deduplication prevents double-counting

---

## When to Migrate

### ✅ **Must Migrate** (Critical)

Migrate immediately if you're doing:
- Financial calculations (investment totals, ROI)
- Student count summaries
- Project counts
- Efficiency metrics ($/project, $/student)
- Any metric reporting

### ⚠️ **Should Consider** (Recommended)

Consider migrating if you're doing:
- Trend analysis over time
- Cross-dataset comparisons
- Reproducible research
- Stakeholder reporting

### ✔️ **Can Keep** (Optional)

Can continue using fact sheet for:
- Keyword frequency analysis
- Geographic visualizations
- 2025-specific descriptive stats
- Quick exploratory analysis (with caveats)

---

## Migration Examples

### Example 1: Investment Calculations

#### ❌ Before (Incorrect - Fact Sheet)

```python
import pandas as pd

# Load fact sheet
df = pd.read_excel('fact sheet data.xlsx', sheet_name='2025 data')

# Calculate investment (MAY DOUBLE-COUNT!)
total_investment = df['Award Amount'].sum()

print(f"Total Investment: ${total_investment:,.2f}")
# Result: $13,404,152 (potentially inflated - 75 rows, unknown duplicates)
```

#### ✅ After (Correct - Master with Data Loader)

```python
from iwrc_data_loader import IWRCDataLoader

# Initialize loader
loader = IWRCDataLoader()

# Load master data with automatic deduplication
df = loader.load_master_data(deduplicate=True)

# Filter to 2025 (or your desired period)
df_2025 = df[df['project_year'] == 2025]

# Calculate metrics (guaranteed deduplicated)
metrics = loader.calculate_metrics(df_2025)

print(f"Total Investment: ${metrics['investment']:,.2f}")
# Result: Accurate, deduplicated value
```

---

### Example 2: Student Counts

#### ❌ Before (Incorrect - Fact Sheet)

```python
df = pd.read_excel('fact sheet data.xlsx', sheet_name='2025 data')

# Sum students (MAY DOUBLE-COUNT!)
total_phd = df['PhD'].sum()
total_ms = df['MS'].sum()
total_ug = df['undergrad'].sum()
total_students = total_phd + total_ms + total_ug

print(f"Total Students: {total_students}")
# May be inflated due to unknown duplicates
```

#### ✅ After (Correct - Master with Data Loader)

```python
from iwrc_data_loader import IWRCDataLoader

loader = IWRCDataLoader()
df = loader.load_master_data(deduplicate=True)
df_2025 = df[df['project_year'] == 2025]

metrics = loader.calculate_metrics(df_2025)

print(f"Total Students: {metrics['students']}")
print(f"  PhD: {metrics['phd']}")
print(f"  Master's: {metrics['masters']}")
print(f"  Undergraduate: {metrics['undergrad']}")
print(f"  Post-Doctoral: {metrics['postdoc']}")
# All values guaranteed deduplicated
```

---

### Example 3: ROI Calculations

#### ❌ Before (Incorrect - Fact Sheet)

```python
df = pd.read_excel('fact sheet data.xlsx', sheet_name='2025 data')

# Calculate ROI (WRONG - denominator may be inflated!)
investment = df['Award Amount'].sum()  # May double-count
followon = 275195  # From elsewhere
roi = followon / investment

print(f"ROI: {roi:.1%}")
# Incorrect - denominator is unreliable
```

#### ✅ After (Correct - Master with Data Loader)

```python
from iwrc_data_loader import IWRCDataLoader

loader = IWRCDataLoader()
df = loader.load_master_data(deduplicate=True)

# Calculate for desired period
metrics = loader.calculate_metrics(df, period='10yr')

print(f"Investment: ${metrics['investment']:,.2f}")
print(f"Follow-on: ${metrics['followon']:,.2f}")
print(f"ROI: {metrics['roi']:.1%}")
# All values accurate and deduplicated
```

---

### Example 4: Keeping Fact Sheet for Visualizations

#### ✅ Mixed Approach (Visualizations + Verified Totals)

```python
import pandas as pd
from iwrc_data_loader import IWRCDataLoader

# Use fact sheet for visualization (keywords, geography)
df_viz = pd.read_excel('fact sheet data.xlsx', sheet_name='2025 data')

# Keyword analysis (SAFE - frequency counts)
keyword_counts = df_viz['Keyword 2'].value_counts()

# Create pie chart
import plotly.express as px
fig = px.pie(values=keyword_counts.values, names=keyword_counts.index,
             title='Research Keywords Distribution')
fig.show()

# But verify financial totals with master data
loader = IWRCDataLoader()
df_master = loader.load_master_data(deduplicate=True)
metrics = loader.calculate_metrics(df_master, period='10yr')

print(f"\n✅ Visualization: Based on fact sheet")
print(f"✅ Financial Total (verified): ${metrics['investment']:,.2f}")
print(f"✅ Student Total (verified): {metrics['students']}")
```

---

## Step-by-Step Migration Guide

### Step 1: Install/Import Data Loader

```python
# Add to top of your script
from iwrc_data_loader import IWRCDataLoader
```

### Step 2: Replace Data Loading

**Old:**
```python
df = pd.read_excel('fact sheet data.xlsx', sheet_name='2025 data')
```

**New:**
```python
loader = IWRCDataLoader()
df = loader.load_master_data(deduplicate=True)
```

### Step 3: Filter to Desired Period

```python
# For specific year
df_2025 = df[df['project_year'] == 2025]

# For 10-year period
df_10yr = df[df['project_year'].between(2015, 2024)]

# For 5-year period
df_5yr = df[df['project_year'].between(2020, 2024)]
```

### Step 4: Calculate Metrics

**Old:**
```python
investment = df['Award Amount'].sum()
students = df['PhD'].sum() + df['MS'].sum() + df['undergrad'].sum()
```

**New:**
```python
metrics = loader.calculate_metrics(df_2025)
investment = metrics['investment']
students = metrics['students']
```

### Step 5: Verify Results

```python
# Print metrics for verification
print(f"Projects: {metrics['projects']}")
print(f"Investment: ${metrics['investment']:,.2f}")
print(f"Students: {metrics['students']}")
print(f"Institutions: {metrics['institutions']}")
print(f"ROI: {metrics['roi']:.1%}")
```

---

## Common Patterns

### Pattern 1: Simple Total

**Before:**
```python
total = df['Award Amount'].sum()
```

**After:**
```python
loader = IWRCDataLoader()
df = loader.load_master_data(deduplicate=True)
metrics = loader.calculate_metrics(df, period='10yr')
total = metrics['investment']
```

### Pattern 2: Grouped Analysis

**Before:**
```python
by_institution = df.groupby('Institution')['Award Amount'].sum()
```

**After:**
```python
loader = IWRCDataLoader()
df = loader.load_master_data(deduplicate=True)
# DataFrame is already deduplicated, safe to group
by_institution = df.groupby('institution')['award_amount_numeric'].sum()
```

### Pattern 3: Time Series

**Before:**
```python
# Not possible with fact sheet (no year field reliable)
```

**After:**
```python
loader = IWRCDataLoader()
df = loader.load_master_data(deduplicate=True)
by_year = df.groupby('project_year')['award_amount_numeric'].sum()
```

---

## Verification Checklist

After migration, verify:

- [ ] Data loader imported correctly
- [ ] Master data loaded with `deduplicate=True`
- [ ] Filtered to correct time period
- [ ] Metrics calculated using `loader.calculate_metrics()`
- [ ] Results match expected corrected values:
  - [ ] 10-Year Investment: ~$3.96M (not $8.5M)
  - [ ] 10-Year Students: ~160 (not 304)
  - [ ] 10-Year ROI: ~7% (not 3%)
- [ ] No `.sum()` calls on raw award_amount without deduplication
- [ ] All financial totals use deduplicated data

---

## Comparison: Old vs New

| Aspect | Fact Sheet (Old) | Master + Data Loader (New) |
|--------|------------------|---------------------------|
| **File** | `fact sheet data.xlsx` | `IWRC Seed Fund Tracking.xlsx` |
| **Loading** | `pd.read_excel()` | `loader.load_master_data()` |
| **Deduplication** | ❌ Impossible | ✅ Automatic |
| **Project ID** | ❌ Missing | ✅ Present |
| **Investment Calc** | `df['Award Amount'].sum()` | `metrics['investment']` |
| **Student Calc** | `df['PhD'].sum()` | `metrics['students']` |
| **Accuracy** | ⚠️ Unreliable | ✅ Verified |
| **10yr Investment** | Unknown (no year) | $3,958,980 |
| **10yr Students** | Unknown | 160 |
| **10yr ROI** | N/A | 7% |

---

## Troubleshooting

### Q: I'm getting different numbers than before

**A:** This is expected! The old fact sheet numbers were likely inflated due to unknown duplicates. The new numbers are correct and deduplicated.

**Verify:**
```python
loader = IWRCDataLoader()
df = loader.load_master_data(deduplicate=True)
validation = loader.validate_data_quality(df)
print(validation)
# Should show duplication_factor: 1.0 (no duplicates)
```

### Q: Can I still use fact sheet for anything?

**A:** Yes! Use it for:
- Keyword visualizations ✅
- Geographic maps ✅
- Descriptive stats ✅

But always cross-verify financial totals with master data.

### Q: What if I need 2025 data specifically?

**A:** Filter master data by year:
```python
df = loader.load_master_data(deduplicate=True)
df_2025 = df[df['project_year'] == 2025]
metrics_2025 = loader.calculate_metrics(df_2025)
```

### Q: My code breaks after migration

**A:** Common issues:
1. Column names changed (e.g., `'Award Amount'` → `'award_amount_numeric'`)
2. Need to call `loader.calculate_metrics()` instead of `.sum()`
3. Check imports: `from iwrc_data_loader import IWRCDataLoader`

---

## Additional Resources

- **Data Loader Documentation:** `analysis/scripts/iwrc_data_loader.py`
- **Fact Sheet Limitations:** `data/consolidated/FACT_SHEET_DATA_README.md`
- **Corrected Files Index:** `CORRECTED_FILES_INDEX.md`
- **Data Quality Audit:** `docs/DATA_QUALITY_AUDIT_REPORT.md`
- **Gemini Integrity Report:** Provided separately

---

## Need Help?

**For questions:**
1. Check `iwrc_data_loader.py` docstrings
2. Review examples in this guide
3. See `DATA_QUALITY_AUDIT_REPORT.md`
4. Contact IWRC Data Quality Team

**Quick Reference:**
```python
# Complete migration template
from iwrc_data_loader import IWRCDataLoader

# Load data
loader = IWRCDataLoader()
df = loader.load_master_data(deduplicate=True)

# Filter period
df_filtered = df[df['project_year'].between(2015, 2024)]

# Calculate metrics
metrics = loader.calculate_metrics(df_filtered, period='10yr')

# Use metrics
print(f"Investment: ${metrics['investment']:,.2f}")
print(f"Students: {metrics['students']}")
print(f"ROI: {metrics['roi']:.1%}")
```

---

**Document Version:** 1.0
**Last Updated:** November 27, 2025
**Maintainer:** IWRC Data Quality Team
