# Quick Start Guide

## 🚀 Using the Repository

### View the Interface
Simply double-click or open [index.html](index.html) in any browser.

The page loads **instantly** with embedded data - no server required!

## 🔄 Updating Data

When you add new files or make changes to the repository:

```bash
python3 scripts/update_repo_metadata.py
```

This automatically:
- ✅ Counts files in each category
- ✅ Updates statistics
- ✅ Saves to `config/repo-metadata.json`
- ✅ Embeds data into `index.html`

Takes 2 seconds vs 10+ minutes of manual editing!

## 📊 What's Included

- **77 projects** tracked (2015-2024)
- **$8.5M** in investment
- **304 students** supported
- **14 institutions** funded
- **87+ deliverables** organized

## ✨ Features

### Modern UI
- Smooth animations
- Responsive mobile design
- Professional gradients & depth
- Loading states

### Dynamic System
- Auto-updates from repository
- Embedded data (no server needed)
- Works offline
- JSON + embedded fallback

### Easy Maintenance
- Run one script to update
- No manual HTML editing
- Version controlled config
- Self-documenting

## 📚 Documentation

- [Dynamic Updates Guide](docs/DYNAMIC_UPDATES_GUIDE.md) - Complete system guide
- [November 2025 Update](docs/NOVEMBER_2025_UI_UPDATE.md) - Technical details
- [Update Summary](UPDATE_SUMMARY.md) - Quick reference
- [README](README.md) - Repository overview

## 🎯 Common Tasks

### Adding New Deliverables
1. Add files to `deliverables_final/`
2. Run `python3 scripts/update_repo_metadata.py`
3. Done! The index automatically updates

### Adding Analysis Files
1. Add notebooks to `analysis/notebooks/`
2. Add scripts to `analysis/scripts/`
3. Run `python3 scripts/update_repo_metadata.py`
4. Done!

### Customizing Navigation
Edit `config/repo-metadata.json` to change:
- Navigation card descriptions
- Quick links
- Features lists
- Any displayed text

Then open `index.html` to see changes instantly!

## 🛠️ Troubleshooting

### Page shows old data
- Hard refresh: Cmd+Shift+R (Mac) or Ctrl+F5 (Windows)
- Clear browser cache

### Script fails
```bash
# Check Python version (3.7+ required)
python3 --version

# Run from repository root
cd /Users/shivpat/seed-fund-tracking
python3 scripts/update_repo_metadata.py
```

### Navigation not loading
The page now has embedded data, so it should load instantly.
If you see loading spinners, hard refresh the browser.

## 🌐 Serving via HTTP (Optional)

For better performance over a network:

```bash
# Start simple HTTP server
python3 -m http.server 8000

# Open browser to:
# http://localhost:8000
```

The JSON file will be fetched dynamically when served via HTTP,
but embedded data is used when opening via file://.

## 💡 Tips

- **Backup**: Old version saved to `index.html.backup`
- **Revert**: Copy backup back to `index.html` if needed
- **Git**: Commit after running update script
- **Schedule**: Add script to cron/scheduler for automatic updates

## ✅ System Status

Run this to check everything:

```bash
python3 -c "
import json
with open('config/repo-metadata.json') as f:
    data = json.load(f)
print('✅ JSON valid')
print(f\"📊 {data['stats']['projects']} projects\")
print(f\"💰 {data['stats']['totalInvestment']} investment\")
print(f\"📅 Updated: {data['lastUpdated']}\")
"
```

---

**Need Help?**
- See [docs/DYNAMIC_UPDATES_GUIDE.md](docs/DYNAMIC_UPDATES_GUIDE.md)
- Check [UPDATE_SUMMARY.md](UPDATE_SUMMARY.md)
- Review browser console for errors

---

**Version**: 2.0 - Dynamic System
**Last Updated**: November 28, 2025
**Status**: ✅ Ready to use!
