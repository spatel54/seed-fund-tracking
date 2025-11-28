#!/usr/bin/env python3
"""
Generate Detailed Reports with Corrected IWRC Data
Updated: November 24, 2025

This script creates four detailed report PDFs:
1. IWRC_Detailed_Analysis_Report.pdf - Deep dive analysis
2. IWRC_Fact_Sheet.pdf - One-page fact sheet
3. IWRC_Financial_Summary.pdf - Financial breakdown
4. IWRC_Seed_Fund_Executive_Summary.pdf - Executive summary
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
    USE_IWRC_BRANDING = True
    print("✓ Imported IWRC branding modules")
except ImportError as e:
    print(f"Warning: Could not import IWRC modules ({e}). Using fallback colors.")
    USE_IWRC_BRANDING = False
    IWRC_COLORS = {
        'primary': '#1f77b4',
        'secondary': '#ff7f0e',
        'success': '#2ca02c',
        'accent': '#d62728',
        'purple': '#9467bd',
        'light_blue': '#e8f4f8',
        'dark_blue': '#003d7a'
    }

# ============================================================================
# CONFIGURATION
# ============================================================================

OUTPUT_DIR = Path('/Users/shivpat/seed-fund-tracking/deliverables_final/reports/detailed')
DATA_FILE = Path('/Users/shivpat/seed-fund-tracking/data/processed/clean_iwrc_tracking.xlsx')

# Use IWRC brand colors
COLORS = {
    'primary': IWRC_COLORS['primary'],           # #258372 - Teal
    'secondary': IWRC_COLORS['secondary'],       # #639757 - Olive
    'success': IWRC_COLORS['accent'],            # #FCC080 - Peach/Gold
    'accent': IWRC_COLORS['light_teal'],         # #3fa890 - Light Teal
    'purple': IWRC_COLORS['sage'],               # #8ab38a - Sage
    'light_blue': IWRC_COLORS['background'],     # #F6F6F6 - Light Gray
    'dark_blue': IWRC_COLORS['dark_teal']        # #1a5f52 - Dark Teal
}

# Configure matplotlib for IWRC branding
if USE_IWRC_BRANDING:
    configure_matplotlib_iwrc()

# ============================================================================
# DATA LOADING AND PREPARATION
# ============================================================================

def load_and_prepare_data():
    """Load and prepare the IWRC seed fund data."""
    print("Loading data from Excel...")
    df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')

    col_map = {
        'Project ID ': 'project_id',
        'Award Type': 'award_type',
        'Project Title': 'project_title',
        'Project PI': 'pi_name',
        'Academic Institution of PI': 'institution',
        'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount',
        'Number of PhD Students Supported by WRRA $': 'phd_students',
        'Number of MS Students Supported by WRRA $': 'ms_students',
        'Number of Undergraduate Students Supported by WRRA $': 'undergrad_students',
        'Number of Post Docs Supported by WRRA $': 'postdoc_students',
        "Award, Achievement, or Grant\n (This may include awards and achievements for projects from the previous year to this 5-year cycle, so long as they were not already included in last year's report)": 'awards_grants',
        'Keyword (Primary)': 'keyword_primary',
        'Keyword 2': 'keyword_2',
        'Keyword 3': 'keyword_3'
    }

    df = df.rename(columns=col_map)

    student_cols = ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']
    for col in student_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    def extract_year(project_id):
        if pd.isna(project_id):
            return None
        project_id_str = str(project_id).strip()
        year_match = re.search(r'(20\d{2}|19\d{2})', project_id_str)
        if year_match:
            return int(year_match.group(1))
        fy_match = re.search(r'FY(\d{2})', project_id_str, re.IGNORECASE)
        if fy_match:
            fy_year = int(fy_match.group(1))
            return 2000 + fy_year if fy_year < 100 else fy_year
        return None

    df['project_year'] = df['project_id'].apply(extract_year)

    df_10yr = df[df['project_year'].between(2015, 2024, inclusive='both')].copy()
    df_5yr = df[df['project_year'].between(2020, 2024, inclusive='both')].copy()

    print(f"✓ Data loaded: {len(df)} total rows")
    print(f"✓ 10-Year period: {df_10yr['project_id'].nunique()} unique projects")
    print(f"✓ 5-Year period: {df_5yr['project_id'].nunique()} unique projects")

    return df, df_10yr, df_5yr

# ============================================================================
# METRICS CALCULATION
# ============================================================================

def clean_monetary_value(value):
    """Clean and convert monetary values to float."""
    if pd.isna(value):
        return 0.0
    value_str = str(value).strip().upper()
    if value_str in ['NA', 'N/A', 'NONE', '']:
        return 0.0
    dollar_pattern = r'\$?\s*([\d,]+(?:\.\d{2})?)'
    matches = re.findall(dollar_pattern, value_str)
    if matches:
        total = 0.0
        for match in matches:
            try:
                amount = float(match.replace(',', ''))
                total += amount
            except (ValueError, TypeError):
                continue
        return total if total > 0 else 0.0
    return 0.0

def categorize_award(award_text):
    """Categorize awards into Grant, Award, or Achievement."""
    if pd.isna(award_text):
        return None
    award_str = str(award_text).lower()
    if 'grant' in award_str:
        return 'Grant'
    elif 'award' in award_str:
        return 'Award'
    elif 'achievement' in award_str:
        return 'Achievement'
    else:
        return 'Other'

def calculate_metrics(df):
    """Calculate all key metrics for a time period."""
    investment = df['award_amount'].sum()
    num_projects = df['project_id'].nunique()

    df['award_category'] = df['awards_grants'].apply(categorize_award)
    df_with_awards = df[df['award_category'].notna()].copy()

    awards_count = len(df_with_awards)
    followon_funding = 0
    roi = 0

    if investment > 0:
        roi = followon_funding / investment

    students = {
        'phd': df['phd_students'].sum(),
        'ms': df['ms_students'].sum(),
        'undergrad': df['undergrad_students'].sum(),
        'postdoc': df['postdoc_students'].sum()
    }
    students['total'] = sum(students.values())

    num_institutions = df['institution'].nunique()

    return {
        'investment': investment,
        'projects': num_projects,
        'followon_funding': followon_funding,
        'roi': roi,
        'awards_count': awards_count,
        'students': students,
        'institutions': num_institutions
    }

# ============================================================================
# REPORT 1: DETAILED ANALYSIS REPORT
# ============================================================================

def generate_detailed_analysis_report(df_10yr, df_5yr, metrics_10yr, metrics_5yr):
    """Generate comprehensive detailed analysis report."""
    print("\nGenerating IWRC_Detailed_Analysis_Report.pdf...")

    pdf_path = OUTPUT_DIR / 'IWRC_Detailed_Analysis_Report.pdf'

    with PdfPages(pdf_path) as pdf:
        # Page 1: Title and Overview
        fig = plt.figure(figsize=(8.5, 11))
        fig.patch.set_facecolor('white')
        ax = fig.add_subplot(111)
        ax.axis('off')

        ax.text(0.5, 0.90, 'IWRC DETAILED ANALYSIS REPORT', ha='center', fontsize=18,
               fontweight='bold', transform=ax.transAxes, color=COLORS['dark_blue'])
        ax.text(0.5, 0.85, 'Illinois Water Resources Research Center', ha='center', fontsize=12,
               style='italic', transform=ax.transAxes)
        ax.text(0.5, 0.80, 'Seed Fund Program Analysis (2015-2024)', ha='center', fontsize=11,
               transform=ax.transAxes)

        # Background for Overview
        # Create a rectangle for the background
        # Transform coordinates to display coordinates
        rect = plt.Rectangle((0.05, 0.10), 0.9, 0.65,
                            facecolor=COLORS['light_blue'],
                            edgecolor="none",
                            transform=ax.transAxes)
        ax.add_patch(rect)

        # Executive Overview Title
        ax.text(0.5, 0.73, 'EXECUTIVE OVERVIEW', ha='center', fontsize=12, fontweight='bold',
               transform=ax.transAxes, color=COLORS['dark_blue'])
        
        # Intro Text
        intro_text = "This detailed report provides comprehensive analysis of the IWRC Seed Fund program\nacross the 10-year period from 2015 to 2024."
        ax.text(0.5, 0.70, intro_text, ha='center', va='top', fontsize=10,
               transform=ax.transAxes, color=COLORS['primary'])

        # Helper to create tables
        def add_stats_table(y_pos, title, data):
            # Title
            ax.text(0.5, y_pos, title, ha='center', va='bottom', fontsize=10, fontweight='bold',
                   transform=ax.transAxes, color=COLORS['dark_blue'])
            ax.plot([0.3, 0.7], [y_pos-0.005, y_pos-0.005], color='black', linewidth=1, transform=ax.transAxes)
            
            # Table
            table_data = []
            for label, value in data:
                table_data.append([label, value])
            
            # Create table centered at y_pos - height
            # We'll use a separate axes for the table to control it better or just place it carefully
            # For simplicity on this page, let's use text alignment since we want it centered
            
            current_y = y_pos - 0.025
            for label, value in data:
                ax.text(0.48, current_y, label, ha='right', va='top', fontsize=10, transform=ax.transAxes)
                ax.text(0.52, current_y, value, ha='left', va='top', fontsize=10, transform=ax.transAxes)
                current_y -= 0.02
            
            return current_y - 0.02

        # Key Statistics
        stats_data = [
            ('Total IWRC Investment:', f"${metrics_10yr['investment']:,.0f}"),
            ('Number of Unique Projects:', f"{metrics_10yr['projects']}"),
            ('Number of Institutions:', f"{metrics_10yr['institutions']}"),
            ('Total Students Trained:', f"{int(metrics_10yr['students']['total'])}")
        ]
        next_y = add_stats_table(0.65, 'KEY STATISTICS (10-Year Period)', stats_data)

        # Student Breakdown
        student_data = [
            ('PhD Students:', f"{int(metrics_10yr['students']['phd'])}"),
            ("Master's Students:", f"{int(metrics_10yr['students']['ms'])}"),
            ('Undergraduate Students:', f"{int(metrics_10yr['students']['undergrad'])}"),
            ('Post-Doctoral Researchers:', f"{int(metrics_10yr['students']['postdoc'])}")
        ]
        next_y = add_stats_table(next_y, 'STUDENT BREAKDOWN (10-Year)', student_data)

        # Five-Year Comparison
        comparison_data = [
            ('Total Investment:', f"${metrics_5yr['investment']:,.0f}"),
            ('Number of Projects:', f"{metrics_5yr['projects']}"),
            ('Number of Institutions:', f"{metrics_5yr['institutions']}"),
            ('Total Students Trained:', f"{int(metrics_5yr['students']['total'])}")
        ]
        add_stats_table(next_y, 'FIVE-YEAR COMPARISON (2020-2024)', comparison_data)

        # Data Correction Note
        note_text = "DATA CORRECTION NOTE\nThis report reflects corrected data as of November 24, 2025.\nProject counts represent unique projects, not spreadsheet rows."
        ax.text(0.5, 0.08, note_text, ha='center', va='top', fontsize=8, style='italic',
               transform=ax.transAxes, color=COLORS['secondary'])

        ax.text(0.5, 0.02, f"Report Generated: {datetime.now().strftime('%B %d, %Y')}",
               ha='center', fontsize=8, style='italic', color='gray', transform=ax.transAxes)

        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

        # Page 2: Investment Analysis with Charts
        fig = plt.figure(figsize=(8.5, 11))
        fig.suptitle('Investment Analysis', fontsize=14, fontweight='bold', y=0.97)

        gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3, top=0.94, bottom=0.08)

        # Investment by Period
        ax1 = fig.add_subplot(gs[0, :])
        periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']
        investments = [metrics_10yr['investment'], metrics_5yr['investment']]
        bars = ax1.bar(periods, investments, color=[COLORS['primary'], COLORS['secondary']], width=0.5)
        for bar, value in zip(bars, investments):
            ax1.text(bar.get_x() + bar.get_width()/2, value, f'${value:,.0f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Total Investment ($)', fontsize=10, fontweight='bold')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.grid(axis='y', alpha=0.3)

        # Projects
        ax2 = fig.add_subplot(gs[1, 0])
        projects = [metrics_10yr['projects'], metrics_5yr['projects']]
        bars = ax2.bar(periods, projects, color=[COLORS['primary'], COLORS['secondary']], width=0.5)
        for bar, value in zip(bars, projects):
            ax2.text(bar.get_x() + bar.get_width()/2, value, f'{int(value)}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Number of Projects', fontsize=10, fontweight='bold')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.grid(axis='y', alpha=0.3)

        # Average per project
        ax3 = fig.add_subplot(gs[1, 1])
        avg_10yr = metrics_10yr['investment'] / metrics_10yr['projects']
        avg_5yr = metrics_5yr['investment'] / metrics_5yr['projects']
        avg_values = [avg_10yr, avg_5yr]
        bars = ax3.bar(periods, avg_values, color=[COLORS['primary'], COLORS['secondary']], width=0.5)
        for bar, value in zip(bars, avg_values):
            ax3.text(bar.get_x() + bar.get_width()/2, value, f'${value:,.0f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        ax3.set_ylabel('Avg per Project ($)', fontsize=10, fontweight='bold')
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.grid(axis='y', alpha=0.3)

        # Institutions served
        ax4 = fig.add_subplot(gs[2, 0])
        institutions = [metrics_10yr['institutions'], metrics_5yr['institutions']]
        bars = ax4.bar(periods, institutions, color=[COLORS['primary'], COLORS['secondary']], width=0.5)
        for bar, value in zip(bars, institutions):
            ax4.text(bar.get_x() + bar.get_width()/2, value, f'{int(value)}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        ax4.set_ylabel('Institutions Served', fontsize=10, fontweight='bold')
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        ax4.grid(axis='y', alpha=0.3)

        # Total students
        ax5 = fig.add_subplot(gs[2, 1])
        total_students = [int(metrics_10yr['students']['total']), int(metrics_5yr['students']['total'])]
        bars = ax5.bar(periods, total_students, color=[COLORS['primary'], COLORS['secondary']], width=0.5)
        for bar, value in zip(bars, total_students):
            ax5.text(bar.get_x() + bar.get_width()/2, value, f'{value}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        ax5.set_ylabel('Students Trained', fontsize=10, fontweight='bold')
        ax5.spines['top'].set_visible(False)
        ax5.spines['right'].set_visible(False)
        ax5.grid(axis='y', alpha=0.3)

        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

        # Page 3: Student Distribution
        fig = plt.figure(figsize=(8.5, 11))
        fig.suptitle('Student Distribution Analysis', fontsize=14, fontweight='bold', y=0.97)

        gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3, top=0.94, bottom=0.08)

        categories = ['PhD', "Master's", 'Undergrad', 'PostDoc']
        data_10yr = [
            metrics_10yr['students']['phd'],
            metrics_10yr['students']['ms'],
            metrics_10yr['students']['undergrad'],
            metrics_10yr['students']['postdoc']
        ]
        data_5yr = [
            metrics_5yr['students']['phd'],
            metrics_5yr['students']['ms'],
            metrics_5yr['students']['undergrad'],
            metrics_5yr['students']['postdoc']
        ]

        # Bar chart
        ax1 = fig.add_subplot(gs[0, :])
        x = np.arange(len(categories))
        width = 0.35
        ax1.bar(x - width/2, data_10yr, width, label='10-Year', color=COLORS['primary'])
        ax1.bar(x + width/2, data_5yr, width, label='5-Year', color=COLORS['secondary'])
        ax1.set_ylabel('Number of Students', fontsize=10, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(categories)
        ax1.legend(loc='upper right')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.grid(axis='y', alpha=0.3)

        # 10-year pie
        ax2 = fig.add_subplot(gs[1, 0])
        colors_pie = [COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['purple']]
        ax2.pie(data_10yr, labels=categories, autopct='%1.1f%%', colors=colors_pie, startangle=90)
        ax2.set_title(f"10-Year Distribution\n{int(metrics_10yr['students']['total'])} total", fontsize=10)

        # 5-year pie
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.pie(data_5yr, labels=categories, autopct='%1.1f%%', colors=colors_pie, startangle=90)
        ax3.set_title(f"5-Year Distribution\n{int(metrics_5yr['students']['total'])} total", fontsize=10)

        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

        # Page 4: Static Visualizations (Topic Areas) - High Quality
        try:
            static_viz_dir = Path('/Users/shivpat/seed-fund-tracking/deliverables_final/visualizations/static/topics')
            topic_areas_img1 = static_viz_dir / 'topic_areas_funding.png'
            topic_areas_img2 = static_viz_dir / 'topic_areas_pyramid_stacked.png'

            if topic_areas_img1.exists() and topic_areas_img2.exists():
                fig = plt.figure(figsize=(8.5, 11), dpi=300)  # Higher DPI for quality
                fig.suptitle('Research Topic Areas Analysis', fontsize=14, fontweight='bold', y=0.97)
                
                # Topic Areas Image 1
                ax1 = fig.add_axes([0.1, 0.55, 0.8, 0.35])
                img1 = plt.imread(topic_areas_img1)
                ax1.imshow(img1, interpolation='lanczos', aspect='auto')  # Better interpolation
                ax1.axis('off')
                ax1.set_title('Topic Areas by Funding Comparison', fontsize=12, fontweight='bold')

                # Topic Areas Image 2
                ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.35])
                img2 = plt.imread(topic_areas_img2)
                ax2.imshow(img2, interpolation='lanczos', aspect='auto')  # Better interpolation
                ax2.axis('off')
                ax2.set_title('Topic Areas Distribution', fontsize=12, fontweight='bold')

                pdf.savefig(fig, bbox_inches='tight', dpi=300)  # Save at high DPI
                plt.close(fig)
                print("✓ Added static visualizations page (high quality)")
            else:
                print("Warning: Static visualizations not found, skipping page 4")
        except Exception as e:
            print(f"Warning: Could not add static visualizations: {e}")

    print(f"✓ Saved: {pdf_path}")

# ============================================================================
# REPORT 2: FACT SHEET
# ============================================================================

def generate_fact_sheet(metrics_10yr, metrics_5yr):
    """Generate one-page fact sheet."""
    print("Generating IWRC_Fact_Sheet.pdf...")

    pdf_path = OUTPUT_DIR / 'IWRC_Fact_Sheet.pdf'

    fig = plt.figure(figsize=(8.5, 11))
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Header with IWRC primary teal color
    ax.add_patch(plt.Rectangle((0, 0.92), 1, 0.08, facecolor=COLORS['primary'], transform=ax.transAxes))
    ax.text(0.5, 0.96, 'IWRC SEED FUND FACT SHEET', ha='center', fontsize=16, fontweight='bold',
           color='white', transform=ax.transAxes)

    # Main content
    fact_text = f"""
ABOUT THE IWRC SEED FUND PROGRAM

The Illinois Water Resources Research Center (IWRC) Seed Fund Program provides competitive grants
to support innovative water resources research at Illinois institutions. This one-time seed funding
has enabled researchers to develop preliminary data that supports larger federal grant proposals.

KEY FINDINGS (2015-2024)

Total Investment
${metrics_10yr['investment']:,.0f}  invested in {metrics_10yr['projects']} unique projects

Student Training
{int(metrics_10yr['students']['total'])} students trained across all degree levels
  • {int(metrics_10yr['students']['phd'])} PhD students
  • {int(metrics_10yr['students']['ms'])} Master's students
  • {int(metrics_10yr['students']['undergrad'])} Undergraduate students
  • {int(metrics_10yr['students']['postdoc'])} Post-Doctoral researchers

Institutional Reach
{metrics_10yr['institutions']} Illinois institutions served by the program

Research Distribution
Programs span diverse water resources research topics including water quality, water treatment,
groundwater, flooding, and environmental remediation.

FIVE-YEAR COMPARISON (2020-2024)

Recent Focus (2020-2024)
${metrics_5yr['investment']:,.0f}  invested in {metrics_5yr['projects']} projects
{int(metrics_5yr['students']['total'])} students trained

Investment Per Project
10-Year Average: ${metrics_10yr['investment']/metrics_10yr['projects']:,.0f} per project
5-Year Average:  ${metrics_5yr['investment']/metrics_5yr['projects']:,.0f} per project

PROGRAM IMPACT

    -  Provides preliminary data for larger federal grant proposals
    -  Supports graduate and undergraduate education
    -  Addresses critical water resources challenges in Illinois
    -  Promotes collaboration across multiple institutions
    -  Builds research capacity in underrepresented areas

Data corrected November 24, 2025 - Represents unique projects in the program
    """

    # Background rectangle
    rect = plt.Rectangle((0.05, 0.05), 0.9, 0.85,
                        facecolor=COLORS['light_blue'],
                        edgecolor="none",
                        transform=ax.transAxes,
                        zorder=0)
    ax.add_patch(rect)

    ax.text(0.5, 0.89, fact_text, ha='center', va='top', fontsize=9, transform=ax.transAxes, zorder=10)

    ax.text(0.5, 0.01, f"Generated: {datetime.now().strftime('%B %d, %Y')}",
           ha='center', fontsize=7, style='italic', color='gray', transform=ax.transAxes)

    with PdfPages(pdf_path) as pdf:
        pdf.savefig(fig, bbox_inches='tight')

    plt.close(fig)
    print(f"✓ Saved: {pdf_path}")

# ============================================================================
# REPORT 3: FINANCIAL SUMMARY
# ============================================================================

def generate_financial_summary(metrics_10yr, metrics_5yr):
    """Generate financial summary report."""
    print("Generating IWRC_Financial_Summary.pdf...")

    pdf_path = OUTPUT_DIR / 'IWRC_Financial_Summary.pdf'

    with PdfPages(pdf_path) as pdf:
        # Page 1: Financial Overview
        fig = plt.figure(figsize=(8.5, 11))
        fig.suptitle('IWRC SEED FUND FINANCIAL SUMMARY', fontsize=16, fontweight='bold', y=0.97)

        gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3, top=0.94, bottom=0.08)

        # Investment comparison
        ax1 = fig.add_subplot(gs[0, :])
        periods = ['10-Year\n(2015-2024)', '5-Year\n(2020-2024)']
        investments = [metrics_10yr['investment'], metrics_5yr['investment']]
        bars = ax1.bar(periods, investments, color=[COLORS['primary'], COLORS['secondary']], width=0.5)
        for bar, value in zip(bars, investments):
            ax1.text(bar.get_x() + bar.get_width()/2, value, f'${value:,.0f}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Total Investment ($)', fontsize=11, fontweight='bold')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.grid(axis='y', alpha=0.3)
        ax1.set_ylim(0, max(investments) * 1.2)

        # Cost per project
        ax2 = fig.add_subplot(gs[1, 0])
        avg_per_project = [
            metrics_10yr['investment'] / metrics_10yr['projects'],
            metrics_5yr['investment'] / metrics_5yr['projects']
        ]
        bars = ax2.bar(periods, avg_per_project, color=[COLORS['primary'], COLORS['secondary']], width=0.5)
        for bar, value in zip(bars, avg_per_project):
            ax2.text(bar.get_x() + bar.get_width()/2, value, f'${value:,.0f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Cost per Project ($)', fontsize=10, fontweight='bold')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.grid(axis='y', alpha=0.3)

        # Cost per student
        ax3 = fig.add_subplot(gs[1, 1])
        cost_per_student = [
            metrics_10yr['investment'] / metrics_10yr['students']['total'],
            metrics_5yr['investment'] / metrics_5yr['students']['total']
        ]
        bars = ax3.bar(periods, cost_per_student, color=[COLORS['primary'], COLORS['secondary']], width=0.5)
        for bar, value in zip(bars, cost_per_student):
            ax3.text(bar.get_x() + bar.get_width()/2, value, f'${value:,.0f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        ax3.set_ylabel('Cost per Student Trained ($)', fontsize=10, fontweight='bold')
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.grid(axis='y', alpha=0.3)

        # Financial metrics table
        ax4 = fig.add_subplot(gs[2, :])
        ax4.axis('off')

        financial_data = [
            ['Financial Metric', '10-Year (2015-2024)', '5-Year (2020-2024)'],
            ['Total Investment', f'${metrics_10yr["investment"]:,.0f}', f'${metrics_5yr["investment"]:,.0f}'],
            ['Number of Projects', f'{metrics_10yr["projects"]}', f'{metrics_5yr["projects"]}'],
            ['Avg Cost per Project', f'${metrics_10yr["investment"]/metrics_10yr["projects"]:,.0f}',
             f'${metrics_5yr["investment"]/metrics_5yr["projects"]:,.0f}'],
            ['Number of Students', f'{int(metrics_10yr["students"]["total"])}',
             f'{int(metrics_5yr["students"]["total"])}'],
            ['Cost per Student', f'${metrics_10yr["investment"]/metrics_10yr["students"]["total"]:,.0f}',
             f'${metrics_5yr["investment"]/metrics_5yr["students"]["total"]:,.0f}'],
            ['Institutions Served', f'{metrics_10yr["institutions"]}', f'{metrics_5yr["institutions"]}'],
            ['Avg per Institution', f'${metrics_10yr["investment"]/metrics_10yr["institutions"]:,.0f}',
             f'${metrics_5yr["investment"]/metrics_5yr["institutions"]:,.0f}']
        ]

        table = ax4.table(cellText=financial_data, cellLoc='center', loc='center',
                         colWidths=[0.35, 0.325, 0.325])
        table.auto_set_font_size(False)
        table.set_fontsize(8.5)
        table.scale(1, 2.2)

        # Style header
        for i in range(3):
            table[(0, i)].set_facecolor(COLORS['dark_blue'])
            table[(0, i)].set_text_props(weight='bold', color='white')

        # Alternate row colors with IWRC neutral light
        for i in range(1, len(financial_data)):
            for j in range(3):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor(IWRC_COLORS['neutral_light'])

        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

    print(f"✓ Saved: {pdf_path}")

# ============================================================================
# REPORT 4: EXECUTIVE SUMMARY
# ============================================================================

def generate_executive_summary(metrics_10yr, metrics_5yr):
    """Generate executive summary report."""
    print("Generating IWRC_Seed_Fund_Executive_Summary.pdf...")

    pdf_path = OUTPUT_DIR / 'IWRC_Seed_Fund_Executive_Summary.pdf'

    fig = plt.figure(figsize=(8.5, 11))
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Header with IWRC primary teal color
    ax.add_patch(plt.Rectangle((0, 0.88), 1, 0.12, facecolor=COLORS['primary'], transform=ax.transAxes))
    ax.text(0.5, 0.95, 'EXECUTIVE SUMMARY', ha='center', fontsize=18, fontweight='bold',
           color='white', transform=ax.transAxes)
    ax.text(0.5, 0.90, 'IWRC Seed Fund Program 2015-2024', ha='center', fontsize=12,
           color='white', style='italic', transform=ax.transAxes)

    # Program Overview
    overview_text = "PROGRAM OVERVIEW\n\nThe Illinois Water Resources Research Center (IWRC) administers a competitive seed funding program\ndesigned to support innovative water resources research projects at Illinois institutions. Over a ten-\nyear period (2015-2024), the program has made significant investments in research and education."
    
    # Background rectangle for overview
    rect = plt.Rectangle((0.05, 0.78), 0.9, 0.08,
                        facecolor=COLORS['light_blue'],
                        edgecolor="none",
                        transform=ax.transAxes)
    ax.add_patch(rect)

    ax.text(0.5, 0.85, overview_text, ha='center', va='top', fontsize=9, transform=ax.transAxes)

    # Key Performance Indicators Title
    ax.text(0.5, 0.65, 'KEY PERFORMANCE INDICATORS', ha='center', fontsize=12, fontweight='bold',
           transform=ax.transAxes, color=COLORS['dark_blue'])

    # Helper for aligned stats
    def add_kpi_section(y_pos, title, data):
        ax.text(0.2, y_pos, title, ha='left', va='bottom', fontsize=10, fontweight='bold',
               transform=ax.transAxes, color=COLORS['dark_blue'])
        
        current_y = y_pos - 0.025
        for label, value in data:
            ax.text(0.6, current_y, label, ha='right', va='top', fontsize=10, transform=ax.transAxes)
            ax.text(0.65, current_y, value, ha='left', va='top', fontsize=10, transform=ax.transAxes)
            current_y -= 0.02
        return current_y - 0.015

    # Financial Performance
    fin_data = [
        ('Total Program Investment:', f"${metrics_10yr['investment']:,.0f}"),
        ('Average Cost per Project:', f"${metrics_10yr['investment']/metrics_10yr['projects']:,.0f}"),
        ('Average Cost per Student Trained:', f"${metrics_10yr['investment']/metrics_10yr['students']['total']:,.0f}")
    ]
    next_y = add_kpi_section(0.60, 'Financial Performance:', fin_data)

    # Research Scope
    scope_data = [
        ('Number of Projects Funded:', f"{metrics_10yr['projects']}"),
        ('Number of Institutions Served:', f"{metrics_10yr['institutions']}")
    ]
    next_y = add_kpi_section(next_y, 'Research Scope:', scope_data)

    # Education Impact
    edu_data = [
        ('Total Students Trained:', f"{int(metrics_10yr['students']['total'])}")
    ]
    next_y = add_kpi_section(next_y, 'Education Impact:', edu_data)

    # Degree Level Distribution
    degree_data = [
        ('PhD Students:', f"{int(metrics_10yr['students']['phd'])}"),
        ("Master's Students:", f"{int(metrics_10yr['students']['ms'])}"),
        ('Undergraduate Students:', f"{int(metrics_10yr['students']['undergrad'])}"),
        ('Post-Doctoral Researchers:', f"{int(metrics_10yr['students']['postdoc'])}")
    ]
    
    ax.text(0.25, next_y, 'Degree Level Distribution:', ha='left', va='bottom', fontsize=9, style='italic',
           transform=ax.transAxes)
    next_y -= 0.02
    for label, value in degree_data:
        ax.text(0.6, next_y, f"- {label}", ha='right', va='top', fontsize=9, transform=ax.transAxes)
        ax.text(0.65, next_y, value, ha='left', va='top', fontsize=9, transform=ax.transAxes)
        next_y -= 0.02

    # Recent Performance
    ax.text(0.5, next_y - 0.02, 'RECENT PERFORMANCE (2020-2024)', ha='center', fontsize=11, fontweight='bold',
           transform=ax.transAxes, color=COLORS['dark_blue'])
    
    ax.text(0.5, next_y - 0.05, 'The five-year period from 2020-2024 demonstrates continued program activity:',
           ha='center', fontsize=9, transform=ax.transAxes)
    
    recent_data = [
        ('Investment Level:', f"${metrics_5yr['investment']:,.0f}"),
        ('Projects Funded:', f"{metrics_5yr['projects']}"),
        ('Students Trained:', f"{int(metrics_5yr['students']['total'])}")
    ]
    
    current_y = next_y - 0.08
    for label, value in recent_data:
        ax.text(0.48, current_y, label, ha='right', va='top', fontsize=10, transform=ax.transAxes)
        ax.text(0.52, current_y, value, ha='left', va='top', fontsize=10, transform=ax.transAxes)
        current_y -= 0.02

    # Conclusions
    ax.text(0.5, current_y - 0.03, 'CONCLUSIONS', ha='center', fontsize=11, fontweight='bold',
           transform=ax.transAxes, color=COLORS['dark_blue'])
    
    conclusions = [
        "Provides seed funding for innovative research projects",
        "Supports graduate and undergraduate student training",
        "Reaches all regions of Illinois through diverse institutions",
        "Enables development of preliminary data for larger federal grants",
        "Advances understanding of critical water resources issues"
    ]
    
    current_y -= 0.06
    for item in conclusions:
        ax.text(0.2, current_y, f"- {item}", ha='left', va='top', fontsize=9, transform=ax.transAxes)
        current_y -= 0.02

    ax.text(0.5, current_y - 0.02, "Data Source: Corrected analysis as of November 24, 2025",
           ha='center', fontsize=8, style='italic', transform=ax.transAxes)

    ax.text(0.5, 0.01, f"Report Generated: {datetime.now().strftime('%B %d, %Y')}",
           ha='center', fontsize=7, style='italic', color='gray', transform=ax.transAxes)

    with PdfPages(pdf_path) as pdf:
        pdf.savefig(fig, bbox_inches='tight')

    plt.close(fig)
    print(f"✓ Saved: {pdf_path}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print("GENERATING DETAILED REPORTS WITH CORRECTED DATA")
    print("="*70)

    # Load data
    df, df_10yr, df_5yr = load_and_prepare_data()

    # Calculate metrics
    print("\nCalculating metrics...")
    metrics_10yr = calculate_metrics(df_10yr)
    metrics_5yr = calculate_metrics(df_5yr)

    print(f"\n10-Year Metrics:")
    print(f"  Investment: ${metrics_10yr['investment']:,.0f}")
    print(f"  Projects: {metrics_10yr['projects']}")
    print(f"  Students: {int(metrics_10yr['students']['total'])}")

    print(f"\n5-Year Metrics:")
    print(f"  Investment: ${metrics_5yr['investment']:,.0f}")
    print(f"  Projects: {metrics_5yr['projects']}")
    print(f"  Students: {int(metrics_5yr['students']['total'])}")

    # Generate reports
    print("\n" + "="*70)
    print("GENERATING REPORTS")
    print("="*70)

    generate_detailed_analysis_report(df_10yr, df_5yr, metrics_10yr, metrics_5yr)
    generate_fact_sheet(metrics_10yr, metrics_5yr)
    generate_financial_summary(metrics_10yr, metrics_5yr)
    generate_executive_summary(metrics_10yr, metrics_5yr)

    print("\n" + "="*70)
    print("✓ ALL REPORTS GENERATED SUCCESSFULLY")
    print("="*70)
    print(f"\nOutput Directory: {OUTPUT_DIR}")
    print("\nGenerated Files:")
    print(f"  1. IWRC_Detailed_Analysis_Report.pdf")
    print(f"  2. IWRC_Fact_Sheet.pdf")
    print(f"  3. IWRC_Financial_Summary.pdf")
    print(f"  4. IWRC_Seed_Fund_Executive_Summary.pdf")
    print("\nAll reports contain corrected data (November 24, 2025)")
    print("="*70)
