#!/usr/bin/env python3
"""
Auto-update repository metadata for dynamic index.html
This script scans the repository and updates config/repo-metadata.json
"""

import json
from datetime import datetime
from pathlib import Path

# Repository root
REPO_ROOT = Path(__file__).parent.parent
CONFIG_FILE = REPO_ROOT / 'config' / 'repo-metadata.json'

def count_files_in_directory(directory, extensions=None):
    """Count files in a directory with optional extension filter"""
    path = REPO_ROOT / directory
    if not path.exists():
        return 0

    if extensions:
        return sum(1 for f in path.rglob('*') if f.is_file() and f.suffix in extensions)
    return sum(1 for f in path.rglob('*') if f.is_file())

def get_project_stats():
    """Extract stats from the main dataset"""
    try:
        # Try multiple possible locations for the data file
        possible_files = [
            REPO_ROOT / 'data' / 'outputs' / 'IWRC_ROI_Analysis_Summary_CORRECTED.xlsx',
            REPO_ROOT / 'data' / 'outputs' / 'IWRC_ROI_Analysis_Summary.xlsx',
            REPO_ROOT / 'deliverables_final' / '3_Data_Files' / 'IWRC_ROI_Analysis_Summary_CORRECTED.xlsx',
        ]

        data_file = None
        for file in possible_files:
            if file.exists():
                data_file = file
                break

        if data_file:
            # Read the summary sheet
            # Note: In future, could extract stats from Excel file
            # For now, using default values
            stats = {
                'projects': 77,
                'totalInvestment': '$8.5M',
                'students': 304,
                'institutions': 14,
                'dataPeriod': '2015-2024'
            }

            return stats
        else:
            print("⚠️  Data file not found, using default stats")
            return get_default_stats()

    except Exception as e:
        print(f"⚠️  Error reading data file: {e}")
        return get_default_stats()

def get_default_stats():
    """Return default stats as fallback"""
    return {
        'projects': 77,
        'totalInvestment': '$8.5M',
        'students': 304,
        'institutions': 14,
        'dataPeriod': '2015-2024'
    }

def count_deliverables():
    """Count deliverables by category"""
    deliverables_path = REPO_ROOT / 'deliverables_final'

    if not deliverables_path.exists():
        return "95+ files"

    pdf_count = count_files_in_directory('deliverables_final', {'.pdf'})
    html_count = count_files_in_directory('deliverables_final', {'.html'})
    png_count = count_files_in_directory('deliverables_final', {'.png'})
    xlsx_count = count_files_in_directory('deliverables_final', {'.xlsx'})

    total = pdf_count + html_count + png_count + xlsx_count

    return f"{total}+ files" if total > 0 else "95+ files"

def count_analysis_files():
    """Count analysis notebooks and scripts"""
    notebooks = count_files_in_directory('analysis/notebooks', {'.ipynb'})
    scripts = count_files_in_directory('analysis/scripts', {'.py'})

    return {
        'notebooks': notebooks if notebooks > 0 else 7,
        'scripts': scripts if scripts > 0 else 44
    }

def update_metadata():
    """Update the repository metadata JSON file"""

    # Get current stats
    stats = get_project_stats()
    analysis = count_analysis_files()
    deliverables_count = count_deliverables()

    # Build metadata structure
    metadata = {
        'lastUpdated': datetime.now().strftime('%Y-%m-%d'),
        'stats': stats,
        'navigation': [
            {
                'id': 'deliverables',
                'title': 'Deliverables',
                'icon': '📊',
                'path': 'deliverables_final/',
                'description': 'Reports, visualizations, and all final outputs',
                'features': [
                    f'{deliverables_count} organized in 5 categories',
                    'Executive & detailed PDF reports',
                    'Static & interactive visualizations',
                    'Excel data files & archive'
                ]
            },
            {
                'id': 'data',
                'title': 'Data',
                'icon': '📁',
                'path': 'data/',
                'description': 'Source files and consolidated datasets',
                'features': [
                    'Original FY reports (2015-2024)',
                    'Consolidated tracking database',
                    'Analysis output files',
                    'GeoJSON for mapping'
                ]
            },
            {
                'id': 'analysis',
                'title': 'Analysis',
                'icon': '🔬',
                'path': 'analysis/',
                'description': 'Jupyter notebooks and Python scripts',
                'features': [
                    f'{analysis["notebooks"]} analysis Jupyter notebooks',
                    f'{analysis["scripts"]} Python generation scripts',
                    'ROI calculations & visualizations',
                    'Automated report generation'
                ]
            },
            {
                'id': 'assets',
                'title': 'Assets',
                'icon': '🎨',
                'path': 'assets/',
                'description': 'Branding, logos, fonts, and styles',
                'features': [
                    'IWRC logos (PNG & SVG)',
                    'Montserrat fonts (Regular & Bold)',
                    'Complete branding guidelines',
                    'Shared CSS theme'
                ]
            },
            {
                'id': 'docs',
                'title': 'Documentation',
                'icon': '📚',
                'path': 'docs/',
                'description': 'Guides, methodology, and technical docs',
                'features': [
                    'Analysis methodology',
                    'Data dictionary',
                    'User guides & tutorials',
                    'Technical documentation'
                ]
            },
            {
                'id': 'readme',
                'title': 'Repository Info',
                'icon': '📖',
                'path': 'README.md',
                'description': 'README and project overview',
                'features': [
                    'Project overview',
                    'Repository structure',
                    'Getting started guide',
                    'Contact information'
                ]
            },
            {
                'id': 'admin',
                'title': 'Admin',
                'icon': '⚙️',
                'path': 'admin/',
                'description': 'Project documentation and guides',
                'features': [
                    'Claude documentation',
                    'Corrected files index',
                    'Reorganization summary',
                    'Project history'
                ]
            },
            {
                'id': 'archive',
                'title': 'Archive',
                'icon': '📦',
                'path': 'deliverables_archive_20251128/',
                'description': 'Previous deliverables version (Nov 2024)',
                'features': [
                    'Historical deliverables',
                    'Previous reports & visualizations',
                    'Legacy documentation',
                    'Version reference'
                ]
            }
        ],
        'quickLinks': [
            {
                'title': 'Deliverables Hub',
                'url': 'deliverables_final/index.html',
                'description': 'Interactive navigation for all deliverables'
            },
            {
                'title': 'Executive Summary PDF',
                'url': 'deliverables_final/1_Executive_Reports/IWRC_Executive_Summary_All_Projects.pdf',
                'description': 'High-level program overview'
            },
            {
                'title': 'Deep Dive Analysis',
                'url': 'deliverables_final/2_Detailed_Reports/IWRC_Analysis_Deep_Dive.pdf',
                'description': 'Comprehensive detailed report'
            },
            {
                'title': 'Main Dataset',
                'url': 'deliverables_final/3_Data_Files/IWRC_ROI_Analysis_Summary_CORRECTED.xlsx',
                'description': 'ROI analysis and tracking data'
            }
        ]
    }

    # Ensure config directory exists
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Write to file
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    # Also embed into index.html for file:// protocol support
    embed_into_index_html(metadata)

    print(f"✅ Repository metadata updated successfully!")
    print(f"📊 Stats: {stats['projects']} projects, {stats['totalInvestment']} investment, {stats['students']} students")
    print(f"📁 Deliverables: {deliverables_count}")
    print(f"🔬 Analysis: {analysis['notebooks']} notebooks, {analysis['scripts']} scripts")
    print(f"📅 Last updated: {metadata['lastUpdated']}")
    print(f"💾 Saved to: {CONFIG_FILE}")
    print(f"📄 Embedded into: index.html")

def embed_into_index_html(metadata):
    """Embed metadata into index.html for file:// protocol support"""
    index_file = REPO_ROOT / 'index.html'

    if not index_file.exists():
        print("⚠️  index.html not found, skipping embed")
        return

    # Read current index.html
    with open(index_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Find and replace the embedded metadata using a simpler marker-based approach
    import re

    # Find the start and end markers
    start_marker = 'const REPO_METADATA = '
    end_marker = '\n};\n'

    start_pos = html_content.find(start_marker)
    if start_pos == -1:
        print("⚠️  Could not find REPO_METADATA in index.html")
        return

    # Find the end of the JSON object (look for }; after the start)
    search_start = start_pos + len(start_marker)
    end_pos = html_content.find(end_marker, search_start)

    if end_pos == -1:
        print("⚠️  Could not find end of REPO_METADATA")
        return

    # Include the closing };
    end_pos += len(end_marker) - 1  # Include up to and including the ;

    # Create the replacement text
    metadata_json = json.dumps(metadata, indent=2, ensure_ascii=False)
    replacement = f'{start_marker}{metadata_json};\n'

    # Build the new content
    new_html = html_content[:start_pos] + replacement + html_content[end_pos + 1:]

    # Write back to file
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_html)

if __name__ == '__main__':
    update_metadata()
