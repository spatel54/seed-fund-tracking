# IWRC Seed Fund Tracking: Methodology and Data Analysis

## 1. Overview
This document details the methodology, data sources, and analysis logic used to generate the IWRC Seed Fund Tracking reports and visualizations. It provides transparency into how numbers are calculated and how visualizations are constructed.

## 2. Data Source
*   **Source File**: `data/processed/clean_iwrc_tracking.xlsx`
*   **Primary Sheet**: `Project Overview`
*   **Data Scope**: The analysis covers seed funding projects managed by the Illinois Water Resources Center (IWRC).

## 3. Data Processing & Cleaning
The raw data is processed using the `iwrc_data_loader.py` module to ensure consistency and accuracy.

### 3.1. Year Extraction
*   **Logic**: The fiscal year is extracted from the `Project ID` column (first 4 digits).
*   **Range**: The analysis focuses on two primary periods:
    *   **10-Year Period**: 2015 - 2024
    *   **5-Year Period**: 2020 - 2024

### 3.2. Award Type Categorization
Projects are categorized based on the `Award Type` column:
*   **104B**: Base seed funding (Federal).
*   **104G**: Competitive national grants.
*   **Coordination**: Administrative and coordination funding.
*   **Other**: Any other funding types.

### 3.3. Institution Name Standardization
To ensure accurate reporting, institution names are standardized to consolidate spelling variations:

#### Standardization Mappings
*   **University of Illinois** variations → `University of Illinois at Urbana-Champaign`:
    *   `University of Illinois Urbana-Champaign`
    *   `University of Illinois`
    *   `University of Illinois  ` (with trailing space)
    *   `Univeristy of Illinois` (typo)
*   **Southern Illinois University** variations → `Southern Illinois University`:
    *   `Southern Illinois University at Carbondale`
    *   `Southern Illinois University Carbondale`

#### Implementation
*   **Location**: Applied in `iwrc_data_loader.py` (centralized data loader) and `generate_overview_charts.py` (visualization script)
*   **Process**: 
    1. Strip leading/trailing whitespace from all institution names
    2. Apply name mapping to consolidate variations
*   **Impact**: Reduces unique institution count (2015-2024) from 16 to 11, with:
    *   University of Illinois at Urbana-Champaign: 49 projects (consolidated from 27+17+12)
    *   Southern Illinois University: 7 projects (consolidated from 7+2)

### 3.4. Metric Calculations
*   **Total Investment**: Sum of `Award Amount Allocated ($)` for all filtered projects.
*   **Number of Projects**: Count of unique `Project ID`s.
*   **Students Supported**: Sum of values in student columns:
    *   `Number of PhD Students Supported by WRRA $`
    *   `Number of MS Students Supported by WRRA $`
    *   `Number of Undergraduate Students Supported by WRRA $`
    *   `Number of Post Docs Supported by WRRA $`
*   **Follow-on Funding**: Sum of `Follow-on Funding ($)`. If missing, estimated based on historical ratios (3-4% of award amount) for projection purposes only (noted in charts).

## 4. Visualization Logic

### 4.1. Pie Charts (e.g., Student Distribution)
*   **Thresholding**: To improve readability, percentage labels are **hidden** for slices smaller than **3%**.
*   **Legend**: Category labels are moved to a dedicated legend to prevent text overlap on the chart itself.

### 4.2. Bar Charts (e.g., Top Institutions, Research Topics)
*   **Sorting**: Bars are typically sorted by value (descending) to highlight top contributors.
*   **Labeling**: Exact values are displayed at the end of each bar.
*   **Margins**:
    *   **Left Margin**: Increased (e.g., to 40%) to accommodate long labels (Institution names, Topic areas).
    *   **Right/Top Margin**: Added to prevent value labels from being cut off.

### 4.3. Pyramid Charts (Topic Areas)
*   **Structure**: Compares two time periods side-by-side.
    *   **Left Side (Negative Axis)**: 5-Year Period (2020-2024).
    *   **Right Side (Positive Axis)**: 10-Year Period (2015-2024).
*   **Sorting**: Sorted by the 10-Year total to show the most historically significant topics at the top.

## 5. Report Specifics

### 5.1. Executive Summary
*   **Purpose**: High-level overview for stakeholders.
*   **Key Metrics**: Total investment, total projects, total students supported, and ROI (leveraged funding).
*   **Variants**:
    *   `All Projects`: Includes 104B, 104G, and Coordination.
    *   `104B Only`: Focuses strictly on the base seed funding program.

### 5.2. Program Summary
*   **Focus**: Operational details and reach.
*   **Key Charts**:
    *   **Student Breakdown**: Distribution of PhD, MS, and Undergrad students.
    *   **Institutional Reach**: Funding distribution across different universities.

### 5.3. Analysis Deep Dive
*   **Focus**: Thematic and strategic analysis.
*   **Key Charts**:
    *   **Topic Areas**: Funding allocation by research topic (e.g., Water Quality, Invasive Species).
    *   **Project Types**: Breakdown by specific project categories.

## 6. Branding
All outputs adhere to the IWRC Brand Guidelines:
*   **Fonts**: **Montserrat** (Regular and Bold weights).
*   **Colors**:
    *   **Primary**: Navy Blue (`#1F407A`)
    *   **Secondary**: Teal (`#00A0B0`)
    *   **Accent**: Orange (`#F26522`)
## 7. Technical Implementation Details

### 7.1. Source Code & Scripts
The following Python scripts (`analysis/scripts/`) were used to generate the reports and visualizations:

*   **Core Logic**:
    *   `iwrc_data_loader.py`: Handles data loading, cleaning, and standardization.
    *   `iwrc_brand_style.py`: Centralized definition of IWRC colors, fonts, and plotting styles.

*   **Report Generation**:
    *   `generate_pdf_reports_stage4_CORRECTED.py`: Generates the **Executive Summary** PDFs.
    *   `generate_fresh_reports_CORRECTED.py`: Generates the **Program Summary** and **Analysis Deep Dive** PDFs.

*   **Visualization Generation**:
    *   `generate_all_visualizations_CORRECTED.py`: Generates overview charts (Investment, ROI, Projects by Year).
    *   `generate_topic_areas_pyramid.py`: Generates the Topic Areas pyramid charts.
    *   `generate_award_type_breakdown_static.py`: Generates Award Type bar charts.
    *   `generate_project_type_breakdown.py`: Generates Project Type breakdown charts.
    *   `generate_university_funding_chart.py`: Generates the University Funding comparison chart.
    *   `generate_followon_breakdown.py`: Generates the Follow-on Funding chart.

### 7.2. Data Files
*   **Primary Data**: `data/processed/clean_iwrc_tracking.xlsx`
    *   Used by all scripts as the single source of truth.

### 7.4. Data File Usage Note
*   Most scripts use `data/processed/clean_iwrc_tracking.xlsx`.
*   **Exception**: The University Funding chart (`generate_university_funding_chart.py`) uses `data/consolidated/fact sheet data.xlsx`.

## 8. Artifact Source Mapping

The following table maps each generated file to its source script and data file:

## 8. Artifact Source Mapping

The following table maps every generated file to its source script and data file.

| Category | File Name | Generator Script | Data Source |
| :--- | :--- | :--- | :--- |
| **PDF Reports** | IWRC_Executive_Summary_All_Projects.pdf | generate_pdf_reports_stage4_CORRECTED | IWRC Seed Fund Tracking |
| | IWRC_Executive_Summary_104B_Only.pdf | generate_pdf_reports_stage4_CORRECTED | IWRC Seed Fund Tracking |
| | IWRC_Program_Summary.pdf | generate_fresh_reports_CORRECTED | IWRC Seed Fund Tracking |
| | IWRC_Analysis_Deep_Dive.pdf | generate_fresh_reports_CORRECTED | IWRC Seed Fund Tracking |
| **Overview** | investment_comparison.png | generate_all_visualizations_CORRECTED | IWRC Seed Fund Tracking |
| | roi_comparison.png | generate_all_visualizations_CORRECTED | IWRC Seed Fund Tracking |
| | projects_by_year.png | generate_all_visualizations_CORRECTED | IWRC Seed Fund Tracking |
| | summary_dashboard.png | generate_all_visualizations_CORRECTED | IWRC Seed Fund Tracking |
| **Topic Areas** | topic_areas_pyramid_stacked.png | generate_topic_areas_pyramid | IWRC Seed Fund Tracking |
| | topic_areas_pyramid_overlapping.png | generate_topic_areas_pyramid | IWRC Seed Fund Tracking |
| **Award Types** | award_type_*.png | generate_award_type_breakdown_static | IWRC Seed Fund Tracking |
| **Project Types** | [Category]/[Period]/*.png | generate_project_type_breakdown | IWRC Seed Fund Tracking |
| **Other** | university_funding_comparison.png | generate_university_funding_chart | fact sheet data |
| | followon_breakdown.png | generate_followon_breakdown | IWRC Seed Fund Tracking |

**Path Reference:**
- All PDF reports are in: `deliverables/reports/`
- All visualizations are in: `deliverables/visualizations/static/` (with subdirectories as indicated)
- All generator scripts are in: `analysis/scripts/` (with `.py` extension)
- All data sources are in: `data/consolidated/` (with `.xlsx` extension)
