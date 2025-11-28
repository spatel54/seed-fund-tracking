# Audit of Files Referencing Old Dataset

## Active Scripts (High Priority)
- `analysis/scripts/generate_static_visualizations.py` (Likely, need to check if it imports a loader or uses file directly)
- `analysis/scripts/iwrc_data_loader.py` (This is the central loader, updating this might fix many things)
- `analysis/scripts/generate_pdf_reports.py` (or similar active report generators)

## Documentation
- `README.md`
- `docs/METHODOLOGY.md`
- `docs/DATA_DICTIONARY.md`
- `data/README.md`
- `data/consolidated/FACT_SHEET_DATA_README.md`

## Deprecated/Legacy (Low Priority)
- `deprecated/scripts/*`
- `deprecated/notebooks/*`
- `docs/archived_old_docs_*`

## Action Items
1.  **Check `iwrc_data_loader.py`**: If this script centralizes data loading, updating it is the single most effective change.
2.  **Check `generate_static_visualizations.py`**: Verify how it loads data.
3.  **Update Documentation**: Reflect the change to `clean_iwrc_tracking.xlsx`.
