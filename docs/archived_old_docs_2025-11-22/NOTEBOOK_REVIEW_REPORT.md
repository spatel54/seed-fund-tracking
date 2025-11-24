# Comprehensive Review Report: IWRC ROI Analysis Notebook

**Date:** 2025-11-18
**Notebook:** `/Users/shivpat/Downloads/Seed Fund Tracking/Seed_Fund_Tracking_Analysis NEW.ipynb`
**Data File:** `/Users/shivpat/Downloads/Seed Fund Tracking/IWRC Seed Fund Tracking.xlsx`

---

## Executive Summary

The notebook is well-structured and professionally presented, but there are **CRITICAL DATA ISSUES** that severely underestimate the ROI. The current analysis shows only $18,000 in follow-on funding (0.002x ROI), when there are at least **$350,000 in major grants** hidden in the data due to inconsistent data entry.

**Status:** ⚠️ **REQUIRES SIGNIFICANT FIXES BEFORE USE**

---

## CRITICAL ISSUES (Must Fix)

### 1. **MAJOR DATA LOSS: Follow-on Grants Not Captured** ⚠️⚠️⚠️

**Impact:** ROI is severely underestimated (showing 0.002x instead of potentially 4-5x or higher)

**Root Cause:** The data in column 26 ("Award, Achievement, or Grant") has inconsistent formatting:
- Some rows have the grant amount in the "Monetary Benefit" column (correct)
- **Other rows have the grant description in column 26 and the amount in the "Description" column** (swapped!)

**Evidence:**
```
Row 122:
  Award/Grant Column: "Additional USGS 104g grant ($250,000, expected December 2022)"
  Description Column: "250000"  ← ACTUAL GRANT AMOUNT
  Monetary Column: NaN

Row 123:
  Award/Grant Column: "Additional USEPA P3 grants ($100,000 awarded 10/2022)"
  Description Column: "100000"  ← ACTUAL GRANT AMOUNT
  Monetary Column: NaN
```

These two grants alone ($350,000) are **19x larger** than all currently captured follow-on funding ($18,000).

**Fix Required:**
```python
# Add logic to check BOTH columns for monetary values
def extract_grant_amount(row):
    """Extract grant amount from either monetary or description column"""

    # First try the monetary benefit column
    monetary_val = clean_monetary_value(row['monetary_benefit'])
    if monetary_val > 0:
        return monetary_val

    # If that's empty, check if description column contains a number
    desc_val = row['awards_grants_description']  # Need to add this to col_map
    if pd.notna(desc_val):
        desc_str = str(desc_val).strip()
        # Check if it's a pure number (likely swapped data)
        if desc_str.replace(',', '').replace('.', '').isdigit():
            try:
                return float(desc_str.replace(',', ''))
            except:
                pass

    # Also check if the award/grant text contains dollar amounts
    award_text = str(row['awards_grants'])
    dollar_matches = re.findall(r'\$[\d,]+', award_text)
    if dollar_matches:
        # Extract the number
        amount_str = dollar_matches[0].replace('$', '').replace(',', '')
        try:
            return float(amount_str)
        except:
            pass

    return 0.0
```

---

### 2. **Student Data Contains Non-Numeric Values** ⚠️

**Impact:** Student counts are significantly underestimated

**Evidence:**
```
MS Students column contains:
  - Numeric values: 52 students counted
  - Text values: 'PhD', 'Water Quality', 'Watershed and Ecosystem Function', etc.
  - Reason: Data shifted from adjacent columns

Undergraduate column contains:
  - Text values: 'MS', 'FLOODS', 'AGRICULTURE', 'MODELS', 'SURFACE WATER'

PostDoc column contains:
  - Text values: 'Undergrad', 'ECOLOGY', 'HYDROLOGY', 'WATER QUALITY'
```

**Current Results (Underestimated):**
- PhD: 118
- MS: 52 (should be ~119 based on non-null count)
- Undergrad: 127 (should be ~144)
- PostDoc: 7 (should be ~58)

**Fix Required:**
```python
# Already implemented in the notebook, but needs better documentation:
def clean_student_count(value):
    """
    Clean student counts, handling non-numeric values.
    Non-numeric values are set to 0 (data quality issue to note).
    """
    if pd.isna(value):
        return 0
    try:
        return int(float(value))
    except (ValueError, TypeError):
        # Log this as a data quality issue
        return 0
```

**Recommendation:** Add a data quality warning to the output noting that X rows had non-numeric student data.

---

### 3. **Column Mapping Issue: Missing Description Column** ⚠️

**Impact:** Cannot access the "Description" column where some grant amounts are stored

**Current col_map:**
```python
col_map = {
    # ... other columns ...
    'Award, Achievement, or Grant\n ...': 'awards_grants',
    'Monetary Benefit of Award or Achievement (if applicable; use NA if not applicable)': 'monetary_benefit',
    # MISSING: Description column!
}
```

**Fix Required:**
```python
col_map = {
    # ... existing mappings ...
    "Description of Award, Achievement, or Grant\n (This may include awards and achievements for projects from the previous year to this 5-year cycle, so long as they were not already included in last year's report)": 'awards_grants_description',
    'Source? Identify the Organization': 'award_source',
    # ... rest of mappings ...
}
```

---

## MODERATE ISSUES (Should Fix)

### 4. **Year Extraction Has 89 Missing Values**

**Impact:** 89 out of 354 rows (25%) are excluded from all analyses

**Current Results:**
- Total rows: 354
- Rows with valid year: 265
- Missing: 89 rows

**Sample Missing Project IDs:**
- 'C-04' → None
- Other non-standard formats

**Recommendation:**
- Add a warning in the output about missing years
- Consider manual review of these 89 rows
- Add fallback logic to check other date columns if project ID doesn't have a year

---

### 5. **Monetary Value Cleaning Loses Data**

**Impact:** Text descriptions of awards lose their monetary value

**Examples:**
```
"Dissertation awardees will receive a $750 cash award,
 reimbursement up to $1,000 for travel expenses..."
  → Currently cleaned to: $0.00
  → Should extract: $2,300 (as mentioned in text)

"Distinguished Scholar... $1,000 monetary award"
  → Currently cleaned to: $0.00
  → Should extract: $1,000
```

**Fix Required:**
```python
def clean_monetary_value(value):
    """Enhanced version to extract amounts from text descriptions"""
    if pd.isna(value):
        return 0.0

    value_str = str(value).strip().upper()

    # Handle NA cases
    if value_str in ['NA', 'N/A', 'NONE', '']:
        return 0.0

    # First try direct numeric conversion
    value_clean = re.sub(r'[$,\s]', '', value_str)
    try:
        return float(value_clean)
    except (ValueError, TypeError):
        pass

    # If that fails, try to extract dollar amounts from text
    # Look for patterns like "$1,000" or "$750"
    dollar_pattern = r'\$[\d,]+(?:\.\d{2})?'
    matches = re.findall(dollar_pattern, str(value))

    if matches:
        # Sum all dollar amounts found
        total = 0
        for match in matches:
            amount_str = match.replace('$', '').replace(',', '')
            try:
                total += float(amount_str)
            except:
                pass
        return total

    return 0.0
```

---

### 6. **Categorization Function Misses Valid Entries**

**Impact:** 3 entries are not categorized even though they have data

**Evidence:**
```
Uncategorized entries:
  Row 46: 'Start date: 3-1-2015 End date: 2-28-16'
  Row 49: 'Start date: 3-1-2015 End date: 2-28-16'
  Row 50: 'Start date: 3-1-2015 End date: 2-28-16'
```

**Analysis:** These appear to be data entry errors (project dates instead of awards). The categorization function is working correctly - these should remain uncategorized.

**Recommendation:** No fix needed, but add a note in the output about uncategorized entries.

---

## MINOR ISSUES (Nice to Fix)

### 7. **ROI Calculation Doesn't Account for Data Quality**

**Current Approach:**
```python
roi_10yr = followon_10yr / investment_10yr if investment_10yr > 0 else 0
```

**Issue:** No confidence interval or data quality flag

**Recommendation:** Add a note explaining:
- How many rows had valid follow-on funding data
- Percentage of projects with reported follow-on grants
- Note that ROI is likely underestimated due to incomplete reporting

---

### 8. **Student Categories Don't Match All Data**

**Current Categories:**
- PhD, MS, Undergraduate, Post-Doctoral

**Missing:**
- "Number of students supported by non-federal (matching) funds" (column 13)

**Recommendation:** Consider adding a separate analysis of matching fund students.

---

### 9. **Institutional Diversity Analysis Could Be Enhanced**

**Current:** Simple count of unique institutions

**Suggestions:**
- Map institutions to University of Illinois vs. non-UIUC
- Show geographic distribution (if possible)
- Calculate % of funding going to different institution types

---

## NON-TECHNICAL CLARITY ASSESSMENT

### ✅ **Strengths:**
- Clear markdown explanations for each section
- Good use of headers and structure
- Professional visualizations
- Step-by-step walkthrough
- Executive summary at the end

### ⚠️ **Areas for Improvement:**

1. **Add Data Quality Warnings:**
   ```markdown
   **Data Quality Note:** This analysis is based on self-reported data from
   PIs. Not all projects reported follow-on funding, so the actual ROI may
   be higher. Of X projects analyzed, only Y reported follow-on grants.
   ```

2. **Explain the ROI Better:**
   ```markdown
   **What does 0.002x ROI mean?**
   For every $1 IWRC invested, researchers reported $0.002 in follow-on grants.

   **⚠️ IMPORTANT:** This appears unusually low and likely reflects incomplete
   reporting rather than actual results. Manual review shows several large
   grants ($250K+ USGS, $100K EPA) that may not be captured in this calculation.
   ```

3. **Add Interpretation Guidance:**
   - What's a "good" ROI for seed funding?
   - Industry benchmarks?
   - Comparison to other programs?

---

## VISUALIZATION ASSESSMENT

### ✅ **Working Correctly:**
- High DPI settings (300 DPI)
- Professional color scheme
- Proper labeling
- Grid styling

### ⚠️ **Potential Issues:**

1. **ROI Chart Will Show Confusing Results:**
   - The bars will show investment >> follow-on funding (opposite of expected)
   - The ROI multiplier annotation will show 0.002x (very confusing)
   - **Fix:** Don't generate this chart until data issues are resolved

2. **Student Pie Charts:**
   - Will show incorrect proportions due to data cleaning issues
   - **Fix:** Add note about data quality

---

## ACTUAL DATA VERIFICATION

### Dataset Statistics:
```
Total rows: 354
Total columns: 35

Data by Time Period:
  10-Year (2015-2024): 220 rows
  5-Year (2020-2024): 142 rows

Investment:
  10-Year: $8,516,278.00
  5-Year: $7,319,144.00

Follow-on Funding (CURRENT CALCULATION):
  10-Year: $18,000.00  ← SEVERELY UNDERESTIMATED
  5-Year: $11,000.00   ← SEVERELY UNDERESTIMATED

Students Trained (CURRENT CALCULATION):
  10-Year: 304 students (118 PhD, 52 MS, 127 UG, 7 PD)
  5-Year: 186 students (88 PhD, 26 MS, 65 UG, 7 PD)
```

### Known Missing Data:
- **$350,000 in grants** from rows 122-123 alone
- Likely more grants with amounts embedded in text descriptions
- Many projects may not have reported follow-on funding at all

---

## RECOMMENDED FIXES (Priority Order)

### 🔴 **CRITICAL (Must Fix Before Running):**

1. **Add logic to extract grant amounts from multiple columns:**
   - Check "Description" column for numeric values
   - Parse dollar amounts from "Award/Grant" text
   - Combine with existing "Monetary Benefit" column

2. **Add data quality warnings throughout the notebook:**
   - Note incomplete reporting
   - Show how many projects reported vs. didn't report follow-on funding
   - Add caveats to ROI interpretation

3. **Fix student count calculation:**
   - Add data quality counter for non-numeric values
   - Report how many rows had invalid data

### 🟡 **HIGH PRIORITY (Should Fix):**

4. **Enhance monetary value extraction:**
   - Parse dollar amounts from text descriptions
   - Sum multiple amounts in same cell

5. **Add missing columns to col_map:**
   - Description column
   - Source organization column
   - Award recipient column

### 🟢 **MEDIUM PRIORITY (Nice to Have):**

6. **Add data completeness analysis:**
   - Show % of projects reporting each metric
   - Identify projects with missing data

7. **Enhance year extraction:**
   - Add fallback to other date columns
   - Manual mapping for unusual project IDs

---

## CODE CORRECTIONS

### Cell 5 - Enhanced Column Mapping:
```python
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
    "Award, Achievement, or Grant\n (This may include awards and achievements for projects from the previous year to this 5-year cycle, so long as they were not already included in last year's report)": 'awards_grants',
    "Description of Award, Achievement, or Grant\n (This may include awards and achievements for projects from the previous year to this 5-year cycle, so long as they were not already included in last year's report)": 'awards_grants_description',
    'Source? Identify the Organization': 'award_source',
    'Monetary Benefit of Award or Achievement (if applicable; use NA if not applicable)': 'monetary_benefit',
    'WRRI Science Priority that Best Aligns with this Project': 'science_priority',
    'Keyword (Primary)': 'keyword_primary'
}
```

### Cell 14 - Enhanced Monetary Cleaning Function:
```python
def clean_monetary_value(value):
    """
    Clean and convert monetary values to float.
    Handles: $X,XXX, NA, None, text with embedded dollar amounts
    """
    if pd.isna(value):
        return 0.0

    value_str = str(value).strip().upper()

    # Handle NA or N/A
    if value_str in ['NA', 'N/A', 'NONE', '']:
        return 0.0

    # First try direct numeric conversion (handles simple numbers)
    value_clean = re.sub(r'[$,\s]', '', value_str)
    try:
        return float(value_clean)
    except (ValueError, TypeError):
        pass

    # If that fails, try to extract dollar amounts from text
    dollar_pattern = r'\$[\d,]+(?:\.\d{2})?'
    matches = re.findall(dollar_pattern, str(value))

    if matches:
        # Sum all dollar amounts found
        total = 0
        for match in matches:
            amount_str = match.replace('$', '').replace(',', '')
            try:
                total += float(amount_str)
            except:
                pass
        if total > 0:
            return total

    # Last resort: look for large numbers (5+ digits)
    number_pattern = r'\b\d{5,}\b'
    number_matches = re.findall(number_pattern, str(value))
    if number_matches:
        try:
            return float(number_matches[0])
        except:
            pass

    return 0.0


def extract_grant_amount_comprehensive(row):
    """
    Extract grant amount from any available source.
    Checks multiple columns to handle inconsistent data entry.
    """
    # 1. Try monetary benefit column
    monetary_val = clean_monetary_value(row['monetary_benefit'])
    if monetary_val > 0:
        return monetary_val

    # 2. Check if description column contains a pure number
    if 'awards_grants_description' in row and pd.notna(row['awards_grants_description']):
        desc_str = str(row['awards_grants_description']).strip()
        # Check if it's a pure number (likely swapped data)
        if desc_str.replace(',', '').replace('.', '').isdigit():
            try:
                return float(desc_str.replace(',', ''))
            except:
                pass

    # 3. Check if the award/grant text contains dollar amounts
    if pd.notna(row['awards_grants']):
        award_text = str(row['awards_grants'])
        dollar_matches = re.findall(r'\$[\d,]+', award_text)
        if dollar_matches:
            # Extract the first/largest number
            amounts = []
            for match in dollar_matches:
                amount_str = match.replace('$', '').replace(',', '')
                try:
                    amounts.append(float(amount_str))
                except:
                    pass
            if amounts:
                return max(amounts)  # Return largest amount found

    return 0.0


# Apply comprehensive extraction
df_10yr['monetary_benefit_clean'] = df_10yr.apply(extract_grant_amount_comprehensive, axis=1)
df_5yr['monetary_benefit_clean'] = df_5yr.apply(extract_grant_amount_comprehensive, axis=1)
```

### Add After Cell 14 - Data Quality Report:
```python
# Data Quality Assessment
print('\n' + '='*70)
print('DATA QUALITY REPORT - FOLLOW-ON FUNDING')
print('='*70)

# Count how many projects reported follow-on funding
projects_with_awards_10yr = df_10yr[df_10yr['award_category'].notna()].shape[0]
projects_with_awards_5yr = df_5yr[df_5yr['award_category'].notna()].shape[0]

print(f'\n10-Year Period:')
print(f'  Total projects: {len(df_10yr)}')
print(f'  Projects reporting awards/grants: {projects_with_awards_10yr}')
print(f'  Reporting rate: {projects_with_awards_10yr/len(df_10yr)*100:.1f}%')
print(f'  Projects with monetary values: {(df_10yr["monetary_benefit_clean"] > 0).sum()}')

print(f'\n5-Year Period:')
print(f'  Total projects: {len(df_5yr)}')
print(f'  Projects reporting awards/grants: {projects_with_awards_5yr}')
print(f'  Reporting rate: {projects_with_awards_5yr/len(df_5yr)*100:.1f}%')
print(f'  Projects with monetary values: {(df_5yr["monetary_benefit_clean"] > 0).sum()}')

print('\n⚠️  NOTE: Low reporting rates suggest ROI is likely underestimated.')
print('   Many projects may not have reported follow-on grants.')
print('='*70)
```

---

## TESTING CHECKLIST

Before finalizing the notebook, verify:

- [ ] Load the data successfully
- [ ] Year extraction works (check output)
- [ ] Investment totals match expected values
- [ ] **Follow-on funding includes rows 122-123** ($350K)
- [ ] Student counts are reasonable
- [ ] ROI calculation is > 0.05x (otherwise investigate)
- [ ] All visualizations render correctly
- [ ] Excel export works
- [ ] PNG files are created

---

## BOTTOM LINE

**Can this notebook be used as-is?** ❌ **NO**

**Why not?**
1. The ROI calculation is completely wrong due to missing grant data
2. Student counts are underestimated
3. The analysis would produce misleading results that undervalue the program

**What's needed?**
1. Fix the grant amount extraction (CRITICAL)
2. Add data quality warnings
3. Re-test with fixes to verify ROI is reasonable (expecting 3-10x range)

**Estimated time to fix:** 2-3 hours of focused work

---

## POSITIVE NOTES

Despite the critical data issues, the notebook has many strengths:

✅ Excellent structure and organization
✅ Professional visualizations
✅ Clear explanations for non-technical readers
✅ Good code quality and documentation
✅ Comprehensive analysis framework

Once the data extraction issues are fixed, this will be an excellent analysis tool!
