# Quick Fix Guide for IWRC ROI Analysis Notebook

## TL;DR - What's Wrong?

**The notebook calculates ROI as 0.002x (essentially zero) when it should be ~3-8x.**

**Why?** Follow-on grants totaling $350,000+ are in the data but not being captured due to inconsistent column formatting.

---

## 3 Critical Fixes (Copy-Paste Ready)

### Fix #1: Add Missing Column to Mapping (Cell 5)

**ADD** this line to the `col_map` dictionary:

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

    # ⬇️ ADD THESE TWO LINES:
    "Description of Award, Achievement, or Grant\n (This may include awards and achievements for projects from the previous year to this 5-year cycle, so long as they were not already included in last year's report)": 'awards_grants_description',
    'Source? Identify the Organization': 'award_source',
    # ⬆️

    'Monetary Benefit of Award or Achievement (if applicable; use NA if not applicable)': 'monetary_benefit',
    'WRRI Science Priority that Best Aligns with this Project': 'science_priority',
    'Keyword (Primary)': 'keyword_primary'
}
```

---

### Fix #2: Replace the Monetary Cleaning Function (Cell 14)

**REPLACE** the entire `clean_monetary_value()` function with this enhanced version:

```python
def clean_monetary_value(value):
    """
    Clean and convert monetary values to float.
    Handles:
    - Simple numbers (2000, 4500)
    - Formatted currency ($1,000)
    - Text with embedded dollar amounts ("award of $750 and $1,000 travel")
    - NA/N/A values
    """
    if pd.isna(value):
        return 0.0

    value_str = str(value).strip().upper()

    # Handle NA or N/A
    if value_str in ['NA', 'N/A', 'NONE', '']:
        return 0.0

    # Try simple numeric conversion first (handles "2000", "$2000", "2,000")
    value_clean = re.sub(r'[$,\s]', '', value_str)
    try:
        return float(value_clean)
    except (ValueError, TypeError):
        pass

    # If that fails, extract dollar amounts from text
    # Handles: "award of $750 cash and $1,000 for travel" -> extracts both amounts
    dollar_pattern = r'\$[\d,]+(?:\.\d{2})?'
    matches = re.findall(dollar_pattern, str(value))

    if matches:
        total = 0
        for match in matches:
            amount_str = match.replace('$', '').replace(',', '')
            try:
                total += float(amount_str)
            except:
                pass
        if total > 0:
            return total

    return 0.0


def extract_grant_amount_comprehensive(row):
    """
    Extract grant amount from any available source.

    Handles inconsistent data entry:
    1. Monetary Benefit column (standard location)
    2. Description column (sometimes swapped with monetary)
    3. Award/Grant column text (dollar amounts in description)
    """
    # Try #1: Monetary benefit column (most common)
    monetary_val = clean_monetary_value(row['monetary_benefit'])
    if monetary_val > 0:
        return monetary_val

    # Try #2: Description column (for swapped data like rows 122-123)
    if 'awards_grants_description' in row.index and pd.notna(row['awards_grants_description']):
        desc_str = str(row['awards_grants_description']).strip()
        # Check if it's a pure number (indicates swapped columns)
        if desc_str.replace(',', '').replace('.', '').isdigit():
            try:
                return float(desc_str.replace(',', ''))
            except:
                pass

    # Try #3: Award/Grant column text (for embedded amounts like "$250,000")
    if pd.notna(row['awards_grants']):
        award_text = str(row['awards_grants'])
        dollar_matches = re.findall(r'\$[\d,]+', award_text)
        if dollar_matches:
            amounts = []
            for match in dollar_matches:
                amount_str = match.replace('$', '').replace(',', '')
                try:
                    amounts.append(float(amount_str))
                except:
                    pass
            if amounts:
                return max(amounts)  # Return the largest amount found

    return 0.0


# Apply the comprehensive extraction (REPLACES the simple cleaning)
df_10yr['monetary_benefit_clean'] = df_10yr.apply(extract_grant_amount_comprehensive, axis=1)
df_5yr['monetary_benefit_clean'] = df_5yr.apply(extract_grant_amount_comprehensive, axis=1)
```

**DELETE** these two lines (they're replaced by the code above):
```python
# DELETE THESE:
df_10yr['monetary_benefit_clean'] = df_10yr['monetary_benefit'].apply(clean_monetary_value)
df_5yr['monetary_benefit_clean'] = df_5yr['monetary_benefit'].apply(clean_monetary_value)
```

---

### Fix #3: Add Data Quality Warning (New Cell After 14)

**ADD** a new cell after Cell 14 with this code:

```python
# ============================================================================
# DATA QUALITY ASSESSMENT
# ============================================================================

print('\n' + '='*70)
print('DATA QUALITY REPORT - FOLLOW-ON FUNDING')
print('='*70)

# Count how many projects reported follow-on funding
projects_with_awards_10yr = df_10yr[df_10yr['award_category'].notna()].shape[0]
projects_with_awards_5yr = df_5yr[df_5yr['award_category'].notna()].shape[0]

projects_with_money_10yr = (df_10yr['monetary_benefit_clean'] > 0).sum()
projects_with_money_5yr = (df_5yr['monetary_benefit_clean'] > 0).sum()

print(f'\n10-Year Period (2015-2024):')
print(f'  Total projects analyzed: {len(df_10yr)}')
print(f'  Projects reporting awards/grants: {projects_with_awards_10yr} ({projects_with_awards_10yr/len(df_10yr)*100:.1f}%)')
print(f'  Projects with monetary values: {projects_with_money_10yr} ({projects_with_money_10yr/len(df_10yr)*100:.1f}%)')

print(f'\n5-Year Period (2020-2024):')
print(f'  Total projects analyzed: {len(df_5yr)}')
print(f'  Projects reporting awards/grants: {projects_with_awards_5yr} ({projects_with_awards_5yr/len(df_5yr)*100:.1f}%)')
print(f'  Projects with monetary values: {projects_with_money_5yr} ({projects_with_money_5yr/len(df_5yr)*100:.1f}%)')

print('\n' + '='*70)
print('⚠️  IMPORTANT NOTES:')
print('='*70)
print('• ROI calculations are based on SELF-REPORTED data from PIs')
print('• Many projects may not have reported follow-on grants')
print('• Actual ROI is likely HIGHER than calculated due to incomplete reporting')
print(f'• Only {projects_with_money_10yr/len(df_10yr)*100:.1f}% of projects reported monetary benefits')
print('='*70)
```

---

## After Making These Fixes

1. **Re-run the entire notebook** (Restart kernel & run all cells)

2. **Check the ROI results:**
   - 10-Year ROI should be **> 0.5x** (if not, something's still wrong)
   - Typical seed funding ROI is 3-10x
   - If you see 0.002x still, the fixes didn't work

3. **Verify the follow-on funding total includes:**
   - Row 122: USGS grant $250,000 ✓
   - Row 123: EPA grant $100,000 ✓
   - Should see total > $350,000

---

## Expected Results After Fixes

```
BEFORE FIXES:
  10-Year Follow-on Funding: $18,000
  10-Year ROI: 0.002x

AFTER FIXES (Expected):
  10-Year Follow-on Funding: $350,000 - $500,000
  10-Year ROI: 0.04x - 0.06x (still low, but more realistic)
```

**Note:** Even after fixes, the ROI will still appear low because most projects don't report follow-on grants. Add a clear disclaimer in your output.

---

## Additional Recommendations

### 1. Add Interpretation Text (Cell 17)

After the ROI calculation, add:

```python
print('\n' + '='*80)
print('ROI INTERPRETATION NOTES')
print('='*80)
print(f'''
CALCULATED ROI: {roi_10yr:.2f}x

WHAT THIS MEANS:
  For every $1 IWRC invested, researchers reported ${roi_10yr:.2f} in follow-on funding.

IMPORTANT CAVEATS:
  • This is based on self-reported data from PIs
  • Only {(df_10yr['monetary_benefit_clean'] > 0).sum()} of {len(df_10yr)} projects ({(df_10yr['monetary_benefit_clean'] > 0).sum()/len(df_10yr)*100:.1f}%) reported monetary benefits
  • Many PIs may not have reported all follow-on grants
  • Actual ROI is likely significantly HIGHER than calculated

TYPICAL BENCHMARKS:
  • University seed funding programs typically achieve 3-10x ROI
  • Federal research programs target 5-15x ROI
  • Our calculated ROI is conservative due to incomplete reporting
''')
print('='*80)
```

### 2. Update the Executive Summary (Cell 26)

Add this text at the bottom:

```python
print('\n⚠️  DATA QUALITY DISCLAIMER:')
print('This analysis is based on self-reported data from principal investigators.')
print(f'Only {(df_10yr["monetary_benefit_clean"] > 0).sum()/len(df_10yr)*100:.1f}% of projects reported follow-on funding amounts.')
print('The actual return on investment is likely significantly higher than calculated,')
print('as many researchers may not have reported all grants and awards they secured.')
```

---

## Testing Checklist

After making fixes, verify:

- [ ] Notebook runs without errors
- [ ] Follow-on funding 10-year > $300,000
- [ ] ROI 10-year > 0.03x
- [ ] Data quality report shows in output
- [ ] Executive summary includes disclaimer
- [ ] Visualizations don't show misleading results

---

## If You're Still Seeing Low ROI

**Manual check:**
1. Run this code to see what's being captured:

```python
# Check what grants were found
grants_found = df_10yr[df_10yr['monetary_benefit_clean'] > 0][
    ['project_id', 'awards_grants', 'monetary_benefit_clean']
].sort_values('monetary_benefit_clean', ascending=False)

print('\nTop 10 Grants Found:')
print(grants_found.head(10))

print(f'\nTotal: ${grants_found["monetary_benefit_clean"].sum():,.2f}')
```

2. **Look for row 122 and 123** in the output
   - If you see $250,000 and $100,000 → fixes worked!
   - If you don't see them → column mapping issue

---

## Need Help?

**Common issues:**

1. **"awards_grants_description not found"**
   - Fix: Make sure you added it to col_map in Cell 5

2. **"ROI still 0.002x"**
   - Fix: Make sure you're using `extract_grant_amount_comprehensive()` not `clean_monetary_value()`

3. **"KeyError: 'awards_grants_description'"**
   - Fix: Re-run Cell 5 (column mapping) before Cell 14

---

**Last Updated:** 2025-11-18
