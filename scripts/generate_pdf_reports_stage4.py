#!/usr/bin/env python3
"""
IWRC Seed Fund Tracking - PDF Report Generation (Stage 4)

Generate 6 strategic PDF reports using ReportLab:
- 3 report types (Executive Summary, Fact Sheet, Financial Summary)
- 2 track versions each (All Projects, 104B Only)

Uses text-based PDFs with formatted tables and metrics.
"""

import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
import sys
import re
from datetime import datetime

# Setup
sys.path.insert(0, '/Users/shivpat/Downloads/Seed Fund Tracking/scripts')

PROJECT_ROOT = '/Users/shivpat/Downloads/Seed Fund Tracking'
DATA_FILE = os.path.join(PROJECT_ROOT, 'data/consolidated/IWRC Seed Fund Tracking.xlsx')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'FINAL_DELIVERABLES 2/reports')

# IWRC Colors for PDF
IWRC_COLORS = {
    'primary': '#258372',           # Teal
    'secondary': '#639757',         # Olive
    'text': '#54595F',              # Dark gray
    'accent': '#FCC080',            # Peach
    'background': '#F6F6F6',        # Light gray
    'dark_teal': '#1a5f52',         # Dark teal
}

print(f"\n{'█' * 80}")
print(f"█ STAGE 4: PDF REPORTS WITH FORMATTED TABLES".center(80) + "█")
print(f"{'█' * 80}\n")


def load_and_prepare_data():
    """Load and prepare data for PDF generation."""
    print("=" * 80)
    print("LOADING DATA FOR PDF GENERATION")
    print("=" * 80)

    df = pd.read_excel(DATA_FILE, sheet_name='Project Overview')

    # Column mapping
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
    }
    df = df.rename(columns=col_map)

    # Convert to numeric
    for col in ['phd_students', 'ms_students', 'undergrad_students', 'postdoc_students']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df['award_amount'] = pd.to_numeric(df['award_amount'], errors='coerce').fillna(0)

    # Extract year
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

    # Time periods
    df_10yr = df[df['project_year'].between(2015, 2024, inclusive='both')]

    # Tracks
    all_10yr = df_10yr
    b104_10yr = df_10yr[df_10yr['award_type'] == 'Base Grant (104b)']

    print(f"✓ Data loaded")
    print(f"  All Projects: {all_10yr['project_id'].nunique()} projects")
    print(f"  104B Only:    {b104_10yr['project_id'].nunique()} projects\n")

    return all_10yr, b104_10yr


def calculate_metrics(df, label):
    """Calculate key metrics for a dataset."""
    total_students = (df['phd_students'].sum() + df['ms_students'].sum() +
                     df['undergrad_students'].sum() + df['postdoc_students'].sum())

    return {
        'Track': label,
        'Total Investment': df['award_amount'].sum(),
        'Number of Projects': df['project_id'].nunique(),
        'Total Students': total_students,
        'Avg per Project': df['award_amount'].sum() / df['project_id'].nunique(),
        'Avg Students per Project': total_students / df['project_id'].nunique() if df['project_id'].nunique() > 0 else 0,
        'Cost per Student': df['award_amount'].sum() / total_students if total_students > 0 else 0,
        'Projects per $1M': (df['project_id'].nunique() / df['award_amount'].sum()) * 1_000_000,
        'Students per $1M': (total_students / df['award_amount'].sum()) * 1_000_000,
        'PhD': df['phd_students'].sum(),
        'Masters': df['ms_students'].sum(),
        'Undergrad': df['undergrad_students'].sum(),
        'Postdoc': df['postdoc_students'].sum(),
    }


def format_currency(value):
    """Format value as currency string."""
    if isinstance(value, (int, float)):
        return f"${value:,.0f}" if value >= 1 else f"${value:.2f}"
    return str(value)


def format_number(value):
    """Format value as number with commas."""
    if isinstance(value, (int, float)):
        return f"{value:,.0f}" if value >= 1 else f"{value:.2f}"
    return str(value)


def create_executive_summary(all_metrics, b104_metrics):
    """Create Executive Summary PDF reports."""
    print("  Creating: Executive Summary PDFs")

    # All Projects version
    doc = SimpleDocTemplate(
        os.path.join(OUTPUT_DIR, 'IWRC_Executive_Summary_All_Projects.pdf'),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor(IWRC_COLORS['dark_teal']),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor(IWRC_COLORS['primary']),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=colors.HexColor(IWRC_COLORS['text']),
        spaceAfter=10,
        alignment=TA_LEFT
    )

    story = []

    # Title
    story.append(Paragraph("IWRC Seed Fund Tracking", title_style))
    story.append(Paragraph("Executive Summary - All Projects (2015-2024)", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))

    # Summary text
    summary_text = f"""
    The Illinois Wheat and Rice Center (IWRC) Seed Fund Program has supported research
    and education across multiple funding mechanisms, including Base Grants (104B) and
    strategic awards (104G-AIS, 104G-PFAS, and Coordination projects).
    """
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 0.2*inch))

    # Key metrics table
    story.append(Paragraph("Key Performance Metrics (2015-2024)", heading_style))

    metrics_data = [
        ['Metric', 'Value'],
        ['Total Investment', format_currency(all_metrics['Total Investment'])],
        ['Number of Projects', format_number(all_metrics['Number of Projects'])],
        ['Students Trained', format_number(all_metrics['Total Students'])],
        ['Average per Project', format_currency(all_metrics['Avg per Project'])],
        ['Average Students per Project', format_number(all_metrics['Avg Students per Project'])],
        ['Cost per Student', format_currency(all_metrics['Cost per Student'])],
    ]

    metrics_table = Table(metrics_data, colWidths=[3.5*inch, 2*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(IWRC_COLORS['primary'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(IWRC_COLORS['background'])),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(IWRC_COLORS['background'])]),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 0.3*inch))

    # Students by degree
    story.append(Paragraph("Students Trained by Degree Level", heading_style))
    students_data = [
        ['Degree Level', 'Count'],
        ['PhD', format_number(all_metrics['PhD'])],
        ['Masters', format_number(all_metrics['Masters'])],
        ['Undergraduate', format_number(all_metrics['Undergrad'])],
        ['Postdoc', format_number(all_metrics['Postdoc'])],
    ]

    students_table = Table(students_data, colWidths=[3.5*inch, 2*inch])
    students_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(IWRC_COLORS['primary'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(IWRC_COLORS['background'])),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(IWRC_COLORS['background'])]),
    ]))
    story.append(students_table)
    story.append(Spacer(1, 0.3*inch))

    # Efficiency metrics
    story.append(Paragraph("Efficiency Metrics (per $1M Invested)", heading_style))
    efficiency_data = [
        ['Metric', 'Value'],
        ['Projects per $1M', format_number(all_metrics['Projects per $1M'])],
        ['Students per $1M', format_number(all_metrics['Students per $1M'])],
    ]

    efficiency_table = Table(efficiency_data, colWidths=[3.5*inch, 2*inch])
    efficiency_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(IWRC_COLORS['primary'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(IWRC_COLORS['background'])),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(IWRC_COLORS['background'])]),
    ]))
    story.append(efficiency_table)
    story.append(Spacer(1, 0.2*inch))

    # Footer
    footer_text = f"<i>Report Generated: {datetime.now().strftime('%B %d, %Y')}</i>"
    story.append(Paragraph(footer_text, styles['Normal']))

    doc.build(story)
    print(f"    ✓ Generated: IWRC_Executive_Summary_All_Projects.pdf")

    # 104B Only version
    doc = SimpleDocTemplate(
        os.path.join(OUTPUT_DIR, 'IWRC_Executive_Summary_104B_Only.pdf'),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    story = []
    story.append(Paragraph("IWRC Seed Fund Tracking", title_style))
    story.append(Paragraph("Executive Summary - 104B Only / Base Grants (2015-2024)", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))

    summary_text_104b = f"""
    The Base Grant (104B) program represents the foundational seed funding mechanism
    of the Illinois Wheat and Rice Center, supporting numerous research and educational
    initiatives across Illinois institutions.
    """
    story.append(Paragraph(summary_text_104b, body_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Key Performance Metrics (2015-2024)", heading_style))
    metrics_data_104b = [
        ['Metric', 'Value'],
        ['Total Investment', format_currency(b104_metrics['Total Investment'])],
        ['Number of Projects', format_number(b104_metrics['Number of Projects'])],
        ['Students Trained', format_number(b104_metrics['Total Students'])],
        ['Average per Project', format_currency(b104_metrics['Avg per Project'])],
        ['Average Students per Project', format_number(b104_metrics['Avg Students per Project'])],
        ['Cost per Student', format_currency(b104_metrics['Cost per Student'])],
    ]

    metrics_table_104b = Table(metrics_data_104b, colWidths=[3.5*inch, 2*inch])
    metrics_table_104b.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(IWRC_COLORS['secondary'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(IWRC_COLORS['background'])),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(IWRC_COLORS['background'])]),
    ]))
    story.append(metrics_table_104b)
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("Students Trained by Degree Level", heading_style))
    students_data_104b = [
        ['Degree Level', 'Count'],
        ['PhD', format_number(b104_metrics['PhD'])],
        ['Masters', format_number(b104_metrics['Masters'])],
        ['Undergraduate', format_number(b104_metrics['Undergrad'])],
        ['Postdoc', format_number(b104_metrics['Postdoc'])],
    ]

    students_table_104b = Table(students_data_104b, colWidths=[3.5*inch, 2*inch])
    students_table_104b.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(IWRC_COLORS['secondary'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(IWRC_COLORS['background'])),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(IWRC_COLORS['background'])]),
    ]))
    story.append(students_table_104b)
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("Efficiency Metrics (per $1M Invested)", heading_style))
    efficiency_data_104b = [
        ['Metric', 'Value'],
        ['Projects per $1M', format_number(b104_metrics['Projects per $1M'])],
        ['Students per $1M', format_number(b104_metrics['Students per $1M'])],
    ]

    efficiency_table_104b = Table(efficiency_data_104b, colWidths=[3.5*inch, 2*inch])
    efficiency_table_104b.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(IWRC_COLORS['secondary'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(IWRC_COLORS['background'])),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(IWRC_COLORS['background'])]),
    ]))
    story.append(efficiency_table_104b)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph(footer_text, styles['Normal']))

    doc.build(story)
    print(f"    ✓ Generated: IWRC_Executive_Summary_104B_Only.pdf")


def create_fact_sheets(all_metrics, b104_metrics):
    """Create Fact Sheet PDF reports."""
    print("  Creating: Fact Sheet PDFs")

    # All Projects version
    doc = SimpleDocTemplate(
        os.path.join(OUTPUT_DIR, 'IWRC_Fact_Sheet_All_Projects.pdf'),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor(IWRC_COLORS['dark_teal']),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor(IWRC_COLORS['primary']),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.HexColor(IWRC_COLORS['text']),
        spaceAfter=8
    )

    story = []

    story.append(Paragraph("IWRC Seed Fund Program", title_style))
    story.append(Paragraph("Fact Sheet - All Projects (2015-2024)", heading_style))
    story.append(Spacer(1, 0.15*inch))

    # Quick facts
    story.append(Paragraph("<b>Quick Facts</b>", heading_style))
    facts = [
        [f"Total Projects: {format_number(all_metrics['Number of Projects'])}"],
        [f"Total Investment: {format_currency(all_metrics['Total Investment'])}"],
        [f"Students Trained: {format_number(all_metrics['Total Students'])}"],
        [f"Average Award per Project: {format_currency(all_metrics['Avg per Project'])}"],
    ]

    facts_table = Table(facts, colWidths=[5.5*inch])
    facts_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(IWRC_COLORS['background'])),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor(IWRC_COLORS['text'])),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
    ]))
    story.append(facts_table)
    story.append(Spacer(1, 0.2*inch))

    # Highlights
    story.append(Paragraph("<b>Program Highlights</b>", heading_style))
    highlights = [
        f"• Supported {format_number(all_metrics['Number of Projects'])} research and educational projects",
        f"• Trained {format_number(all_metrics['Total Students'])} students across multiple degree levels",
        f"• Invested {format_currency(all_metrics['Total Investment'])} in agricultural research",
        f"• Produced {all_metrics['Projects per $1M']:.1f} projects per $1 million invested",
    ]

    for highlight in highlights:
        story.append(Paragraph(highlight, body_style))

    story.append(Spacer(1, 0.2*inch))

    # Contact information
    story.append(Paragraph("<b>For More Information</b>", heading_style))
    contact_text = "Illinois Wheat and Rice Center (IWRC)<br/>For detailed analysis and visualizations, see the interactive dashboards and comprehensive reports."
    story.append(Paragraph(contact_text, body_style))

    story.append(Spacer(1, 0.2*inch))
    footer_text = f"<i>Report Generated: {datetime.now().strftime('%B %d, %Y')}</i>"
    story.append(Paragraph(footer_text, styles['Normal']))

    doc.build(story)
    print(f"    ✓ Generated: IWRC_Fact_Sheet_All_Projects.pdf")

    # 104B Only version
    doc = SimpleDocTemplate(
        os.path.join(OUTPUT_DIR, 'IWRC_Fact_Sheet_104B_Only.pdf'),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    story = []

    story.append(Paragraph("IWRC Base Grant (104B) Program", title_style))
    story.append(Paragraph("Fact Sheet (2015-2024)", heading_style))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("<b>Quick Facts</b>", heading_style))
    facts_104b = [
        [f"Total Projects: {format_number(b104_metrics['Number of Projects'])}"],
        [f"Total Investment: {format_currency(b104_metrics['Total Investment'])}"],
        [f"Students Trained: {format_number(b104_metrics['Total Students'])}"],
        [f"Average Award per Project: {format_currency(b104_metrics['Avg per Project'])}"],
    ]

    facts_table_104b = Table(facts_104b, colWidths=[5.5*inch])
    facts_table_104b.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(IWRC_COLORS['background'])),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor(IWRC_COLORS['text'])),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
    ]))
    story.append(facts_table_104b)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>Program Highlights</b>", heading_style))
    highlights_104b = [
        f"• Supported {format_number(b104_metrics['Number of Projects'])} seed funding projects",
        f"• Trained {format_number(b104_metrics['Total Students'])} students across multiple degree levels",
        f"• Invested {format_currency(b104_metrics['Total Investment'])} in foundational research",
        f"• Produced {b104_metrics['Projects per $1M']:.1f} projects per $1 million invested",
        f"• {(b104_metrics['Projects per $1M']/all_metrics['Projects per $1M']):.1f}x more efficient at creating projects than strategic awards",
    ]

    for highlight in highlights_104b:
        story.append(Paragraph(highlight, body_style))

    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>For More Information</b>", heading_style))
    story.append(Paragraph(contact_text, body_style))

    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(footer_text, styles['Normal']))

    doc.build(story)
    print(f"    ✓ Generated: IWRC_Fact_Sheet_104B_Only.pdf")


def create_financial_summaries(all_metrics, b104_metrics):
    """Create Financial Summary PDF reports."""
    print("  Creating: Financial Summary PDFs")

    # All Projects version
    doc = SimpleDocTemplate(
        os.path.join(OUTPUT_DIR, 'IWRC_Financial_Summary_All_Projects.pdf'),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor(IWRC_COLORS['dark_teal']),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor(IWRC_COLORS['primary']),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.HexColor(IWRC_COLORS['text']),
        spaceAfter=8
    )

    story = []

    story.append(Paragraph("IWRC Seed Fund Program", title_style))
    story.append(Paragraph("Financial Summary & ROI Analysis - All Projects (2015-2024)", heading_style))
    story.append(Spacer(1, 0.15*inch))

    # Financial overview
    story.append(Paragraph("<b>Financial Overview</b>", heading_style))
    financial_data = [
        ['Metric', 'Amount'],
        ['Total Investment', format_currency(all_metrics['Total Investment'])],
        ['Cost per Project', format_currency(all_metrics['Avg per Project'])],
        ['Cost per Student', format_currency(all_metrics['Cost per Student'])],
    ]

    financial_table = Table(financial_data, colWidths=[3.5*inch, 2*inch])
    financial_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(IWRC_COLORS['primary'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(IWRC_COLORS['background'])),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(IWRC_COLORS['background'])]),
    ]))
    story.append(financial_table)
    story.append(Spacer(1, 0.2*inch))

    # ROI metrics
    story.append(Paragraph("<b>Return on Investment (ROI) Metrics</b>", heading_style))
    roi_text = f"""
    The IWRC Seed Fund program demonstrates strong returns on investment:
    <br/><br/>
    <b>Projects Generated:</b> {all_metrics['Projects per $1M']:.1f} projects per $1 million invested
    <br/>
    <b>Students Trained:</b> {all_metrics['Students per $1M']:.0f} students per $1 million invested
    <br/>
    <b>Education Efficiency:</b> Each $1,000 invested trains approximately {(all_metrics['Students per $1M']/1000):.2f} students
    """
    story.append(Paragraph(roi_text, body_style))
    story.append(Spacer(1, 0.2*inch))

    # Comparative analysis
    story.append(Paragraph("<b>Key Financial Insights</b>", heading_style))
    insights = [
        f"• Average project size: {format_currency(all_metrics['Avg per Project'])}",
        f"• Average students per project: {format_number(all_metrics['Avg Students per Project'])}",
        f"• Total students trained: {format_number(all_metrics['Total Students'])}",
        f"• Total projects supported: {format_number(all_metrics['Number of Projects'])}",
    ]

    for insight in insights:
        story.append(Paragraph(insight, body_style))

    story.append(Spacer(1, 0.2*inch))
    footer_text = f"<i>Report Generated: {datetime.now().strftime('%B %d, %Y')}</i>"
    story.append(Paragraph(footer_text, styles['Normal']))

    doc.build(story)
    print(f"    ✓ Generated: IWRC_Financial_Summary_All_Projects.pdf")

    # 104B Only version
    doc = SimpleDocTemplate(
        os.path.join(OUTPUT_DIR, 'IWRC_Financial_Summary_104B_Only.pdf'),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    story = []

    story.append(Paragraph("IWRC Base Grant (104B) Program", title_style))
    story.append(Paragraph("Financial Summary & ROI Analysis (2015-2024)", heading_style))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("<b>Financial Overview</b>", heading_style))
    financial_data_104b = [
        ['Metric', 'Amount'],
        ['Total Investment', format_currency(b104_metrics['Total Investment'])],
        ['Cost per Project', format_currency(b104_metrics['Avg per Project'])],
        ['Cost per Student', format_currency(b104_metrics['Cost per Student'])],
    ]

    financial_table_104b = Table(financial_data_104b, colWidths=[3.5*inch, 2*inch])
    financial_table_104b.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(IWRC_COLORS['secondary'])),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor(IWRC_COLORS['background'])),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(IWRC_COLORS['background'])]),
    ]))
    story.append(financial_table_104b)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>Return on Investment (ROI) Metrics</b>", heading_style))
    roi_text_104b = f"""
    The 104B Base Grant program demonstrates exceptional efficiency:
    <br/><br/>
    <b>Projects Generated:</b> {b104_metrics['Projects per $1M']:.1f} projects per $1 million invested
    <br/>
    <b>Students Trained:</b> {b104_metrics['Students per $1M']:.0f} students per $1 million invested
    <br/>
    <b>Education Efficiency:</b> Each $1,000 invested trains approximately {(b104_metrics['Students per $1M']/1000):.2f} students
    <br/>
    <b>Comparative Advantage:</b> {(b104_metrics['Projects per $1M']/all_metrics['Projects per $1M']):.1f}x more efficient than strategic awards
    """
    story.append(Paragraph(roi_text_104b, body_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>Key Financial Insights</b>", heading_style))
    insights_104b = [
        f"• Average project size: {format_currency(b104_metrics['Avg per Project'])}",
        f"• Average students per project: {format_number(b104_metrics['Avg Students per Project'])}",
        f"• Total students trained: {format_number(b104_metrics['Total Students'])}",
        f"• Total projects supported: {format_number(b104_metrics['Number of Projects'])}",
    ]

    for insight in insights_104b:
        story.append(Paragraph(insight, body_style))

    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(footer_text, styles['Normal']))

    doc.build(story)
    print(f"    ✓ Generated: IWRC_Financial_Summary_104B_Only.pdf")


def main():
    """Main orchestration."""
    all_10yr, b104_10yr = load_and_prepare_data()

    all_metrics = calculate_metrics(all_10yr, 'All Projects')
    b104_metrics = calculate_metrics(b104_10yr, '104B Only')

    print("\n" + "=" * 80)
    print("GENERATING PDF REPORTS")
    print("=" * 80 + "\n")

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate all 6 PDFs
    create_executive_summary(all_metrics, b104_metrics)
    create_fact_sheets(all_metrics, b104_metrics)
    create_financial_summaries(all_metrics, b104_metrics)

    print("\n" + "█" * 80)
    print("█" + " ✓ STAGE 4 COMPLETE: 6 PDF Reports Generated".center(78) + "█")
    print("█" * 80)
    print("\nGenerated Reports:")
    print("  • IWRC_Executive_Summary_All_Projects.pdf")
    print("  • IWRC_Executive_Summary_104B_Only.pdf")
    print("  • IWRC_Fact_Sheet_All_Projects.pdf")
    print("  • IWRC_Fact_Sheet_104B_Only.pdf")
    print("  • IWRC_Financial_Summary_All_Projects.pdf")
    print("  • IWRC_Financial_Summary_104B_Only.pdf\n")


if __name__ == '__main__':
    main()
