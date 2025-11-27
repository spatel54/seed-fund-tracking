# Analysis Scripts

## Overview
Python scripts for automated data processing, visualization generation, and report creation (44 scripts total).

## Key Scripts by Category

### Report Generation
- `generate_pdf_reports.py` - Generate PDF reports from templates
- `generate_detailed_reports.py` - Create detailed analysis PDFs
- `generate_final_deliverables.py` / `generate_final_deliverables_v2.py` - Package deliverables

### Visualization Generation
- `generate_static_visualizations.py` - Create PNG charts
- `generate_all_static_visualizations.py` - Batch generate all static charts
- `generate_interactive_visualizations.py` - Build HTML dashboards
- `generate_project_type_breakdown.py` - Project type analysis charts

### Map Creation
- `create_illinois_institutions_map.py` - Illinois institutions map
- `create_illinois_map_final.py` - Final map version
- `convert_map_html_to_pdf.py` - Map to PDF conversion

### Data Processing
- `award_type_filters.py` - Filter and categorize awards
- `verify_funding_data.py` - Data validation
- `debug_data.py` - Debugging utilities

### Excel/Documentation
- `generate_excel_workbooks.py` - Excel output creation
- `generate_comprehensive_documentation.py` - Auto-generate docs
- `stage5_excel_and_documentation.py` - Final stage processing

### Branding/Style
- `iwrc_brand_style.py` - IWRC branding configuration (colors, fonts, logos)

### Conversion Utilities
- `convert_html_to_pdf.py` - HTML to PDF
- `convert_interactive_to_static.py` - Interactive to static images

### Notebook Execution
- `execute_notebooks.py` - Batch execute notebooks
- `run_notebooks.py` / `run_single_notebook.py` - Notebook runners

## Usage

### Running Individual Scripts
```bash
python analysis/scripts/generate_static_visualizations.py
```

### Configuration
Most scripts use `iwrc_brand_style.py` for consistent branding. Modify this file to update colors, fonts, or logos across all outputs.

### Output Locations
- Reports: `deliverables/reports/`
- Static visualizations: `deliverables/visualizations/static/`
- Interactive dashboards: `deliverables/visualizations/interactive/`
- Excel outputs: `data/outputs/`

## Dependencies
See [../README.md](../README.md) for required Python packages.

## Last Updated
November 27, 2025
