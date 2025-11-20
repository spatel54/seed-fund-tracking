# Export Interactive HTML Visualizations to PDF

## Quick Method: Print to PDF from Browser

### For Each HTML File:

1. **Open the HTML file in your browser:**
   - Right-click the file → "Open With" → Choose your browser (Chrome, Safari, Firefox)
   - Or drag the file into an open browser window

2. **Print to PDF:**
   - **Chrome/Edge:** 
     - Press `Cmd + P` (Mac) or `Ctrl + P` (Windows)
     - Destination: "Save as PDF"
     - Click "Save"
   
   - **Safari:**
     - Press `Cmd + P`
     - Click "PDF" dropdown → "Save as PDF"
   
   - **Firefox:**
     - Press `Cmd + P` (Mac) or `Ctrl + P` (Windows)
     - Destination: "Microsoft Print to PDF" or "Save as PDF"
     - Click "Print"

3. **Recommended Print Settings:**
   - Orientation: Landscape (for better chart visibility)
   - Margins: Minimal
   - Background graphics: Enabled (to capture colors)

---

## Files to Export

### Interactive Visualizations (4 files)

**Location:** `visualizations/interactive/`

1. ✅ **IWRC_ROI_Analysis_Report.html** (21 KB)
   - Full report with styled HTML
   - Works well as PDF
   - Suggested filename: `IWRC_ROI_Analysis_Report.pdf`

2. ✅ **2025_keyword_pie_chart_interactive.html** (4.8 MB)
   - Interactive Plotly chart
   - **Note:** Interactive features will be lost in PDF, but chart will be visible
   - Suggested filename: `2025_keyword_pie_chart.pdf`

3. ✅ **2025_illinois_institutions_map_interactive.html** (4.8 MB)
   - Interactive Plotly map
   - **Note:** Interactive features will be lost in PDF
   - Suggested filename: `2025_illinois_institutions_map.pdf`

4. ✅ **Seed_Fund_Tracking_Analysis.html** (888 KB)
   - Full notebook export
   - Multiple pages when printed
   - Suggested filename: `Seed_Fund_Tracking_Analysis.pdf`

---

## Alternative: Command Line (Advanced)

If you have Python installed with the required packages:

### Install wkhtmltopdf (one-time setup):
```bash
# On macOS
brew install wkhtmltopdf
```

### Convert using script:
```bash
# Navigate to the interactive folder
cd "/Users/shivpat/Downloads/Seed Fund Tracking/visualizations/interactive"

# Convert each file
wkhtmltopdf --enable-local-file-access IWRC_ROI_Analysis_Report.html IWRC_ROI_Analysis_Report.pdf
wkhtmltopdf --enable-local-file-access 2025_keyword_pie_chart_interactive.html 2025_keyword_pie_chart.pdf
wkhtmltopdf --enable-local-file-access 2025_illinois_institutions_map_interactive.html 2025_illinois_institutions_map.pdf
wkhtmltopdf --enable-local-file-access Seed_Fund_Tracking_Analysis.html Seed_Fund_Tracking_Analysis.pdf
```

---

## Alternative: Automated Python Script

### Install required package:
```bash
pip install pdfkit
```

### Run this script:
```python
import pdfkit
import os

html_dir = "/Users/shivpat/Downloads/Seed Fund Tracking/visualizations/interactive"
pdf_dir = "/Users/shivpat/Downloads/Seed Fund Tracking/visualizations/pdfs"

# Create PDF directory
os.makedirs(pdf_dir, exist_ok=True)

html_files = [
    "IWRC_ROI_Analysis_Report.html",
    "2025_keyword_pie_chart_interactive.html",
    "2025_illinois_institutions_map_interactive.html",
    "Seed_Fund_Tracking_Analysis.html"
]

for html_file in html_files:
    html_path = os.path.join(html_dir, html_file)
    pdf_path = os.path.join(pdf_dir, html_file.replace('.html', '.pdf'))
    
    print(f"Converting {html_file}...")
    pdfkit.from_file(html_path, pdf_path)
    print(f"✓ Saved to {pdf_path}")
```

---

## Important Notes

### About Interactive Features:
- **Plotly charts** (keyword pie chart, institutions map) will lose interactivity in PDF
- They will appear as static images showing the default view
- For presentations where interaction matters, use the HTML files directly

### Best Quality Results:
1. Use **Chrome** for best PDF rendering
2. Enable **"Background graphics"** to capture colors
3. Use **Landscape orientation** for charts
4. Set margins to **"Minimal"**

### File Sizes:
- PDFs will be much smaller than the HTML files
- Expected PDF sizes: 500 KB - 2 MB each

---

## Recommendation

**Fastest & Easiest:** Use Chrome's "Print to PDF" feature (Option 1)
- Takes ~2 minutes for all 4 files
- No additional software needed
- High-quality results
- Works on all operating systems

**For Automation:** Use wkhtmltopdf or Python script if converting many files regularly
