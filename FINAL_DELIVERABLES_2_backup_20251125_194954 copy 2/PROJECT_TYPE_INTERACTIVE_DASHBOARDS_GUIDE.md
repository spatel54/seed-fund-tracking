# Project Type Interactive Dashboards Guide

**Added:** November 26, 2025
**Location:** `/visualizations/interactive/`
**Format:** HTML (Plotly-based)

---

## Overview

Two new interactive dashboards have been added to FINAL_DELIVERABLES_2, providing dynamic exploration of project type composition across time periods. These dashboards complement the static composition pie charts with interactive features including hover tooltips, zoomable charts, and detailed data tables.

---

## Files Added

### 1. `project_type_interactive_All_Projects.html` (4.6 MB)
**Comprehensive Analysis Dashboard**

Interactive dashboard showing project type breakdown for all IWRC Seed Fund projects (104B + 104G + Coordination).

**Layout:** 2×2 grid with 4 panels
- **Panel 1 (Top-Left):** Investment by Project Type - Stacked bars
- **Panel 2 (Top-Right):** Projects by Project Type - Grouped bars
- **Panel 3 (Bottom-Left):** Students by Project Type - Stacked bars
- **Panel 4 (Bottom-Right):** Summary Metrics Table

### 2. `project_type_interactive_104B_Only.html` (4.6 MB)
**Seed Funding Focus Dashboard**

Same layout as All Projects, but filtered to show only Base Grant (104B) projects - the core seed funding mechanism.

---

## Dashboard Features

### Interactive Elements

**Hover Tooltips:**
- Hover over any bar to see exact values
- Shows period, project type, and metric value
- Example: "10-Year: Investment: $5,343,102"

**Zoom & Pan:**
- Click and drag to zoom into specific areas
- Double-click to reset zoom
- Pan by clicking and dragging after zoom

**Legend Controls:**
- Click legend items to show/hide data series
- Double-click to isolate single series
- Useful for focusing on specific project types

**Responsive Design:**
- Automatically adjusts to screen size
- Works on desktop, tablet, and mobile
- Professional appearance for presentations

### Panel Details

#### Panel 1: Investment by Project Type (Stacked Bars)
**Purpose:** Show how total investment breaks down by project type

**Chart Type:** Stacked bar chart
- X-axis: Two periods (10-Year, 5-Year)
- Y-axis: Total Investment ($)
- Stacks: 104B (teal), 104G (olive), Coordination (peach)

**What You'll See:**
- 10-Year bar stacked to ~$8.5M total
- 5-Year bar stacked to ~$7.3M total
- Each segment labeled with project type
- Hover shows exact dollar amounts

**Use For:**
- Demonstrating investment allocation
- Comparing period totals
- Showing project type proportions

#### Panel 2: Projects by Project Type (Grouped Bars)
**Purpose:** Compare number of projects across project types and periods

**Chart Type:** Grouped bar chart
- X-axis: Three project types (104B, 104G, Coordination)
- Y-axis: Number of Projects
- Groups: 10-Year (teal) vs 5-Year (olive) side-by-side

**What You'll See:**
- 104B: ~60 projects (10yr) vs ~33 projects (5yr)
- 104G: ~10 projects (10yr) vs ~9 projects (5yr)
- Coordination: ~5 projects (10yr) vs ~3 projects (5yr)

**Use For:**
- Identifying which project types have most activity
- Comparing trends between periods
- Understanding project volume distribution

#### Panel 3: Students by Project Type (Stacked Bars)
**Purpose:** Show student training distribution by project type

**Chart Type:** Stacked bar chart (same format as Panel 1)
- X-axis: Two periods (10-Year, 5-Year)
- Y-axis: Total Students Trained
- Stacks: 104B (teal), 104G (olive), Coordination (peach)

**What You'll See:**
- 10-Year: ~304 students total
- 5-Year: ~186 students total
- 104B dominates student training (66% in 10yr, 54% in 5yr)

**Use For:**
- Demonstrating educational impact
- Showing which project types train most students
- Justifying student training programs

#### Panel 4: Summary Metrics Table
**Purpose:** Provide exact numbers for all metrics

**Format:** Interactive data table with sortable columns
- **Columns:** Period, Type, Projects, Investment, Students
- **Rows:** 6 total (3 project types × 2 periods)

**What You'll See:**
| Period | Type | Projects | Investment | Students |
|--------|------|----------|------------|----------|
| 10-Year | 104B | 60 | $1,675,465 | 202 |
| 10-Year | 104G | 10 | $5,343,102 | 90 |
| 10-Year | Coordination | 5 | $1,497,711 | 12 |
| 5-Year | 104B | 33 | $1,074,700 | 100 |
| 5-Year | 104G | 9 | $4,844,444 | 76 |
| 5-Year | Coordination | 3 | $1,400,000 | 10 |

**Use For:**
- Quick reference for exact figures
- Copy-paste into reports/presentations
- Verify calculations

---

## How to Use the Dashboards

### Opening the Dashboard

**Method 1: Direct Open**
1. Navigate to `FINAL_DELIVERABLES_2/visualizations/interactive/`
2. Double-click `project_type_interactive_All_Projects.html`
3. Dashboard opens in your default web browser

**Method 2: Drag & Drop**
1. Drag the HTML file onto your web browser window
2. Dashboard loads immediately

**Method 3: Right-Click**
1. Right-click the HTML file
2. Select "Open With" → Choose your preferred browser

**No Internet Required:** Dashboards work completely offline

### Navigation Tips

**Exploring Data:**
1. Start by hovering over bars to see exact values
2. Use Panel 4 table for precise numbers
3. Compare panels to understand relationships

**Focusing on Specific Data:**
1. Click legend items to hide/show project types
2. Zoom into specific areas for detail
3. Use grouped bars (Panel 2) for side-by-side comparison

**Taking Screenshots:**
1. Position dashboard to show desired view
2. Use browser screenshot tools or OS screenshot
3. High-quality captures for presentations

### Presentation Mode

**For Live Presentations:**
1. Open dashboard in full-screen mode (F11 in most browsers)
2. Use hover tooltips to highlight specific data points
3. Zoom into details when answering questions
4. Switch between All Projects and 104B Only dashboards to show different perspectives

**For Screen Sharing:**
1. Dashboard responsive design works well for video calls
2. Hover interactions visible to remote participants
3. Can navigate between panels during presentation

---

## Key Insights from the Dashboards

### All Projects Dashboard Highlights

**Investment Concentration (Panel 1):**
- 104G receives 63-66% of total investment
- Despite being only 13-19% of projects
- Average 104G project: $530K+ vs $28-33K for 104B

**Project Volume (Panel 2):**
- 104B projects dominate in quantity (70-78%)
- Coordination maintains steady ~6% share
- 104G projects show consistency across periods

**Student Training (Panel 3):**
- 104B trains majority of students (54-66%)
- Due to higher project volume, not larger project size
- Cost-effective student training mechanism

### 104B Only Dashboard Highlights

**Single Type Display:**
- Shows 100% 104B data (no 104G or Coordination)
- Useful for seed funding-specific analysis
- Demonstrates isolated impact of core grant mechanism

**Comparative Value:**
- Compare All Projects vs 104B Only dashboards
- Understand 104B contribution to overall program
- Quantify value-add of 104G and Coordination

---

## Technical Specifications

### File Format
- **Type:** HTML5 with embedded JavaScript
- **Library:** Plotly.js (self-contained, no CDN dependencies)
- **Data:** Embedded in HTML (no external files needed)
- **Size:** ~4.6 MB each (due to embedded Plotly library + data)

### Browser Compatibility
- **Chrome/Chromium:** Full support
- **Firefox:** Full support
- **Safari:** Full support
- **Edge:** Full support
- **Minimum:** Any modern browser (released 2018+)

### Performance
- **Load Time:** 1-3 seconds on typical connection
- **Interaction:** Instant response to hover/click
- **Memory:** ~50-100 MB when open (normal for interactive charts)

### Accessibility
- **Keyboard Navigation:** Supported
- **Screen Readers:** Limited (visual content)
- **Color Contrast:** WCAG AA compliant
- **Text Size:** Scalable via browser zoom

---

## Use Cases

### For Executive Presentations
**Scenario:** Board meeting on program effectiveness

**How to Use:**
1. Open All Projects dashboard full-screen
2. Show Panel 1 to demonstrate investment allocation
3. Highlight 104G's larger share despite fewer projects
4. Switch to Panel 3 to show 104B's student training dominance
5. Use Panel 4 table for specific numbers when asked

**Key Message:** "Balanced portfolio - volume through 104B, depth through 104G"

### For Budget Planning
**Scenario:** Planning next year's allocations

**How to Use:**
1. Compare 10-Year vs 5-Year bars in each panel
2. Identify trends (e.g., 104G maintaining investment share)
3. Use Panel 2 to see project count changes
4. Reference Panel 4 for budget modeling

**Key Message:** "Historical patterns inform future allocations"

### For Grant Proposals
**Scenario:** Writing proposal for new funding source

**How to Use:**
1. Screenshot Panel 3 showing student training impact
2. Include Panel 4 table in budget justification
3. Reference Panel 1 to show efficient resource use
4. Compare All Projects vs 104B Only to highlight seed funding value

**Key Message:** "Proven track record across multiple funding mechanisms"

### For Stakeholder Reports
**Scenario:** Annual report to funding agency

**How to Use:**
1. Embed screenshots from all four panels
2. Include link to HTML dashboard for interactive exploration
3. Provide context from Panel 4 data table
4. Show both dashboards to demonstrate transparency

**Key Message:** "Comprehensive impact across all project types"

---

## Comparison with Static Charts

### When to Use Interactive Dashboards

**Best For:**
- Live presentations with Q&A
- Exploratory data analysis
- Stakeholder meetings requiring detail
- Digital distribution (email, web)

**Advantages:**
- Exact values via hover
- Multiple views in one file
- Zoom for detail
- Professional interactive experience

### When to Use Static PNG Charts

**Best For:**
- Print materials (reports, brochures)
- PowerPoint/Keynote presentations
- Email attachments (smaller files)
- Situations without computer access

**Advantages:**
- Smaller file size (~265 KB vs 4.6 MB)
- Universal compatibility
- Print-ready quality (300 DPI)
- Simple, focused message

**Recommendation:** Use both - static PNGs for broad distribution, interactive dashboards for deep engagement

---

## Troubleshooting

### Dashboard Won't Open
**Problem:** HTML file doesn't open or shows blank page

**Solutions:**
1. Try different browser (Chrome recommended)
2. Check file isn't corrupted (should be 4.6 MB)
3. Disable browser extensions temporarily
4. Update browser to latest version

### Charts Not Interactive
**Problem:** Can't hover or zoom

**Solutions:**
1. Ensure JavaScript is enabled in browser
2. Try private/incognito window
3. Check browser console for errors (F12)

### Performance Issues
**Problem:** Dashboard slow or laggy

**Solutions:**
1. Close other browser tabs
2. Update browser to latest version
3. Restart browser
4. Try on different device

### Can't See All Panels
**Problem:** Layout looks broken or cut off

**Solutions:**
1. Zoom out in browser (Ctrl/Cmd + minus)
2. Maximize browser window
3. Try landscape mode on tablet
4. Check minimum screen size (1024px recommended)

---

## Data Source & Methodology

### Data Source
- **File:** `data/consolidated/IWRC Seed Fund Tracking.xlsx`
- **Sheet:** Project Overview
- **Rows:** 354 total (220 in 10-year, 142 in 5-year after filtering)

### Processing
1. **Project Type Categorization:**
   - 104B: Award Type = "Base Grant (104b)"
   - 104G: Award Type contains "104g" (combines AIS, General, PFAS)
   - Coordination: Award Type = "Coordination Grant"

2. **Time Period Filtering:**
   - 10-Year: Projects from 2015-2024
   - 5-Year: Projects from 2020-2024

3. **Metric Calculation:**
   - Projects: Count of unique Project IDs
   - Investment: Sum of Award Amount
   - Students: Sum of PhD + MS + Undergrad + PostDoc

### Quality Assurance
- All data deduplicated (unique projects only)
- Cross-validated with static charts
- Metrics consistent with other deliverables
- Verified against source spreadsheet

---

## Related Documentation

**For More Details:**
- See `PROJECT_TYPE_COMPOSITION_CHARTS_GUIDE.md` for static chart documentation
- Review `README.md` for complete deliverables overview
- Explore `FINAL_DELIVERABLES_3/` for full project type analysis

**For Source Data:**
- `data/consolidated/IWRC Seed Fund Tracking.xlsx`
- `scripts/generate_project_type_breakdown.py` (generation script)

---

## Version History

**v1.0 - November 26, 2025**
- Initial release
- All Projects and 104B Only dashboards
- 2×2 panel layout
- IWRC brand styling

---

**Created:** November 26, 2025
**Added to:** FINAL_DELIVERABLES_2 (v1.1)
**File Size:** 4.6 MB each (2 files, 9.2 MB total)
**Format:** HTML5 + Plotly.js
**Works Offline:** Yes
