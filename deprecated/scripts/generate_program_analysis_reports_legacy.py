#!/usr/bin/env python3
"""
Generate Fresh IWRC Reports
Created: November 26, 2025

This script generates two clean PDF reports from scratch:
1. IWRC_Program_Summary.pdf
2. IWRC_Analysis_Deep_Dive.pdf
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import re
import sys
from pathlib import Path
from datetime import datetime

# Add scripts to path for IWRC branding imports
sys.path.insert(0, '/Users/shivpat/seed-fund-tracking/scripts')

# Import IWRC branding
try:
    from iwrc_brand_style import IWRC_COLORS, configure_matplotlib_iwrc, apply_iwrc_matplotlib_style
    configure_matplotlib_iwrc()
    print("✓ Imported IWRC branding modules")
except ImportError as e:
    print(f"Warning: Could not import IWRC modules ({e}). Using fallback colors.")
    IWRC_COLORS = {
        'primary': '#258372',
        'secondary': '#639757',
        'text': '#54595F',
        'accent': '#FCC080',
        'background': '#F6F6F6',
        'dark_teal': '#1a5f52',
        'light_teal': '#3fa890',
        'sage': '#8ab38a',
        'neutral_light': '#f5f5f5',
        'neutral_dark': '#333333',
    }

# Configuration
DATA_FILE = Path('/Users/shivpat/seed-fund-tracking/data/consolidated/IWRC Seed Fund Tracking.xlsx')
OUTPUT_DIR = Path('/Users/shivpat/seed-fund-tracking/FINAL_DELIVERABLES_2_backup_20251125_194954 copy 2/reports/fresh')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_data():
    """Load and clean the data."""
    print("Loading data...")
    df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')
    
    # Clean column names
    df.columns = df.columns.str.strip()
    print("Columns found:", df.columns.tolist())
    
    # Rename columns
    col_map = {
        'Project ID': 'project_id',
        'Award Type': 'award_type',
        'Project Title': 'project_title',
        'Project PI': 'pi_name',
        'Academic Institution of PI': 'institution',
        'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount',
        'Number of PhD Students Supported by WRRA $': 'phd',
        'Number of MS Students Supported by WRRA $': 'ms',
        'Number of Undergraduate Students Supported by WRRA $': 'undergrad',
        'Number of Post Docs Supported by WRRA $': 'postdoc',
        'Keyword (Primary)': 'keyword_1',
        'Keyword (Secondary, if applicable)': 'keyword_2'
    }
    df = df.rename(columns=col_map)
    
    # Clean numeric columns
    for col in ['phd', 'ms', 'undergrad', 'postdoc']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    df['total_students'] = df['phd'] + df['ms'] + df['undergrad'] + df['postdoc']
    
    # Clean award amount
    def clean_money(val):
        if pd.isna(val): return 0.0
        val_str = str(val).replace('$', '').replace(',', '').strip()
        try:
            return float(val_str)
        except:
            return 0.0
            
    df['award_amount'] = df['award_amount'].apply(clean_money)
    
    return df

def create_header(ax, title, subtitle=None):
    """Create a standard IWRC header."""
    ax.add_patch(plt.Rectangle((0, 0.90), 1, 0.10, facecolor=IWRC_COLORS['primary'], transform=ax.transAxes))
    ax.text(0.5, 0.96, title, ha='center', fontsize=16, fontweight='bold', color='white', transform=ax.transAxes)
    if subtitle:
        ax.text(0.5, 0.92, subtitle, ha='center', fontsize=12, style='italic', color='white', transform=ax.transAxes)

def generate_program_summary(df):
    """Generate IWRC_Program_Summary.pdf"""
    pdf_path = OUTPUT_DIR / 'IWRC_Program_Summary.pdf'
    print(f"Generating {pdf_path}...")
    
    with PdfPages(pdf_path) as pdf:
        # Page 1: Executive Summary
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        create_header(ax, 'IWRC SEED FUND PROGRAM', 'Program Summary & Impact')
        
        # Metrics
        total_investment = df['award_amount'].sum()
        total_projects = df['project_id'].nunique()
        total_students = df['total_students'].sum()
        total_institutions = df['institution'].nunique()
        
        # Display Metrics
        y_start = 0.75
        metrics = [
            ('Total Investment', f"${total_investment:,.0f}"),
            ('Projects Funded', f"{total_projects}"),
            ('Students Supported', f"{int(total_students)}"),
            ('Institutions Served', f"{total_institutions}")
        ]
        
        for i, (label, value) in enumerate(metrics):
            x = 0.25 if i % 2 == 0 else 0.75
            y = y_start if i < 2 else y_start - 0.15
            
            ax.text(x, y, value, ha='center', fontsize=24, fontweight='bold', color=IWRC_COLORS['primary'], transform=ax.transAxes)
            ax.text(x, y-0.04, label, ha='center', fontsize=12, color=IWRC_COLORS['text'], transform=ax.transAxes)
            
        # Student Breakdown Chart
        ax_chart = fig.add_axes([0.15, 0.15, 0.7, 0.35])
        student_types = ['PhD', 'Master\'s', 'Undergrad', 'PostDoc']
        student_counts = [df['phd'].sum(), df['ms'].sum(), df['undergrad'].sum(), df['postdoc'].sum()]
        
        bars = ax_chart.bar(student_types, student_counts, color=IWRC_COLORS['secondary'])
        ax_chart.set_title('Student Training by Degree Level', fontsize=12, fontweight='bold', color=IWRC_COLORS['dark_teal'])
        apply_iwrc_matplotlib_style(fig, ax_chart)
        
        # Add labels
        for bar in bars:
            height = bar.get_height()
            ax_chart.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', color=IWRC_COLORS['text'])
        
        pdf.savefig(fig)
        plt.close()
        
        # Page 2: Institutional Reach
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_subplot(111)
        ax.axis('off')
        create_header(ax, 'INSTITUTIONAL REACH', 'Supporting Research Across Illinois')
        
        # Top Institutions Chart
        inst_counts = df['institution'].value_counts().head(10)
        ax_chart = fig.add_axes([0.15, 0.2, 0.75, 0.6])
        y_pos = np.arange(len(inst_counts))
        
        bars = ax_chart.barh(y_pos, inst_counts.values, color=IWRC_COLORS['primary'])
        ax_chart.set_yticks(y_pos)
        ax_chart.set_yticklabels(inst_counts.index)
        ax_chart.invert_yaxis()  # labels read top-to-bottom
        ax_chart.set_xlabel('Number of Projects')
        ax_chart.set_title('Top 10 Institutions by Projects Funded', fontsize=12, fontweight='bold', color=IWRC_COLORS['dark_teal'])
        
        apply_iwrc_matplotlib_style(fig, ax_chart)
        
        pdf.savefig(fig)
        plt.close()

def generate_analysis_deep_dive(df):
    """Generate IWRC_Analysis_Deep_Dive.pdf"""
    pdf_path = OUTPUT_DIR / 'IWRC_Analysis_Deep_Dive.pdf'
    print(f"Generating {pdf_path}...")
    
    with PdfPages(pdf_path) as pdf:
        # Page 1: Financial Overview
        fig = plt.figure(figsize=(8.5, 11))
        ax = fig.add_subplot(111)
        ax.axis('off')
        create_header(ax, 'ANALYSIS DEEP DIVE', 'Financial & Research Insights')
        
        # Award Type Analysis
        ax_chart = fig.add_axes([0.15, 0.5, 0.7, 0.3])
        award_type_counts = df['award_type'].value_counts()
        
        # Filter out small/nan
        award_type_counts = award_type_counts[award_type_counts > 1]
        
        colors = [IWRC_COLORS['primary'], IWRC_COLORS['secondary'], IWRC_COLORS['accent'], IWRC_COLORS['light_teal']]
        wedges, texts, autotexts = ax_chart.pie(award_type_counts, labels=award_type_counts.index, 
                                               autopct='%1.1f%%', colors=colors, startangle=90)
        ax_chart.set_title('Distribution of Award Types', fontsize=12, fontweight='bold', color=IWRC_COLORS['dark_teal'])
        
        # Research Topics (Keywords)
        ax_topics = fig.add_axes([0.15, 0.1, 0.7, 0.3])
        keywords = pd.concat([df['keyword_1'], df['keyword_2']]).dropna()
        top_keywords = keywords.value_counts().head(8)
        
        bars = ax_topics.barh(np.arange(len(top_keywords)), top_keywords.values, color=IWRC_COLORS['sage'])
        ax_topics.set_yticks(np.arange(len(top_keywords)))
        ax_topics.set_yticklabels(top_keywords.index)
        ax_topics.invert_yaxis()
        ax_topics.set_title('Top Research Topics', fontsize=12, fontweight='bold', color=IWRC_COLORS['dark_teal'])
        apply_iwrc_matplotlib_style(fig, ax_topics)
        
        pdf.savefig(fig)
        plt.close()

if __name__ == "__main__":
    print("Starting Fresh Report Generation...")
    df = load_data()
    generate_program_summary(df)
    generate_analysis_deep_dive(df)
    print("Done!")
