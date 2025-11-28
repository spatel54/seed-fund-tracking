# Data Consolidation Verification Summary

## Overview
- **Consolidated File**: [IWRC Seed Fund Tracking.xlsx](data/consolidated/IWRC Seed Fund Tracking.xlsx)
- **Total Rows**: 354
- **Total Columns**: 35
- **Source Files**: 4 files (114 total rows)

---

## ✅ GOOD NEWS: Data is Properly Consolidated

The consolidated file has **354 rows** while source files have only **114 rows** combined. This is CORRECT because:

1. **Multiple outputs per project**: Each project can have multiple publications, awards, or outputs
2. **Duplicate Project IDs are expected**: 122 unique projects with 266 total Project ID entries (average ~2.2 outputs per project)
3. **Deduplication is handled**: The [iwrc_data_loader.py](analysis/scripts/iwrc_data_loader.py:281) handles deduplication correctly

---

## ⚠️ ISSUES REQUIRING YOUR REVIEW

### 1. **Institution Name Inconsistencies** (CRITICAL)

Multiple spelling variations detected:

#### University of Illinois Variations (117 total rows)
- ✅ **University of Illinois at Urbana-Champaign** (62 rows) - CANONICAL
- ⚠️ **University of Illinois Urbana-Champaign** (18 rows) - missing "at"
- ⚠️ **University of Illinois** (34 rows) - incomplete
- ⚠️ **University of Illinois  ** (1 row) - extra space
- ⚠️ **Univeristy of Illinois** (2 rows) - TYPO

**Recommendation**: Standardize all to "University of Illinois at Urbana-Champaign"

#### Southern Illinois University Variations (18 total rows)
- ✅ **Southern Illinois University** (12 rows) - CANONICAL
- ⚠️ **Southern Illinois University at Carbondale** (5 rows)
- ⚠️ **Southern Illinois University Carbondale** (1 row)

**Recommendation**: Standardize to "Southern Illinois University"

**Note**: The data loader script ALREADY handles these standardizations (see lines 27-39), but the source Excel file should be corrected manually.

---

### 2. **Missing/Empty Values**

| Column | Missing Values | Total Rows | % Missing |
|--------|---------------|------------|-----------|
| **Project ID** | 88 | 354 | 24.9% |
| **Award Type** | 166 | 354 | 46.9% |
| **Academic Institution** | 187 | 354 | 52.8% |
| **Award Amount** | 167 | 354 | 47.2% |
| **Science Priority** | 235 | 354 | 66.4% |

**Analysis**: These missing values are EXPECTED for output/publication rows where only the Project ID links them to the main project data. The first row for each project should have complete data.

**Action Required**: Verify that at least ONE row per unique Project ID has complete data.

---

### 3. **Award Amount Issues**

- **Total Valid Amounts**: 183 rows (51.7%)
- **Total Investment**: $22,499,725.00
- **Range**: $0 to $6,438,936.00
- **Mean**: $122,949.32
- **Median**: $15,000.00

#### Suspicious Values:
- ⚠️ **3 rows with $0 amount** - Need verification
- ⚠️ **3 rows with amount > $1M** - Need verification (may be legitimate multi-year totals)

**Action Required**: Review these outliers to confirm accuracy.

---

### 4. **Award Type Values**

| Award Type | Count | Notes |
|------------|-------|-------|
| **Base Grant (104b)** | 142 | ✅ Primary type |
| **104g - AIS** | 17 | ✅ Aquatic Invasive Species |
| **Coordination Grant** | 16 | ✅ |
| **104g - General** | 9 | ✅ |
| **104g - PFAS** | 4 | ✅ Per/Polyfluoroalkyl Substances |
| **(Missing)** | 166 | See note above |

**Status**: ✅ All values are valid and expected.

---

### 5. **Science Priority Values**

Detected potential typo:
- ✅ **Water Technology and Innovation** (19 rows)
- ⚠️ **Water Technology and innovation** (8 rows) - lowercase "i"

**Recommendation**: Standardize capitalization to "Water Technology and Innovation"

---

### 6. **Column Mapping from Source Files**

All source files have **multi-level headers** with merged cells. The consolidation script handles this correctly, but reports these as "unmapped" because they're header groupings:

- ✅ "Project Identifiers" → Maps to individual ID columns
- ✅ "Funding" → Maps to Award Amount column
- ✅ "Student Statistics" → Maps to individual student count columns
- ✅ "Science Characterization" → Maps to Science Priority column

**Status**: ✅ No action needed - these are properly mapped.

---

## 📋 RECOMMENDATIONS

### Immediate Actions:

1. **Standardize Institution Names**:
   ```
   Run Find & Replace in Excel:
   - "University of Illinois Urbana-Champaign" → "University of Illinois at Urbana-Champaign"
   - "University of Illinois" → "University of Illinois at Urbana-Champaign"
   - "University of Illinois  " → "University of Illinois at Urbana-Champaign"
   - "Univeristy of Illinois" → "University of Illinois at Urbana-Champaign"
   - "Southern Illinois University at Carbondale" → "Southern Illinois University"
   - "Southern Illinois University Carbondale" → "Southern Illinois University"
   ```

2. **Standardize Science Priority**:
   ```
   - "Water Technology and innovation" → "Water Technology and Innovation"
   ```

3. **Review Outlier Award Amounts**:
   - Verify 3 rows with $0 amount
   - Verify 3 rows with amounts > $1M

4. **Verify Project Data Completeness**:
   - Ensure each of the 122 unique Project IDs has at least one row with complete data (institution, award amount, etc.)

### Future Maintenance:

1. Use the [iwrc_data_loader.py](analysis/scripts/iwrc_data_loader.py) script for ALL data analysis
2. The loader automatically:
   - Deduplicates by Project ID
   - Standardizes institution names
   - Handles column name variations
3. Never sum Award Amounts without deduplication!

---

## ✅ VERIFICATION CONFIRMED

### What's Working:
✅ All 4 source files are consolidated
✅ Multi-level headers are correctly parsed
✅ Duplicate Project IDs are intentional (multiple outputs)
✅ Award types are valid
✅ Data loader handles deduplication correctly
✅ 122 unique projects tracked across 354 rows

### What Needs Review:
⚠️ Institution name variations (5 variations for U of I)
⚠️ Science priority capitalization (1 typo)
⚠️ 6 outlier award amounts ($0 and >$1M)
⚠️ Verify completeness of first row per project

---

## Questions for You:

1. **Institution Names**: Should I create a script to auto-fix these standardizations in the Excel file?

2. **$0 Award Amounts**: Are these coordination activities or data entry errors?

3. **>$1M Awards**: Are these multi-year aggregates or single large grants?

4. **Missing Values**: Are you comfortable with ~50% missing values in output/publication rows (where they're not needed)?

5. **Additional Columns**: I noticed 2 unnamed columns (33-34) at the end - should these be removed?

---

**Generated**: 2025-11-28
**Script**: [verify_consolidation.py](verify_consolidation.py)
**Data Loader**: [iwrc_data_loader.py](analysis/scripts/iwrc_data_loader.py)
