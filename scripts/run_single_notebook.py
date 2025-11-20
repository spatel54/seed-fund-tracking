#!/usr/bin/env python3
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os
import sys

notebook_path = sys.argv[1] if len(sys.argv) > 1 else None
if not notebook_path:
    print("Usage: python run_single_notebook.py <notebook_path>")
    sys.exit(1)

os.chdir('/Users/shivpat/Downloads/Seed Fund Tracking')

print(f"Executing: {notebook_path}")

try:
    with open(notebook_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path) or '.'}})

    with open(notebook_path, 'w') as f:
        nbformat.write(nb, f)

    print(f"✅ Successfully executed: {notebook_path}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
