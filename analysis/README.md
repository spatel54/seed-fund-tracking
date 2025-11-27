# Analysis

## Overview
This folder contains all analysis code including Jupyter notebooks and Python scripts for data processing, visualization generation, and report creation.

## Contents

### [notebooks/](notebooks/) - Jupyter Notebooks
Analysis workflows and data exploration:
- **current/** - Active analysis notebooks (7 files)
  - 01_comprehensive_roi_analysis.ipynb
  - 01_comprehensive_roi_analysis_CORRECTED.ipynb
  - 02_roi_visualizations.ipynb
  - 03_interactive_html_visualizations.ipynb
  - 04_fact_sheet_static_charts.ipynb
  - 05_project_type_breakdown.ipynb
  - 06_interactive_breakdown.ipynb
- **archive/** - Historical notebook versions

### [scripts/](scripts/) - Python Scripts
Generation and utility scripts (44 files):
- Report generation (`generate_pdf_reports.py`, `generate_detailed_reports.py`)
- Visualization creation (`generate_static_visualizations.py`, `generate_interactive_visualizations.py`)
- Data processing (`award_type_filters.py`, `verify_funding_data.py`)
- Deliverables packaging (`generate_final_deliverables.py`)
- Branding utilities (`iwrc_brand_style.py`)

## Execution Order

### Notebooks (recommended sequence)
1. `01_comprehensive_roi_analysis.ipynb` - Calculate ROI metrics
2. `02_roi_visualizations.ipynb` - Generate ROI charts
3. `03_interactive_html_visualizations.ipynb` - Create interactive dashboards
4. `04_fact_sheet_static_charts.ipynb` - Generate static PNG charts
5. `05_project_type_breakdown.ipynb` - Analyze project types
6. `06_interactive_breakdown.ipynb` - Interactive project type dashboards

### Scripts
Run individual scripts as needed for specific outputs. See [scripts/README.md](scripts/README.md) for details.

## Dependencies

### Python Packages
- pandas >= 1.3.0
- numpy >= 1.21.0
- matplotlib >= 3.4.0
- plotly >= 5.0.0
- openpyxl >= 3.0.0
- reportlab >= 3.6.0
- folium >= 0.12.0

### Data Sources
- `data/consolidated/IWRC Seed Fund Tracking.xlsx`
- `data/outputs/` (analysis results)

## Output Locations
- Reports → `deliverables/reports/`
- Static visualizations → `deliverables/visualizations/static/`
- Interactive dashboards → `deliverables/visualizations/interactive/`

## Last Updated
November 27, 2025 - Reorganized from root-level notebooks/ and scripts/
