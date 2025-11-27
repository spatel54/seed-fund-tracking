# IWRC Seed Fund Tracking & Analysis System

**Illinois Water Resources Center (IWRC)** - Comprehensive tracking and analysis of research funding, student outcomes, and project impact across fiscal years 2016-2024.

## 🎯 Quick Start

**[Open Navigation Hub](index.html)** - Professional IWRC-branded interface to browse all content

## 📊 Repository Overview

This repository contains:
- **77 projects** analyzed (2015-2024)
- **$8.5 million** in investment tracked
- **304 students** supported
- **14 Illinois institutions** funded

### November 2025 - Major Repository Reorganization

The repository has been completely reorganized with improved structure, IWRC branding, and comprehensive navigation:

✅ **Clean Organization** - Logical separation of deliverables, analysis, data, and assets
✅ **IWRC Branding** - Professional branded index pages and CSS theme
✅ **Comprehensive Documentation** - README.md in every major folder
✅ **45% Size Reduction** - Removed 128 MB of duplicates (282 MB → 154 MB)
✅ **Improved Navigation** - Card-based navigation hubs with breadcrumbs

## 📁 Repository Structure

```
seed-fund-tracking/
├── index.html                    # 🏠 Main navigation hub (START HERE)
├── README.md                     # This file
│
├── deliverables/                 # 📊 All final outputs
│   ├── index.html                # Deliverables navigation
│   ├── reports/                  # 6 PDF reports
│   │   ├── executive/            # Executive summary, fact sheet, financial
│   │   └── detailed/             # Detailed analysis, project breakdowns
│   └── visualizations/           # Charts and dashboards
│       ├── static/               # 36 PNG charts (by category)
│       └── interactive/          # 15 HTML dashboards
│
├── data/                         # 📁 Source and processed data
│   ├── source/                   # Original FY reports
│   ├── consolidated/             # Main tracking database
│   └── outputs/                  # Analysis results
│
├── analysis/                     # 🔬 Analysis code
│   ├── notebooks/                # 7 Jupyter notebooks
│   └── scripts/                  # 44 Python scripts
│
├── assets/                       # 🎨 Branding and design
│   ├── branding/                 # Logos, fonts, guidelines
│   └── styles/                   # Shared CSS theme
│
└── docs/                         # 📚 Documentation (22 files)
```

## 🚀 Quick Access

### For Stakeholders & Leadership
- [Executive Summary PDF](deliverables/reports/executive/executive_summary.pdf) - High-level overview
- [Fact Sheet PDF](deliverables/reports/executive/fact_sheet.pdf) - One-page snapshot
- [Interactive Dashboards](deliverables/visualizations/interactive/index.html) - Browse visualizations

### For Researchers & Analysts
- [Main Dataset](data/consolidated/IWRC%20Seed%20Fund%20Tracking.xlsx) - Consolidated tracking database
- [Analysis Notebooks](analysis/notebooks/) - Jupyter notebooks for analysis
- [Methodology Documentation](docs/METHODOLOGY.md) - Analysis approach

### For Developers
- [Analysis Scripts](analysis/scripts/) - Python generation scripts
- [Branding Guidelines](assets/branding/IWRC_BRANDING_GUIDELINES.md) - Colors, fonts, logos
- [Repository Summary](REPOSITORY_SUMMARY.md) - Detailed structure overview

## 📊 Deliverables Summary

### Reports (6 PDFs)
**Executive Reports:**
- Executive Summary (38 KB) - Program overview with key metrics
- Fact Sheet (33 KB) - One-page impact snapshot
- Financial Summary (22 KB) - ROI and financial analysis

**Detailed Reports:**
- Detailed Analysis Report (342 KB) - Comprehensive analysis with charts
- Project Type Analysis - 104B Only (24 KB) - Base grant breakdown
- Project Type Analysis - All Projects (25 KB) - Complete breakdown

### Visualizations (51 total)
**Static Charts (36 PNGs)** - Organized by category:
- Overview (4): Investment, ROI, project trends
- Institutions (4): Reach, funding distribution
- Students (3): Training outcomes
- Topics (7): Research area analysis
- Awards (10): Award type comparisons
- Project Types (8): Type breakdowns

**Interactive Dashboards (15 HTML)**:
- Core (5): ROI, detailed analysis, investment, students, timeline
- Geographic (2): Illinois institutions maps
- Award Types (3): Award analysis dashboards
- Project Types (4): Interactive breakdowns

## 💻 Technical Setup

### Prerequisites
```bash
# Python 3.8+ required
pip install pandas numpy matplotlib plotly openpyxl reportlab folium
```

### Running Analysis
```bash
# Launch Jupyter for notebooks
jupyter notebook analysis/notebooks/

# Run specific analysis scripts
python analysis/scripts/generate_static_visualizations.py
```

### Generating Deliverables
```bash
# Execute all notebooks in order
python analysis/scripts/execute_notebooks.py

# Generate final reports and visualizations
python analysis/scripts/generate_final_deliverables_v2.py
```

## 📖 Documentation

### Core Docs
- [METHODOLOGY.md](docs/METHODOLOGY.md) - Analysis methodology
- [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) - Data structure and columns
- [FINDINGS.md](docs/FINDINGS.md) - Research findings

### Guides
- [AWARD_TYPE_ANALYSIS_GUIDE.md](docs/AWARD_TYPE_ANALYSIS_GUIDE.md) - Award types explained
- [FINAL_DELIVERABLES_GUIDE.md](docs/FINAL_DELIVERABLES_GUIDE.md) - Deliverables structure
- [REORGANIZATION_NOVEMBER_2025.md](docs/REORGANIZATION_NOVEMBER_2025.md) - November reorganization

### All Documentation
See [docs/](docs/) folder for complete documentation (22 files)

## 🎨 IWRC Branding

### Brand Colors
- **Primary:** #258372 (Teal)
- **Secondary:** #639757 (Olive)
- **Text:** #54595F (Gray)
- **Accent:** #FCC080 (Peach)

### Typography
- **Font Family:** Montserrat (Regular, Bold)
- **Headers:** Bold weight
- **Body:** Regular weight

See [IWRC_BRANDING_GUIDELINES.md](assets/branding/IWRC_BRANDING_GUIDELINES.md) for complete specifications.

## 📈 Key Metrics (2015-2024)

- **Projects:** 77 unique projects
- **Investment:** $8,516,278 (10-year), $7,319,144 (5-year)
- **Students:** 304 total trained
- **Institutions:** 14 Illinois institutions
- **ROI:** 3% overall return on investment

## 🔄 Data Updates

### Update Procedure
1. Add new FY report to `data/source/`
2. Update `data/consolidated/IWRC Seed Fund Tracking.xlsx`
3. Run analysis notebooks in `analysis/notebooks/current/`
4. Regenerate deliverables with scripts in `analysis/scripts/`

### Current Data Coverage
- **Source:** FY2016 - FY2024 (9 fiscal years)
- **Analysis Period:** 2015-2024 (10-year period)
- **Last Updated:** November 27, 2025

## 🤝 Contributing

For questions or contributions:
1. Review documentation in [docs/](docs/)
2. Check [METHODOLOGY.md](docs/METHODOLOGY.md) for analysis approach
3. Follow [IWRC branding guidelines](assets/branding/IWRC_BRANDING_GUIDELINES.md)

## 📞 Contact

**Illinois Water Resources Center (IWRC)**
University of Illinois System

## 📄 License

Data and analysis for Illinois Water Resources Center internal use and reporting.

---

**Navigation:** [Home](index.html) | [Deliverables](deliverables/) | [Data](data/) | [Analysis](analysis/) | [Docs](docs/)

**Last Updated:** November 27, 2025 | **Repository Size:** 154 MB | **Version:** 2.0 (Reorganized)
