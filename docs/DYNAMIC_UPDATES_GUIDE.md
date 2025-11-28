# Dynamic Updates Guide

## Overview

The IWRC Seed Fund repository now features a **modern, dynamic navigation system** that automatically updates when repository contents change. This system eliminates manual updates to index pages and ensures data stays current.

## How It Works

### 1. Configuration File
All repository metadata is stored in [`config/repo-metadata.json`](../config/repo-metadata.json):
- Project statistics (projects, investment, students, institutions)
- Navigation card information
- Quick links
- Last updated date

### 2. Dynamic Index Page
The main [`index.html`](../index.html) loads data from the config file using JavaScript:
- **Stats Bar**: Automatically displays current project metrics
- **Navigation Cards**: Generated from JSON configuration
- **Quick Links**: Dynamically populated
- **Last Updated**: Shows most recent update date

### 3. Auto-Update Script
[`scripts/update_repo_metadata.py`](../scripts/update_repo_metadata.py) automatically scans the repository and updates the configuration:
- Counts files in each category
- Extracts statistics from data files
- Updates navigation features
- Sets the last updated date

## Using the System

### Automatic Updates

Run the update script whenever repository contents change:

```bash
cd /Users/shivpat/seed-fund-tracking
python3 scripts/update_repo_metadata.py
```

**Output:**
```
✅ Repository metadata updated successfully!
📊 Stats: 77 projects, $8.5M investment, 304 students
📁 Deliverables: 88+ files
🔬 Analysis: 8 notebooks, 42 scripts
📅 Last updated: 2025-11-28
💾 Saved to: /Users/shivpat/seed-fund-tracking/config/repo-metadata.json
```

### When to Run Updates

Run the script after:
- ✅ Adding new deliverables (reports, visualizations)
- ✅ Adding analysis notebooks or scripts
- ✅ Updating data files with new fiscal year data
- ✅ Restructuring directories
- ✅ Before committing changes to git

### Automating Updates

#### Option 1: Git Pre-Commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
cd "$(git rev-parse --show-toplevel)"
python3 scripts/update_repo_metadata.py
git add config/repo-metadata.json
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

#### Option 2: GitHub Actions (if using GitHub)

Create `.github/workflows/update-metadata.yml`:

```yaml
name: Update Repository Metadata

on:
  push:
    paths:
      - 'deliverables_final/**'
      - 'analysis/**'
      - 'data/**'

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install pandas openpyxl
      - name: Update metadata
        run: python3 scripts/update_repo_metadata.py
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add config/repo-metadata.json
          git commit -m "Auto-update repository metadata" || true
          git push
```

## Modern UI Features

### Visual Improvements

1. **Modern Card Design**
   - Smooth hover animations
   - Gradient accents
   - Drop shadows with depth
   - Responsive grid layout

2. **Loading States**
   - Animated loading spinners
   - Graceful fallback if JSON fails to load
   - Fade-in animations

3. **Responsive Design**
   - Mobile-friendly layout
   - Adaptive grid columns
   - Touch-optimized interactions

4. **Live Update Indicator**
   - Pulsing dot shows system is dynamic
   - Formatted last-updated date
   - Auto-refreshes from config

### Browser Compatibility

The system works in all modern browsers:
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

### Fallback System

If `config/repo-metadata.json` cannot be loaded:
- Static fallback data is used
- User experience is unaffected
- Console warning appears for debugging

## Customization

### Adding New Navigation Cards

Edit `scripts/update_repo_metadata.py` to add new sections:

```python
{
    'id': 'new-section',
    'title': 'New Section',
    'icon': '🆕',
    'path': 'new-folder/',
    'description': 'Description of the section',
    'features': [
        'Feature 1',
        'Feature 2',
        'Feature 3',
        'Feature 4'
    ]
}
```

### Updating Statistics

The script automatically reads from:
1. `data/outputs/IWRC_ROI_Analysis_Summary_CORRECTED.xlsx`
2. `deliverables_final/3_Data_Files/IWRC_ROI_Analysis_Summary_CORRECTED.xlsx`

To change stat sources, edit the `get_project_stats()` function.

### Changing Colors/Branding

Edit CSS variables in `index.html`:

```css
:root {
    --primary-teal: #258372;    /* Main brand color */
    --dark-teal: #1a5f52;       /* Darker shade */
    --light-teal: #3fa890;      /* Lighter shade */
    --accent-peach: #FCC080;    /* Accent color */
}
```

## Technical Details

### File Structure

```
seed-fund-tracking/
├── index.html                      # Main landing page (dynamic)
├── config/
│   └── repo-metadata.json          # Configuration file
├── scripts/
│   └── update_repo_metadata.py     # Auto-update script
└── docs/
    └── DYNAMIC_UPDATES_GUIDE.md    # This file
```

### Dependencies

**Python Script:**
- pandas
- openpyxl
- pathlib (built-in)
- json (built-in)
- datetime (built-in)

**Web Interface:**
- Modern browser with JavaScript enabled
- No external dependencies (uses Fetch API)

### Performance

- **Initial Load**: <100ms (local file system)
- **Network Load**: ~2-5KB JSON file
- **Rendering**: Instant with modern browsers
- **No external API calls**: All data is local

## Troubleshooting

### Config file not loading

**Symptom**: Stats show loading spinners indefinitely

**Solutions:**
1. Check browser console for errors
2. Verify `config/repo-metadata.json` exists
3. Ensure JSON is valid (use JSONLint.com)
4. Check file permissions

### Script fails to run

**Symptom**: Python script errors

**Solutions:**
```bash
# Install dependencies
pip install pandas openpyxl

# Check Python version (3.7+ required)
python3 --version

# Run with verbose output
python3 -v scripts/update_repo_metadata.py
```

### Stats not updating

**Symptom**: Old data shown despite running script

**Solutions:**
1. Hard refresh browser (Cmd+Shift+R or Ctrl+F5)
2. Clear browser cache
3. Verify config file was actually updated
4. Check file modification date

## Migration from Static

The old static `index.html` has been backed up to `index.html.backup`.

### Key Changes:
- ✅ Stats load dynamically from JSON
- ✅ Navigation cards generated from config
- ✅ Modern, responsive UI design
- ✅ Automatic update capability
- ✅ Improved visual hierarchy

### Reverting (if needed):
```bash
mv index.html.backup index.html
```

## Future Enhancements

Potential improvements:
- [ ] Real-time git statistics integration
- [ ] Automatic data extraction from Excel files
- [ ] Search functionality across deliverables
- [ ] Analytics dashboard integration
- [ ] PDF thumbnail generation
- [ ] Version history tracking

## Support

For questions or issues:
1. Check this guide
2. Review `scripts/update_repo_metadata.py` comments
3. Inspect browser console for errors
4. Verify JSON structure in config file

---

**Last Updated**: November 28, 2025
**Version**: 2.0 (Dynamic System)
