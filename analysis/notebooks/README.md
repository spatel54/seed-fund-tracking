# Analysis Notebooks

## Overview
Jupyter notebooks for IWRC Seed Fund data analysis and visualization generation.

## Current Notebooks

### 01_comprehensive_roi_analysis.ipynb (35 KB)
Calculate ROI metrics, follow-on funding, and performance indicators.
- Loads consolidated data
- Calculates 10-year and 5-year ROI
- Analyzes follow-on funding by institution
- Outputs: `data/outputs/IWRC_ROI_Analysis_Summary.xlsx`

### 02_roi_visualizations.ipynb (12 KB)
Generate ROI trend charts and comparison visualizations.
- Creates time-series ROI plots
- Institution comparison charts
- Outputs: PNG files to `visualizations/static/`

### 03_interactive_html_visualizations.ipynb (13 KB)
Build interactive Plotly dashboards.
- ROI dashboard, investment treemap, student sunburst
- Timeline visualization
- Outputs: HTML files to `visualizations/interactive/core/`

### 04_fact_sheet_static_charts.ipynb (12 KB)
Generate static charts for fact sheets and reports.
- High-resolution PNG charts (300 DPI)
- Institution reach, student distribution, topic areas
- Outputs: PNG files to `visualizations/static/`

### 05_project_type_breakdown.ipynb (30 KB)
Analyze project types (104g, 104b, etc.) and generate breakdowns.
- Project type categorization
- Investment/student distribution by type
- Outputs: Static PNG charts

### 06_interactive_breakdown.ipynb (38 KB)
Create interactive project type dashboards.
- 104B-only and all-projects views
- Interactive charts with filters
- Outputs: HTML files to `visualizations/interactive/project_types/`

## Archive Folder
Contains historical notebook versions for reference.

## Usage

### Running Notebooks
```bash
# Launch Jupyter
jupyter notebook

# Or use JupyterLab
jupyter lab
```

### Execution Notes
- Run notebooks in numerical order for full workflow
- Ensure data files are in `data/consolidated/`
- Check output paths match current structure

## Dependencies
See [../README.md](../README.md) for required packages.

## Last Updated
November 27, 2025
