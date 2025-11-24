# IWRC Seed Fund Analysis - Methodology

**Document Version:** 2.0 (Corrected)
**Date Generated:** November 23, 2025

---

## Overview

This document describes the complete methodology used to analyze the IWRC Seed Fund program's return on investment and impact metrics.

---

## Data Source

### Primary Data File
- **File:** IWRC Seed Fund Tracking.xlsx
- **Sheet:** Project Overview
- **Time Range:** Fiscal Years 2016-2024
- **Total Rows:** 354
- **Total Columns:** 35

### Data Collection
The source spreadsheet consolidates seed fund project data from multiple fiscal years. Each row represents a **project output or milestone**, not a unique project.

---

## Year Extraction Methodology

Project years are extracted from the Project ID field using the following logic:

### 1. Four-Digit Year Extraction
```python
year_match = re.search(r'(20\d{2}|19\d{2})', project_id_str)
```
Extracts full year (e.g., "2020" from "2020IL103AIS")

### 2. Fiscal Year (FY) Format
```python
fy_match = re.search(r'FY(\d{2})', project_id_str, re.IGNORECASE)
```
Converts FY notation (e.g., "FY20" becomes 2020)

### 3. Handling Missing Data
Projects without extractable years are excluded from time-based filtering.

---

## Project Counting Approach

### CRITICAL CORRECTION

**Original (Incorrect) Method:**
```python
num_projects = len(df_filtered)  # Counts all rows
```

**Corrected Method:**
```python
num_projects = df_filtered['project_id'].nunique()  # Counts unique Project IDs
```

### Why This Matters

The source spreadsheet structure causes projects to appear multiple times:

1. **Multiple Publications:** One project = multiple publication rows
2. **Multiple Awards:** One project = multiple achievement rows
3. **Multiple Reporting Periods:** Projects span multiple fiscal years
4. **Multiple Student Entries:** Student counts may be reported separately

**Example:** Project "2020IL103AIS" appears **9 times** in the spreadsheet with different outputs.

### Impact of Correction

| Period | Rows (Old) | Unique Projects (Corrected) | Inflation Factor |
|--------|------------|----------------------------|------------------|
| 10-Year (2015-2024) | 220 | **77** | 2.86x |
| 5-Year (2020-2024) | 142 | **47** | 3.02x |

---

## Time Period Filtering

### 10-Year Period (2015-2024)
```python
df_10yr = df_work[df_work['project_year'].between(2015, 2024, inclusive='both')]
```
- Includes all projects starting between 2015 and 2024
- Projects: **77 unique**
- Rows: **220**

### 5-Year Period (2020-2024)
```python
df_5yr = df_work[df_work['project_year'].between(2020, 2024, inclusive='both')]
```
- Includes all projects starting between 2020 and 2024
- Projects: **47 unique**
- Rows: **142**

---

## Metrics Calculation Formulas

### 1. IWRC Investment
```python
investment = df_filtered['award_amount'].sum()
```
**10-Year:** $8,516,278.00
**5-Year:** $7,319,144.00

**Note:** Not affected by duplicate project rows since award amounts are summed consistently.

---

### 2. Follow-on Funding

#### Extraction Logic
```python
def extract_grant_amount_comprehensive(row):
    # Check monetary_benefit column first
    # Then check award_description column
    # Finally check awards_grants column
    # Return 0.0 if no valid amount found
```

#### Monetary Value Cleaning
```python
def clean_monetary_value(value):
    # Handle NA, N/A, None
    # Extract dollar amounts using regex
    # Sum multiple amounts if present
    # Return 0.0 for invalid entries
```

**10-Year Follow-on Funding:** $275,195.00
**5-Year Follow-on Funding:** $261,000.00

---

### 3. ROI Calculation

```python
roi = follow_on_funding / iwrc_investment
```

**10-Year ROI:** 0.03x ($275,195.00 / $8,516,278.00)
**5-Year ROI:** 0.04x ($261,000.00 / $7,319,144.00)

**Interpretation:** For every $1 of IWRC seed funding, researchers secure $X in follow-on funding.

---

### 4. Student Training

Student totals are calculated by summing across four categories:

```python
students_total = (
    df['phd_students'].sum() +
    df['ms_students'].sum() +
    df['undergrad_students'].sum() +
    df['postdoc_students'].sum()
)
```

**10-Year Total:** 304 students
**5-Year Total:** 186 students

**Note:** Not affected by duplicate project rows since student counts are summed from the original data structure.

---

### 5. Institutional Reach

```python
num_institutions = df_filtered['institution'].nunique()
```

**10-Year:** 16 institutions
**5-Year:** 11 institutions

---

## Data Quality Assurance

### Validation Steps

1. **Project ID Verification**
   - Confirmed all Project IDs follow expected format
   - Verified year extraction accuracy
   - Identified projects without valid years

2. **Duplicate Analysis**
   - Counted occurrences of each Project ID
   - Identified reasons for multiple appearances
   - Verified correction methodology

3. **Financial Data Validation**
   - Checked for negative or zero award amounts
   - Verified monetary value parsing accuracy
   - Handled NA and missing values appropriately

4. **Student Count Validation**
   - Converted all student fields to numeric
   - Handled missing values as zero
   - Verified totals across categories

---

## Limitations and Assumptions

### Limitations

1. **Self-Reported Data:** Follow-on funding amounts are self-reported by PIs
2. **Incomplete Records:** Some projects may not report all follow-on funding
3. **Time Lag:** Recent projects may not yet have follow-on funding
4. **Attribution:** Multiple funding sources may contribute to outcomes

### Assumptions

1. **Award amounts** are accurate and up-to-date
2. **Student counts** represent unique individuals (not duplicated)
3. **Follow-on funding** is directly attributable to IWRC seed funding
4. **Project years** accurately represent project start dates

---

## Reproducibility

All analysis can be reproduced using:

1. **Source Data:** `data/consolidated/IWRC Seed Fund Tracking.xlsx`
2. **Analysis Script:** `scripts/regenerate_analysis.py`
3. **Documentation Script:** `scripts/generate_comprehensive_documentation.py`

### Python Environment
- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- openpyxl

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 18, 2025 | Initial analysis using row counts |
| 2.0 | Nov 22, 2025 | **Corrected to use unique Project IDs** |

---

**Methodology developed by:** IWRC Data Analysis Team
**Last updated:** November 23, 2025
