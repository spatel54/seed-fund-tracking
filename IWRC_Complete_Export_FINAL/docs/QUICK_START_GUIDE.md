# IWRC ROI Analysis - Quick Start Guide

## 🚀 How to Run the Analysis

### Step 1: Open the Notebook

**Option A - Using Jupyter Notebook:**
```bash
cd "/Users/shivpat/Downloads/Seed Fund Tracking"
jupyter notebook
```
Then click on `Seed_Fund_Tracking_Analysis NEW.ipynb`

**Option B - Using VSCode:**
1. Open VSCode
2. Navigate to the folder: `/Users/shivpat/Downloads/Seed Fund Tracking`
3. Open `Seed_Fund_Tracking_Analysis NEW.ipynb`
4. VSCode will automatically detect it's a Jupyter notebook

### Step 2: Run All Cells

**In Jupyter:**
- Click: `Kernel` → `Restart & Run All`

**In VSCode:**
- Click: `Run All` button at the top of the notebook

### Step 3: View Results

The notebook will:
- Display all analysis results inline
- Generate 5 high-quality PNG charts
- Create `IWRC_ROI_Analysis_Summary.xlsx` with all tables

**Expected runtime**: 30-60 seconds

---

## 📊 What You'll Get

### Console Output
- Investment totals for each time period
- Follow-on funding breakdown by type (Grant/Award/Achievement)
- ROI calculations
- Student counts by degree level
- Institutional diversity metrics
- Executive summary dashboard

### Generated Files

1. **IWRC_ROI_Analysis_Summary.xlsx**
   - Ready to share with stakeholders
   - Multiple sheets with different analyses
   - Professionally formatted tables

2. **Visualization PNG Files** (300 DPI, publication-ready):
   - `iwrc_investment_comparison.png`
   - `followon_funding_count.png`
   - `roi_comparison.png`
   - `students_trained.png`
   - `student_distribution_pie.png`

---

## 📈 Key Results at a Glance

### 10-Year Period (2015-2024)
```
💰 Investment:         $8,516,278
💵 Follow-on Funding:  $275,195 (minimum documented)
📊 ROI:                0.032x
👥 Students Trained:   304
   - PhD:              118
   - Master's:         52
   - Undergraduate:    127
   - Post-Doctoral:    7
```

### 5-Year Period (2020-2024)
```
💰 Investment:         $7,319,144
💵 Follow-on Funding:  $261,000 (minimum documented)
📊 ROI:                0.036x
👥 Students Trained:   186
   - PhD:              88
   - Master's:         26
   - Undergraduate:    65
   - Post-Doctoral:    7
```

---

## ⚠️ Important Note: ROI is Underestimated

**The ROI of 0.032x appears low because:**

1. Only 10 out of 220 projects (~5%) have documented follow-on funding amounts
2. Many researchers likely secured grants but didn't report them in the dataset
3. Some entries have text descriptions but no dollar values

**What to communicate:**
- "$275,000 in *documented* follow-on funding"
- "Actual ROI likely much higher with complete reporting"
- **Emphasize the 304 students trained** - this is a concrete, measurable outcome

---

## 🎯 For Your One-Pager

### Best Metrics to Highlight

1. **Students Trained: 304 over 10 years**
   - Most reliable data point
   - Clear impact on workforce development

2. **Sustained Investment: $8.5M over 10 years**
   - Shows long-term commitment

3. **Geographic Reach: Multiple institutions served**
   - Demonstrates statewide impact

4. **Minimum Follow-on Funding: $275K documented**
   - With caveat about underreporting

### Best Visualizations

Use these charts in your one-pager:

1. **students_trained.png** - Clear, impactful, easy to understand
2. **roi_comparison.png** - Shows investment vs. return visually
3. **iwrc_investment_comparison.png** - Simple, clean comparison

---

## 🔧 Troubleshooting

### "Module not found" Error

Install missing packages:
```bash
pip3 install pandas numpy matplotlib seaborn plotly openpyxl
```

### "File not found" Error

Make sure you're in the correct directory:
```bash
cd "/Users/shivpat/Downloads/Seed Fund Tracking"
ls -la "IWRC Seed Fund Tracking.xlsx"
```

### Charts Don't Display

If running in VSCode, make sure you have the Jupyter extension installed.

### Want to Re-run Analysis

Just run all cells again. The notebook will overwrite the previous output files.

---

## 📞 Need Help?

1. Check `ANALYSIS_SUMMARY.md` for detailed findings and data quality notes
2. Review code comments in the notebook for technical details
3. Ensure all files are in the same directory:
   - `Seed_Fund_Tracking_Analysis NEW.ipynb`
   - `IWRC Seed Fund Tracking.xlsx`

---

## ✅ Checklist Before Presenting

- [ ] Run the notebook successfully
- [ ] Review all generated charts
- [ ] Check the Excel summary file
- [ ] Read the data quality notes in `ANALYSIS_SUMMARY.md`
- [ ] Prepare talking points about underreported ROI
- [ ] Emphasize student training numbers (most reliable metric)

---

**Ready to run?** Open the notebook and click "Run All"! 🚀
