# IWRC Seed Fund Analysis - Project Count Correction Summary

## Overview
The original project count analysis was using **row counts** instead of **unique Project IDs**, resulting in significantly inflated project numbers.

## The Problem
- **Original method:** `len(df_filtered)` counted every row in the spreadsheet
- **Issue:** Projects appear multiple times due to different outputs (publications, awards, reporting periods)
- **Result:** Counts were inflated by approximately **2.86x to 3.02x**

## The Solution
- **Corrected method:** `df_filtered['project_id'].nunique()` counts unique Project IDs only
- **Implementation:** Updated analysis notebooks and all dependent visualizations

---

## Corrected Counts

### 10-Year Period (2015-2024)
| Metric | Old Count | Corrected Count | Change |
|--------|-----------|-----------------|--------|
| **Projects** | 220 | **77** | -143 (-65%) |
| **IWRC Investment** | $8.5M | $8.5M | (Same) |
| **Students** | 304 | 304 | (Same) |
| **ROI** | N/A | 0.03x | (Recalculated) |
| **Institutions** | 16 | 16 | (Same) |

### 5-Year Period (2020-2024)
| Metric | Old Count | Corrected Count | Change |
|--------|-----------|-----------------|--------|
| **Projects** | 142 | **47** | -95 (-67%) |
| **IWRC Investment** | $7.3M | $7.3M | (Same) |
| **Students** | 186 | 186 | (Same) |
| **ROI** | N/A | 0.04x | (Recalculated) |
| **Institutions** | 11 | 11 | (Same) |

---

## Files Generated

### New Corrected Files (Copies - Originals Preserved)

#### Notebooks
- **[01_comprehensive_roi_analysis_CORRECTED.ipynb](notebooks/current/01_comprehensive_roi_analysis_CORRECTED.ipynb)**
  - Updated with unique Project ID counting logic
  - Ready to be executed with corrected results

#### Executive Summary Visualization
- **[REVIEW_EXECUTIVE_SUMMARY_CORRECTED.png](visualizations/static/REVIEW_EXECUTIVE_SUMMARY_CORRECTED.png)**
  - Professional infographic with corrected metrics
  - Shows old vs new project counts side-by-side
  - 65% reduction for 10-year, 67% reduction for 5-year

#### Detailed Analysis Charts
- **[iwrc_investment_comparison_corrected.png](visualizations/static/iwrc_investment_comparison_corrected.png)**
- **[roi_comparison_corrected.png](visualizations/static/roi_comparison_corrected.png)**
- **[students_trained_corrected.png](visualizations/static/students_trained_corrected.png)**
- **[project_count_correction.png](visualizations/static/project_count_correction.png)** - Shows correction visually

#### Excel Workbooks
- **[IWRC_ROI_Analysis_Summary_CORRECTED.xlsx](data/outputs/IWRC_ROI_Analysis_Summary_CORRECTED.xlsx)**
  - Executive Summary sheet
  - Investment breakdown
  - Students Trained data
  - Follow-on Funding details

#### Verification Files
- **[project_recount_verification.xlsx](data/outputs/project_recount_verification.xlsx)**
  - Complete list of 77 unique projects (10-year)
  - Complete list of 47 unique projects (5-year)
  - Duplicate analysis showing why counts were inflated
  - Year-by-year breakdown

---

## Why Duplicates Exist

The spreadsheet uses a **one-row-per-output structure**:

- Each project appears once per publication
- Each project appears once per award/achievement
- Each project can appear for different reporting periods
- Each project can have multiple student count entries

**Example:** Project "2020IL103AIS" appears **9 times** with different milestones and publications.

---

## Impact on Other Metrics

The following metrics remain accurate (not affected by the count correction):
- ✅ **IWRC Investment:** Same (based on `award_amount.sum()`)
- ✅ **Students Trained:** Same (based on direct student counts)
- ✅ **Institutions:** Same (based on `institution.nunique()`)
- ✅ **Follow-on Funding:** Same (based on documented grants)

The **ROI calculation** was affected only because denominator changed, but numerator (follow-on funding) remains unchanged.

---

## Recommendation

**Update your official analysis to use the corrected project counts:**
- 10-Year: **77 projects** (not 220)
- 5-Year: **47 projects** (not 142)

These numbers accurately represent the unique research projects funded by IWRC, not the row count in the data source.

---

## Version Control

- **Original Files:** Preserved and unchanged in `notebooks/current/` and `visualizations/static/`
- **Corrected Files:** Created as new copies with `_CORRECTED` suffix
- **Analysis Date:** November 22, 2025
- **Data Source:** Consolidated spreadsheet with combined FY2016-2024 data

---

*Correction methodology verified by counting unique Project IDs instead of spreadsheet rows.*
