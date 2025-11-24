# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a data analysis project for IWRC (Illinois Water Resources Center) Seed Fund Tracking. The project consolidates data from multiple Excel files spanning fiscal years 2016-2024 (9 years of data) and provides comprehensive analysis of research funding (10-year ROI tracking from 2015-2024), student outcomes, and project impact across Illinois institutions.

**Key Metrics:**
- **539 total projects analyzed**
- **10-year ROI: $13.90 per $1 invested**
- **$33.2M follow-on funding generated**
- **275+ students trained** (PhD, MS, Undergrad, Post-Docs)
- **10+ Illinois institutions** participating

## Repository Structure

```
.
├── data/
│   ├── source/                # Original Excel files from FY16-FY24 (DO NOT MODIFY)
│   ├── consolidated/          # Primary working datasets (2 files)
│   └── outputs/               # Analysis summaries and ROI calculations
├── notebooks/
│   ├── current/               # ACTIVE NOTEBOOKS - Always use these (4 files)
│   └── archive/               # Historical versions (executed notebooks)
├── scripts/                   # Python utility scripts for automation (8 scripts)
├── visualizations/
│   ├── static/                # PNG charts (8 files, 300 DPI)
│   ├── interactive/           # HTML dashboards (4 files, Plotly)
│   └── pdfs/                  # PDF exports of visualizations (4 files)
├── docs/                      # Documentation and guides (6+ files)
└── README.md / REPOSITORY_SUMMARY.md
```

## Data Architecture

### Primary Data File
- **`data/consolidated/IWRC Seed Fund Tracking.xlsx`** (539 rows, 35 columns)
  - Main working dataset with all projects consolidated from FY16-FY24
  - Contains single "Project Overview" sheet
  - Automatic backup created as `IWRC Seed Fund Tracking_BACKUP.xlsx`

### Source Data Files
All located in `data/source/` (NEVER MODIFY):
- `FY24_reporting_IL.xlsx` - FY2024 Illinois reporting (MOST RECENT)
- `FY23_reporting_IL.xlsx` - FY2023 Illinois reporting
- `IWRC-2022-WRRA-Annual-Report-v.101923.xlsx` - FY2022 annual report
- `IL_5yr_FY16_20_2.xlsx` - 5-year aggregate (FY2016-2020)

**Critical:** All source files use **multi-level headers** (3 rows) with merged cells. Consolidation script handles this via `header=[0,1,2]`.

### Key Data Columns (35 total)
- **Project Info:** Project ID, Title, Award Type
- **Personnel:** PI Name, Email, Institution
- **Funding:** Award Amount, Matching Funds
- **Students:** PhD, MS, Undergraduate, Post-Doc (WRRA-funded and matching)
- **Diversity:** Underrepresented minority data, Female student tracking
- **Research:** Science priorities, keywords, methodologies
- **Outputs:** Publications, presentations, awards, DOIs

## Current Analysis Notebooks

**Location:** `notebooks/current/` (ALWAYS USE THESE, NEVER archive versions)

1. **`01_comprehensive_roi_analysis.ipynb`**
   - Complete 10-year ROI analysis (FY2015-2024)
   - Follow-on funding tracking by institution
   - Student training metrics aggregation
   - Outputs: ROI Summary Excel file

2. **`02_roi_visualizations.ipynb`**
   - Investment vs. matching funds charts
   - ROI multiplier comparisons
   - Student impact distribution
   - Outputs: PNG charts + Excel summaries

3. **`03_interactive_html_visualizations.ipynb`**
   - Interactive Plotly maps of Illinois institutions
   - Keyword analysis with hover tooltips
   - Geographic distribution dashboards
   - Outputs: HTML files (4.8+ MB each)

4. **`04_fact_sheet_static_charts.ipynb`**
   - Publication-ready 300 DPI PNG images
   - Illinois institution geographic map
   - Keyword distribution pie charts
   - Outputs: High-resolution PNG files

## Common Commands

### Data Consolidation (Add New Fiscal Year)
```bash
# Add new Excel file to data/source/
# Then run:
python3 scripts/combine_excel_files_v2.py
```
This script:
- Reads all source files with multi-level headers
- Intelligently maps columns using fuzzy matching
- Appends new rows to consolidated dataset
- Creates automatic backup before modifications
- Preserves all data values exactly as they appear (NO cleaning)

### Execute Analysis Notebooks
```bash
# Run specific notebook
jupyter notebook notebooks/current/01_comprehensive_roi_analysis.ipynb

# Or batch run all 4 notebooks
python3 scripts/execute_notebooks.py
```

### Export Distribution Package
```bash
# Update and recreate the complete export
cd /Users/shivpat/Downloads/Seed\ Fund\ Tracking
python3 << 'EOF'
import zipfile, os
files = [
    "notebooks/current/*.ipynb",
    "visualizations/static/*",
    "visualizations/pdfs/*",
    "visualizations/interactive/*",
    "data/consolidated/*",
    "README.md", "docs/*.md"
]
# Create IWRC_Complete_Export_FINAL.zip
EOF
```

### Convert HTML Visualizations to PDF
```bash
python3 scripts/convert_html_to_pdf.py
```

## Important Implementation Details

### Excel Multi-Level Headers
- Source files: 3-row headers with merged cells
- Column names are in **index 1** (second row)
- Read with: `pd.read_excel(file, header=[0,1,2])`
- After reading, flatten to single level for analysis

### Column Mapping in Consolidation Script
The `combine_excel_files_v2.py` uses this strategy:
1. **Exact matching:** Case-insensitive, whitespace-normalized names
2. **Partial matching:** Keywords must have 2+ word overlap
3. **Filters:** Automatically removes "Unnamed" columns
4. **Order:** Maps to existing consolidated columns first

### Data Integrity Rules (CRITICAL)
- **NEVER clean or modify data values** during consolidation
- Preserve exact values from source files (including inconsistent formats)
- Only skip completely empty rows
- Maintain NaN values as-is
- Always create backups before modifying consolidated data

## Visualization Outputs

### Static Charts (`visualizations/static/`)
- `2025_illinois_institutions_map.png` - Interactive-ready geographic map
- `2025_keyword_pie_chart.png` - Research keyword distribution
- `roi_comparison.png` - ROI multiplier comparison
- `iwrc_investment_comparison.png` - Investment vs. matching funds
- `students_trained.png` - Student training outcomes
- `student_distribution_pie.png` - PhD/MS/UG breakdown
- High resolution: 300 DPI, suitable for print

### Interactive Visualizations (`visualizations/interactive/`)
- `2025_illinois_institutions_map_interactive.html` - Plotly geographic map
- `2025_keyword_pie_chart_interactive.html` - Interactive sunburst chart
- `IWRC_ROI_Analysis_Report.html` - ROI dashboard
- `Seed_Fund_Tracking_Analysis.html` - Complete analysis report

### PDF Exports (`visualizations/pdfs/`)
- PDF versions of all major interactive visualizations
- Generated via convert_html_to_pdf.py script

## Dependencies

Required packages (Python 3.8+):
```
pandas>=1.0.0          # Data manipulation
openpyxl>=3.0.0        # Excel file handling (REQUIRED)
numpy>=1.19.0          # Numerical operations
matplotlib>=3.2.0      # Static visualization
seaborn>=0.11.0        # Statistical visualization
plotly>=5.0.0          # Interactive visualization (for HTML outputs)
```

Install all: `pip3 install pandas openpyxl numpy matplotlib seaborn plotly`

## Key Workflows

### Workflow 1: Add New Fiscal Year Data
1. Obtain new Excel file from IWRC
2. Place in `data/source/`
3. Run: `python3 scripts/combine_excel_files_v2.py`
4. Verify row count increased and data looks correct
5. Re-run notebooks to regenerate analyses and visualizations

### Workflow 2: Create Distribution Package
1. Ensure all current notebooks have been executed
2. Verify visualizations are up-to-date in `visualizations/`
3. Run export script to create `IWRC_Complete_Export_FINAL.zip`
4. Zip includes: notebooks, visualizations, data files, documentation

### Workflow 3: Generate New Visualization
1. Create new notebook in `notebooks/current/`
2. Use data from `data/consolidated/IWRC Seed Fund Tracking.xlsx`
3. Save outputs to appropriate `visualizations/` subfolder
4. Update relevant notebook and README

## Version Control Notes

- **Production files:** Notebooks in `notebooks/current/`
- **Backups:** Automatic `_BACKUP.xlsx` files created before consolidation
- **Archives:** Old executed notebooks stored in `notebooks/archive/`
- **Export:** Latest package is `IWRC_Complete_Export_FINAL.zip` (7.5+ MB)
