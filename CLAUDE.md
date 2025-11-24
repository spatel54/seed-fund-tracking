# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

The IWRC Seed Fund Tracking project is a comprehensive data analysis initiative for the Illinois Water Resources Center (IWRC). It tracks research funding, student outcomes, and program impact across fiscal years 2016-2024. The project consolidates data from multiple annual reporting files, performs ROI analysis, generates visualizations, and produces professional reports for stakeholders.

**Critical Note:** All metrics use corrected project counts (unique Project IDs) rather than spreadsheet rows. This correction was applied November 2025 due to the source data containing one row per output rather than one row per project.

---

## Architecture Overview

### Core Data Pipeline

```
data/source/          → combine_excel_files_v2.py → data/consolidated/
[Annual reports]                                    [IWRC Seed Fund Tracking.xlsx]
                                                            ↓
                                    regenerate_analysis.py (Core metrics)
                                                            ↓
                        [10-year: 77 projects | 5-year: 47 projects]
                                                            ↓
                    ┌─────────────────┬─────────────────┬──────────────┐
                    ↓                 ↓                 ↓              ↓
            Analysis Notebooks   PDF Reports      Visualizations   Data Outputs
            (notebooks/current/) (FINAL_DELIVERABLES/) (visualizations/) (data/outputs/)
```

### Key Metrics Architecture

All analysis uses **unique Project IDs** for entity counting:

```python
# CORRECT approach (used throughout codebase)
num_projects = df['project_id'].nunique()  # Counts unique projects

# Key metrics calculated from aggregated/summed values (unaffected by deduplication)
investment = df['award_amount'].sum()        # Not duplicated across rows
students = df['phd_students'].sum() + ...    # Summed from all rows
institutions = df['institution'].nunique()   # Uses nunique()
followon_funding = df['monetary_benefit'].sum() # Summed from all rows
```

**Why this matters:** The source data contains one row per publication/award/milestone, not one row per project. A single project can appear 3-9 times. Always use `nunique()` for entity counts and `sum()` for aggregated values.

---

## Data Source & Structure

### Primary Data File
- **Location:** `data/consolidated/IWRC Seed Fund Tracking.xlsx`
- **Sheet:** "Project Overview" (only relevant sheet)
- **Size:** 354 rows × 35 columns
- **Date Range:** FY2016-FY2024
- **Unique Projects:** 77 (10-year), 47 (5-year)

### Column Categories
1. **Project Info:** Project ID, Title, Award Type
2. **Personnel:** PI Name, Email, Institution
3. **Funding:** Award Amount ($), Matching Funds ($)
4. **Students:** PhD, MS, Undergraduate, PostDoc counts (WRRA-funded and matching)
5. **Diversity:** Underrepresented minority, female student data
6. **Research:** Science priorities, keywords, methodologies
7. **Outputs:** Publications, presentations, awards, DOIs, monetary benefits

### Data Characteristics
- **Multi-level headers in source files:** Some source Excel files have headers spanning rows 0-2
- **Column naming inconsistency:** Different fiscal year files use slightly different column names
- **Row duplication:** Each project typically appears 2-9 times (one row per publication/award/milestone)
- **Missing values:** Monetary benefits and follow-on funding are often unreported (treated as $0)

### How to Load Data
```python
import pandas as pd

# Basic load
df = pd.read_excel('data/consolidated/IWRC Seed Fund Tracking.xlsx', sheet_name='Project Overview')

# For source files with multi-level headers
df = pd.read_excel(source_file, sheet_name='Project Overview', header=[0,1,2])
column_names = [col[1] if isinstance(col, tuple) else col for col in df.columns]
df.columns = column_names
```

---

## Common Development Tasks

### 1. Run Core Analysis
The main analysis script regenerates all metrics from consolidated data:
```bash
python3 scripts/regenerate_analysis.py
```
- Loads consolidated data from `data/consolidated/IWRC Seed Fund Tracking.xlsx`
- Extracts project years from Project IDs (regex patterns for "20XX" and "FYXX" formats)
- Creates 10-year (2015-2024) and 5-year (2020-2024) filtered datasets
- Calculates all key metrics using corrected methodology
- Outputs summary statistics to console
- **Time to run:** ~5 seconds

### 2. Update Consolidated Dataset
When new fiscal year data becomes available:
```bash
# 1. Add new Excel file to data/source/
# 2. Run consolidation script
python3 scripts/combine_excel_files_v2.py
```
- Reads all source files from `data/source/`
- Handles multi-level headers intelligently (header=[0,1,2])
- Matches columns between different fiscal years
- Removes duplicate rows
- Creates backup with `_BACKUP` suffix
- Outputs to `data/consolidated/IWRC Seed Fund Tracking.xlsx`
- **Important:** Original source files in `data/source/` are never modified

### 3. Generate Visualizations
Three main visualization workflows:

#### Static PNG Charts (300 DPI, publication-ready)
```bash
python3 scripts/generate_all_static_visualizations.py
# Or individual script:
python3 scripts/generate_static_visualizations.py
```
**Outputs:** `visualizations/static/` (19+ PNG files)

#### Interactive HTML Dashboards (Plotly)
- **Notebook:** `notebooks/current/03_interactive_html_visualizations.ipynb`
- **Outputs:** `FINAL_DELIVERABLES/visualizations/interactive/` (7 HTML files)
- Features: Hover tooltips, zoom, pan, responsive design
- Can be viewed offline in any modern browser

#### Illinois Map (Two approaches available)
- **Matplotlib version** (CURRENT): `scripts/create_illinois_map_final.py`
  - Output: 2-page PDF with geographic map + institution listing table
  - Outputs to: `FINAL_DELIVERABLES/pdfs/2025_illinois_institutions_map.pdf`
- **Plotly version** (ALTERNATIVE): `scripts/convert_map_html_to_pdf.py`
  - Converts interactive Plotly map to PDF
  - Uses kaleido package for rendering
  - May have marker visibility issues in PDF format

### 4. Generate Professional Reports
Two main report generation scripts:

#### PDF Visualizations (Analysis charts)
```bash
python3 scripts/generate_pdf_reports.py
```
**Outputs:**
- `IWRC_ROI_Analysis_Report.pdf` - Multi-page ROI analysis
- `Seed_Fund_Tracking_Analysis.pdf` - Complete seed fund tracking report
- `2025_keyword_pie_chart.pdf` - Research topics distribution
- `2025_illinois_institutions_map.pdf` - Geographic institution map

#### Executive Reports (Professional documents)
```bash
python3 scripts/generate_detailed_reports.py
```
**Outputs:**
- `IWRC_Seed_Fund_Executive_Summary.pdf` (1 page) - Decision-maker overview
- `IWRC_Fact_Sheet.pdf` - General audience summary
- `IWRC_Detailed_Analysis_Report.pdf` (3 pages) - Comprehensive analysis
- `IWRC_Financial_Summary.pdf` - Financial metrics and calculations

All outputs go to `FINAL_DELIVERABLES/reports/` and `FINAL_DELIVERABLES/pdfs/`.

### 5. Run Jupyter Notebooks
The main analytical notebooks (in `notebooks/current/`):

```bash
# Comprehensive ROI analysis (LATEST VERSION)
jupyter notebook notebooks/current/01_comprehensive_roi_analysis.ipynb

# ROI visualizations (generates static charts)
jupyter notebook notebooks/current/02_roi_visualizations.ipynb

# Interactive HTML dashboards (generates Plotly visualizations)
jupyter notebook notebooks/current/03_interactive_html_visualizations.ipynb

# Fact sheet static charts (publication-ready PNGs)
jupyter notebook notebooks/current/04_fact_sheet_static_charts.ipynb
```

**Always use files in `notebooks/current/` as the latest versions.** Archive versions are for historical reference only.

---

## Critical Implementation Details

### Year Extraction from Project IDs
Project years are extracted using regex patterns. Common Project ID formats:
- `2020IL103AIS` → Extracts "2020"
- `FY23-2024-001` → Extracts "23" and converts to 2023
- `2021-WRRA-Proj` → Extracts "2021"

```python
def extract_year_from_project_id(project_id):
    """Extract year from Project ID."""
    project_id_str = str(project_id).strip()

    # Try 4-digit year first
    year_match = re.search(r'(20\d{2}|19\d{2})', project_id_str)
    if year_match:
        return int(year_match.group(1))

    # Try FY format (FY20 = 2020)
    fy_match = re.search(r'FY(\d{2})', project_id_str, re.IGNORECASE)
    if fy_match:
        fy_year = int(fy_match.group(1))
        return 2000 + fy_year if fy_year < 100 else fy_year

    return None
```

### Monetary Value Extraction
Follow-on funding amounts are extracted from multiple columns and cleaned:

```python
def extract_grant_amount_comprehensive(row):
    # Check monetary_benefit column first
    # Then check award_description column (parse dollar amounts from text)
    # Finally check awards_grants column
    # Return 0.0 if no valid amount found
    pass

def clean_monetary_value(value):
    # Handle NA, N/A, None, missing values → 0.0
    # Extract dollar amounts using regex
    # Sum multiple amounts if present
    # Return float
    pass
```

### Project Deduplication
Always use `nunique()` for counting unique projects:
```python
# For filtering by time period
df_10yr = df[df['project_year'].between(2015, 2024, inclusive='both')]

# For counting unique projects (NOT len(df))
num_projects = df_10yr['project_id'].nunique()  # Result: 77
```

---

## Key Metrics & Formulas

### Corrected Metrics (November 2025)
All metrics below use the corrected project counting methodology.

| Metric | 10-Year (2015-2024) | 5-Year (2020-2024) |
|--------|---------------------|-------------------|
| **Unique Projects** | 77 | 47 |
| **IWRC Investment** | $8,516,278 | $7,319,144 |
| **Follow-on Funding** | $275,195 | $261,000 |
| **ROI** | 0.03x | 0.04x |
| **Students Trained** | 304 | 186 |
| **Institutions** | 16 | 11 |
| **Cost per Project** | $110,601 | $155,726 |
| **Students per Project** | 3.9 | 4.0 |

### ROI Calculation
```python
roi = follow_on_funding / iwrc_investment
# 10-year: $275,195 / $8,516,278 = 0.03x
# 5-year: $261,000 / $7,319,144 = 0.04x
```

### Student Distribution (10-year)
```python
total_students = 304
phd_students = 118 (39%)
ms_students = 52 (17%)
undergrad_students = 127 (42%)
postdoc_students = 7 (2%)
```

---

## Directory Structure

```
.
├── data/
│   ├── source/                              # Original annual Excel files (NEVER modify)
│   ├── consolidated/                        # Combined dataset
│   │   └── IWRC Seed Fund Tracking.xlsx    # Primary data source
│   └── outputs/                             # Analysis outputs
├── notebooks/
│   ├── current/                             # ACTIVE NOTEBOOKS (use these)
│   │   ├── 01_comprehensive_roi_analysis.ipynb
│   │   ├── 02_roi_visualizations.ipynb
│   │   ├── 03_interactive_html_visualizations.ipynb
│   │   └── 04_fact_sheet_static_charts.ipynb
│   └── archive/                             # Historical versions
├── scripts/
│   ├── regenerate_analysis.py               # Core metrics calculation
│   ├── combine_excel_files_v2.py            # Data consolidation
│   ├── generate_pdf_reports.py              # Analysis PDFs
│   ├── generate_detailed_reports.py         # Executive reports
│   ├── create_illinois_map_final.py         # Institution map (current)
│   ├── convert_map_html_to_pdf.py           # Map HTML-to-PDF (alternative)
│   └── [other visualization scripts]
├── visualizations/
│   ├── static/                              # PNG charts (300 DPI)
│   │   ├── roi_comparison.png
│   │   ├── investment_comparison.png
│   │   ├── students_trained.png
│   │   └── [15+ other static charts]
│   └── interactive/                         # HTML dashboards
│       ├── index.html                       # Landing page
│       ├── institutional_distribution_map.html
│       ├── roi_analysis_dashboard.html
│       └── [7 total interactive dashboards]
├── docs/
│   ├── METHODOLOGY.md                       # Analysis methodology & formulas
│   ├── CORRECTION_NOTES.md                  # Data correction explanation
│   ├── DATA_DICTIONARY.md                   # Column definitions
│   ├── ANALYSIS_SUMMARY.md                  # Key findings
│   └── [other documentation]
├── FINAL_DELIVERABLES/                      # Professional distribution package
│   ├── README.md                            # Deliverables guide
│   ├── INTERACTIVE_DASHBOARDS_GUIDE.md      # Dashboard viewing instructions
│   ├── reports/                             # Executive PDFs
│   ├── pdfs/                                # Analysis visualizations
│   └── visualizations/                      # All static & interactive
└── PROJECT_ARCHIVES/                        # Temporary/legacy files
```

---

## Important Files to Know

### Data
- **[data/consolidated/IWRC Seed Fund Tracking.xlsx](data/consolidated/IWRC Seed Fund Tracking.xlsx)** - Primary data source (354 rows, 35 columns)

### Documentation
- **[docs/METHODOLOGY.md](docs/METHODOLOGY.md)** - Complete analysis methodology with formulas
- **[docs/CORRECTION_NOTES.md](docs/CORRECTION_NOTES.md)** - Data correction explanation (critical read)
- **[docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md)** - Column definitions and schema
- **[FINAL_DELIVERABLES/README.md](FINAL_DELIVERABLES/README.md)** - Deliverables inventory and usage guide

### Key Scripts
- **[scripts/regenerate_analysis.py](scripts/regenerate_analysis.py)** - Core metrics calculation
- **[scripts/combine_excel_files_v2.py](scripts/combine_excel_files_v2.py)** - Data consolidation
- **[scripts/generate_pdf_reports.py](scripts/generate_pdf_reports.py)** - Analysis PDF generation
- **[scripts/create_illinois_map_final.py](scripts/create_illinois_map_final.py)** - Institution map (matplotlib)

### Active Notebooks
- **[notebooks/current/01_comprehensive_roi_analysis.ipynb](notebooks/current/01_comprehensive_roi_analysis.ipynb)** - Main analysis
- **[notebooks/current/03_interactive_html_visualizations.ipynb](notebooks/current/03_interactive_html_visualizations.ipynb)** - Interactive dashboards

---

## Data Correction Context (November 2025)

### The Issue
The original analysis counted spreadsheet rows (220 for 10-year, 142 for 5-year) instead of unique projects because the source data contains one row per output (publication, award, milestone) rather than one row per project.

### The Fix
Changed project counting from `len(df)` to `df['project_id'].nunique()`, revealing the true count of 77 unique projects (10-year) and 47 (5-year).

### Impact
- Project counts reduced by 2.86x-3.02x
- Cost per project increased from $38,710 to $110,601 (10-year)
- Students per project increased from 1.4 to 3.9 (10-year)
- All other metrics (investment, students, institutions) remained accurate
- **All current reports use corrected counts**

### Files with Corrected Data
- All Python scripts in `scripts/`
- All notebooks in `notebooks/current/`
- All outputs in `FINAL_DELIVERABLES/`
- All documentation in `docs/`

---

## Dependencies & Environment

### Python Packages
```
pandas                  # Data manipulation
numpy                   # Numerical computing
matplotlib              # Static visualizations
seaborn                 # Statistical graphics
plotly                  # Interactive visualizations
openpyxl                # Excel file reading/writing
kaleido                 # Plotly image export (for PDF generation)
```

### Python Version
- **Minimum:** Python 3.8
- **Tested on:** Python 3.13

### Installation
A virtual environment is configured in `.venv/`. To use it:
```bash
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows
```

---

## Working with Git

### Current Configuration
- **Remote:** https://github.com/spatel54/seed-fund-tracking.git
- **User:** Claude Code (claude@anthropic.com)
- **Default branch:** main

### Recent Workflow (November 24, 2025)
```
93cda6d Add comprehensive guide for viewing interactive HTML dashboards
70f3429 Archive temporary project files
c0514e5 Final deliverables and repository reorganization
f9f9c6d Add static PNG versions of all interactive visualizations
```

### When Making Changes
1. **Never force push** to main branch
2. **Always pull** before making changes: `git pull origin main`
3. **Commit messages** should be descriptive (past tense)
4. **Avoid committing:**
   - `.env` files (none present)
   - Credentials or API keys
   - Large binary files (use FINAL_DELIVERABLES for distribution)
   - Notebook checkpoints (`.ipynb_checkpoints/`)

---

## Quality Standards

### Data Integrity
- Source files in `data/source/` are never modified
- Automatic backups created with `_BACKUP` suffix
- All transformations are documented and reproducible
- Always verify metrics against source data

### Analysis Standards
- Use `nunique()` for entity counts (projects, institutions)
- Use `sum()` for aggregated values (funding, students)
- Handle missing values explicitly (treat as 0 for sums)
- Always filter by `project_year` using `.between(start, end, inclusive='both')`

### Visualization Standards
- Static PNGs: 300 DPI for print quality
- PDF Reports: Professional formatting with headers, footers, page numbers
- Interactive HTML: Responsive design, offline-functional
- All charts include title, legend, and data source attribution

### Documentation Standards
- Include methodology explanation in comments
- Document assumptions and limitations
- Update METHODOLOGY.md when changing calculation logic
- Keep README.md synchronized with actual project structure

---

## Common Issues & Solutions

### Issue: "File not found" when loading data
**Solution:** Always use absolute paths or ensure you're in the correct working directory. Data files are in `data/consolidated/`, not in script directories.

### Issue: Year extraction returns None
**Solution:** Check Project ID format. Must contain either:
- A 4-digit year (20XX or 19XX)
- An FY format (FYXX)
Other formats won't extract automatically.

### Issue: Project counts seem wrong
**Solution:** Verify you're using `nunique()` for projects:
```python
# WRONG
num_projects = len(df)

# CORRECT
num_projects = df['project_id'].nunique()
```

### Issue: Monetary value extraction returns 0
**Solution:** Check that the `monetary_benefit` column exists and isn't completely empty. Follow-on funding is often unreported and defaults to 0.

### Issue: Interactive HTML files show blank map
**Solution:**
1. Verify Plotly installation: `pip install plotly`
2. Check that GeoJSON data is available and properly referenced
3. Test in different browser
4. Check browser console for JavaScript errors

---

## When to Use Which Tools

| Task | Tool | Notes |
|------|------|-------|
| Quick metric check | `scripts/regenerate_analysis.py` | Outputs to console in ~5 seconds |
| Update data with new fiscal year | `scripts/combine_excel_files_v2.py` | Creates backup before modifying |
| Generate all static charts | `scripts/generate_all_static_visualizations.py` | Takes 2-3 minutes |
| Generate interactive dashboards | Run notebook: `03_interactive_html_visualizations.ipynb` | Takes 1-2 minutes |
| Create professional reports | `scripts/generate_detailed_reports.py` | Outputs polished PDFs |
| Detailed exploration/analysis | Jupyter notebooks in `notebooks/current/` | Use for interactive analysis |
| Fix Illinois institution map | `scripts/create_illinois_map_final.py` | Matplotlib version is stable |

---

## Future Maintenance

### When Adding New Fiscal Year Data
1. Add Excel file to `data/source/`
2. Run `combine_excel_files_v2.py`
3. Run `regenerate_analysis.py` to verify metrics
4. Update notebooks if column structure changed
5. Regenerate visualizations
6. Update FINAL_DELIVERABLES with latest outputs
7. Commit changes with message: "Update with FY{YEAR} data"

### When Updating Analysis Logic
1. Update the relevant Python script
2. Test thoroughly with known metrics
3. Verify corrected project counting still applies
4. Regenerate all affected outputs
5. Update METHODOLOGY.md
6. Update this CLAUDE.md if architecture changes
7. Commit with descriptive message

### When Creating New Visualizations
1. Place static PNGs in `visualizations/static/`
2. Place interactive HTML in `visualizations/interactive/`
3. Copy to `FINAL_DELIVERABLES/visualizations/`
4. Update `FINAL_DELIVERABLES/README.md`
5. Test all outputs work correctly
6. Commit with message: "Add [visualization name]"

---

**Last Updated:** November 24, 2025
**Next Review:** When new fiscal year data becomes available or analysis methodology changes
