# Project Type Composition Charts Guide

**Added:** November 26, 2025
**Location:** `/visualizations/static/`

---

## Overview

Two new composition charts have been added to FINAL_DELIVERABLES_2 showing how IWRC Seed Fund projects break down by project type across different time periods.

---

## Files Added

### 1. `project_type_composition_10yr_All_Projects.png`
**10-Year Period Analysis (2015-2024)**

Shows three side-by-side pie charts displaying the distribution across project types:
- **Left pie:** Investment Distribution
- **Center pie:** Project Distribution
- **Right pie:** Student Distribution

**Project Types:**
- **104B (Teal):** Base Grants - core seed funding mechanism
- **104G (Olive):** Specialized programs (AIS, General, PFAS combined)
- **Coordination (Peach):** Strategic coordination and administrative support

### 2. `project_type_composition_5yr_All_Projects.png`
**5-Year Period Analysis (2020-2024)**

Same format as 10-year chart, showing more recent trends.

---

## Key Metrics

### 10-Year Period (2015-2024)

| Metric | 104B | 104G | Coordination |
|--------|------|------|--------------|
| **Projects** | 60 (78%) | 10 (13%) | 5 (6%) |
| **Investment** | $1.7M (20%) | $5.3M (63%) | $1.5M (17%) |
| **Students** | 202 (66%) | 90 (30%) | 12 (4%) |
| **Avg per Project** | $28K | $530K | $299K |

### 5-Year Period (2020-2024)

| Metric | 104B | 104G | Coordination |
|--------|------|------|--------------|
| **Projects** | 33 (70%) | 9 (19%) | 3 (6%) |
| **Investment** | $1.1M (15%) | $4.8M (66%) | $1.4M (19%) |
| **Students** | 100 (54%) | 76 (41%) | 10 (5%) |
| **Avg per Project** | $33K | $538K | $467K |

---

## Key Insights

### 1. Investment Concentration
**104G programs** receive the majority of funding (63-66%) despite representing only 13-19% of projects. This reflects their nature as larger, specialized research initiatives.

### 2. Student Training Dominance
**104B projects** train the majority of students (54-66%) through higher project volume and lower cost per student (~$8,300 vs $75,000+ for 104G).

### 3. Project Type Roles
- **104B:** High-volume, cost-effective seed funding that maximizes student training
- **104G:** Lower volume, higher investment specialized research on critical water challenges
- **Coordination:** Small but essential administrative support (6% of projects)

### 4. Efficiency Trade-offs
- **104B:** More students per dollar, broader institutional reach
- **104G:** Deeper research impact, focused expertise on specific challenges
- **Coordination:** Strategic program management and stakeholder engagement

---

## How to Use These Charts

### For Presentations
- Use to show **program composition** and resource allocation
- Highlight the **complementary nature** of different project types
- Demonstrate **balanced portfolio** approach (volume + depth)

### For Budget Planning
- Understand **investment distribution** patterns
- Plan resource allocation between **seed funding** (104B) and **specialized programs** (104G)
- Justify need for **both** project types to maximize impact

### For Grant Proposals
- Cite **student training efficiency** of 104B projects
- Reference **research depth** enabled by 104G programs
- Show **strategic coordination** through Coordination grants

### For Program Evaluation
- Compare **10-year vs 5-year** trends to identify shifts
- Assess whether current **mix** of project types aligns with goals
- Identify opportunities to **optimize** portfolio balance

---

## Chart Specifications

- **Format:** PNG (Portable Network Graphics)
- **Resolution:** 300 DPI (print quality)
- **Dimensions:** 4800 × 1800 pixels (16" × 6" at 300 DPI)
- **Color Scheme:** IWRC brand colors
  - 104B: Teal (#258372)
  - 104G: Olive (#639757)
  - Coordination: Peach (#FCC080)
- **Font:** Montserrat
- **Size:** ~265 KB each

---

## Related Deliverables

These composition charts complement existing deliverables:

- **Investment comparison charts:** Show total investment over time
- **Student distribution pie:** Shows breakdown by degree level
- **Institutional reach charts:** Show geographic distribution
- **ROI analysis:** Shows return on investment metrics

For complete project type breakdown analysis including stacked/grouped bar charts and interactive dashboards, see **FINAL_DELIVERABLES_3**.

---

## Data Source

- **Source File:** `data/consolidated/IWRC Seed Fund Tracking.xlsx`
- **Sheet:** Project Overview
- **Time Periods:** 2015-2024 (10-year), 2020-2024 (5-year)
- **Methodology:** Unique project counts (not duplicate rows)
- **Project Type Categorization:**
  - 104B: Award Type = "Base Grant (104b)"
  - 104G: Award Type contains "104g" (AIS, General, PFAS combined)
  - Coordination: Award Type contains "Coordination"

---

## Questions?

For more information about project type analysis:
- See full breakdown in **FINAL_DELIVERABLES_3/**
- Review generation script: `scripts/generate_project_type_breakdown.py`
- Consult data source: `data/consolidated/IWRC Seed Fund Tracking.xlsx`

---

**Generated:** November 26, 2025
**Added to:** FINAL_DELIVERABLES_2 (v1.1)
