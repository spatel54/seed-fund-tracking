# Illinois Institutions Map - User Guide

## Overview
This interactive map displays all Illinois institutions that have received IWRC (Illinois Water Resources Center) Seed Fund grants from 1999-2024. The map provides comprehensive project information through an intuitive, clickable interface.

## File Information
- **File Name:** `illinois_institutions_map_enhanced.html`
- **File Size:** 840 KB
- **File Location:** `/Users/shivpat/Downloads/Seed Fund Tracking/visualizations/interactive/award_types/`
- **Data Source:** IWRC Seed Fund Tracking.xlsx (Project Overview sheet)
- **Last Updated:** November 23, 2025

## Features Implemented

### 1. Base Map
- **Map Provider:** CartoDB Positron (clean, professional style)
- **Center:** Illinois state center (40.0°N, -89.0°W)
- **Zoom Level:** 7 (shows entire state)
- **Controls:** Zoom in/out, pan, scale indicator

### 2. Visual Encoding

#### Bubble Size
- **Represents:** Total funding amount per institution
- **Range:** 12px to 45px radius
- **Scale:**
  - Small bubbles (12-20px): $10K - $100K
  - Medium bubbles (20-30px): $100K - $1M
  - Large bubbles (30-45px): > $1M

#### Bubble Color
- **Represents:** Number of projects per institution
- **Gradient:** Light blue → Dark blue
- **Scale:** Lighter = fewer projects, Darker = more projects
- **Color Legend:** Displayed on map

### 3. Interactive Elements

#### Hover Tooltips
When you hover over a bubble, you'll see:
- Institution name
- Number of projects
- Total funding amount

#### Click Popups
When you click on a bubble, a detailed popup appears with:

**Institution Header:**
- Institution name (large, bold)
- City, Illinois
- Year range of projects

**Summary Statistics (4 cards):**
1. Total Funding (formatted as $X.XXM or $X,XXX)
2. Number of Projects
3. Total Students Trained
4. Number of Principal Investigators

**Additional Statistics (2 cards):**
1. Student Breakdown (PhD, MS, Undergrad, PostDoc)
2. Award Type Distribution (104g, 104b, Coordination)

**Project List:**
Each project card includes:
- Color-coded award type badge (104g-General, 104g-AIS, 104g-PFAS, 104b, Coordination)
- Project ID and year
- Project title
- Award amount (prominent display)
- Number of students trained for that project
- Principal Investigator name
- Department
- PI contact email (if available)
- Students trained (detailed breakdown)
- Science priority
- Keywords
- Collapsible project summary (click "View Project Summary" to expand)

### 4. Award Type Color Coding

The map uses consistent color coding for award types:

- **104g-General:** Green (#28a745)
- **104g-AIS (Aquatic Invasive Species):** Teal (#20c997)
- **104g-PFAS:** Orange (#fd7e14)
- **104b (Base Grant):** Blue (#007bff)
- **Coordination:** Yellow (#ffc107)
- **Other:** Gray (#6c757d)

### 5. Legend
The legend (bottom left) shows:
- Bubble size meaning (funding ranges)
- Award type badge colors
- Clear visual examples

## How to Use the Map

### Basic Navigation
1. **Open the Map:** Double-click `illinois_institutions_map_enhanced.html` to open in your default web browser
2. **Pan:** Click and drag to move around the map
3. **Zoom:** Use scroll wheel or +/- buttons to zoom in/out
4. **Reset View:** Refresh the browser to reset to default view

### Exploring Institutions
1. **Quick Info:** Hover over any bubble to see basic institution information
2. **Detailed View:** Click on a bubble to open the full project popup
3. **Scroll Through Projects:** Use your mouse wheel or trackpad to scroll within the popup
4. **Read Summaries:** Click "View Project Summary" on any project to expand full description
5. **Close Popup:** Click the X in the top-right of the popup or click elsewhere on the map

### Finding Specific Information
- **Largest Funders:** Look for the biggest bubbles (UIUC dominates with $7.2M)
- **Most Projects:** Look for the darkest blue bubbles
- **Regional Distribution:** Pan around to see geographic spread across Illinois
- **Recent Projects:** Check the year badge on each project card

## Data Summary

### Overall Statistics
- **Institutions Mapped:** 14
- **Total Projects:** 162
- **Total Funding:** $9,393,288
- **Year Range:** 1999-2024 (25 years)
- **Students Trained:** 304 total across all institutions

### Top 5 Institutions by Funding
1. **University of Illinois at Urbana-Champaign**
   - $7.23M | 115 projects | Urbana-Champaign
   - 192 students trained
   - Award types: 85 (104b), 19 (104g), 10 (Coordination)

2. **Illinois Institute of Technology**
   - $1.05M | 7 projects | Chicago
   - 24 students trained
   - Award types: 4 (104g), 3 (104b)

3. **Southern Illinois University Carbondale**
   - $842K | 18 projects | Carbondale
   - 42 students trained
   - Award types: 12 (104b), 4 (104g), 2 (Coordination)

4. **Illinois State University**
   - $79.8K | 8 projects | Normal
   - 20 students trained
   - Award types: 8 (104b)

5. **Illinois State Water Survey**
   - $60K | 1 project | Champaign
   - 0 students trained
   - Award types: 1 (104b)

### Geographic Coverage
The map includes institutions in the following Illinois cities:
- Urbana-Champaign (central Illinois)
- Chicago/Evanston (northeast)
- Carbondale (southern Illinois)
- Normal (central Illinois)
- Godfrey/Alton (western Illinois)
- DeKalb (northern Illinois)
- Charleston (eastern Illinois)
- Romeoville (northeast Illinois)

## Browser Compatibility

### Recommended Browsers
✅ **Chrome** (version 90+) - Best performance
✅ **Microsoft Edge** (version 90+) - Best performance
✅ **Firefox** (version 88+) - Good performance
✅ **Safari** (version 14+) - Good performance

### Mobile Browsers
✅ Chrome for Android
✅ Safari for iOS
✅ Firefox Mobile

### Known Issues
- Older browsers (IE11 and below) are not supported
- Some mobile browsers may have slower performance with many popups open
- Print functionality may not preserve all interactive elements

## Technical Details

### Technologies Used
- **Folium:** Python library for interactive maps (built on Leaflet.js)
- **CartoDB Positron:** Base map tiles
- **Branca:** Colormap generation
- **HTML5/CSS3:** Popup styling and layout
- **JavaScript:** Interactive behavior (included in Folium)

### Data Processing
- Institution names normalized for consistency (e.g., "University of Illinois" → "University of Illinois at Urbana-Champaign")
- Years extracted from Project IDs using regex patterns
- Missing data handled gracefully (displayed as "N/A" or "None")
- Projects sorted by year (most recent first) within each popup

### Geocoding
- All Illinois institutions manually geocoded with accurate coordinates
- Out-of-state institutions excluded (e.g., University of Texas at Austin)
- Institutions without clear location data excluded (e.g., "Unknown")

## Data Limitations

### Excluded Data
- **187 projects** with "Unknown" institution (missing data in source)
- **5 projects** from out-of-state or non-standard institutions:
  - Basil's Harvest (1 project)
  - Cary Institute of Ecosystem Studies (1 project)
  - University of Texas at Austin (1 project)
  - 2 projects with typographical errors in institution name

### Data Quality Notes
- Some project summaries may be truncated if longer than 500 characters
- Email addresses not available for all PIs
- Student counts may be zero for some projects (data not collected/reported)
- Year extraction from Project IDs may be imprecise for some older projects

## Exporting and Sharing

### Sharing the Map
1. **Email:** Attach the HTML file (840 KB) to an email
2. **Cloud Storage:** Upload to Google Drive, Dropbox, etc.
3. **Web Hosting:** Upload to any web server for public access
4. **USB/Network Drive:** Copy file to shared location

### Screenshots
To capture a screenshot of the map:
1. Open the map in your browser
2. Click on an institution to open a popup (optional)
3. Use your system's screenshot tool:
   - **Mac:** Cmd + Shift + 4
   - **Windows:** Win + Shift + S
   - **Browser:** Right-click → "Save As" or print to PDF

### Printing
To print the map:
1. Open the map in your browser
2. Press Ctrl+P (Windows) or Cmd+P (Mac)
3. Adjust print settings as needed
4. Note: Interactive popups won't be visible in print

## Troubleshooting

### Map Won't Load
- Ensure you have an active internet connection (needed for base map tiles)
- Try opening in a different browser
- Check that the HTML file hasn't been corrupted
- Clear your browser cache

### Popups Won't Open
- Try clicking directly on the center of the bubble
- Refresh the page (F5 or Cmd+R)
- Check browser console for JavaScript errors (F12)

### Performance Issues
- Close other browser tabs to free up memory
- Try a different browser (Chrome recommended)
- Ensure your computer has sufficient RAM (2GB+ recommended)
- Close other applications

### Display Issues
- Zoom in/out to adjust view
- Try fullscreen mode (F11)
- Adjust browser zoom level (Ctrl/Cmd + '+' or '-')
- Check screen resolution (1280x720 minimum recommended)

## Future Enhancements

Potential features for future versions:
- [ ] Time period filters (All years, 10-year, 5-year)
- [ ] Award type filters (toggle 104g, 104b, Coordination)
- [ ] Search functionality for specific projects or PIs
- [ ] Export project data as CSV from popup
- [ ] Print-friendly popup view
- [ ] Clustering for overlapping markers
- [ ] Animation showing funding over time
- [ ] Comparison view for multiple institutions

## Contact and Support

For questions, issues, or suggestions regarding this map, please contact:
- **Illinois Water Resources Center (IWRC)**
- Data sourced from: IWRC Seed Fund Tracking.xlsx

## Credits

**Created:** November 23, 2025
**Data Source:** IWRC Seed Fund Tracking Database
**Generated by:** Claude Code (Anthropic)
**Tools Used:** Python 3, Folium, Pandas, Branca

---

**Map File:** `illinois_institutions_map_enhanced.html`
**Documentation:** `MAP_GUIDE.md`
**Version:** 1.0
