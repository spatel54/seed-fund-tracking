# Repository Reorganization - November 27, 2025

## Summary

On November 27, 2025, the IWRC Seed Fund Tracking repository underwent a major reorganization:

✅ **45% Size Reduction** - From 282 MB to 154 MB (removed 128 MB of duplicates)
✅ **Clean Structure** - Logical separation of deliverables, analysis, data, and assets
✅ **Professional Navigation** - IWRC-branded index.html pages
✅ **Comprehensive Documentation** - README.md in every major folder

## Key Changes

### New Structure
- **Created `/deliverables/`** - All final outputs (reports + visualizations)
- **Created `/analysis/`** - All code (notebooks + scripts)
- **Reorganized `/assets/`** - Centralized branding (logos, fonts, guidelines)
- **Added index.html pages** - Professional navigation hubs

### Files Moved
- `/notebooks/` → `/analysis/notebooks/`
- `/scripts/` → `/analysis/scripts/`
- Reports → `/deliverables/reports/` (executive + detailed)
- Visualizations → `/deliverables/visualizations/` (static + interactive)
- Logos/fonts → `/assets/branding/`

### Files Deleted (205 MB)
- `SKIP/` and `SKIP2/` (74 MB duplicates)
- `FINAL_DELIVERABLES*` folders (131 MB)
- `PROJECT_ARCHIVES/`
- Test scripts (test_plotly.py, fix_notebook_*.py)
- All __pycache__ directories

### Deliverables Organized
- **6 PDFs** in `/deliverables/reports/` (renamed for clarity)
- **36 PNGs** in `/deliverables/visualizations/static/` (categorized: overview, institutions, students, topics, awards, project types)
- **15 HTML** in `/deliverables/visualizations/interactive/` (organized: core, geographic, award types, project types)

## New Structure

```
seed-fund-tracking/
├── index.html                    # Main navigation hub
├── deliverables/                 # All final outputs
│   ├── reports/                  # 6 PDFs
│   └── visualizations/           # 36 PNGs + 15 HTML
├── analysis/                     # All code
│   ├── notebooks/                # 7 Jupyter notebooks
│   └── scripts/                  # 44 Python scripts
├── data/                         # Source + outputs
├── assets/                       # Branding + styles
└── docs/                         # Documentation
```

## Benefits

**For Users:**
- Easy navigation with visual index pages
- Quick access to reports and visualizations
- Professional IWRC branding

**For Developers:**
- Clean code organization in `/analysis/`
- Centralized assets in `/assets/branding/`
- Comprehensive documentation

## Migration Notes

Update bookmarked paths:
- `/notebooks/` → `/analysis/notebooks/`
- `/scripts/` → `/analysis/scripts/`
- `/reports/` → `/deliverables/reports/`
- `/visualizations/` → `/deliverables/visualizations/`

---

**Date:** November 27, 2025 | **Version:** 2.0
