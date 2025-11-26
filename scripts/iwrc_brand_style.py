#!/usr/bin/env python3
"""
IWRC Brand Style Module

Centralized branding configuration for all IWRC Seed Fund Tracking visualizations.
Handles colors, fonts, logo integration, and style application across matplotlib and Plotly.

Color Palette from IWRC Logo:
- Primary Teal: #258372
- Secondary Olive: #639757
- Text Dark Gray: #54595F
- Accent Peach: #FCC080
- Background Light Gray: #F6F6F6
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import os
from pathlib import Path

# ============================================================================
# IWRC BRAND COLORS
# ============================================================================

IWRC_COLORS = {
    'primary': '#258372',           # Teal green - main brand color
    'secondary': '#639757',         # Olive green - secondary
    'text': '#54595F',              # Dark gray - body text
    'accent': '#FCC080',            # Peach - accent highlights
    'background': '#F6F6F6',        # Light gray - backgrounds
    'dark_teal': '#1a5f52',         # Dark teal - headers/emphasis
    'light_teal': '#3fa890',        # Light teal - secondary highlights
    'sage': '#8ab38a',              # Sage green - tertiary
    'gold': '#e6a866',              # Gold - alternative accent
    'neutral_light': '#f5f5f5',     # Very light gray
    'neutral_dark': '#333333',      # Dark gray for text
}

# Extended palette for multi-series charts (8 colors)
IWRC_PALETTE = [
    IWRC_COLORS['primary'],         # #258372 - Teal
    IWRC_COLORS['secondary'],       # #639757 - Olive
    IWRC_COLORS['accent'],          # #FCC080 - Peach
    IWRC_COLORS['light_teal'],      # #3fa890 - Light Teal
    IWRC_COLORS['sage'],            # #8ab38a - Sage
    IWRC_COLORS['gold'],            # #e6a866 - Gold
    IWRC_COLORS['dark_teal'],       # #1a5f52 - Dark Teal
    '#7ca87a',                       # Gray-green for 8-color palette
]

# ============================================================================
# IWRC FONTS
# ============================================================================

IWRC_FONTS = {
    'headline': 'Montserrat',
    'headline_weight': 'semibold',
    'body': 'Montserrat',
    'body_weight': 'light',
}

# Logo path
LOGO_PATH = '/Users/shivpat/Downloads/Seed Fund Tracking/IWRC Logo - Full Color.svg'
LOGO_PNG_PATH = '/Users/shivpat/Downloads/Seed Fund Tracking/IWRC_Logo.png'

# ============================================================================
# MATPLOTLIB CONFIGURATION
# ============================================================================

def configure_matplotlib_iwrc():
    """Configure matplotlib to use IWRC fonts and styling."""
    try:
        plt.rcParams['font.family'] = 'Montserrat'
        plt.rcParams['font.sans-serif'] = ['Montserrat', 'DejaVu Sans']
    except Exception as e:
        print(f"Warning: Could not configure Montserrat font: {e}")
        print("Falling back to default sans-serif")
        plt.rcParams['font.family'] = 'sans-serif'

    # Title and label weights
    plt.rcParams['font.weight'] = 'light'
    plt.rcParams['axes.titleweight'] = 'semibold'
    plt.rcParams['figure.titleweight'] = 'semibold'

    # Grid and spine styling
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.color'] = IWRC_COLORS['background']

    # Figure background
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'


def apply_iwrc_matplotlib_style(fig, ax=None):
    """
    Apply IWRC styling to matplotlib figure and axes.

    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        Figure object to style
    ax : matplotlib.axes.Axes or list of Axes, optional
        Axes to style. If None, applies to all axes in figure.
    """
    configure_matplotlib_iwrc()

    # Handle single or multiple axes
    axes = ax if isinstance(ax, (list, np.ndarray)) else [ax] if ax else fig.get_axes()

    for axis in axes:
        if axis is None:
            continue

        # Spine styling
        for spine in ['top', 'right']:
            axis.spines[spine].set_visible(False)

        for spine in ['left', 'bottom']:
            axis.spines[spine].set_color(IWRC_COLORS['neutral_dark'])
            axis.spines[spine].set_linewidth(0.8)

        # Tick styling
        axis.tick_params(colors=IWRC_COLORS['text'], labelsize=10)

        # Label styling
        if axis.get_xlabel():
            axis.xaxis.label.set_color(IWRC_COLORS['text'])
            axis.xaxis.label.set_weight('semibold')
        if axis.get_ylabel():
            axis.yaxis.label.set_color(IWRC_COLORS['text'])
            axis.yaxis.label.set_weight('semibold')

        # Title styling
        if axis.get_title():
            axis.title.set_color(IWRC_COLORS['dark_teal'])
            axis.title.set_weight('semibold')
            axis.title.set_fontsize(12)

    # Figure title styling
    if fig._suptitle:
        fig._suptitle.set_color(IWRC_COLORS['dark_teal'])
        fig._suptitle.set_weight('semibold')

    # Tight layout
    fig.tight_layout()


# ============================================================================
# LOGO HANDLING
# ============================================================================

def add_logo_to_matplotlib_figure(fig, position='top-right', size=0.08):
    """
    Add IWRC logo to matplotlib figure.

    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        Figure to add logo to
    position : str, default 'top-right'
        Position of logo: 'top-left', 'top-right', 'bottom-left', 'bottom-right'
    size : float, default 0.08
        Size of logo relative to figure width (0-1)
    """
    try:
        from PIL import Image

        # Try PNG first, then SVG conversion
        logo_path = None
        if os.path.exists(LOGO_PNG_PATH):
            logo_path = LOGO_PNG_PATH
        elif os.path.exists(LOGO_PATH):
            # Try to convert SVG to PNG using cairosvg if available
            try:
                import cairosvg
                logo_path = LOGO_PNG_PATH
                if not os.path.exists(logo_path):
                    cairosvg.svg2png(url=LOGO_PATH, write_to=logo_path, dpi=150)
            except ImportError:
                print("Warning: cairosvg not available for SVG conversion")
                return

        if not logo_path or not os.path.exists(logo_path):
            print(f"Warning: Logo file not found at {LOGO_PATH} or {LOGO_PNG_PATH}")
            return

        # Load and add logo
        logo = Image.open(logo_path)

        # Calculate position
        position_map = {
            'top-right': (0.92, 0.95),
            'top-left': (0.05, 0.95),
            'bottom-right': (0.92, 0.05),
            'bottom-left': (0.05, 0.05),
        }

        x, y = position_map.get(position, (0.92, 0.95))

        # Add logo as annotation
        ax = fig.get_axes()[0] if fig.get_axes() else fig.add_axes([0, 0, 1, 1])

        imagebox = OffsetImage(logo, zoom=size * 200)  # Adjust zoom multiplier as needed
        ab = AnnotationBbox(imagebox, xy=(x, y), xycoords='figure fraction',
                           frameon=False, pad=0)
        ax.add_artist(ab)

    except Exception as e:
        print(f"Warning: Could not add logo to figure: {e}")


# ============================================================================
# PLOTLY STYLING
# ============================================================================

def get_iwrc_plotly_template():
    """
    Create and return IWRC-styled Plotly template.

    Returns:
    --------
    plotly.graph_objects.layout.Template
        Configured template for Plotly figures
    """
    from plotly.graph_objects import layout

    template = layout.Template(
        layout=layout.Layout(
            colorway=IWRC_PALETTE,
            paper_bgcolor='white',
            plot_bgcolor=IWRC_COLORS['background'],
            font=dict(
                family='Montserrat, sans-serif',
                size=11,
                color=IWRC_COLORS['text']
            ),
            title=dict(
                font=dict(
                    family='Montserrat, sans-serif',
                    size=18,
                    color=IWRC_COLORS['dark_teal'],
                ),
                x=0.5,
                xanchor='center',
            ),
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor=IWRC_COLORS['neutral_light'],
                zeroline=False,
                showline=True,
                linewidth=1,
                linecolor=IWRC_COLORS['neutral_dark'],
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor=IWRC_COLORS['neutral_light'],
                zeroline=False,
                showline=True,
                linewidth=1,
                linecolor=IWRC_COLORS['neutral_dark'],
            ),
        )
    )

    return template


def apply_iwrc_plotly_style(fig):
    """
    Apply IWRC styling to Plotly figure.

    Parameters:
    -----------
    fig : plotly.graph_objects.Figure
        Figure to style

    Returns:
    --------
    plotly.graph_objects.Figure
        Styled figure
    """
    template = get_iwrc_plotly_template()
    fig.update_layout(template=template)

    # Add Google Fonts reference for Montserrat
    fig.update_layout(
        font=dict(
            family='Montserrat, sans-serif'
        )
    )

    return fig


def add_logo_to_plotly_figure(fig, position='top right', size=0.08):
    """
    Add IWRC logo to Plotly figure.

    Parameters:
    -----------
    fig : plotly.graph_objects.Figure
        Figure to add logo to
    position : str, default 'top right'
        Position: 'top left', 'top right', 'bottom left', 'bottom right'
    size : float, default 0.08
        Size relative to figure
    """
    try:
        if not os.path.exists(LOGO_PNG_PATH):
            print(f"Warning: Logo PNG not found at {LOGO_PNG_PATH}")
            return fig

        # Position mapping for Plotly
        position_map = {
            'top right': (0.92, 0.95),
            'top left': (0.05, 0.95),
            'bottom right': (0.92, 0.05),
            'bottom left': (0.05, 0.05),
        }

        x, y = position_map.get(position, (0.92, 0.95))

        from PIL import Image
        import base64
        from io import BytesIO

        # Load and encode image
        img = Image.open(LOGO_PNG_PATH)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Add as layout image
        fig.add_layout_image(
            dict(
                source=f"data:image/png;base64,{img_str}",
                xref="paper",
                yref="paper",
                x=x,
                y=y,
                sizex=size,
                sizey=size,
                xanchor="right",
                yanchor="top"
            )
        )

    except Exception as e:
        print(f"Warning: Could not add logo to Plotly figure: {e}")

    return fig


# ============================================================================
# COLOR PALETTE UTILITIES
# ============================================================================

def get_iwrc_color_palette(n_colors=8, include_neutrals=False):
    """
    Get IWRC color palette, cycling or extending as needed.

    Parameters:
    -----------
    n_colors : int, default 8
        Number of colors needed
    include_neutrals : bool, default False
        Whether to include neutral colors

    Returns:
    --------
    list
        List of hex color strings
    """
    base_palette = IWRC_PALETTE

    if n_colors <= len(base_palette):
        return base_palette[:n_colors]

    # Cycle through palette if more colors needed
    colors = []
    for i in range(n_colors):
        colors.append(base_palette[i % len(base_palette)])

    return colors


def create_colormap_iwrc(name='iwrc', n=256):
    """
    Create matplotlib colormap using IWRC palette.

    Parameters:
    -----------
    name : str, default 'iwrc'
        Name for the colormap
    n : int, default 256
        Number of colors in colormap

    Returns:
    --------
    matplotlib.colors.LinearSegmentedColormap
        IWRC colormap
    """
    from matplotlib.colors import LinearSegmentedColormap

    # Use primary to secondary gradient
    colors_list = [IWRC_COLORS['light_teal'], IWRC_COLORS['primary'],
                   IWRC_COLORS['dark_teal']]

    cmap = LinearSegmentedColormap.from_list(name, colors_list, N=n)
    plt.colormaps.register(cmap)

    return cmap


# ============================================================================
# STYLING UTILITIES
# ============================================================================

def format_currency(value):
    """Format value as currency string."""
    if value >= 1_000_000:
        return f"${value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"${value/1_000:.0f}K"
    else:
        return f"${value:.0f}"


def format_percentage(value):
    """Format value as percentage string."""
    return f"{value:.1f}%"


def add_data_labels_to_bars(ax, fmt=None, fontsize=9, color=None):
    """
    Add value labels on top of bar chart bars.

    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        Axes containing bars
    fmt : callable, optional
        Function to format values (e.g., format_currency)
    fontsize : int, default 9
        Font size for labels
    color : str, optional
        Text color (default: dark_teal)
    """
    color = color or IWRC_COLORS['dark_teal']

    for container in ax.containers:
        labels = []
        for bar in container:
            height = bar.get_height()
            label = fmt(height) if fmt else f'{height:.1f}'
            labels.append(label)

        ax.bar_label(container, labels=labels, fontsize=fontsize,
                     color=color, weight='semibold')


def create_legend_iwrc(ax, labels, colors=None, loc='best', **kwargs):
    """
    Create IWRC-styled legend.

    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        Axes to add legend to
    labels : list
        Legend labels
    colors : list, optional
        Legend colors (default: IWRC palette)
    loc : str, default 'best'
        Legend location
    """
    if colors is None:
        colors = get_iwrc_color_palette(len(labels))

    patches = [mpatches.Patch(facecolor=color, label=label)
               for color, label in zip(colors, labels)]

    legend = ax.legend(handles=patches, loc=loc,
                      frameon=True, framealpha=0.95,
                      fancybox=True, shadow=False,
                      fontsize=10, **kwargs)

    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor(IWRC_COLORS['neutral_light'])

    return legend


# ============================================================================
# INITIALIZATION
# ============================================================================

# Configure matplotlib on import
configure_matplotlib_iwrc()

# Register IWRC colormap
try:
    create_colormap_iwrc()
except Exception as e:
    print(f"Warning: Could not register IWRC colormap: {e}")


if __name__ == '__main__':
    # Test the brand style module
    print("IWRC Brand Style Module Test")
    print("=" * 50)
    print("\nIWRC Colors:")
    for name, color in IWRC_COLORS.items():
        print(f"  {name:20} {color}")

    print("\nIWRC Palette (8 colors):")
    for i, color in enumerate(IWRC_PALETTE, 1):
        print(f"  {i}. {color}")

    print("\nFonts:")
    for key, val in IWRC_FONTS.items():
        print(f"  {key:20} {val}")

    print("\nLogo paths:")
    print(f"  SVG: {LOGO_PATH} (exists: {os.path.exists(LOGO_PATH)})")
    print(f"  PNG: {LOGO_PNG_PATH} (exists: {os.path.exists(LOGO_PNG_PATH)})")

    # Test matplotlib styling
    print("\n" + "=" * 50)
    print("Testing matplotlib styling...")

    fig, ax = plt.subplots(figsize=(8, 6))

    # Sample data
    categories = ['Q1', 'Q2', 'Q3', 'Q4']
    values = [10, 15, 12, 18]

    bars = ax.bar(categories, values, color=IWRC_COLORS['primary'])
    ax.set_ylabel('Values', weight='semibold', color=IWRC_COLORS['text'])
    ax.set_title('IWRC Brand Style Test', weight='semibold', color=IWRC_COLORS['dark_teal'])

    apply_iwrc_matplotlib_style(fig, ax)
    add_logo_to_matplotlib_figure(fig, position='top-right', size=0.08)

    print("✓ Matplotlib styling test complete")
    print("  (Figure not displayed in non-interactive mode)")
