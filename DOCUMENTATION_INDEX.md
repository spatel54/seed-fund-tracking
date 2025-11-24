# IWRC Seed Fund Documentation Index

**Last Updated:** November 23, 2025

---

## Quick Reference

All documentation has been regenerated with **CORRECTED project counts**:
- **10-Year (2015-2024):** 77 unique projects (not 220 rows)
- **5-Year (2020-2024):** 47 unique projects (not 142 rows)

---

## Markdown Documentation (`/docs/`)

### Core Analysis Documents

1. **[ANALYSIS_SUMMARY.md](docs/ANALYSIS_SUMMARY.md)**
   - Executive overview with key findings
   - 10-year and 5-year summary metrics
   - Corrected project counts: 77 (10yr), 47 (5yr)
   - Student breakdowns and institutional reach

2. **[METHODOLOGY.md](docs/METHODOLOGY.md)**
   - Complete analysis methodology
   - Year extraction from Project IDs
   - Project counting approach (unique IDs)
   - Metrics calculation formulas
   - Data quality assurance

3. **[DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md)**
   - All column and field definitions
   - Data types and formats
   - Valid values and ranges
   - Source-to-analysis column mapping

### Detailed Analysis Documents

4. **[INSTITUTIONAL_REACH.md](docs/INSTITUTIONAL_REACH.md)**
   - 16 institutions (10-year), 11 institutions (5-year)
   - Funding distribution by institution
   - Geographic equity analysis
   - Top 10 institutions by funding

5. **[STUDENT_ANALYSIS.md](docs/STUDENT_ANALYSIS.md)**
   - 304 students total (10yr), 186 students (5yr)
   - PhD: 118/88, Master's: 52/26, Undergrad: 127/65, PostDoc: 7/7
   - Students per year trends
   - Students per institution

6. **[FINDINGS.md](docs/FINDINGS.md)**
   - Key insights and conclusions
   - ROI analysis: 0.03x (10yr), 0.04x (5yr)
   - Program effectiveness assessment
   - Evidence-based recommendations

### Correction Documentation

7. **[CORRECTION_NOTES.md](docs/CORRECTION_NOTES.md)**
   - Explanation of project count correction
   - Why duplicates existed (one-row-per-output structure)
   - Impact: Old counts inflated by ~3x
   - Verification methodology

---

## PDF Reports (`/reports/`)

### Executive and Summary Reports

1. **[IWRC_Seed_Fund_Executive_Summary.pdf](reports/IWRC_Seed_Fund_Executive_Summary.pdf)**
   - 2-page professional summary
   - Key metrics for 10-year and 5-year periods
   - Ideal for stakeholder presentations

2. **[IWRC_Fact_Sheet.pdf](reports/IWRC_Fact_Sheet.pdf)**
   - 1-page quick reference
   - Large, prominent numbers
   - Scannable format for communications

### Detailed Analysis Reports

3. **[IWRC_Detailed_Analysis_Report.pdf](reports/IWRC_Detailed_Analysis_Report.pdf)**
   - Multi-page comprehensive report
   - Student training tables
   - Top institutions analysis
   - Conclusions and recommendations

4. **[IWRC_Financial_Summary.pdf](reports/IWRC_Financial_Summary.pdf)**
   - Investment breakdown
   - ROI analysis tables
   - Cost per project and per student
   - Funding by institution

---

## Support Documents

### Generation and Process

- **[DOCUMENTATION_GENERATION_SUMMARY.md](DOCUMENTATION_GENERATION_SUMMARY.md)**
  - Complete summary of documentation generation
  - File verification checklist
  - Regeneration instructions

- **[CORRECTION_SUMMARY.md](CORRECTION_SUMMARY.md)**
  - Original correction summary from Nov 22
  - Shows before/after comparison
  - Lists all corrected files

### Scripts

- **[scripts/generate_comprehensive_documentation.py](scripts/generate_comprehensive_documentation.py)**
  - Python script to regenerate all documentation
  - Reads from consolidated data file
  - Generates 7 markdown files + 4 PDFs

- **[scripts/regenerate_analysis.py](scripts/regenerate_analysis.py)**
  - Core analysis script with corrected counts
  - Generates visualizations
  - Exports to Excel

---

## Corrected Metrics Summary

### 10-Year Period (2015-2024)
| Metric | Value |
|--------|-------|
| Unique Projects | **77** |
| IWRC Investment | $8,516,278 |
| Follow-on Funding | $275,195 |
| ROI | 0.03x |
| Students Trained | 304 |
| Institutions | 16 |

### 5-Year Period (2020-2024)
| Metric | Value |
|--------|-------|
| Unique Projects | **47** |
| IWRC Investment | $7,319,144 |
| Follow-on Funding | $261,000 |
| ROI | 0.04x |
| Students Trained | 186 |
| Institutions | 11 |

---

## Usage Guide

### For Quick Reference
→ Use **IWRC_Fact_Sheet.pdf**

### For Executive Presentations
→ Use **IWRC_Seed_Fund_Executive_Summary.pdf**

### For Detailed Analysis
→ Use **IWRC_Detailed_Analysis_Report.pdf** + **ANALYSIS_SUMMARY.md**

### For Methodology Questions
→ Use **METHODOLOGY.md** + **CORRECTION_NOTES.md**

### For Grant Applications
→ Combine **IWRC_Detailed_Analysis_Report.pdf** + **INSTITUTIONAL_REACH.md** + **STUDENT_ANALYSIS.md**

### For Budget Planning
→ Use **IWRC_Financial_Summary.pdf** + **FINDINGS.md**

---

## File Sizes

**Markdown Files (7 total):** 52.9 KB
**PDF Files (4 total):** 13.6 KB
**Total Documentation:** 66.5 KB

---

## Regeneration

To regenerate all documentation:

```bash
cd "/Users/shivpat/Downloads/Seed Fund Tracking"
source .venv/bin/activate
python3 scripts/generate_comprehensive_documentation.py
```

---

**Documentation Status:** COMPLETE
**All files use corrected project counts (77, 47)**
**Last verified:** November 23, 2025
