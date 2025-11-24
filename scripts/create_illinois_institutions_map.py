import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon, Wedge, Circle
import numpy as np
from pathlib import Path
import json

# Define Illinois institutions with coordinates and funding data
INSTITUTIONS = [
    {
        "name": "University of Illinois Urbana-Champaign",
        "lat": 40.1020,
        "lon": -88.2272,
        "funding": 6063340,
        "projects": 99,
        "city": "Urbana-Champaign"
    },
    {
        "name": "Illinois Institute of Technology",
        "lat": 41.8348,
        "lon": -87.6266,
        "funding": 1050000,
        "projects": 7,
        "city": "Chicago"
    },
    {
        "name": "Southern Illinois University Carbondale",
        "lat": 37.7213,
        "lon": -89.2167,
        "funding": 842519,
        "projects": 18,
        "city": "Carbondale"
    },
    {
        "name": "Illinois State University",
        "lat": 40.5142,
        "lon": -88.9907,
        "funding": 79770,
        "projects": 8,
        "city": "Normal"
    },
    {
        "name": "Illinois State Water Survey",
        "lat": 40.1164,
        "lon": -88.2434,
        "funding": 59997,
        "projects": 1,
        "city": "Champaign"
    },
    {
        "name": "University of Illinois Chicago",
        "lat": 41.8708,
        "lon": -87.6470,
        "funding": 39706,
        "projects": 4,
        "city": "Chicago"
    },
    {
        "name": "Northwestern University",
        "lat": 42.0565,
        "lon": -87.6753,
        "funding": 20000,
        "projects": 2,
        "city": "Evanston"
    },
    {
        "name": "Illinois Sustainable Technology Center",
        "lat": 40.1164,
        "lon": -88.2434,
        "funding": 15000,
        "projects": 1,
        "city": "Champaign"
    },
    {
        "name": "Lewis and Clark Community College",
        "lat": 38.9742,
        "lon": -90.1840,
        "funding": 15000,
        "projects": 1,
        "city": "Godfrey"
    },
    {
        "name": "National Great Rivers Research & Education Center",
        "lat": 38.8881,
        "lon": -90.1068,
        "funding": 15000,
        "projects": 1,
        "city": "East Alton"
    },
    {
        "name": "Loyola University Chicago",
        "lat": 41.9989,
        "lon": -87.6576,
        "funding": 10000,
        "projects": 1,
        "city": "Chicago"
    },
    {
        "name": "Eastern Illinois University",
        "lat": 39.4817,
        "lon": -88.2039,
        "funding": 9977,
        "projects": 1,
        "city": "Charleston"
    },
    {
        "name": "Northern Illinois University",
        "lat": 41.9306,
        "lon": -88.7712,
        "funding": 8331,
        "projects": 1,
        "city": "DeKalb"
    },
    {
        "name": "Basil's Harvest",
        "lat": 40.0,
        "lon": -89.0,
        "funding": 5000,
        "projects": 1,
        "city": "Illinois"
    },
    {
        "name": "Lewis University",
        "lat": 41.6070,
        "lon": -88.0892,
        "funding": 2000,
        "projects": 1,
        "city": "Romeoville"
    }
]

# Illinois river coordinates (simplified polylines for major rivers)
RIVERS = {
    "Mississippi River": [
        (42.5, -91.0), (42.0, -91.2), (41.0, -91.5), (40.0, -91.4),
        (39.0, -91.3), (38.5, -91.2), (37.5, -91.0)
    ],
    "Illinois River": [
        (42.3, -89.8), (41.5, -89.2), (40.5, -88.5), (39.5, -88.8),
        (39.0, -88.9), (38.5, -89.2)
    ],
    "Rock River": [
        (42.5, -89.0), (42.0, -88.8), (41.2, -88.5), (40.5, -88.3)
    ],
    "Fox River": [
        (42.2, -88.8), (41.8, -88.4), (41.5, -88.2), (41.0, -88.0)
    ],
    "Sangamon River": [
        (40.5, -88.5), (39.8, -88.8), (39.2, -89.1)
    ],
    "Kaskaskia River": [
        (40.5, -88.8), (39.8, -89.2), (38.8, -89.5), (38.2, -90.0)
    ],
    "Embarras River": [
        (39.5, -87.8), (39.0, -88.2), (38.5, -88.5)
    ],
    "Wabash River": [
        (40.5, -87.5), (39.5, -87.8), (38.5, -87.9), (37.8, -87.8)
    ]
}

# Major lakes/reservoirs (approximated as regions)
LAKES = {
    "Lake Michigan": {
        "bounds": [(42.5, -87.3), (42.0, -87.3), (42.0, -87.5), (42.5, -87.5)]
    },
    "Carlyle Lake": {
        "center": (38.4, -89.3),
        "radius": 0.3
    },
    "Lake Shelbyville": {
        "center": (39.8, -88.5),
        "radius": 0.25
    },
    "Lake Springfield": {
        "center": (39.8, -89.6),
        "radius": 0.2
    },
    "Upper Peoria Lake": {
        "center": (40.8, -89.6),
        "radius": 0.2
    },
    "Senachwine Lake": {
        "center": (41.2, -88.7),
        "radius": 0.15
    },
    "Rend Lake": {
        "center": (38.2, -89.0),
        "radius": 0.2
    },
    "Crab Orchard Lake": {
        "center": (37.8, -88.8),
        "radius": 0.2
    }
}

def create_star(ax, x, y, size=200, color='darkblue', zorder=5):
    """Create a star marker at given coordinates"""
    ax.scatter(x, y, marker='*', s=size, color=color, edgecolors='darkblue',
               linewidths=0.5, zorder=zorder)

def get_marker_size(funding):
    """Determine marker size based on funding amount"""
    if funding > 1000000:
        return 800
    elif funding > 100000:
        return 600
    elif funding > 10000:
        return 400
    else:
        return 300

def draw_illinois_map():
    """Create the Illinois institutions map"""
    fig, ax = plt.subplots(figsize=(10, 13), dpi=300)

    # Set background color to beige/tan (matching GIS Geography style)
    ax.set_facecolor('#E8DCC8')
    fig.patch.set_facecolor('white')

    # Set map bounds for Illinois
    ax.set_xlim(-92.0, -86.8)
    ax.set_ylim(36.9, 42.6)

    # Set aspect ratio to match Illinois shape
    ax.set_aspect('equal')

    # Draw Illinois state outline (simplified polygon)
    illinois_outline = [
        (37.0, -91.5), (37.2, -91.2), (37.5, -90.8), (37.8, -90.5),
        (38.0, -90.2), (38.2, -89.8), (38.4, -89.5), (38.5, -89.0),
        (38.7, -88.8), (38.9, -88.5), (39.1, -88.2), (39.3, -87.8),
        (39.5, -87.5), (39.7, -87.2), (39.9, -87.0), (40.1, -87.0),
        (40.3, -87.2), (40.5, -87.0), (40.7, -86.9), (41.0, -87.0),
        (41.5, -87.2), (42.0, -87.3), (42.3, -87.5), (42.5, -88.0),
        (42.3, -88.5), (42.0, -89.0), (41.5, -89.5), (41.0, -89.8),
        (40.5, -90.2), (40.0, -90.8), (39.5, -91.0), (39.0, -91.2),
        (38.5, -91.3), (38.0, -91.2), (37.5, -91.0), (37.0, -91.5)
    ]

    illinois_poly = Polygon(illinois_outline, closed=True, fill=False,
                           edgecolor='black', linewidth=2, zorder=3)
    ax.add_patch(illinois_poly)

    # Draw rivers
    for river_name, coords in RIVERS.items():
        lons = [c[1] for c in coords]
        lats = [c[0] for c in coords]
        ax.plot(lons, lats, color='#4A90E2', linewidth=1.5, alpha=0.7, zorder=2)

    # Draw lakes
    for lake_name, lake_data in LAKES.items():
        if "bounds" in lake_data:
            bounds = lake_data["bounds"]
            lons = [b[1] for b in bounds]
            lats = [b[0] for b in bounds]
            lake_poly = Polygon(list(zip(lons, lats)), closed=True,
                               facecolor='#4A90E2', alpha=0.5,
                               edgecolor='#4A90E2', linewidth=1, zorder=2)
            ax.add_patch(lake_poly)
        elif "center" in lake_data:
            center = lake_data["center"]
            radius = lake_data["radius"]
            circle = Circle((center[1], center[0]), radius,
                           facecolor='#4A90E2', alpha=0.5,
                           edgecolor='#4A90E2', linewidth=1, zorder=2)
            ax.add_patch(circle)

    # Plot institutions
    for inst in INSTITUTIONS:
        size = get_marker_size(inst["funding"])
        create_star(ax, inst["lon"], inst["lat"], size=size, color='#00264D', zorder=5)

    # Add labels for major institutions (top 5 by funding)
    top_institutions = sorted(INSTITUTIONS, key=lambda x: x["funding"], reverse=True)[:5]
    for inst in top_institutions:
        ax.text(inst["lon"] + 0.15, inst["lat"] + 0.15,
               inst["name"].split()[0],
               fontsize=8, fontweight='bold', zorder=6,
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                        alpha=0.7, edgecolor='none'))

    # Add title and attribution
    ax.set_title('IWRC Seed Fund Tracking - Illinois Institutions (2015-2024)',
                fontsize=14, fontweight='bold', pad=20)
    ax.text(0.99, 0.01, 'Source: GISGeography.com',
           transform=ax.transAxes, fontsize=9, ha='right', va='bottom',
           style='italic')

    # Remove axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Add legend
    legend_elements = [
        plt.scatter([], [], marker='*', s=800, color='#00264D',
                   label='>$1M funding (1 institution)', edgecolors='#00264D'),
        plt.scatter([], [], marker='*', s=600, color='#00264D',
                   label='$100K-$1M (2 institutions)', edgecolors='#00264D'),
        plt.scatter([], [], marker='*', s=400, color='#00264D',
                   label='$10K-$100K (8 institutions)', edgecolors='#00264D'),
        plt.scatter([], [], marker='*', s=300, color='#00264D',
                   label='<$10K (4 institutions)', edgecolors='#00264D')
    ]
    ax.legend(handles=legend_elements, loc='lower left', fontsize=9,
             framealpha=0.9, edgecolor='black')

    # Save the figure
    output_path = Path("/Users/shivpat/Downloads/Seed Fund Tracking/visualizations/static/illinois_institutions_map.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Map saved to: {output_path}")
    plt.close()

if __name__ == "__main__":
    draw_illinois_map()
    print("Illinois institutions map created successfully!")
