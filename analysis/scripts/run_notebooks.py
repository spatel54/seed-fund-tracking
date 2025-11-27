#!/usr/bin/env python3
"""
Execute notebooks using nbformat and nbconvert
"""
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

os.chdir('/Users/shivpat/seed-fund-tracking')

notebooks = [
    'notebooks/current/2025_fact_sheet_visualizations.ipynb',
    'notebooks/current/Seed_Fund_Tracking_Analysis NEW.ipynb',
    'notebooks/current/2025_interactive_visualizations.ipynb',
    'notebooks/current/2025_visualizations_FIXED.ipynb'
]

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

for i, notebook_path in enumerate(notebooks, 1):
    print('='*70)
    print(f'Executing {i}/{len(notebooks)}: {notebook_path}')
    print('='*70)

    try:
        # Read the notebook
        with open(notebook_path, 'r') as f:
            nb = nbformat.read(f, as_version=4)

        # Execute the notebook
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path) or '.'}})

        # Write the executed notebook back
        with open(notebook_path, 'w') as f:
            nbformat.write(nb, f)

        print(f'✅ Successfully executed: {notebook_path}')

    except Exception as e:
        print(f'❌ Error executing {notebook_path}: {e}')

    print()

print('='*70)
print('ALL NOTEBOOKS EXECUTED')
print('='*70)
