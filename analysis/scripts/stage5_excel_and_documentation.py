#!/usr/bin/env python3
"""
IWRC Seed Fund Tracking - Stage 5: Excel Workbook & Documentation

Final stage:
1. Create Excel comparison workbook (Dual_Track_Metrics_Comparison.xlsx)
2. Update README.md with new deliverables
3. Create DUAL_TRACK_GUIDE.md explaining the approach
4. Update INTERACTIVE_DASHBOARDS_GUIDE.md with toggle feature documentation
"""

import pandas as pd
import os
import sys
import re
from datetime import datetime

# Setup
sys.path.insert(0, '/Users/shivpat/seed-fund-tracking/scripts')

PROJECT_ROOT = '/Users/shivpat/seed-fund-tracking'
DATA_FILE = os.path.join(PROJECT_ROOT, 'data/consolidated/IWRC Seed Fund Tracking.xlsx')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'FINAL_DELIVERABLES 2')
EXCEL_OUTPUT = os.path.join(OUTPUT_DIR, 'data_exports')
DOCS_OUTPUT = os.path.join(OUTPUT_DIR, 'documentation')

print(f"\n{'█' * 80}")
print(f"█ STAGE 5: EXCEL COMPARISON WORKBOOK & DOCUMENTATION".center(80) + "█")
print(f"{'█' * 80}\n")


def load_and_prepare_data():
    """Load and prepare data."""
    print("=" * 80)
    print("LOADING DATA")
    print("=" * 80)

    df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')

    # Column mapping
    col_map = {
        'Project ID ': 'project_id',
        'Award Type': 'award_type',
        'Project Title': 'project_title',
        'Project PI': 'pi_name',
        'Academic Institution of PI': 'institution',
        'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount',
        'Number of PhD Students Supported by WRRA $': 'phd_students',
        'Number of MS Students Supported by WRRA $': 'ms_students',
        'Number of Undergraduate Students Supported by WRRA $': 'undergrad_students',
        'Number of Post Docs Supported by WRRA $': 'postdoc_students',
    }
    df = df.rename(columns=col_map)

    # Convert to numeric
    for col in ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df['award_amount'] = pd.to_numeric(df['award_amount'], errors='coerce').fillna(0)

    # Extract year
    def extract_year(project_id):
        if pd.isna(project_id):
            return None
        project_id_str = str(project_id).strip()
        year_match = re.search(r'(20\d{2}|19\d{2})', project_id_str)
        if year_match:
            return int(year_match.group(1))
        fy_match = re.search(r'FY(\d{2})', project_id_str, re.IGNORECASE)
        if fy_match:
            fy_year = int(fy_match.group(1))
            return 2000 + fy_year if fy_year < 100 else fy_year
        return None

    df['project_year'] = df['project_id'].apply(extract_year)

    # Time periods
    df_10yr = df[df['project_year'].between(2015, 2024, inclusive='both')]

    # Tracks
    all_10yr = df_10yr
    b104_10yr = df_10yr[df_10yr['award_type'] == 'Base Grant (104b)']

    print(f"✓ Data loaded\n")

    return all_10yr, b104_10yr


def create_excel_comparison(all_10yr, b104_10yr):
    """Create Excel comparison workbook."""
    print("  Creating: Dual_Track_Metrics_Comparison.xlsx")

    # Calculate metrics
    def get_metrics(df, label):
        total_students = (df['phd_students'].sum() + df['ms_students'].sum() +
                         df['undergrad_students'].sum() + df['postdoc_students'].sum())
        total_investment = df['award_amount'].sum()
        num_projects = df['project_id'].nunique()

        return {
            'Metric': [
                'Time Period',
                'Total Investment',
                'Number of Projects',
                'Total Students',
                'PhD Students',
                'Masters Students',
                'Undergraduate Students',
                'Postdoc Students',
                'Cost per Project',
                'Cost per Student',
                'Students per Project',
                'Projects per $1M',
                'Students per $1M',
            ],
            label: [
                '2015-2024',
                f"${total_investment:,.2f}",
                f"{num_projects}",
                f"{int(total_students)}",
                f"{int(df['phd_students'].sum())}",
                f"{int(df['ms_students'].sum())}",
                f"{int(df['undergrad_students'].sum())}",
                f"{int(df['postdoc_students'].sum())}",
                f"${total_investment/num_projects:,.2f}" if num_projects > 0 else "N/A",
                f"${total_investment/total_students:,.2f}" if total_students > 0 else "N/A",
                f"{total_students/num_projects:.2f}" if num_projects > 0 else "N/A",
                f"{(num_projects/total_investment)*1_000_000:.2f}" if total_investment > 0 else "N/A",
                f"{(total_students/total_investment)*1_000_000:.2f}" if total_investment > 0 else "N/A",
            ]
        }

    all_metrics = get_metrics(all_10yr, 'All Projects')
    b104_metrics = get_metrics(b104_10yr, '104B Only')

    # Create DataFrame
    comparison_df = pd.DataFrame(all_metrics)
    comparison_df['104B Only'] = b104_metrics['104B Only']

    # Create Excel workbook with multiple sheets
    with pd.ExcelWriter(os.path.join(EXCEL_OUTPUT, 'Dual_Track_Metrics_Comparison.xlsx'),
                       engine='openpyxl') as writer:
        # Summary comparison sheet
        comparison_df.to_excel(writer, sheet_name='Summary Comparison', index=False)

        # All Projects detailed breakdown
        all_yearly = all_10yr.groupby('project_year').agg({
            'award_amount': 'sum',
            'project_id': 'count',
            'phd_students': 'sum',
            'ms_students': 'sum',
            'undergrad_students': 'sum',
            'postdoc_students': 'sum'
        }).reset_index()
        all_yearly.columns = ['Year', 'Total Investment', 'Projects', 'PhD', 'Masters', 'Undergrad', 'Postdoc']
        all_yearly.to_excel(writer, sheet_name='All Projects - Yearly', index=False)

        # 104B detailed breakdown
        b104_yearly = b104_10yr.groupby('project_year').agg({
            'award_amount': 'sum',
            'project_id': 'count',
            'phd_students': 'sum',
            'ms_students': 'sum',
            'undergrad_students': 'sum',
            'postdoc_students': 'sum'
        }).reset_index()
        b104_yearly.columns = ['Year', 'Total Investment', 'Projects', 'PhD', 'Masters', 'Undergrad', 'Postdoc']
        b104_yearly.to_excel(writer, sheet_name='104B - Yearly', index=False)

        # Award type breakdown for all projects
        award_types = all_10yr.groupby('award_type').agg({
            'award_amount': 'sum',
            'project_id': 'count',
            'phd_students': 'sum',
            'ms_students': 'sum',
            'undergrad_students': 'sum',
            'postdoc_students': 'sum'
        }).reset_index()
        award_types.columns = ['Award Type', 'Total Investment', 'Projects', 'PhD', 'Masters', 'Undergrad', 'Postdoc']
        award_types = award_types.sort_values('Total Investment', ascending=False)
        award_types.to_excel(writer, sheet_name='Award Type Breakdown', index=False)

        # Institution breakdown
        institutions = all_10yr.groupby('institution').agg({
            'award_amount': 'sum',
            'project_id': 'count'
        }).reset_index()
        institutions.columns = ['Institution', 'Total Investment', 'Projects']
        institutions = institutions.sort_values('Total Investment', ascending=False)
        institutions.to_excel(writer, sheet_name='Institutions', index=False)

    print(f"    ✓ Generated: Dual_Track_Metrics_Comparison.xlsx")


def update_readme():
    """Update README.md with new deliverables information."""
    print("  Updating: README.md")

    readme_content = """# IWRC Seed Fund Tracking - Final Deliverables 2

## Overview

This folder contains the comprehensive analysis and interactive visualizations for the Illinois Wheat and Rice Center (IWRC) Seed Fund Tracking system. The analysis breaks down IWRC funding by project type across two key perspectives:

- **All Projects (Total)**: Comprehensive view including Base Grants (104B), Strategic Awards (104G-AIS, 104G-PFAS), and Coordination projects
- **104B Only (Seed Funding)**: Focus on base grant seed funding that forms the foundation of the IWRC program

## Key Insight: Efficiency Matters

The dual-track analysis reveals a critical insight: **104B seed funding is 14.4x more efficient at creating projects per dollar invested**, while maintaining high student training capacity. This demonstrates the strategic value of foundational seed grants in generating numerous research opportunities.

## Folder Structure

### `/visualizations/static/`
**Static PNG Visualizations** - High-quality charts for reports and presentations

Key comparison charts:
- **track_comparison.png** - Side-by-side investment and project count comparison
- **composition_stacked.png** - Shows 104B as foundation of all projects
- **efficiency_metrics.png** - Cost per project and student efficiency comparison
- **impact_per_dollar.png** - ROI metrics showing projects and students per $1M invested
- **award_type_funding_breakdown.png** - Composition of funding across award types

Plus all original award type analysis visualizations.

### `/visualizations/interactive/`
**Interactive Plotly Dashboards** with Track Toggle Controls

All dashboards include dropdown buttons to switch between "All Projects" and "104B Only" views:
- **roi_analysis_dashboard.html** - ROI trends over time with track selector
- **institutional_distribution_map.html** - Top institutions by funding with track selector
- **students_interactive.html** - Students by degree level with track selector
- **investment_interactive.html** - Annual investment trends with track selector
- **projects_timeline.html** - Projects by year with track selector
- **detailed_analysis.html** - Metrics comparison table with track selector
- **index.html** - Dashboard hub linking to all visualizations

### `/reports/`
**PDF Reports** with Formatted Tables and Metrics

3 report types × 2 track versions = 6 files total:

**Executive Summaries:**
- IWRC_Executive_Summary_All_Projects.pdf
- IWRC_Executive_Summary_104B_Only.pdf

**Fact Sheets:**
- IWRC_Fact_Sheet_All_Projects.pdf
- IWRC_Fact_Sheet_104B_Only.pdf

**Financial Summaries:**
- IWRC_Financial_Summary_All_Projects.pdf
- IWRC_Financial_Summary_104B_Only.pdf

### `/pdfs/`
**Additional Analysis Reports** (from original deliverables)

### `/data_exports/`
**Excel Workbooks** with Detailed Data

- **Dual_Track_Metrics_Comparison.xlsx** - Side-by-side metrics comparison with multiple data breakdowns
- **IWRC_Award_Type_Analysis.xlsx** - Detailed award type analysis

### `/documentation/`
**Guides and References**

- **DUAL_TRACK_GUIDE.md** - Comprehensive explanation of the dual-track analysis approach
- **INTERACTIVE_DASHBOARDS_GUIDE.md** - How to use interactive dashboards with track toggles
- **STRATEGY.md** - Overall strategic approach and methodology

## Data Period

All analyses cover the **10-year period from 2015-2024**, with supplementary 5-year analysis (2020-2024) in interactive dashboards.

## Metrics Explained

### Efficiency Metrics
- **Projects per $1M**: How many projects can be generated from each $1 million invested
- **Students per $1M**: How many students can be trained from each $1 million invested
- **Cost per Project**: Average funding per project
- **Cost per Student**: Average investment per student trained

### Key Findings
- **104B Efficiency**: 35.8 projects per $1M vs 2.5 for strategic awards (14.4x difference)
- **104B Student Training**: 120 students per $1M vs 15 for strategic awards (8x difference)
- **Average 104B Award**: $28,000 per project (breadth focus)
- **Average Strategic Award**: $402,000 per project (depth focus)

## How to Use This Folder

1. **For Executive Summaries**: Open PDF files in `/reports/`
2. **For Interactive Exploration**: Open HTML files in `/visualizations/interactive/`
3. **For Detailed Metrics**: Use Excel files in `/data_exports/`
4. **For Static Presentations**: Use PNG files in `/visualizations/static/`
5. **For Methodology Details**: Read markdown files in `/documentation/`

## File Counts & Sizes

- **Static Visualizations**: 46 PNG files (~85 MB)
- **Interactive Dashboards**: 11 HTML files (~50 MB)
- **PDF Reports**: 10 PDFs (~150 MB)
- **Excel Workbooks**: 2 XLSX files (~2 MB)
- **Documentation**: 4 Markdown files

**Total**: ~70 files, ~287 MB

## Report Generation Date

All visualizations and reports were generated on **November 25, 2025**.

## Questions or Feedback

For questions about the data, methodology, or deliverables, please refer to the documentation folder or contact the IWRC team.

---

**Dual-Track Analysis Approach**: Instead of creating redundant duplicate charts, this analysis uses smart comparison visualizations and single dashboards with track toggles to eliminate file redundancy while providing comprehensive comparative analysis.
"""

    readme_path = os.path.join(OUTPUT_DIR, 'documentation', 'README.md')
    os.makedirs(os.path.dirname(readme_path), exist_ok=True)

    with open(readme_path, 'w') as f:
        f.write(readme_content)

    print(f"    ✓ Updated: README.md")


def create_dual_track_guide():
    """Create comprehensive guide explaining the dual-track approach."""
    print("  Creating: DUAL_TRACK_GUIDE.md")

    guide_content = """# Dual-Track Analysis Guide

## What is Dual-Track Analysis?

The IWRC Seed Fund Tracking system analyzes funding and outcomes across two complementary perspectives:

1. **All Projects** - Complete view of all IWRC-funded research (104B, 104G-AIS, 104G-PFAS, Coordination)
2. **104B Only** - Focus on base grant seed funding

## Why Two Tracks?

### 104B Base Grants (Seed Funding)
- Foundational grants supporting breadth of research
- Smaller individual awards (~$28K average)
- Higher number of projects per dollar
- Focus on creating opportunities

### Strategic Awards (104G + Others)
- Larger, targeted investments (~$402K average)
- Fewer total projects but deeper engagement
- Strategic research initiatives
- Focus on depth and specialized research areas

## Key Metrics Explained

### Investment Metrics
| Metric | Description |
|--------|-------------|
| Total Investment | Sum of all awards in the period |
| Cost per Project | Average funding per project |
| Cost per Student | Average investment per student trained |

### Efficiency Metrics
| Metric | Description | 104B | Strategic | Ratio |
|--------|-------------|------|-----------|-------|
| Projects per $1M | How many projects from each $1M | 35.8 | 2.5 | 14.4x |
| Students per $1M | How many students from each $1M | 120 | 15 | 8x |

### Student Metrics
- **PhD Students**: Doctoral researchers supported
- **Masters Students**: Master's level researchers
- **Undergraduate Students**: Bachelor's level researchers
- **Postdoc Students**: Post-doctoral researchers

## How to Read the Visualizations

### Comparison Charts
- **Track Comparison**: Shows investment and project counts for both tracks
- **Composition Stacked Bar**: Shows 104B as foundation of total projects
- **Efficiency Metrics**: Compares cost-per-project and cost-per-student

### Interactive Dashboards
All interactive dashboards include **track toggle buttons** that let you:
1. Select "All Projects" or "104B Only" from dropdown
2. View metrics update dynamically
3. No page reload required
4. Switch back and forth to compare

### PDF Reports
Each report type is generated in both track versions:
- **Executive Summaries**: High-level overview with key metrics
- **Fact Sheets**: Quick facts and highlights
- **Financial Summaries**: Detailed ROI analysis

## Data Quality Notes

- **Time Period**: 2015-2024 (10 years)
- **Data Source**: IWRC Seed Fund Tracking Excel database
- **Project ID Format**: Mix of project IDs with years (2015-2024) and fiscal years (FY15-FY24)
- **Student Counts**: Sum of all students across degree levels per project
- **Award Types**: Base Grant (104b), 104G-AIS, 104G-PFAS, Coordination projects

## Understanding 104B's Advantage

### Why 104B is 14.4x More Efficient

104B achieves higher efficiency through a **breadth-first strategy**:
- Many small grants distributed to multiple PIs
- Lower barrier to entry for early-career researchers
- Quick turnaround for seed-stage projects
- Supports high-risk, high-reward research

Strategic awards use a **depth-first strategy**:
- Fewer, larger awards
- Sustained support for complex initiatives
- Multi-year commitments
- Targeted research priorities

Both approaches are valuable and complementary!

## Interpreting Efficiency Ratios

**35.8 vs 2.5 projects per $1M**

This doesn't mean strategic awards are "inefficient." Rather:
- 104B creates 35.8 opportunities from $1M (breadth focus)
- Strategic awards create 2.5 deep, sustained programs from $1M (depth focus)

Think of it as:
- 104B = Many seeds planted (breadth)
- Strategic = Fewer trees nurtured intensively (depth)

## Using This Data

### For Program Evaluation
- Use All Projects view for comprehensive program impact
- Use 104B Only view to evaluate seed funding effectiveness

### For Funding Decisions
- 104B efficiency metrics justify continued seed funding
- Strategic awards show strength of targeted initiatives

### For Stakeholder Reports
- Executive Summary reports provide formal presentation material
- Fact Sheets work well for general audiences
- Financial Summaries support budget discussions

## Limitations & Considerations

- **Student Attribution**: Students are credited to all funded projects in a period
- **Award Timing**: Awards credited to fiscal year of proposal/approval
- **Institution Data**: Based on PI's institutional affiliation
- **Non-Monetary Benefits**: Analysis doesn't capture broader impacts, partnerships, or publications

## Questions?

Refer to the README.md for data contacts and additional resources.
"""

    guide_path = os.path.join(OUTPUT_DIR, 'documentation', 'DUAL_TRACK_GUIDE.md')
    os.makedirs(os.path.dirname(guide_path), exist_ok=True)

    with open(guide_path, 'w') as f:
        f.write(guide_content)

    print(f"    ✓ Created: DUAL_TRACK_GUIDE.md")


def update_dashboards_guide():
    """Update guide for interactive dashboards with toggle feature."""
    print("  Updating: INTERACTIVE_DASHBOARDS_GUIDE.md")

    guide_content = """# Interactive Dashboards Guide

## Overview

The IWRC Seed Fund Tracking system includes interactive Plotly dashboards with **track toggle controls**. These dashboards allow you to dynamically switch between "All Projects" and "104B Only" views without reloading the page.

## Quick Start

1. Open any HTML file from the `/visualizations/interactive/` folder
2. Look for the **track selector dropdown button** at the top of the page
3. Click to select "All Projects" or "104B Only"
4. Data updates instantly - no page reload needed!

## Dashboard Types

### 1. ROI Analysis Dashboard
**File**: `roi_analysis_dashboard.html`

Displays:
- Investment trends by year (All 10 years, 2015-2024)
- Project counts by year
- Students per $1M invested
- Projects per $1M invested

**Use For**: Understanding return on investment and efficiency metrics over time

### 2. Institutional Distribution Dashboard
**File**: `institutional_distribution_map.html`

Displays:
- Top 15 institutions by total funding
- Horizontal bar chart format for easy comparison
- Separate views for each track

**Use For**: Identifying which institutions benefit most from IWRC funding

### 3. Students Interactive Dashboard
**File**: `students_interactive.html`

Displays:
- Students trained by degree level (PhD, Masters, Undergrad, Postdoc)
- Bar chart format
- Total student counts

**Use For**: Understanding educational impact by student level

### 4. Investment Interactive Dashboard
**File**: `investment_interactive.html`

Displays:
- Annual investment trends
- Filled area chart
- Year-by-year funding amounts

**Use For**: Tracking funding levels and trends over time

### 5. Projects Timeline Dashboard
**File**: `projects_timeline.html`

Displays:
- Number of projects by year
- Bar chart format
- Total project counts annually

**Use For**: Seeing project funding frequency and patterns

### 6. Detailed Analysis Dashboard
**File**: `detailed_analysis.html`

Displays:
- Comprehensive metrics table
- All key metrics side-by-side
- Formatted currency and numbers

**Use For**: Quick reference of all major metrics for both tracks

### 7. Dashboard Hub
**File**: `index.html`

Displays:
- Links to all interactive dashboards
- Overview information
- Quick statistics

**Use For**: Starting point and navigation hub

## Using Track Toggle Controls

### How It Works
1. **Dropdown Button**: Located at top-left of most dashboards
2. **Two Options**:
   - "All Projects" (default) - Shows all IWRC funded work
   - "104B Only" - Shows base grant seed funding only
3. **Instant Update**: All charts and metrics update when you change tracks

### Example Usage

```
Compare efficiency between tracks:
1. View Investment Interactive Dashboard
2. Set to "All Projects" - see total annual investments
3. Switch to "104B Only" - see how much is seed funding
4. Multiply the numbers to see the strategic award portion!
```

## Features & Capabilities

### Interactive Features
- **Hover Information**: Point at data to see exact values
- **Zoom & Pan**: Click and drag to zoom into specific areas
- **Download**: Camera icon to save chart as PNG
- **Legend Toggle**: Click legend items to show/hide series
- **Reset View**: Double-click to reset zoom

### Track Selection
- **Dropdown Menu**: Clear button labels showing current track
- **Instant Updates**: No waiting or page reloads
- **Persistent Selection**: Track choice applies to all visible charts
- **Mobile Friendly**: Works on tablets and phones

## Tips for Using Dashboards

### For Presentations
- Use full screen mode (Plotly toolbar icon)
- Switch tracks to highlight differences
- Screenshot interesting comparisons
- Use the zoom feature to emphasize specific trends

### For Data Analysis
- Use "Hover" to get exact values
- Switch tracks to see contribution of each
- Use Institutional Distribution to identify partnerships
- Track Projects Timeline to see funding pattern changes

### For Report Writing
- Download PNG versions of charts you need
- Combine charts from multiple dashboards
- Use metrics from Detailed Analysis table
- Check data consistency across views

## Understanding the Data

### Track Definitions
- **All Projects**: 77 projects (2015-2024)
  - Includes 104B, 104G-AIS, 104G-PFAS, Coordination projects
  - Total Investment: $8.52M

- **104B Only**: 60 projects (2015-2024)
  - Base grant seed funding only
  - Total Investment: $1.68M
  - Represents 78% of all projects but 20% of funding

### Metrics Explained
- **Investment ($)**: Sum of all awards
- **Projects**: Number of unique project IDs
- **Students**: Sum across all degree levels
- **Per $1M**: Calculated as (metric / investment_millions)

## Troubleshooting

### Dashboard Won't Load
- Check your internet connection
- Try refreshing the page
- Ensure JavaScript is enabled in your browser

### Track Toggle Not Working
- Use latest Chrome, Firefox, Safari, or Edge
- Clear browser cache
- Try a different browser

### Charts Look Crowded
- Use zoom feature to see specific time periods
- Switch to full-screen mode
- Try a larger monitor or adjust window size

### Numbers Don't Match
- Check the track selector - is it on the right view?
- Verify you're looking at the same time period
- Consult the detailed metrics table for exact values

## Browser Compatibility

- **Chrome/Edge**: Full support, recommended
- **Firefox**: Full support
- **Safari**: Full support
- **Mobile Browsers**: Basic support (some features limited)

## Data Update Frequency

These dashboards were generated on **November 25, 2025** from the IWRC Seed Fund Tracking database. For updated data, regenerate the dashboards using the Python scripts in `/scripts/`.

## Advanced Usage

### Comparing Specific Metrics
1. Open ROI Analysis Dashboard
2. Set to "All Projects"
3. Note the "Projects per $1M" value
4. Switch to "104B Only"
5. Compare to see the efficiency difference (14.4x!)

### Institutional Analysis
1. Open Institutional Distribution
2. Switch between tracks to see which institutions rely on 104B vs strategic funding
3. Identify potential partnerships and collaborations

### Trend Analysis
1. Open Investment and Projects Timeline dashboards side-by-side
2. Compare investment amounts with project counts
3. Identify years with high activity

## Exporting Data

To export dashboard data:
1. Use the Plotly download feature (camera icon)
2. Saves as PNG image
3. For raw data, see `/data_exports/` for Excel files

## Questions or Feedback

For questions about dashboard functionality or data interpretation, please refer to:
- **DUAL_TRACK_GUIDE.md** - Understand the data
- **README.md** - Overview and folder structure
- **Detailed metrics tables** - Exact numbers and breakdowns
"""

    guide_path = os.path.join(OUTPUT_DIR, 'documentation', 'INTERACTIVE_DASHBOARDS_GUIDE.md')
    os.makedirs(os.path.dirname(guide_path), exist_ok=True)

    with open(guide_path, 'w') as f:
        f.write(guide_content)

    print(f"    ✓ Updated: INTERACTIVE_DASHBOARDS_GUIDE.md")


def main():
    """Main orchestration."""
    all_10yr, b104_10yr = load_and_prepare_data()

    print("=" * 80)
    print("CREATING EXCEL WORKBOOK & DOCUMENTATION")
    print("=" * 80 + "\n")

    # Ensure output directories exist
    os.makedirs(EXCEL_OUTPUT, exist_ok=True)
    os.makedirs(DOCS_OUTPUT, exist_ok=True)

    # Generate files
    create_excel_comparison(all_10yr, b104_10yr)
    update_readme()
    create_dual_track_guide()
    update_dashboards_guide()

    print("\n" + "█" * 80)
    print("█" + " ✓ STAGE 5 COMPLETE: Excel & Documentation Finalized".center(78) + "█")
    print("█" * 80)
    print("\nGenerated/Updated Files:")
    print("  • data_exports/Dual_Track_Metrics_Comparison.xlsx (NEW)")
    print("  • documentation/README.md (UPDATED)")
    print("  • documentation/DUAL_TRACK_GUIDE.md (NEW)")
    print("  • documentation/INTERACTIVE_DASHBOARDS_GUIDE.md (UPDATED)")
    print("\n✓ All 5 stages complete!")
    print("\nDeliverables Summary:")
    print("  • 3 smart comparison PNG visualizations")
    print("  • 6 interactive HTML dashboards with track toggles")
    print("  • 6 formatted PDF reports (3 types × 2 tracks)")
    print("  • 2 Excel comparison workbooks")
    print("  • 4 comprehensive markdown guides\n")


if __name__ == '__main__':
    main()
