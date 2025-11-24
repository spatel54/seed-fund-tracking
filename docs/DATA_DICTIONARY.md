# IWRC Seed Fund Analysis - Data Dictionary

**Document Version:** 1.0
**Date Generated:** November 23, 2025

---

## Overview

This document defines all columns and fields in the IWRC Seed Fund Tracking spreadsheet and explains the mapping to analysis variables.

---

## Source Spreadsheet Columns

The following columns exist in the source Excel file (`IWRC Seed Fund Tracking.xlsx`):

### Project Identification

| Column Name | Mapped Name | Data Type | Description |
|-------------|-------------|-----------|-------------|
| Project ID  | `project_id` | String | Unique identifier for each project (format: YYYYILnnnXXX) |
| Award Type | `award_type` | String | Type of seed fund award |
| Project Title | `project_title` | String | Full title of the research project |
| Project PI | `pi_name` | String | Principal Investigator name |
| Academic Institution of PI | `institution` | String | University or institution affiliation |

---

### Financial Data

| Column Name | Mapped Name | Data Type | Description |
|-------------|-------------|-----------|-------------|
| Award Amount Allocated ($) this must be filled in for all lines | `award_amount` | Numeric | IWRC seed funding amount in USD |
| Monetary Benefit of Award or Achievement (if applicable; use NA if not applicable) | `monetary_benefit` | String/Numeric | Follow-on funding amount or "NA" |

**Valid Values:**
- Positive numbers (dollar amounts)
- "NA", "N/A", "None" (no funding)
- Text with embedded dollar amounts (e.g., "$500,000 NSF grant")

**Processing:** Text values are parsed to extract numeric dollar amounts.

---

### Student Training Data

| Column Name | Mapped Name | Data Type | Description |
|-------------|-------------|-----------|-------------|
| Number of PhD Students Supported by WRRA $ | `phd_students` | Numeric | Count of PhD students supported |
| Number of MS Students Supported by WRRA $ | `ms_students` | Numeric | Count of Master's students supported |
| Number of Undergraduate Students Supported by WRRA $ | `undergrad_students` | Numeric | Count of undergraduate students supported |
| Number of Post Docs Supported by WRRA $ | `postdoc_students` | Numeric | Count of post-doctoral researchers supported |

**Valid Range:** 0 or positive integers
**Missing Values:** Treated as 0

---

### Awards and Achievements

| Column Name | Mapped Name | Data Type | Description |
|-------------|-------------|-----------|-------------|
| Award, Achievement, or Grant (This may include awards and achievements for projects from the previous year to this 5-year cycle, so long as they were not already included in last year's report) | `awards_grants` | String | Title/name of award, achievement, or grant |
| Description of Award, Achievement, or Grant (This may include awards and achievements for projects from the previous year to this 5-year cycle, so long as they were not already included in last year's report) | `award_description` | String | Detailed description of the award/grant |

---

### Research Classification

| Column Name | Mapped Name | Data Type | Description |
|-------------|-------------|-----------|-------------|
| WRRI Science Priority that Best Aligns with this Project | `science_priority` | String | WRRI priority area classification |
| Keyword (Primary) | `keyword_primary` | String | Primary research keyword |

---

## Derived Fields

The following fields are calculated during analysis:

### project_year
- **Data Type:** Integer
- **Derivation:** Extracted from `project_id` using regex patterns
- **Format:** Four-digit year (e.g., 2020)
- **Logic:**
  - Pattern 1: Extract `20XX` or `19XX` from Project ID
  - Pattern 2: Convert `FYXX` to `20XX`
- **Usage:** Time period filtering (2015-2024, 2020-2024)

### monetary_benefit_clean
- **Data Type:** Numeric (float)
- **Derivation:** Parsed from `monetary_benefit`, `award_description`, and `awards_grants`
- **Processing:**
  1. Check `monetary_benefit` column first
  2. If NA or empty, check `award_description`
  3. If still NA, check `awards_grants`
  4. Extract dollar amounts using regex
  5. Sum multiple amounts if present
- **Valid Range:** 0.0 or positive numbers
- **Usage:** Follow-on funding calculations

### award_category
- **Data Type:** String
- **Derivation:** Categorized from `awards_grants` text
- **Valid Values:**
  - "Grant" (text contains "grant")
  - "Award" (text contains "award")
  - "Achievement" (text contains "achievement")
  - "Other" (all other cases)
  - None (no award/grant reported)

---

## Data Formats and Validation

### Project ID Format

**Expected Pattern:** `YYYYILNNNXXX`

Examples:
- `2020IL103AIS` - Year 2020, IL state, project 103, type AIS
- `FY20IL104BAS` - Fiscal Year 2020, IL state, project 104, type BAS

**Validation:**
- Must contain extractable year (2015-2024)
- Should be unique per project (but may appear multiple times in spreadsheet)

---

### Award Amount Format

**Expected:** Positive numeric value in USD

Examples:
- `50000` (valid)
- `50000.00` (valid)
- `-1000` (invalid - should not be negative)
- `0` (valid - no award amount)

**Validation:**
- Must be numeric
- Should be >= 0
- Missing values treated as 0

---

### Monetary Benefit Format

**Expected:** Dollar amount or "NA"

Valid Examples:
- `$500,000`
- `500000`
- `$1.2M` (processed as 1,200,000)
- `NA`, `N/A`, `None`
- `NSF grant $450,000 over 3 years`

Invalid Examples:
- Random text without dollar amounts
- Negative amounts

**Processing:** Regular expression extracts all numeric dollar amounts and sums them.

---

## Missing Data Handling

| Field Type | Missing Data Treatment |
|------------|----------------------|
| Project ID | Row excluded from analysis |
| Award Amount | Treated as 0 |
| Student Counts | Treated as 0 |
| Monetary Benefit | Treated as 0 (no follow-on funding) |
| Institution | Excluded from institution counts |
| Project Year | Row excluded from time-filtered analysis |

---

## Common Data Issues

### Issue 1: Duplicate Project IDs
- **Cause:** One-row-per-output structure
- **Solution:** Use `nunique()` to count unique projects
- **Impact:** Project counts were inflated by ~3x before correction

### Issue 2: Inconsistent Monetary Formats
- **Cause:** Free-text entry for funding amounts
- **Solution:** Comprehensive regex parsing and cleaning
- **Impact:** Some follow-on funding may be underreported

### Issue 3: Missing Years
- **Cause:** Non-standard Project ID formats
- **Solution:** Multi-pattern regex extraction
- **Impact:** Small number of projects excluded from time analysis

---

## Column Mapping Reference

Quick reference for code-to-spreadsheet mapping:

```python
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
    'Award, Achievement, or Grant': 'awards_grants',
    'Description of Award, Achievement, or Grant': 'award_description',
    'Monetary Benefit of Award or Achievement': 'monetary_benefit',
    'WRRI Science Priority that Best Aligns with this Project': 'science_priority',
    'Keyword (Primary)': 'keyword_primary'
}
```

---

**Data dictionary maintained by:** IWRC Data Analysis Team
**Last updated:** November 23, 2025
