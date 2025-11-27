# IWRC Seed Fund Tracking Analysis - Repository Summary
**Generated:** November 27, 2025
**Total Size:** 154 MB (down from 282 MB - 45% reduction)
**Status:** Production Ready ✅

---

## 📊 Project Overview

This repository contains comprehensive data analysis for the Illinois Water Resources Center (IWRC) Seed Fund program, tracking research funding, student outcomes, and project impact from fiscal years 2016-2024.

### Key Metrics
- **Total Projects Analyzed:** 77 unique projects
- **Total Investment:** $8,516,278 (10-year), $7,319,144 (5-year)
- **Students Supported:** 304 students (2015-2024)
- **Institutions Funded:** 14 Illinois institutions
- **ROI:** 3% overall return on investment
- **Fiscal Years Covered:** 2016-2024 (9 years)
- **Analysis Period:** 10-year tracking (2015-2024)

---

## 📁 Repository Structure

```
seed-fund-tracking/                     (154 MB)
├── index.html                          Main navigation hub (START HERE)
├── README.md                           Repository overview
│
├── deliverables/                       All final outputs (57 files)
│   ├── index.html                      Deliverables navigation
│   ├── reports/                        6 PDF reports
│   │   ├── executive/                  3 executive reports
│   │   │   ├── executive_summary.pdf
│   │   │   ├── fact_sheet.pdf
│   │   │   └── financial_summary.pdf
│   │   └── detailed/                   3 detailed reports
│   │       ├── detailed_analysis_report.pdf
│   │       ├── project_type_analysis_104b_only.pdf
│   │       └── project_type_analysis_all_projects.pdf
│   └── visualizations/
│       ├── static/                     36 PNG charts (300 DPI)
│       │   ├── overview/               4 files
│       │   ├── institutions/           4 files
│       │   ├── students/               3 files
│       │   ├── topics/                 7 files
│       │   ├── awards/                 10 files
│       │   └── project_types/          8 files
│       │       ├── 104b_only/          6 files
│       │       └── all_projects/       2 files
│       └── interactive/                15 HTML dashboards
│           ├── index.html              Interactive dashboards hub
│           ├── core/                   5 dashboards
│           ├── geographic/             2 maps + guide
│           ├── award_types/            3 dashboards
│           └── project_types/          4 dashboards
│
├── data/                               Source + processed data
│   ├── source/                         Original FY reports (4 files)
│   ├── consolidated/                   Main tracking database (2 files)
│   └── outputs/                        Analysis results (1 file)
│
├── analysis/                           All analysis code
│   ├── notebooks/                      7 Jupyter notebooks
│   │   ├── current/                    Active notebooks (7)
│   │   └── archive/                    Historical versions
│   └── scripts/                        44 Python scripts
│
├── assets/                             Branding and design
│   ├── branding/                       IWRC brand assets
│   │   ├── logos/                      PNG + SVG logos
│   │   ├── fonts/                      Montserrat fonts
│   │   └── IWRC_BRANDING_GUIDELINES.md
│   └── styles/                         Shared CSS theme
│       └── iwrc-theme.css
│
└── docs/                               Documentation (22 files)
    ├── README.md                       Documentation index
    ├── METHODOLOGY.md                  Analysis methodology
    ├── DATA_DICTIONARY.md              Data structure guide
    ├── FINDINGS.md                     Research findings
    ├── REORGANIZATION_NOVEMBER_2025.md Repository reorganization
    └── REPOSITORY_SUMMARY.md           This file
```

---

## 🎯 Core Analysis Notebooks

### Location: `analysis/notebooks/current/`

### 1. **Comprehensive ROI Analysis**
`01_comprehensive_roi_analysis.ipynb`
- **Purpose:** Complete return on investment calculations
- **Outputs:** 10-year and 5-year ROI metrics
- **Key Findings:**
  - Total investment tracked: $8.5M (10-year)
  - Follow-on funding analysis
  - ROI comparisons across fiscal years

### 2. **ROI Visualizations**
`02_roi_visualizations.ipynb`
- **Purpose:** Create publication-ready ROI charts
- **Outputs:** Investment comparison, ROI multipliers, student metrics
- **Format:** Excel summaries + PNG charts

### 3. **Interactive HTML Visualizations**
`03_interactive_html_visualizations.ipynb`
- **Purpose:** Interactive web-based data exploration
- **Outputs:**
  - Interactive maps (Plotly)
  - Institutional distribution analysis
  - Geographic visualization

### 4. **Fact Sheet Static Charts**
`04_fact_sheet_static_charts.ipynb`
- **Purpose:** Generate print-ready graphics for reports
- **Outputs:**
  - Illinois institution geographic maps
  - High-resolution PNG images (300 DPI)
  - Summary visualizations

### 5. **Project Type Breakdown**
`05_project_type_breakdown.ipynb`
- **Purpose:** Analyze project composition and trends
- **Outputs:** Project type breakdowns by award type

### 6. **Interactive Breakdown**
`06_interactive_breakdown.ipynb`
- **Purpose:** Create interactive project type dashboards
- **Outputs:** HTML dashboards with filtering and drill-down

### 7. **Award Type Analysis**
`07_award_type_analysis.ipynb`
- **Purpose:** Deep dive into award type distribution
- **Outputs:** Award type comparisons and trends

---

## 📈 Key Deliverables

### Executive Reports (3 PDFs)
Located: `deliverables/reports/executive/`

| File | Description | Size |
|------|-------------|------|
| `executive_summary.pdf` | Program overview with key metrics (2015-2024) | 38 KB |
| `fact_sheet.pdf` | One-page impact snapshot | 33 KB |
| `financial_summary.pdf` | Financial metrics and ROI analysis | 22 KB |

### Detailed Reports (3 PDFs)
Located: `deliverables/reports/detailed/`

| File | Description | Size |
|------|-------------|------|
| `detailed_analysis_report.pdf` | Comprehensive analysis with charts and insights | 342 KB |
| `project_type_analysis_104b_only.pdf` | 104B base grant project breakdown | 24 KB |
| `project_type_analysis_all_projects.pdf` | Complete project type breakdown | 25 KB |

### Static Visualizations (36 PNGs)
Located: `deliverables/visualizations/static/`

**Overview (4 files):**
- Investment breakdown
- Investment comparison
- ROI comparison
- Projects by year

**Institutions (4 files):**
- Institutional reach
- Investment by institution
- Top institutions
- University funding comparison

**Students (3 files):**
- Students trained
- Students trained breakdown
- Student distribution pie

**Topics (7 files):**
- Topic areas funding
- Topic areas pyramid (multiple variants)
- Topic areas analysis

**Awards (10 files):**
- Award breakdown
- Award type overview (5-year, 10-year, full)
- Award type investment (5-year, 10-year, full)
- Award type average per project (5-year, 10-year, full)

**Project Types (8 files):**
- 104B Only (6): Stacked/grouped investment/count/students
- All Projects (2): 5-year and 10-year composition

### Interactive Visualizations (15 HTML)
Located: `deliverables/visualizations/interactive/`

**Core Dashboards (5):**
- ROI analysis dashboard
- Detailed analysis
- Investment interactive
- Students interactive
- Projects timeline

**Geographic (2 + guide):**
- Institutional distribution map
- Illinois institutions map (enhanced)
- MAP_GUIDE.md

**Award Types (3):**
- Award type dashboard
- Award type comparison
- Award type deep dive

**Project Types (4):**
- Interactive ROI dashboard
- Interactive topic distribution
- Project type breakdown (104B only)
- Project type breakdown (all projects)

---

## 💾 Data Files

### Source Data (`data/source/`)
- `FY24_reporting_IL.xlsx` - FY2024 Illinois reporting (MOST RECENT)
- `FY23_reporting_IL.xlsx` - FY2023 Illinois reporting
- `IWRC-2022-WRRA-Annual-Report-v.101923.xlsx` - FY2022 annual report
- `IL_5yr_FY16_20_2.xlsx` - 5-year aggregate (FY2016-2020)

### Consolidated Data (`data/consolidated/`)
- **`IWRC Seed Fund Tracking.xlsx`** - Main consolidated dataset
  - 77 unique projects
  - 35 columns (comprehensive metrics)
  - Complete tracking (2015-2024)

### Analysis Outputs (`data/outputs/`)
- `IWRC_ROI_Analysis_Summary.xlsx` - Latest ROI calculations with formulas

---

## 🛠️ Utility Scripts (`analysis/scripts/`)

**44 Python scripts organized by function:**

### Generation Scripts
- Report generation (PDF, Excel, interactive)
- Visualization generation (static, interactive)
- Dashboard creation
- Map generation

### Execution Scripts
- Notebook execution automation
- Batch processing
- Analysis pipeline

### Utility Scripts
- Data consolidation
- Brand styling
- Format conversion

---

## 📚 Documentation (`docs/`)

**22 comprehensive documentation files:**

### Core Documentation
- `METHODOLOGY.md` - Analysis approach
- `DATA_DICTIONARY.md` - Column definitions
- `FINDINGS.md` - Research insights
- `ANALYSIS_SUMMARY.md` - Overview

### User Guides
- `AWARD_TYPE_ANALYSIS_GUIDE.md` - Award types explained
- `FINAL_DELIVERABLES_GUIDE.md` - Deliverables structure
- `EXPORT_TO_PDF_GUIDE.md` - PDF export instructions

### Technical Documentation
- `REORGANIZATION_NOVEMBER_2025.md` - November 2025 reorganization
- `REBRANDING_SUMMARY.md` - IWRC branding implementation
- `REPOSITORY_SUMMARY.md` - This file

---

## 🎨 IWRC Branding

### Brand Colors
- **Primary:** #258372 (Teal)
- **Secondary:** #639757 (Olive)
- **Text:** #54595F (Gray)
- **Accent:** #FCC080 (Peach)

### Typography
- **Font Family:** Montserrat
- **Weights:** Regular (400), Bold (700)
- **Headers:** Bold weight
- **Body:** Regular weight

### Assets Location
`assets/branding/`
- Logos: PNG + SVG formats
- Fonts: Montserrat Regular + Bold
- Guidelines: Complete brand specifications

---

## 🎓 Student Training Impact

- **Total Students Trained:** 304 (2015-2024)
  - PhD Students: ~143
  - MS Students: ~97
  - Undergraduate Students: ~35+
  - Post-Doctoral Researchers: Variable

- **Diversity Metrics:**
  - Underrepresented minority students tracked
  - Female student participation tracked
  - Institutional diversity: 14 institutions across Illinois

---

## 🏛️ Institutional Coverage

**14 Illinois Institutions Participating:**
- University of Illinois Urbana-Champaign (Primary)
- Northwestern University
- Southern Illinois University
- Illinois State University
- Governors State University
- And 9 additional institutions

---

## 🚀 Quick Start Commands

### Navigate Repository
```bash
# Open main navigation hub
open index.html

# Open deliverables hub
open deliverables/index.html

# View interactive dashboards
open deliverables/visualizations/interactive/index.html
```

### Run Analysis
```bash
# Activate virtual environment (if using)
source .venv/bin/activate

# Launch Jupyter
jupyter notebook analysis/notebooks/

# Execute all notebooks
python analysis/scripts/execute_notebooks.py

# Generate final deliverables
python analysis/scripts/generate_final_deliverables_v2.py
```

### Update Data
```bash
# Add new FY report to data/source/
# Update consolidated database
# Run analysis notebooks
# Regenerate deliverables
```

---

## ✅ Recent Changes (November 27, 2025)

### Major Reorganization Completed
- ✅ **45% size reduction** - From 282 MB to 154 MB
- ✅ Removed 128 MB of duplicates (SKIP/, FINAL_DELIVERABLES folders)
- ✅ Created logical folder structure (deliverables, analysis, data, assets)
- ✅ Reorganized 57 deliverable files with clear naming
- ✅ Created 13 README.md files for documentation
- ✅ Built 2 IWRC-branded index.html navigation hubs
- ✅ Consolidated all branding assets
- ✅ Moved all code to analysis/ folder
- ✅ Updated all documentation

### New Navigation System
- ✅ Main index.html with 6 navigation cards
- ✅ Deliverables index.html with categorized outputs
- ✅ Professional IWRC branding throughout
- ✅ Responsive design for all devices
- ✅ Breadcrumb navigation

### Deliverables Organization
- ✅ 6 PDFs renamed and categorized (executive + detailed)
- ✅ 36 PNGs organized by category (overview, institutions, students, topics, awards, project types)
- ✅ 15 HTML dashboards organized (core, geographic, award types, project types)

---

## 🎯 Production Status

### Ready for Distribution ✅
- All notebooks execute without errors
- All visualizations generated successfully
- Data consolidated and validated
- Documentation complete and current
- Professional navigation interface
- IWRC branding applied throughout

### Quality Metrics
- **Code Quality:** All notebooks run cleanly
- **Data Integrity:** Source data preserved, backups automated
- **Documentation:** Comprehensive guides (22 files)
- **Reproducibility:** All analyses fully reproducible
- **Organization:** Logical, intuitive structure
- **Accessibility:** Easy navigation for all user types

---

## 📝 Notes

### Repository Organization
- **Deliverables first:** All final outputs in dedicated folder
- **Analysis separated:** All code in analysis/ folder
- **Assets centralized:** All branding in assets/ folder
- **Documentation complete:** README in every major folder
- **Navigation easy:** Professional index.html pages

### Best Practices
- Start with index.html for navigation
- Use deliverables/ for final outputs
- Run notebooks from analysis/notebooks/current/
- Never modify raw source data
- Follow IWRC branding guidelines

### File Naming Conventions
- **PDFs:** lowercase_with_underscores.pdf
- **PNGs:** descriptive_name_with_suffix.png
- **HTML:** descriptive_dashboard_name.html
- **Time variants:** _5_year, _10_year, _full suffixes

---

## 📞 Support Resources

- **Quick Start:** See main README.md
- **Methodology:** See docs/METHODOLOGY.md
- **Findings:** See docs/FINDINGS.md
- **Reorganization:** See docs/REORGANIZATION_NOVEMBER_2025.md
- **Navigation:** Open index.html

---

**Repository Maintained By:** IWRC Data Analysis Team
**Last Updated:** November 27, 2025
**Python Version:** 3.8+
**Key Dependencies:** pandas, openpyxl, numpy, matplotlib, seaborn, plotly, folium, reportlab
