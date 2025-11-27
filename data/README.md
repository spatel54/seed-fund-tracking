# Data

## Overview
Source data, consolidated datasets, and analysis outputs for the IWRC Seed Fund Tracking & Analysis System.

## Directory Structure

### source/
Original Excel files from IWRC reporting:
- `FY23_reporting_IL.xlsx` (323 KB) - FY2023 data
- `FY24_reporting_IL.xlsx` (285 KB) - FY2024 data
- `IL_5yr_FY16_20_2.xlsx` (195 KB) - FY2016-2020 data
- `IWRC-2022-WRRA-Annual-Report-v.101923.xlsx` (319 KB) - 2022 annual report

### consolidated/
Processed and consolidated datasets:
- `IWRC Seed Fund Tracking.xlsx` (125 KB) - **Main working file** with all projects (2015-2024)
- `IWRC Seed Fund Tracking_BACKUP.xlsx` (131 KB) - Backup version
- `fact sheet data.xlsx` (1.9 MB) - Fact sheet source data

### outputs/
Analysis results and generated reports:
- `IWRC_Award_Type_Analysis.xlsx` (6 KB)
- `IWRC_Detailed_Project_Analysis.xlsx` (26 KB)
- `IWRC_Financial_Summary.xlsx` (7 KB)
- `IWRC_ROI_Analysis_Summary.xlsx` (9 KB)
- `illinois_counties.json` (3.2 MB) - GeoJSON for mapping

## Main Dataset Structure

**File:** `consolidated/IWRC Seed Fund Tracking.xlsx`

**Sheets:**
- Project Overview - Main project data (539 projects, FY2016-2024)
- Follow-on Funding - External funding secured
- ROI Calculations - Return on investment metrics
- Metadata - Data dictionary and notes

**Key Columns:**
- Project ID, Year, Institution
- Award Type (104g, 104b, Coordination)
- Investment Amount, Follow-on Funding
- Students (PhD, MS, Undergrad, PostDoc)
- PI Name, Department, Email
- Science Priority, Keywords
- Project Summary

## Data Period
- **Years:** Fiscal Year 2016 - Fiscal Year 2024
- **Projects:** 539 total entries
- **Analysis Period:** 2015-2024 (10-year period for most deliverables)
- **Unique Projects:** 77 (2015-2024 subset)

## Update Procedure
1. Place new annual report in `source/`
2. Update `consolidated/IWRC Seed Fund Tracking.xlsx`
3. Re-run analysis notebooks
4. Regenerate reports and visualizations

## Last Updated
November 27, 2025 - Data through FY2024
