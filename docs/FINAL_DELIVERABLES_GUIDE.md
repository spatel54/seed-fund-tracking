# IWRC Seed Fund Tracking - FINAL_DELIVERABLES Guide

**Purpose:** Comprehensive guide to the FINAL_DELIVERABLES folder structure and contents.

## Directory Structure Overview

```
FINAL_DELIVERABLES/
├── visualizations/
│   ├── static/
│   │   ├── all_projects/
│   │   │   └── [individual project visualizations]
│   │   ├── 104b_only/
│   │   │   └── [seed funding specific visualizations]
│   │   ├── investment_comparison_All_Projects.png
│   │   ├── investment_comparison_104B_Only.png
│   │   ├── students_trained_All_Projects.png
│   │   ├── students_trained_104B_Only.png
│   │   ├── roi_analysis_All_Projects.png
│   │   └── roi_analysis_104B_Only.png
│   ├── interactive/
│   │   ├── all_projects/
│   │   │   ├── roi_analysis_dashboard.html
│   │   │   ├── institutional_distribution_map.html
│   │   │   ├── detailed_analysis.html
│   │   │   ├── students_interactive.html
│   │   │   ├── investment_interactive.html
│   │   │   └── projects_timeline.html
│   │   ├── 104b_only/
│   │   │   ├── roi_analysis_dashboard.html
│   │   │   ├── institutional_distribution_map.html
│   │   │   ├── detailed_analysis.html
│   │   │   ├── students_interactive.html
│   │   │   ├── investment_interactive.html
│   │   │   └── projects_timeline.html
│   │   └── award_type_comparison/
│   │       ├── dual_track_comparison.html
│   │       ├── metrics_dashboard.html
│   │       └── investment_breakdown.html
│   ├── pdfs/
│   │   ├── all_projects/
│   │   │   ├── IWRC_ROI_Analysis_Report.pdf
│   │   │   ├── Seed_Fund_Tracking_Analysis.pdf
│   │   │   ├── Institutional_Distribution.pdf
│   │   │   └── Research_Keywords.pdf
│   │   └── 104b_only/
│   │       ├── IWRC_ROI_Analysis_Report.pdf
│   │       ├── Seed_Fund_Tracking_Analysis.pdf
│   │       ├── Institutional_Distribution.pdf
│   │       └── Research_Keywords.pdf
├── data_exports/
│   ├── Award_Type_Metrics_Comparison.xlsx
│   ├── All_Projects_10Year_Summary.xlsx
│   ├── 104B_Only_10Year_Summary.xlsx
│   ├── Institution_Rankings.xlsx
│   └── Student_Demographics.xlsx
└── README.md
```

## Visualizations Explained

### Static Visualizations (PNG, 300 DPI)

**Location:** `visualizations/static/`

#### 1. Investment Comparison Charts
- **Files:**
  - `investment_comparison_All_Projects.png`
  - `investment_comparison_104B_Only.png`

- **Content:**
  - 10-Year Investment (2015-2024)
  - 5-Year Investment (2020-2024)
  - Side-by-side horizontal bar charts
  - Total amounts labeled on bars

- **Use Cases:**
  - Executive summaries
  - Funding reports
  - Stakeholder presentations
  - Annual reports

- **Specifications:**
  - Size: 10" × 6"
  - Resolution: 300 DPI (print quality)
  - Colors: IWRC #258372 (teal), #639757 (olive)
  - Font: Montserrat Semibold (titles), Light (text)

#### 2. Students Trained Charts
- **Files:**
  - `students_trained_All_Projects.png`
  - `students_trained_104B_Only.png`

- **Content:**
  - Total student training impact
  - 10-Year and 5-Year comparisons
  - Raw numbers displayed
  - Training reach indicator

- **Use Cases:**
  - Educational impact reporting
  - Workforce development claims
  - Institutional contribution summary
  - Research capacity building

#### 3. ROI Analysis Charts
- **Files:**
  - `roi_analysis_All_Projects.png`
  - `roi_analysis_104B_Only.png`

- **Content:**
  - IWRC seed funding amounts
  - Follow-on funding generated
  - Side-by-side comparison bars
  - ROI multiplier calculation

- **Use Cases:**
  - Return on investment justification
  - Funding efficacy demonstration
  - Grant multiplication evidence
  - Economic impact reporting

### Interactive Visualizations (HTML)

**Location:** `visualizations/interactive/`

#### All Projects Track (104B + 104G + Coordination)

**1. ROI Analysis Dashboard**
- **File:** `all_projects/roi_analysis_dashboard.html`
- **Features:**
  - Multi-panel layout (6 subplots)
  - Investment trend line
  - Project count bars
  - Student support area chart
  - ROI trend visualization
  - Top 10 institutions bar chart
  - Project distribution pie chart
- **Interaction:** Hover tooltips, zoom, pan, download
- **Size:** ~2-3 MB

**2. Geographic Distribution Map**
- **File:** `all_projects/institutional_distribution_map.html`
- **Features:**
  - Illinois base map (Folium)
  - Institution markers (size = funding)
  - Color coding by project count
  - Popup information cards
  - Heatmap layer
  - Layer controls
- **Data Points:** All institutions with coordinates
- **Size:** ~1-2 MB

**3. Detailed Analysis Dashboard**
- **File:** `all_projects/detailed_analysis.html`
- **Features:**
  - Funding breakdown by category (stacked bars)
  - Cumulative student training
  - ROI trend with projections
  - Key metrics indicators
  - Multi-year historical data
- **Interaction:** Hover, legend clicks, range selection
- **Size:** ~1.5 MB

**4. Student Analysis (Sunburst)**
- **File:** `all_projects/students_interactive.html`
- **Features:**
  - Hierarchical visualization (Type → Institution)
  - Click to zoom by category
  - Student count breakdown
  - Color-coded by count
  - Interactive legend
- **Degrees Shown:** PhD, Masters, Undergrad, Postdoc
- **Size:** ~1 MB

**5. Investment Analysis (Treemap)**
- **File:** `all_projects/investment_interactive.html`
- **Features:**
  - Two-level hierarchy (Institution → Category)
  - Color-coded by amount
  - Size proportional to investment
  - Click to drill down
  - Percentage display
- **Categories:** Research, Equipment, Students, Other
- **Size:** ~1 MB

**6. Projects Timeline (Gantt)**
- **File:** `all_projects/projects_timeline.html`
- **Features:**
  - Project durations (2015-2024)
  - Institutions on y-axis
  - Color-coded by funding amount
  - Hover for project details
  - Year-based x-axis
- **Projects Shown:** All 77 (10-year)
- **Size:** ~2 MB

#### 104B Only Track (Seed Funding)
- **Same 6 visualizations** as "All Projects"
- **Location:** `104b_only/` subdirectory
- **Difference:** Filtered to 104B awards only (60 projects)

#### Award Type Comparison (New)
- **Location:** `award_type_comparison/`
- **Files:**
  - `dual_track_comparison.html` - Side-by-side metrics
  - `metrics_dashboard.html` - Comparative KPIs
  - `investment_breakdown.html` - 104G vs 104B split

### PDF Reports

**Location:** `pdfs/all_projects/` and `pdfs/104b_only/`

#### 1. IWRC_ROI_Analysis_Report.pdf
- **Pages:** 5
- **Contents:**
  - Title page with key findings
  - Investment overview (bars)
  - Project distribution comparison
  - ROI analysis with funding breakdown
  - Student training by degree level
  - Executive summary table
- **Use:** Funding justification, proposals
- **Size:** ~1-2 MB

#### 2. Seed_Fund_Tracking_Analysis.pdf
- **Pages:** 6-8
- **Contents:**
  - Overview and methodology
  - Detailed metrics breakdown
  - Year-by-year trends
  - Institution rankings
  - Research focus areas
  - Conclusions and recommendations
- **Use:** Comprehensive reporting, archives
- **Size:** ~2-3 MB

#### 3. Institutional_Distribution.pdf
- **Pages:** 3-4
- **Contents:**
  - Geographic map (state level)
  - Institution rankings by funding
  - Institution rankings by projects
  - Institutional reach table
- **Use:** Partner reporting, stakeholder updates
- **Size:** ~1-2 MB

#### 4. Research_Keywords.pdf
- **Pages:** 2-3
- **Contents:**
  - Keyword frequency pie chart
  - Research focus distribution
  - Top keywords table
  - Research theme analysis
- **Use:** Research impact reporting, trend analysis
- **Size:** ~1 MB

### Data Exports (Excel)

**Location:** `data_exports/`

#### 1. Award_Type_Metrics_Comparison.xlsx
- **Sheets:**
  - Comparison: Side-by-side metrics
  - Summary statistics
  - Growth trends (10yr vs 5yr)
- **Metrics:** Projects, Investment, Students, Institutions
- **Use:** Quick reference, data validation
- **Size:** ~50 KB

#### 2. All_Projects_10Year_Summary.xlsx
- **Sheets:**
  - Overview (aggregate metrics)
  - By Year (annual breakdown)
  - By Institution (institution rankings)
  - By Award Type (104B vs 104G split)
  - By Student Level (degree breakdown)
- **Rows:** 77 unique projects
- **Columns:** ID, Title, PI, Institution, Award, Students, Year
- **Size:** ~200 KB

#### 3. 104B_Only_10Year_Summary.xlsx
- **Sheets:** Same as All_Projects version
- **Rows:** 60 unique projects (104B only)
- **Focus:** Seed funding analysis
- **Size:** ~150 KB

#### 4. Institution_Rankings.xlsx
- **Sheets:**
  - By Total Funding
  - By Project Count
  - By Student Impact
  - By Award Count
- **Includes:** All 16 institutions
- **Metrics:** Rankings, totals, percentages
- **Size:** ~100 KB

#### 5. Student_Demographics.xlsx
- **Sheets:**
  - Degree Level Distribution
  - By Institution
  - By Year
  - By Award Type
- **Student Counts:** PhD, Masters, Undergrad, Postdoc
- **Total:** 304 students (all), 202 (104B only)
- **Size:** ~80 KB

## Key Metrics Summary

### All Projects Track
```
Time Period: 2015-2024 (10 years)
Unique Projects: 77
Total Investment: $8,516,278
Students Trained: 304
Institutions: 16
Award Types: 104B, 104G-AIS, 104G-General, 104G-PFAS, Coordination

Time Period: 2020-2024 (5 years)
Unique Projects: 47
Total Investment: $7,319,144
Students Trained: 186
Institutions: 11
```

### 104B Only Track
```
Time Period: 2015-2024 (10 years)
Unique Projects: 60
Total Investment: $1,675,465
Students Trained: 202
Institutions: 16

Time Period: 2020-2024 (5 years)
Unique Projects: 33
Total Investment: $1,074,700
Students Trained: 100
Institutions: 11
```

## Branding Standards

All deliverables follow IWRC branding guidelines:

### Colors
- **Primary:** #258372 (Teal) - Main brand color
- **Secondary:** #639757 (Olive) - Secondary accent
- **Text:** #54595F (Dark Gray) - Body text
- **Accent:** #FCC080 (Peach) - Highlights
- **Background:** #F6F6F6 (Light Gray) - Backgrounds

### Fonts
- **Headlines:** Montserrat Semibold (Bold, 14-24pt)
- **Body Text:** Montserrat Light (Regular, 9-12pt)
- **Labels:** Montserrat Regular (10-11pt)

### Logo
- IWRC logo appears on:
  - All static visualizations (top-right corner)
  - PDF title pages
  - HTML dashboard headers
  - Report covers

### Resolution & Format
- **Static (PNG):** 300 DPI (print quality)
- **Interactive (HTML):** Screen-optimized, responsive
- **Reports (PDF):** 8.5" × 11" (letter size)
- **Exports (Excel):** Standard format, pivot-table ready

## Usage Guidelines

### For Executives/Stakeholders
1. Start with **Investment Comparison** PNGs (quick overview)
2. Review **IWRC_ROI_Analysis_Report.pdf** (comprehensive)
3. Check **metrics_dashboard.html** (interactive exploration)
4. Export to Excel for further analysis if needed

### For Detailed Analysis
1. Open **Detailed_Analysis.html** (interactive)
2. Use **Award_Type_Metrics_Comparison.xlsx** (data validation)
3. Review institution rankings via **Institution_Rankings.xlsx**
4. Explore student impact in **Student_Demographics.xlsx**

### For Reports & Presentations
1. **Static PNGs** (6 charts) - Copy directly into PowerPoint/Word
2. **PDF Reports** - Print or distribute as-is
3. **Excel Files** - Create custom charts/tables as needed
4. **HTML Dashboards** - Share link for interactive exploration

### For Archival
1. All files organized by award type (all_projects vs 104b_only)
2. Multiple formats (PNG, PDF, HTML, XLSX) for long-term access
3. Timestamped: November 25, 2025 generation
4. Version tracked in git repository

## File Access & Download

### Local Access
```bash
# View all static visualizations
open FINAL_DELIVERABLES/visualizations/static/

# Open interactive dashboard
open FINAL_DELIVERABLES/visualizations/interactive/all_projects/roi_analysis_dashboard.html

# Access data exports
open FINAL_DELIVERABLES/data_exports/Award_Type_Metrics_Comparison.xlsx
```

### Sharing with Stakeholders
1. **PNGs:** Can be emailed, posted online, printed
2. **PDFs:** Ready for distribution, print-friendly
3. **HTML:** Can be hosted on web server, shared via link
4. **Excel:** For specific analysis, data-driven decisions

## Quality Assurance Checklist

- ✓ All PNGs at 300 DPI (print quality)
- ✓ IWRC branding on all visualizations
- ✓ Montserrat fonts configured
- ✓ Dual-track analysis complete (All vs 104B)
- ✓ Metrics verified against expected counts
- ✓ File naming conventions consistent
- ✓ Directory structure organized
- ✓ All dates/timestamps current
- ✓ Interactive features tested
- ✓ PDF generation complete

## Updating Deliverables

### To Regenerate Static Visualizations
```bash
python3 scripts/generate_final_deliverables.py
```
Output: 6 PNG files + 1 Excel workbook

### To Regenerate Interactive Dashboards
```bash
python3 scripts/generate_interactive_visualizations.py
```
Output: 12 HTML files (6 per track)

### To Regenerate PDF Reports
```bash
python3 scripts/generate_pdf_reports.py
```
Output: 8 PDF files (4 per track)

## Support & Questions

For questions about:
- **Award type filtering:** See [AWARD_TYPE_ANALYSIS_GUIDE.md](AWARD_TYPE_ANALYSIS_GUIDE.md)
- **IWRC branding:** See [REBRANDING_SUMMARY.md](REBRANDING_SUMMARY.md)
- **Data processing:** See individual script documentation
- **File structure:** See directory structure above

## References

- IWRC Logo: `IWRC Logo - Full Color.svg`
- Branding Module: `scripts/iwrc_brand_style.py`
- Filter Module: `scripts/award_type_filters.py`
- Master Script: `scripts/generate_final_deliverables.py`
- Data Source: `data/consolidated/IWRC Seed Fund Tracking.xlsx`

---

**Last Updated:** November 25, 2025
**Version:** 1.0
**Structure:** Dual-Track Analysis (All Projects & 104B Only)
