#!/usr/bin/env python3
"""
Convert HTML Plotly interactive map to PDF using Selenium/headless browser
Updated: November 24, 2025
"""

import subprocess
import sys
from pathlib import Path

def install_required_packages():
    """Install required packages if not present."""
    try:
        import selenium
    except ImportError:
        print("Installing selenium...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium", "-q"])

    try:
        import playwright
    except ImportError:
        print("Installing playwright...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])

def convert_html_to_pdf_with_playwright():
    """Convert HTML to PDF using Playwright."""
    print("Using Playwright to convert HTML to PDF...")

    from playwright.sync_api import sync_playwright

    html_file = Path('/Users/shivpat/seed-fund-tracking/visualizations/interactive/institutional_distribution_map.html')
    pdf_file = Path('/Users/shivpat/seed-fund-tracking/visualizations/pdfs/2025_illinois_institutions_map.pdf')

    if not html_file.exists():
        print(f"ERROR: HTML file not found: {html_file}")
        return False

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{html_file.absolute()}")
            page.wait_for_load_state("networkidle")
            page.pdf(path=str(pdf_file), format="A4", landscape=True)
            browser.close()

        print(f"✓ PDF saved: {pdf_file}")
        return True
    except Exception as e:
        print(f"Error with Playwright: {e}")
        return False

def convert_html_to_pdf_with_selenium():
    """Fallback: Convert HTML to PDF using Selenium."""
    print("Using Selenium to convert HTML to PDF...")

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        html_file = Path('/Users/shivpat/seed-fund-tracking/visualizations/interactive/institutional_distribution_map.html')
        pdf_file = Path('/Users/shivpat/seed-fund-tracking/visualizations/pdfs/2025_illinois_institutions_map.pdf')

        if not html_file.exists():
            print(f"ERROR: HTML file not found: {html_file}")
            return False

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(options=options)
        driver.get(f"file://{html_file.absolute()}")

        # Wait for page to load
        import time
        time.sleep(3)

        # Print to PDF
        print_settings = {
            'recentDestinations': [{
                'id': 'Save as PDF',
                'origin': 'local'
            }],
            'selectedDestinationId': 'Save as PDF',
            'version': 2
        }

        driver.execute_cdp_cmd('Page.printToPDF', {
            'path': str(pdf_file),
            'format': 'A4',
            'landscape': True
        })

        driver.quit()
        print(f"✓ PDF saved: {pdf_file}")
        return True
    except Exception as e:
        print(f"Error with Selenium: {e}")
        return False

def generate_simple_plotly_pdf():
    """Generate PDF using Plotly's native export capabilities."""
    print("Generating PDF using Plotly...")

    import pandas as pd
    import plotly.graph_objects as go
    from pathlib import Path

    # Load data
    data_file = Path('/Users/shivpat/seed-fund-tracking/data/consolidated/IWRC Seed Fund Tracking.xlsx')
    df = pd.read_excel(data_file, sheet_name='Project Overview')

    # Rename columns
    col_map = {
        'Academic Institution of PI': 'institution',
        'Award Amount Allocated ($) this must be filled in for all lines': 'award_amount'
    }
    df = df.rename(columns=col_map)

    # Prepare institution data
    institution_data = df.groupby('institution').agg({
        'award_amount': ['sum', 'count']
    }).reset_index()

    institution_data.columns = ['institution', 'total_funding', 'project_count']

    # Add coordinates
    coords_map = {
        'University of Illinois Urbana-Champaign': (40.1020, -88.2272),
        'University of Illinois at Urbana-Champaign': (40.1020, -88.2272),
        'Illinois Institute of Technology': (41.8348, -87.6266),
        'Southern Illinois University Carbondale': (37.7213, -89.2167),
        'Southern Illinois University at Carbondale': (37.7213, -89.2167),
        'Southern Illinois University': (37.7213, -89.2167),
        'Illinois State University': (40.5142, -88.9907),
        'Illinois State Water Survey': (40.1164, -88.2434),
        'University of Illinois Chicago': (41.8708, -87.6470),
        'University of Illinois at Chicago': (41.8708, -87.6470),
        'Northwestern University': (42.0565, -87.6753),
        'Illinois Sustainable Technology Center': (40.1164, -88.2434),
        'Lewis and Clark Community College': (38.9742, -90.1840),
        'National Great Rivers Research & Education Center': (38.8881, -90.1068),
        'Loyola University Chicago': (41.9989, -87.6576),
        'Eastern Illinois University': (39.4817, -88.2039),
        'Northern Illinois University': (41.9306, -88.7712),
        'Lewis University': (41.6070, -88.0892),
        'Basil\'s Harvest': (40.0, -89.0),
        'University of Illinois': (40.1020, -88.2272),
        'University of Texas at Austin': (30.2849, -97.7341),  # Out of state
        'Cary Institute of Ecosystem Studies': (41.7861, -73.7440),  # Out of state
    }

    institution_data['lat'] = institution_data['institution'].apply(lambda x: coords_map.get(x, (40.0, -89.0))[0])
    institution_data['lon'] = institution_data['institution'].apply(lambda x: coords_map.get(x, (40.0, -89.0))[1])

    # Filter to Illinois only
    institution_data = institution_data[(institution_data['lat'] >= 36.9) & (institution_data['lat'] <= 42.6)]

    # Create map figure
    fig = go.Figure()

    fig.add_trace(go.Scattergeo(
        lon=institution_data['lon'],
        lat=institution_data['lat'],
        mode='markers+text',
        marker=dict(
            size=institution_data['project_count'] * 5 + 15,
            color=institution_data['total_funding'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title='<b>Total Funding ($)</b>',
                thickness=20,
                len=0.7,
                tickformat='$,.0f'
            ),
            line=dict(width=3, color='darkblue'),
            opacity=0.85,
            sizemin=10
        ),
        text=[inst[:20] for inst in institution_data['institution']],
        textposition='top center',
        textfont=dict(size=9, color='black', family='Arial Black'),
        hovertemplate='<b>%{customdata[0]}</b><br>' +
                      'Projects: %{customdata[2]}<br>' +
                      'Total Funding: $%{customdata[3]:,.0f}<br>' +
                      '<extra></extra>',
        customdata=institution_data[['institution', 'institution', 'project_count', 'total_funding']].values,
        showlegend=False
    ))

    fig.update_geos(
        scope='usa',
        projection_type='albers usa',
        showland=True,
        landcolor='#f5f5f5',
        showlakes=True,
        lakecolor='#cfe2f3',
        showrivers=True,
        rivercolor='#6fa0d6',
        showcountries=True,
        countrycolor='#cccccc',
        showsubunits=True,
        subunitcolor='#e0e0e0',
        lonaxis_range=[-91.5, -87.0],
        lataxis_range=[36.9, 42.6],
        bgcolor='white'
    )

    fig.update_layout(
        title={
            'text': '2025 IWRC Seed Fund - Funded Institutions Across Illinois',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22, 'color': '#003d7a'}
        },
        font=dict(family='Arial', size=12),
        height=1100,
        width=1600,
        margin=dict(l=50, r=150, t=100, b=50),
        paper_bgcolor='white',
        plot_bgcolor='#f9f9f9'
    )

    # Try to save as PDF
    pdf_path = Path('/Users/shivpat/seed-fund-tracking/visualizations/pdfs/2025_illinois_institutions_map.pdf')

    try:
        # Try using kaleido (if available) with larger dimensions
        fig.write_image(str(pdf_path), width=1600, height=1100, scale=2)
        print(f"✓ PDF saved with kaleido: {pdf_path}")
        return True
    except Exception as e:
        print(f"Kaleido export failed: {e}")

        # Fallback: save as HTML and then convert
        try:
            html_path = pdf_path.with_suffix('.html')
            fig.write_html(str(html_path))
            print(f"✓ Saved interactive HTML: {html_path}")
            print("Please open in browser and print to PDF manually, or convert using:")
            print(f"  wkhtmltopdf {html_path} {pdf_path}")
            return False
        except Exception as e2:
            print(f"Error: {e2}")
            return False

if __name__ == '__main__':
    print("="*70)
    print("CONVERTING ILLINOIS MAP TO PDF")
    print("="*70)

    # Try different methods
    print("\nAttempting to generate PDF...\n")

    # Method 1: Try Plotly's native export
    success = generate_simple_plotly_pdf()

    if not success:
        print("\nNote: For better results, you can:")
        print("1. Open the HTML file in a web browser")
        print("2. Right-click and select 'Print'")
        print("3. Change destination to 'Save as PDF'")
        print("4. Click Save")

    print("\n" + "="*70)
