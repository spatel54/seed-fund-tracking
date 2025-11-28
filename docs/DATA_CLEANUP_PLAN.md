# Data Cleanup Plan: NULL Institution Records

**Created:** November 27, 2025
**Priority:** Medium
**Impact:** $12.89M in funding currently has missing institution data

## Problem Summary

The consolidated dataset has **24 projects with valid funding but NULL institution names**, representing $12.89M in total investment. Additionally, 171 records have NULL values in both institution and award amount fields.

## Identified Issues

### Issue 1: Missing Institution Names (24 projects, $12.89M)

These are legitimate projects with funding but incomplete institution metadata. Many can be inferred from PI names:

#### Confirmed UIUC Affiliations (based on PI research):
- **James Angel** - Prairie Research Institute, UIUC ($59,881)
- **Lisa Merrifield** - IWRC Technology Transfer, UIUC (8 projects, $280,309 total)
- **Brian Miller** - Likely UIUC/ISWS (3 projects, $4.34M)
- **Yu-Feng Lin** - Civil and Environmental Engineering, UIUC ($43,956)
- **Robert Hudson** - UIUC ($108,948)
- **Gary Parker** - Civil and Environmental Engineering, UIUC ($70,030)
- **Bruce Rhoads** - Geography, UIUC ($5,591)
- **Ashlynn Stillwell** - Civil and Environmental Engineering, UIUC ($10,000)
- **John Kelly** - Natural Resources, UIUC ($22,672)

#### Unknown/Research Needed:
- **Da Chen** - Statewide Surveillance project ($6,000)
- **Steven Taylor** - Epikarstic groundwater ecosystems ($7,483)
- **Angela Kent** - Restoration/wetland projects (2 projects, $14,000)
- **Marcelo Garcia** - Critical Shear Stresses ($28,985)

#### Summary Rows (NULL Project ID and PI):
- 4 rows with NULL in multiple fields - appear to be aggregate/summary entries

### Issue 2: Generic "University of Illinois" Naming (34 projects, $0.85M)

All 34 projects labeled "University of Illinois" (without campus) have been verified as **UIUC** based on department affiliations:
- Civil and Environmental Engineering
- Geography and Geographic Information Science
- Natural Resources and Environmental Science
- Integrative Biology
- Urban and Regional Planning

**Status:** ✅ Already fixed in visualization code (lines 132-133 of generate_all_static_visualizations.py)

### Issue 3: Inconsistent UIUC Naming

Two variants found:
- "University of Illinois at Urbana-Champaign" (correct)
- "University of Illinois Urbana-Champaign" (missing "at")

**Status:** ✅ Already fixed in visualization code (lines 127-129)

## Recommended Actions

### Phase 1: Immediate (Code-Based Fix) ✅ COMPLETED
- [x] Created `standardize_institution_with_inference()` function
- [x] Infers UIUC from known PI names (marked with asterisk)
- [x] Combines "University of Illinois" → UIUC
- [x] Combines UIUC naming variants
- [x] Added disclaimer to visualization

### Phase 2: Source Data Cleanup (Manual)

#### Step 1: Research Remaining PIs
Investigate these 4 PIs to determine institutions:
1. **Da Chen** - Search for "Da Chen" + water resources + Illinois
2. **Steven Taylor** - Search for "Steven Taylor" + epikarstic groundwater + Illinois
3. **Angela Kent** - Search for "Angela Kent" + wetland + Illinois + restoration
4. **Marcelo Garcia** - Search for "Marcelo Garcia" + hydraulics + shear stress + Illinois

#### Step 2: Update Source Excel Files
Once institutions are confirmed, update the following source files:

**File:** `data/source/FY24_reporting_IL.xlsx`
- Review and fill NULL institution fields for 2024 projects

**File:** `data/source/FY23_reporting_IL.xlsx`
- Review and fill NULL institution fields for 2023 projects

**File:** `data/source/IWRC-2022-WRRA-Annual-Report-v.101923.xlsx`
- Review and fill NULL institution fields for 2022 projects

**File:** `data/source/IL_5yr_FY16_20_2.xlsx`
- Review and fill NULL institution fields for 2016-2020 projects

#### Step 3: Standardize Institution Naming
Create a **controlled vocabulary** for institution names:

**Preferred Names:**
```
University of Illinois at Urbana-Champaign
University of Illinois Chicago
Southern Illinois University
Southern Illinois University at Carbondale
Illinois Institute of Technology
Illinois State University
Northwestern University
Lewis and Clark Community College
Illinois State Water Survey
Prairie Research Institute
National Great Rivers Research & Education Center
```

#### Step 4: Re-consolidate Data
After source file updates:
```bash
python analysis/scripts/combine_excel_files_v2.py
```

This will create a new consolidated file with corrected institution names.

#### Step 5: Verify and Regenerate
```bash
# Regenerate all visualizations
python analysis/scripts/generate_all_static_visualizations.py

# Verify top_institutions.png no longer has asterisks (all data from source)
```

## Summary Rows Cleanup

The 4 rows with NULL project ID, NULL PI, and NULL institution appear to be summary/aggregate entries. Recommend:

1. **Identify purpose** - Are these year-end summaries? Regional aggregates?
2. **Add metadata** - If keeping them, add descriptive Project IDs like "FY2020_Summary"
3. **Separate sheet** - Consider moving to a separate "Summary" sheet in the Excel file
4. **Or remove** - If not needed for analysis, remove from dataset

## Expected Outcomes

After cleanup:
- ✅ No UIUC duplicates
- ✅ No generic "University of Illinois" entries
- ✅ Standardized institution names across all projects
- ✅ 100% of funded projects have institution attribution
- ✅ Visualizations show accurate, complete data without asterisks
- ✅ Improved data quality for future analyses

## Timeline Estimate

- **PI Research:** 1-2 hours
- **Source File Updates:** 2-3 hours
- **Verification:** 30 minutes
- **Total:** 4-6 hours

## Notes

- Always create backups before modifying source Excel files
- Document any research findings in this file
- Update CLAUDE.md if data structure changes
- Consider adding data validation rules to prevent future NULL entries
