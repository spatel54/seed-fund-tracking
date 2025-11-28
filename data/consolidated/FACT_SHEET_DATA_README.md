# Fact Sheet Data - Usage Guidelines & Limitations

**File:** `fact sheet data.xlsx`
**Sheet:** `2025 data`
**Rows:** 75
**Purpose:** 2025-specific visualizations and keyword analysis
**Last Updated:** November 27, 2025

---

## ⚠️ CRITICAL LIMITATIONS

### 1. **No Project ID Column**

This file **DOES NOT HAVE a Project ID column**, which means:
- ❌ Cannot reliably deduplicate projects
- ❌ Cannot cross-reference with master dataset
- ❌ May contain multiple rows per project (unknown)
- ❌ Cannot verify uniqueness of entries

###  2. **Scope Ambiguity**

- Contains **75 rows**
- Master dataset has **77 unique projects** (10-year period)
- **Unclear** if this file represents:
  - A subset of projects
  - A different time period (2025 only?)
  - Duplicate entries for some projects
  - Different data structure entirely

### 3. **Unverifiable Duplicates**

Without Project ID, we cannot determine if:
- Same project appears multiple times
- Award amounts are duplicated
- Student counts are repeated

**Example Risk:**
```
Row 1: PI=Smith, Award=$50,000, Institution=UIUC
Row 2: PI=Smith, Award=$50,000, Institution=UIUC
Are these the same project? Cannot tell without Project ID!
```

---

## Usage Guidelines

### ✅ **SAFE Uses** (Recommended)

These operations do NOT require deduplication:

1. **Keyword Analysis**
   ```python
   df = pd.read_excel('fact sheet data.xlsx', sheet_name='2025 data')
   keyword_counts = df['Keyword 2'].value_counts()  # ✅ Safe
   ```

2. **Geographic Visualizations**
   ```python
   institution_map = df.groupby('Institution')['City'].first()  # ✅ Safe
   ```

3. **Descriptive Statistics**
   ```python
   unique_institutions = df['Institution'].nunique()  # ✅ Safe
   ```

4. **Categorical Distributions**
   ```python
   priority_counts = df['WRRI Science Priority'].value_counts()  # ✅ Safe
   ```

### ⚠️ **CAUTION** (May Double-Count)

These operations may produce inflated results:

1. **Summing Award Amounts**
   ```python
   total = df['Award Amount'].sum()  # ⚠️  May double-count!
   ```

2. **Summing Student Counts**
   ```python
   total_students = df['PhD'].sum() + df['MS'].sum()  # ⚠️  May double-count!
   ```

### ❌ **UNSAFE** (DO NOT Use)

These operations will produce incorrect results:

1. **ROI Calculations**
   ```python
   roi = followon / df['Award Amount'].sum()  # ❌ WRONG - denominator may be inflated
   ```

2. **Financial Reporting**
   ```python
   total_investment = df['Award Amount'].sum()  # ❌ WRONG - cannot verify uniqueness
   ```

3. **Cross-Dataset Comparisons**
   ```python
   # ❌ WRONG - cannot match records without Project ID
   merged = master_df.merge(fact_sheet_df, on='Project ID')
   ```

---

## Recommended Alternatives

### For Accurate Financial Metrics

**DON'T use fact sheet:**
```python
# ❌ WRONG
df = pd.read_excel('fact sheet data.xlsx', sheet_name='2025 data')
investment = df['Award Amount'].sum()
```

**DO use master data:**
```python
# ✅ CORRECT
from iwrc_data_loader import IWRCDataLoader

loader = IWRCDataLoader()
df = loader.load_master_data(deduplicate=True)
df_2025 = df[df['project_year'] == 2025]
metrics = loader.calculate_metrics(df_2025, period='10yr')
investment = metrics['investment']
```

### For Visualizations (Current Use)

**Keep using fact sheet for:**
- Keyword pie charts ✅
- Institution maps ✅
- Geographic distributions ✅

**But cross-verify totals with master dataset!**

---

## Current Usage

### `analysis/notebooks/02_roi_visualizations.ipynb`

This notebook currently uses fact sheet data for:
1. ✅ Keyword pie chart (safe - frequency counts)
2. ✅ Institution map (safe - geographic visualization)

**Updated version includes:**
- ⚠️ Warnings about data limitations
- ✅ Cross-reference with master data for totals
- ✅ Documentation of caveats

---

## Data Structure Comparison

| Feature | Fact Sheet (`fact sheet data.xlsx`) | Master (`IWRC Seed Fund Tracking.xlsx`) |
|---------|-------------------------------------|----------------------------------------|
| **Project ID** | ❌ Missing | ✅ Present (with trailing space) |
| **Rows** | 75 | 354 (dedups to 122 projects) |
| **Deduplication** | ❌ Impossible | ✅ Possible via `project_id` |
| **Cross-Reference** | ❌ Cannot | ✅ Can match projects |
| **Financial Totals** | ❌ Unreliable | ✅ Accurate (with dedup) |
| **Keyword Analysis** | ✅ Safe | ✅ Safe |
| **Geographic Viz** | ✅ Safe | ✅ Safe |

---

## Recommendations

### Short-Term (Keep As-Is)
- ✅ Keep fact sheet for keyword/geography visualizations
- ✅ Add prominent warnings in notebooks using it
- ✅ Cross-verify any totals with master data
- ✅ Document limitations in code comments

### Long-Term (Consider Migration)
- 🔄 Add Project ID column to fact sheet
- 🔄 Or stop using fact sheet for analysis
- 🔄 Migrate all analysis to master dataset
- 🔄 Use fact sheet only for 2025-specific reporting

---

## Example: Safe vs Unsafe Usage

### ❌ Unsafe Example (Current Risk)

```python
# From notebook without warnings
df = pd.read_excel('fact sheet data.xlsx', sheet_name='2025 data')

# This may double-count!
total_funding = df['Award Amount'].sum()
print(f"Total: ${total_funding:,.2f}")  # Could be inflated!

# This may double-count!
total_students = df['PhD'].sum() + df['MS'].sum() + df['undergrad'].sum()
print(f"Students: {total_students}")  # Could be inflated!
```

### ✅ Safe Example (Recommended)

```python
# Use master data with deduplication
from iwrc_data_loader import IWRCDataLoader

loader = IWRCDataLoader()

# Load with automatic deduplication
df = loader.load_master_data(deduplicate=True)

# Filter to 2025
df_2025 = df[df['project_year'] == 2025]

# Calculate metrics (guaranteed deduplicated)
metrics = loader.calculate_metrics(df_2025)

print(f"Total: ${metrics['investment']:,.2f}")  # ✅ Accurate
print(f"Students: {metrics['students']}")  # ✅ Accurate
```

### ✅ Mixed Example (Visualization Only)

```python
# Use fact sheet for visualization
df_viz = pd.read_excel('fact sheet data.xlsx', sheet_name='2025 data')

# Safe: keyword analysis
keywords = df_viz['Keyword 2'].value_counts()
plot_pie_chart(keywords)  # ✅ Safe - frequency counts

# But verify totals with master data
from iwrc_data_loader import IWRCDataLoader
loader = IWRCDataLoader()
df_master = loader.load_master_data(deduplicate=True)
verified_total = loader.calculate_metrics(df_master)['investment']

print(f"Visualization source: fact sheet (for keywords)")
print(f"Financial totals verified with master data: ${verified_total:,.2f}")
```

---

## Questions?

**Why keep this file if it has limitations?**
- Still useful for keyword analysis and geographic visualizations
- User requirement to retain it
- Better to document limitations than delete

**Can we add Project ID to this file?**
- Possible future enhancement
- Would require cross-referencing with master data
- Consider for next update

**Which file should I use?**
- **For analysis/metrics:** Use master data (`IWRC Seed Fund Tracking.xlsx`) with `iwrc_data_loader.py`
- **For visualizations only:** Can use fact sheet with appropriate warnings

**Where's the correct data?**
- ✅ `data/consolidated/IWRC Seed Fund Tracking.xlsx` (master file)
- ✅ `analysis/scripts/iwrc_data_loader.py` (centralized loader)
- ✅ `analysis/scripts/generate_all_visualizations_CORRECTED.py` (correct script)

---

**For More Information:**
- Migration Guide: `docs/MIGRATION_FROM_FACT_SHEET.md`
- Data Quality Audit: `docs/DATA_QUALITY_AUDIT_REPORT.md`
- Corrected Files Index: `CORRECTED_FILES_INDEX.md`

**Last Updated:** November 27, 2025
**Maintainer:** IWRC Data Quality Team
