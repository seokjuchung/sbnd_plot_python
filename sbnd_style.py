# sbnd_style_mpl.py
#
# This style will be automatically applied to any plots made after importing it.
# If you don't want automatic styling, comment out the final line:
#
#     set_sbnd_style()
#
# heavily copied from DUNE official style by J. Wolcott and converted to Matplotlib

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from cycler import cycler

# ----------------------------------------------------------------------------
# Colo(u)r Definitions
# ----------------------------------------------------------------------------

# Define Okabe-Ito colors as RGB tuples (0-1 range)
# RGB values from https://mikemol.github.io/technique/colorblind/2018/02/11/color-safe-palette.html
OKABE_ITO_ORANGE = (0.90, 0.60, 0.00)
OKABE_ITO_SKY_BLUE = (0.35, 0.70, 0.90)
OKABE_ITO_BLUE_GREEN = (0.00, 0.60, 0.50)
OKABE_ITO_YELLOW = (0.95, 0.90, 0.25)
OKABE_ITO_BLUE = (0.00, 0.45, 0.70)
OKABE_ITO_VERMILION = (0.80, 0.30, 0.00) # Modified for SBND logo
OKABE_ITO_RED_PURPLE = (0.80, 0.60, 0.70)
OKABE_ITO_BLACK = (0.0, 0.0, 0.0)

# This ordering gets the SBND logo colors in the first 4 and delays yellow.
OKABE_ITO_COLOR_CYCLE = [
    OKABE_ITO_BLACK,
    OKABE_ITO_VERMILION,
    OKABE_ITO_SKY_BLUE,
    OKABE_ITO_ORANGE,
    OKABE_ITO_BLUE_GREEN,
    OKABE_ITO_RED_PURPLE,
    OKABE_ITO_BLUE,
    OKABE_ITO_YELLOW
]

SBND_COLOR_CYCLE = [
    OKABE_ITO_VERMILION,
    OKABE_ITO_BLUE_GREEN,
    OKABE_ITO_BLUE,
    OKABE_ITO_SKY_BLUE
]


# ----------------------------------------------------------------------------
# Custom Colormaps
# ----------------------------------------------------------------------------

def _register_cmap(name, colors, register=True):
    """Create and optionally register a LinearSegmentedColormap."""
    cmap = LinearSegmentedColormap.from_list(name, colors)
    if register:
        plt.register_cmap(name, cmap)
    return cmap

# Sea Palette: A monochrome palette (white -> blue)
SEA_PALETTE = _register_cmap('sbnd_sea', [
    (1.0, 1.0, 1.0), # White
    OKABE_ITO_BLUE   # SBND Blue
])

# Symmetric Palette: A bichrome palette (blue -> white -> vermilion)
SYMMETRIC_PALETTE = _register_cmap('sbnd_symmetric', [
    OKABE_ITO_BLUE,      # Start
    (1.0, 1.0, 1.0),     # Middle
    OKABE_ITO_VERMILION  # End
])

# ----------------------------------------------------------------------------
# Text Labels
# ----------------------------------------------------------------------------

def _sbnd_watermark_string():
    """Returns the 'SBND' part of the watermark as a list for styling."""
    return [('SBND', {'fontweight': 'bold'})]

def text_label(ax, text_list, x=0.05, y=0.95, ha='left', va='top', **kwargs):
    """
    Apply a text label with mixed styling to a plot axis.

    Args:
        ax (matplotlib.axes.Axes): The axes to draw on.
        text_list (list): A list of (substring, dict) tuples for mathtext.
        x (float): x-location in axes coordinates (0-1).
        y (float): y-location in axes coordinates (0-1).
        ha (str): Horizontal alignment.
        va (str): Vertical alignment.
    """
    # Use mathtext to render strings with different styles
    styled_text = ""
    for s, props in text_list:
        weight = props.get('fontweight', 'normal')
        style = props.get('fontstyle', 'normal')
        
        # Build the mathtext command string
        s_cmd = f"\\mathrm{{{s}}}" # Default to roman
        if weight == 'bold':
            s_cmd = f"\\mathbf{{{s}}}"
        if style == 'italic':
             s_cmd = f"\\mathit{{{s_cmd}}}"

        styled_text += s_cmd
    
    final_text = f"${styled_text}$"
    ax.text(x, y, final_text, ha=ha, va=va, transform=ax.transAxes, **kwargs)


def wip(ax, x=0.05, y=0.95, **kwargs):
    """Write a 'SBND Work in Progress' tag."""
    # FIX: Use mathtext spacing command '\;' to ensure spaces are rendered.
    label_list = _sbnd_watermark_string() + [('\\;Work\\;in\\;Progress', {})]
    text_label(ax, label_list, x=x, y=y, **kwargs)

def preliminary(ax, x=0.05, y=0.95, **kwargs):
    """Write a 'SBND Preliminary' tag."""
    # FIX: Use mathtext spacing command '\;' to ensure spaces are rendered.
    label_list = _sbnd_watermark_string() + [('\\;Preliminary', {})]
    text_label(ax, label_list, x=x, y=y, **kwargs)

def official(ax, x=0.05, y=0.95, **kwargs):
    """Write an 'SBND' tag (for officially approved results)."""
    text_label(ax, _sbnd_watermark_string(), x=x, y=y, **kwargs)

# ----------------------------------------------------------------------------
# Main Style Setter
# ----------------------------------------------------------------------------
def set_sbnd_style():
    """Enable the SBND style for Matplotlib."""
    style_dict = {
        # Figure
        "figure.facecolor": "white",
        "figure.figsize": (8, 6),
        "figure.dpi": 100,
        
        # Font
        "font.family": "sans-serif",
        # FIX: Added common free fonts to avoid warnings on systems without Helvetica/Arial
        "font.sans-serif": ["Helvetica", "Arial", "Liberation Sans", "DejaVu Sans"],
        "font.size": 14,
        "text.usetex": False,

        # Axes
        "axes.facecolor": "white",
        "axes.grid": False,
        "axes.titlesize": "large",
        "axes.labelsize": "large",
        "axes.labelweight": "normal",
        "axes.edgecolor": "black",
        "axes.linewidth": 2,
        "axes.prop_cycle": cycler(color=OKABE_ITO_COLOR_CYCLE),
        "axes.titlelocation": "center",

        # Ticks
        "xtick.major.size": 7,
        "xtick.minor.size": 4,
        "xtick.direction": "in",
        "xtick.labelsize": "medium",
        "ytick.major.size": 7,
        "ytick.minor.size": 4,
        "ytick.direction": "in",
        "ytick.labelsize": "medium",
        "xtick.top": True,
        "ytick.right": True,

        # Lines and Markers
        "lines.linewidth": 2,
        "lines.markersize": 6,
        "lines.marker": 'o',

        # Legend
        "legend.frameon": False,
        "legend.fontsize": "medium",

        # Histogram
        "hist.bins": 20,
        
        # Default Colormap
        "image.cmap": 'cividis'
    }
    plt.style.use(style_dict)

# --- Automatically apply the style upon import ---
# Comment out the line below if you want to apply the style manually.
set_sbnd_style()