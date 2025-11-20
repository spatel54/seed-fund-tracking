# IWRC Seed Fund Tracking Analysis - Repository Summary
**Generated:** November 18, 2025  
**Total Size:** 282 MB  
**Status:** Production Ready ✅

---

## 📊 Project Overview

This repository contains comprehensive data analysis for the Illinois Water Resources Center (IWRC) Seed Fund program, tracking research funding, student outcomes, and project impact from fiscal years 2016-2024.

### Key Metrics
- **Total Projects Analyzed:** 539
- **Data Columns Tracked:** 35
- **Fiscal Years Covered:** 2016-2024 (9 years)
- **Analysis Period:** 10-year ROI tracking (2015-2024)

---

## 📁 Repository Structure

```
IWRC Seed Fund Tracking/              (282 MB)
├── data/                              (6.5 MB)
│   ├── source/                        Source Excel files (4 files)
│   ├── consolidated/                  Combined datasets (2 files)
│   └── outputs/                       Analysis results (1 file)
├── notebooks/                         (1.6 MB, 10 notebooks)
│   ├── current/                       Active analysis notebooks (4)
│   └── archive/                       Historical versions (6)
├── visualizations/                    (12 MB)
│   ├── static/                        PNG charts (8 files, 300 DPI)
│   └── interactive/                   HTML visualizations (4 files)
├── scripts/                           (56 KB, 7 Python scripts)
├── docs/                              (88 KB, 7 documentation files)
└── .venv/                             Python virtual environment
```

---

## 🎯 Core Analysis Notebooks

### 1. **Comprehensive ROI Analysis** 
`notebooks/current/01_comprehensive_roi_analysis.ipynb`
- **Purpose:** Complete return on investment calculations
- **Outputs:** 10-year and 5-year ROI metrics
- **Key Findings:**
  - 10-year ROI: **$13.90 per $1 invested**
  - 5-year ROI: **$13.05 per $1 invested**
  - Follow-on funding: **$33.2M** (FY2015-2024)
  - IWRC investment: **$2.5M**

### 2. **ROI Visualizations**
`notebooks/current/02_roi_visualizations.ipynb`
- **Purpose:** Create publication-ready ROI charts
- **Outputs:** Investment comparison, ROI multipliers, student metrics
- **Format:** Excel summaries + PNG charts

### 3. **Interactive HTML Visualizations**
`notebooks/current/03_interactive_html_visualizations.ipynb`
- **Purpose:** Interactive web-based data exploration
- **Outputs:** 
  - Interactive maps (Plotly)
  - Keyword analysis with hover tooltips
  - Geographic institution distribution

### 4. **Fact Sheet Static Charts**
`notebooks/current/04_fact_sheet_static_charts.ipynb`
- **Purpose:** Generate print-ready graphics for reports
- **Outputs:**
  - Illinois institution geographic maps
  - Keyword distribution pie charts (2025)
  - High-resolution PNG images (300 DPI)

---

## 📈 Key Visualizations

### Static Charts (`visualizations/static/`)
| File | Description | Size |
|------|-------------|------|
| `roi_comparison.png` | ROI analysis comparison | 139 KB |
| `iwrc_investment_comparison.png` | Investment vs. matching funds | 95 KB |
| `students_trained.png` | Student training outcomes | 118 KB |
| `student_distribution_pie.png` | Student type distribution | 258 KB |
| `2025_keyword_pie_chart.png` | Research keyword distribution | 248 KB |
| `2025_illinois_institutions_map.png` | Geographic institution map | 715 KB |

### Interactive Visualizations (`visualizations/interactive/`)
| File | Description | Size |
|------|-------------|------|
| `IWRC_ROI_Analysis_Report.html` | Interactive ROI dashboard | 21 KB |
| `2025_keyword_pie_chart_interactive.html` | Interactive keyword analysis | 4.8 MB |
| `2025_illinois_institutions_map_interactive.html` | Interactive institution map | 4.8 MB |
| `Seed_Fund_Tracking_Analysis.html` | Complete analysis report | 888 KB |

---

## 💾 Data Files

### Source Data (`data/source/`)
- `FY24_reporting_IL.xlsx` - FY2024 Illinois reporting (MOST RECENT)
- `FY23_reporting_IL.xlsx` - FY2023 Illinois reporting
- `IWRC-2022-WRRA-Annual-Report-v.101923.xlsx` - FY2022 annual report
- `IL_5yr_FY16_20_2.xlsx` - 5-year aggregate (FY2016-2020)

### Consolidated Data (`data/consolidated/`)
- **`IWRC Seed Fund Tracking.xlsx`** - Main consolidated dataset
  - 539 rows (projects)
  - 35 columns (comprehensive metrics)
- `fact sheet data.xlsx` - Curated data for reports

### Analysis Outputs (`data/outputs/`)
- `IWRC_ROI_Analysis_Summary.xlsx` - Latest ROI calculations with formulas

---

## 🛠️ Utility Scripts (`scripts/`)

| Script | Purpose |
|--------|---------|
| `combine_excel_files_v2.py` | Merge source Excel files into consolidated dataset |
| `execute_notebook.py` | Programmatically execute Jupyter notebooks |
| `execute_notebooks.py` | Batch notebook execution |
| `run_notebooks.py` | Automated notebook runner |
| `run_single_notebook.py` | Single notebook executor |
| `create_summary_visuals.py` | Generate summary visualizations |

---

## 📚 Documentation (`docs/`)

| Document | Purpose |
|----------|---------|
| `QUICK_START_GUIDE.md` | Fast-start guide for common tasks |
| `CLAUDE.md` | Project instructions and architecture |
| `ANALYSIS_SUMMARY.md` | Analysis findings and insights |
| `RESULTS_READY.md` | Latest results and deliverables |
| `NOTEBOOK_REVIEW_REPORT.md` | Notebook quality review |
| `QUICK_FIX_GUIDE.md` | Troubleshooting common issues |
| `REORGANIZATION_NOVEMBER_2025.md` | Repository reorganization details |

---

## 🎓 Student Training Impact

- **Total Students Trained:** 275+ (2015-2024)
  - PhD Students: 143
  - MS Students: 97
  - Undergraduate Students: 35+
  - Post-Doctoral Researchers: Variable

- **Diversity Metrics:**
  - Underrepresented minority students tracked
  - Female student participation tracked
  - Institutional diversity: 10+ institutions across Illinois

---

## 🔬 Research Focus Areas

**Top Keywords (2025 Analysis):**
- Water Quality
- Nutrients
- Climate Change
- Groundwater
- Watershed Management
- Agricultural Impacts
- Contaminants
- Ecology

---

## 🏛️ Institutional Coverage

**Illinois Universities Participating:**
- University of Illinois Urbana-Champaign (Primary)
- Northwestern University
- Southern Illinois University
- Illinois State University
- Governors State University
- And 5+ additional institutions

---

## 📦 Export Package

**Current Export:** `IWRC_Complete_Export_20251118.zip` (5.1 MB)

**Contents:**
- All 4 current analysis notebooks
- All 8 static visualizations (PNG)
- All 4 interactive visualizations (HTML)
- README and reorganization documentation

**Export Structure:**
```
exports_clean/
├── notebooks/              (4 .ipynb files)
├── static/                 (8 PNG images)
├── interactive/            (4 HTML files)
├── README.md
└── REORGANIZATION_NOVEMBER_2025.md
```

---

## 🚀 Quick Start Commands

### Run Analysis
```bash
# Activate virtual environment
source .venv/bin/activate

# Run comprehensive ROI analysis
jupyter notebook notebooks/current/01_comprehensive_roi_analysis.ipynb

# Generate all visualizations
jupyter notebook notebooks/current/02_roi_visualizations.ipynb
```

### Update Data
```bash
# Consolidate new fiscal year data
python3 scripts/combine_excel_files_v2.py
```

### Create Export
```bash
# Create new export package
cd /Users/shivpat/Downloads/Seed\ Fund\ Tracking
zip -r IWRC_Export_$(date +%Y%m%d).zip \
  notebooks/current/*.ipynb \
  visualizations/static/*.png \
  visualizations/interactive/*.html \
  README.md docs/*.md
```

---

## ✅ Recent Changes (November 18, 2025)

### Major Reorganization Completed
- ✅ Removed 26 MB of duplicate files (old exports/ directory)
- ✅ Cleaned up legacy files and temporary data
- ✅ Renamed notebooks with clear, sequential naming
- ✅ Consolidated documentation into docs/ folder
- ✅ Created structured archive for historical notebooks
- ✅ Updated README with current structure

### New Deliverables
- ✅ 2025 Illinois institutions map (static + interactive)
- ✅ 2025 keyword distribution pie chart (static + interactive)
- ✅ Updated ROI calculations through 2024
- ✅ Complete interactive HTML dashboard

---

## 🎯 Production Status

### Ready for Distribution ✅
- All notebooks execute without errors
- All visualizations generated successfully
- Data consolidated and validated
- Documentation complete and current
- Export package created and tested

### Quality Metrics
- **Code Quality:** All notebooks run cleanly
- **Data Integrity:** Source data preserved, backups automated
- **Documentation:** Comprehensive guides and references
- **Reproducibility:** All analyses fully reproducible

---

## 📝 Notes

### Data Processing
- Source files use **multi-level headers** (3 rows) with merged cells
- Consolidation script handles this automatically via `header=[0,1,2]`
- Original source files remain untouched
- Automatic backups created with `_BACKUP` suffix

### Best Practices
- Always work with `notebooks/current/` for latest versions
- Archive executed notebooks to `notebooks/archive/`
- Never modify raw source data
- Run consolidation script after adding new fiscal year data

---

## 📞 Support Resources

- **Project Architecture:** See `docs/CLAUDE.md`
- **Common Tasks:** See `docs/QUICK_START_GUIDE.md`
- **Latest Results:** See `docs/RESULTS_READY.md`
- **Troubleshooting:** See `docs/QUICK_FIX_GUIDE.md`

---

**Repository Maintained By:** IWRC Data Analysis Team  
**Last Updated:** November 18, 2025  
**Python Version:** 3.8+  
**Key Dependencies:** pandas, openpyxl, numpy, matplotlib, seaborn, plotly
