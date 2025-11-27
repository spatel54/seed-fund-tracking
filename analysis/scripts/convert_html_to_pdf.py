#!/usr/bin/env python3
"""
Convert HTML visualizations to PDF format using Playwright
Requires: pip install playwright && playwright install chromium
"""

import asyncio
import os
from pathlib import Path

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

async def convert_html_to_pdf_async():
    """Convert all HTML visualizations to PDF format using Playwright"""
    
    # Define paths
    base_dir = Path("/Users/shivpat/seed-fund-tracking")
    html_dir = base_dir / "visualizations" / "interactive"
    pdf_dir = base_dir / "visualizations" / "pdfs"
    
    # Create PDF directory if it doesn't exist
    pdf_dir.mkdir(parents=True, exist_ok=True)
    
    # HTML files to convert
    html_files = [
        "IWRC_ROI_Analysis_Report.html",
        "2025_keyword_pie_chart_interactive.html",
        "2025_illinois_institutions_map_interactive.html",
        "Seed_Fund_Tracking_Analysis.html"
    ]
    
    print("=" * 60)
    print("HTML to PDF Converter (Using Playwright)")
    print("=" * 60)
    print()
    
    converted = 0
    failed = 0
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        for html_file in html_files:
            html_path = html_dir / html_file
            pdf_file = html_file.replace('.html', '.pdf')
            pdf_path = pdf_dir / pdf_file
            
            if not html_path.exists():
                print(f"❌ {html_file} - File not found")
                failed += 1
                continue
            
            print(f"Converting: {html_file}")
            print(f"  → {pdf_path}")
            
            try:
                # Load the HTML file
                await page.goto(f"file://{html_path}", wait_until="networkidle")
                
                # Wait a bit for JavaScript to render
                await page.wait_for_timeout(2000)
                
                # Generate PDF
                await page.pdf(
                    path=str(pdf_path),
                    format='Letter',
                    landscape=True,
                    margin={
                        'top': '0.5in',
                        'right': '0.5in',
                        'bottom': '0.5in',
                        'left': '0.5in'
                    },
                    print_background=True
                )
                
                file_size = pdf_path.stat().st_size / (1024 * 1024)  # MB
                print(f"  ✅ Success! ({file_size:.2f} MB)")
                converted += 1
            except Exception as e:
                print(f"  ❌ Failed: {e}")
                failed += 1
            
            print()
        
        await browser.close()
    
    print("=" * 60)
    print(f"Conversion Complete!")
    print(f"  ✅ Successful: {converted}")
    print(f"  ❌ Failed: {failed}")
    print(f"\nPDFs saved to: {pdf_dir}")
    print("=" * 60)
    
    if converted > 0:
        print(f"\nTo view PDFs:")
        print(f"  open \"{pdf_dir}\"")

def convert_html_to_pdf():
    """Wrapper function to run async conversion"""
    if not PLAYWRIGHT_AVAILABLE:
        raise ImportError("playwright package not installed")
    asyncio.run(convert_html_to_pdf_async())

if __name__ == "__main__":
    try:
        convert_html_to_pdf()
    except ImportError:
        print("❌ Error: Playwright not installed")
        print()
        print("Please install Playwright:")
        print("  pip install playwright")
        print("  playwright install chromium")
        print()
        print("This will download a Chromium browser for PDF generation.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
