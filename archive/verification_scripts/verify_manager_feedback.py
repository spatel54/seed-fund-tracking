
import pandas as pd
from pathlib import Path
import sys

# Add scripts to path to import loader
sys.path.insert(0, '/Users/shivpat/seed-fund-tracking/analysis/scripts')
from iwrc_data_loader import IWRCDataLoader

def verify_feedback():
    print("Loading data...")
    loader = IWRCDataLoader()
    df = loader.load_master_data(deduplicate=True)
    
    # Filter 2015-2024
    df = df[df['project_year'].between(2015, 2024, inclusive='both')]
    print(f"\nData filtered to 2015-2024. Total projects: {df['project_id'].nunique()}")
    
    # 1. Check 104B Counts
    b104 = df[df['award_type'] == 'Base Grant (104b)']
    print(f"\n--- 104B Grants ---")
    print(f"Count: {b104['project_id'].nunique()}")
    print(f"Total Investment: ${b104['award_amount'].sum():,.2f}")
    
    # 2. Check Coordination Grants
    coord = df[df['award_type'].str.contains('Coordination', case=False, na=False)]
    print(f"\n--- Coordination Grants ---")
    print(f"Count: {coord['project_id'].nunique()}")
    print(f"Project IDs: {coord['project_id'].tolist()}")
    
    # 3. Investment by Institution (UI Affiliated Only)
    print(f"\n--- Investment by Institution (UI Affiliated Only) ---")
    # Filter out non-UI
    ui_keywords = ['University of Illinois', 'Southern Illinois University']
    # Also exclude Basil's Harvest explicitly
    df_ui = df[
        (df['institution'].str.contains('|'.join(ui_keywords), case=False, na=False)) & 
        (df['institution'] != "Basil's Harvest")
    ]
    inst_funding = df_ui.groupby('institution')['award_amount'].sum().sort_values(ascending=False)
    print(inst_funding)
    
    # 4. ROI Calculation
    print(f"\n--- ROI Calculation ---")
    total_investment = df['award_amount'].sum()
    
    # Calculate follow-on funding from "Monetary Benefit..." column
    follow_on_col = 'Monetary Benefit of Award or Achievement (if applicable; use NA if not applicable)'
    
    def clean_money(val):
        if pd.isna(val): return 0.0
        s = str(val).replace('$', '').replace(',', '').strip()
        try:
            return float(s)
        except:
            return 0.0
            
    total_follow_on = df[follow_on_col].apply(clean_money).sum()
    
    roi = total_follow_on / total_investment if total_investment > 0 else 0
    print(f"Total Investment: ${total_investment:,.2f}")
    print(f"Total Follow-on: ${total_follow_on:,.2f}")
    print(f"ROI Multiplier: {roi:.2f}x")

if __name__ == "__main__":
    verify_feedback()
