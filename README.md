# IWRC Seed Fund Tracking Analysis

Data analysis project for Illinois Water Resources Center (IWRC) tracking research funding, student outcomes, and project impact across fiscal years 2016-2024.

## 🎉 November 2025 Update: IWRC Rebranding & Dual-Track Analysis Complete!

This project has been **completely rebranded with IWRC colors and fonts**, and now includes **dual-track analysis** comparing "All Projects" with "104B Only (Seed Funding)" tracks.

### What's New
- ✓ **IWRC Branded Visualizations** - All charts use IWRC colors (#258372 teal, #639757 olive)
- ✓ **Montserrat Fonts** - Professional typography throughout
- ✓ **Dual-Track Analysis** - Compare comprehensive portfolio vs seed funding focus
- ✓ **FINAL_DELIVERABLES** - Organized output folder with static/interactive/PDF formats
- ✓ **6 Static Charts** - Brand-new generated with proper metrics verification
- ✓ **Comprehensive Documentation** - New guides for rebranding, award types, and deliverables

### Quick Links
- 📖 [Rebranding Summary](docs/REBRANDING_SUMMARY.md) - Overview of changes
- 📚 [Award Type Analysis Guide](docs/AWARD_TYPE_ANALYSIS_GUIDE.md) - Understanding the dual tracks
- 📁 [Final Deliverables Guide](docs/FINAL_DELIVERABLES_GUIDE.md) - File structure and contents
- 📊 [FINAL_DELIVERABLES/](FINAL_DELIVERABLES/) - Generated outputs

## Project Structure

```
.
├── data/
│   ├── source/           # Original Excel files from different fiscal years
│   ├── consolidated/     # Combined and processed datasets
│   └── outputs/          # Analysis outputs and summary files
├── notebooks/
│   ├── current/          # Active analysis notebooks (LATEST VERSIONS)
│   └── archive/          # Executed and historical notebook versions
├── scripts/              # Python utility scripts for data processing
├── visualizations/
│   ├── static/           # PNG charts and graphs (300 DPI)
│   └── interactive/      # HTML interactive visualizations
└── docs/                 # Documentation and reports

```

## Quick Start

### Prerequisites
```bash
# Python 3.8+ required
pip3 install pandas openpyxl numpy matplotlib seaborn plotly
```

### Running Analysis

**IMPORTANT: Always work with files in `notebooks/current/` for the latest versions**

1. **Comprehensive ROI Analysis**: [notebooks/current/01_comprehensive_roi_analysis.ipynb](notebooks/current/01_comprehensive_roi_analysis.ipynb)
   - Complete ROI analysis (2015-2024)
   - Follow-on funding tracking
   - Student training metrics
   - Institutional diversity analysis

2. **ROI Visualizations**: [notebooks/current/02_roi_visualizations.ipynb](notebooks/current/02_roi_visualizations.ipynb)
   - Investment comparison charts
   - ROI multiplier visualizations
   - Student impact graphics
   - Excel summary reports

3. **Interactive HTML Charts**: [notebooks/current/03_interactive_html_visualizations.ipynb](notebooks/current/03_interactive_html_visualizations.ipynb)
   - Interactive maps and charts using Plotly
   - Geographic distribution of institutions
   - Keyword analysis with hover tooltips

4. **Fact Sheet Static Charts**: [notebooks/current/04_fact_sheet_static_charts.ipynb](notebooks/current/04_fact_sheet_static_charts.ipynb)
   - Publication-ready static PNG charts
   - Keyword distribution pie charts
   - Illinois institution geographic maps

### Data Consolidation

To update the consolidated dataset with new fiscal year data:

```bash
python3 scripts/combine_excel_files_v2.py
```

This script:
- Combines source Excel files from `data/source/`
- Handles multi-level headers intelligently
- Creates automatic backups
- Outputs to `data/consolidated/IWRC Seed Fund Tracking.xlsx`

## Key Data Files

### Most Recent (Priority Files)
- **[data/consolidated/IWRC Seed Fund Tracking.xlsx](data/consolidated/IWRC Seed Fund Tracking.xlsx)** - Main consolidated dataset (539 rows, 35 columns)
- **[data/consolidated/fact sheet data.xlsx](data/consolidated/fact sheet data.xlsx)** - Curated data for fact sheets and reports
- **[data/outputs/IWRC_ROI_Analysis_Summary.xlsx](data/outputs/IWRC_ROI_Analysis_Summary.xlsx)** - Latest ROI calculations

### Source Data Files
All located in `data/source/`:
- `FY24_reporting_IL.xlsx` - FY2024 Illinois reporting (MOST RECENT)
- `FY23_reporting_IL.xlsx` - FY2023 Illinois reporting
- `IWRC-2022-WRRA-Annual-Report-v.101923.xlsx` - FY2022 annual report
- `IL_5yr_FY16_20_2.xlsx` - 5-year aggregate (FY2016-2020)

## Key Analysis Outputs

### Latest Visualizations
Located in `visualizations/`:

**Static Images** (`static/`):
- `roi_comparison.png` - ROI analysis comparison
- `iwrc_investment_comparison.png` - Investment vs. matching funds
- `students_trained.png` - Student training outcomes
- `student_distribution_pie.png` - Student type distribution
- `2025_keyword_pie_chart.png` - Research keyword distribution
- `2025_illinois_institutions_map.png` - Geographic institution map

**Interactive** (`interactive/`):
- `IWRC_ROI_Analysis_Report.html` - Interactive ROI dashboard
- `2025_keyword_pie_chart_interactive.html` - Interactive keyword analysis (NEW!)
- `2025_illinois_institutions_map_interactive.html` - Interactive institution map (NEW!)

## Documentation

Located in `docs/`:
- **[QUICK_START_GUIDE.md](docs/QUICK_START_GUIDE.md)** - Fast-start guide for common tasks
- **[CLAUDE.md](docs/CLAUDE.md)** - Project instructions and architecture
- **[ANALYSIS_SUMMARY.md](docs/ANALYSIS_SUMMARY.md)** - Analysis findings and insights
- **[RESULTS_READY.md](docs/RESULTS_READY.md)** - Latest results and deliverables
- **[NOTEBOOK_REVIEW_REPORT.md](docs/NOTEBOOK_REVIEW_REPORT.md)** - Notebook quality review
- **[QUICK_FIX_GUIDE.md](docs/QUICK_FIX_GUIDE.md)** - Troubleshooting common issues

## Data Schema

The consolidated dataset includes 35 columns:
- **Project Info**: Project ID, Title, Award Type
- **Personnel**: PI Name, Email, Institution
- **Funding**: Award Amount, Matching Funds
- **Students**: PhD, MS, Undergraduate, Post Doc counts (WRRA-funded and matching)
- **Diversity**: Underrepresented minority and female student data
- **Research**: Science priorities, keywords, methodologies
- **Outputs**: Publications, presentations, awards, DOIs

## Common Workflows

### 1. Generate Updated Fact Sheet Visualizations
```bash
# Run the fact sheet notebook
jupyter notebook notebooks/current/04_fact_sheet_static_charts.ipynb
```

### 2. Create Interactive Maps
```bash
# Run the interactive visualizations notebook
jupyter notebook notebooks/current/03_interactive_html_visualizations.ipynb
```

### 3. Generate Complete ROI Analysis
```bash
# Run comprehensive analysis notebook
jupyter notebook notebooks/current/01_comprehensive_roi_analysis.ipynb
```

### 4. Update Consolidated Dataset
```bash
# Add new Excel file to data/source/
# Then run:
python3 scripts/combine_excel_files_v2.py
```

## Important Notes

### Excel File Structure
- Source files use **multi-level headers** (3 rows) with merged cells
- Column names are in the **second header level** (index 1)
- Script handles this automatically via `header=[0,1,2]`

### Data Integrity
- Never modify raw data values during consolidation
- All backups are automatic (files with `_BACKUP` suffix)
- Original source files remain untouched in `data/source/`

## Contributing

When adding new analysis:
1. Create new notebook in `notebooks/current/`
2. Follow naming convention: `YYYY_descriptive_name.ipynb`
3. Save outputs to appropriate `visualizations/` subfolder
4. Update this README with new analysis descriptions

## Version History

- **Nov 18, 2025**: Major repository reorganization
  - Removed 26 MB of duplicate files (exports/ directory)
  - Cleaned up legacy files and temporary data
  - Renamed notebooks with clear, sequential naming scheme
  - Consolidated documentation
  - Moved utility scripts to proper locations
- **Nov 18, 2025**: Latest ROI analysis and 2025 visualizations
- **Nov 6, 2025**: Initial consolidation of FY16-FY24 data

## Support

For questions about:
- Data structure: See [docs/CLAUDE.md](docs/CLAUDE.md)
- Quick tasks: See [docs/QUICK_START_GUIDE.md](docs/QUICK_START_GUIDE.md)
- Analysis results: See [docs/RESULTS_READY.md](docs/RESULTS_READY.md)
