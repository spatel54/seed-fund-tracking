#!/usr/bin/env python3
"""
Execute Jupyter notebooks and save visualizations
"""
import subprocess
import sys
import os

# Change to the project directory
os.chdir('/Users/shivpat/Downloads/Seed Fund Tracking')

notebooks = [
    'notebooks/current/2025_fact_sheet_visualizations.ipynb',
    'notebooks/current/Seed_Fund_Tracking_Analysis NEW.ipynb',
    'notebooks/current/2025_interactive_visualizations.ipynb',
    'notebooks/current/2025_visualizations_FIXED.ipynb'
]

for i, notebook in enumerate(notebooks, 1):
    print('='*70)
    print(f'Executing {i}/{len(notebooks)}: {notebook}')
    print('='*70)

    try:
        # Execute the notebook using python -m jupyter
        result = subprocess.run(
            [sys.executable, '-m', 'jupyter', 'nbconvert',
             '--to', 'notebook',
             '--execute',
             '--inplace',
             '--ExecutePreprocessor.timeout=300',
             notebook],
            capture_output=True,
            text=True,
            timeout=600
        )

        if result.returncode == 0:
            print(f'✅ Successfully executed: {notebook}')
        else:
            print(f'❌ Error executing {notebook}')
            print(f'STDOUT: {result.stdout}')
            print(f'STDERR: {result.stderr}')

    except subprocess.TimeoutExpired:
        print(f'⏱️ Timeout executing {notebook}')
    except Exception as e:
        print(f'❌ Exception executing {notebook}: {e}')

    print()

print('='*70)
print('EXECUTION COMPLETE')
print('='*70)
