"""
plot_multi_year_lczmap.py

Generates a multi-panel Local Climate Zone (LCZ) map across multiple years
using classified raster files and a shapefile boundary for overlay.

Author: Shankar Sharma/ shankar.sharma@unsw.edu.au
Affiliation: CCRC, UNSW
License: MIT (or appropriate license)
"""

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import rioxarray as rxr
import geopandas as gpd
from shapely.geometry import mapping
import numpy as np
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plot_lczmap_multi_year(tiff_paths, shapefile_path, output_dir, years, band_to_plot=0, dpi=500, output_filename="multi_year_lcz_map.jpg"):
    """
    Plots a multi-panel LCZ map for multiple years with colorbar and shapefile overlay.

    Parameters:
        tiff_paths (list): List of paths to LCZ-classified GeoTIFFs (one per year).
        shapefile_path (str): Path to shapefile for boundary overlay.
        output_dir (str): Output directory for the figure.
        years (list): List of years corresponding to the tiff_paths.
        band_to_plot (int): Band index to plot (default is 0).
        dpi (int): Resolution of output image.
        output_filename (str): Name of the output figure file.
    """
    
    # LCZ color scheme (WUDAPT standard)
    colors = [
        '#8C0000', '#D10000', '#FF0000', '#BF4D00', '#FF6600', '#FF9955', '#FAEE05',
        '#BCBCBC', '#FFCCAA', '#555555', '#006A00', '#00AA00', '#648525', '#B9DB79',
        '#000000', '#FBF7AE', '#6A6ACD'
    ]

    cb_labels = [
        '1. Compact high-rise', '2. Compact mid-rise', '3. Compact low-rise', '4. Open high-rise',
        '5. Open mid-rise', '6. Open low-rise', '7. Lightweight low-rise', '8. Large low-rise',
        '9. Sparsely built', '10. Heavy industry', 'A. Dense trees', 'B. Scattered trees',
        'C. Bush, scrub', 'D. Low plants', 'E. Bare rock or paved', 'F. Bare soil or sand', 'G. Water'
    ]

    colors1 = colors[::-1]
    cb_labels = cb_labels[::-1]

    cmap = mpl.colors.ListedColormap(colors)
    cmap1 = mpl.colors.ListedColormap(colors1)
    cmap1.set_bad(color='white')
    cmap1.set_under(color='white')

    # Read shapefile
    gdf = gpd.read_file(shapefile_path)
    bounds = gdf.total_bounds

    # Setup figure
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(10, 12),
                             gridspec_kw={'wspace': 0.02, 'hspace': 0.02},
                             sharex=True, sharey=True)
    axes = axes.flatten()

    for i, (year, tiff_path) in enumerate(zip(years, tiff_paths)):
        ax = axes[i]
        lczTif = rxr.open_rasterio(tiff_path)
        im = lczTif[band_to_plot, :, :].plot(cmap=cmap, vmin=1, vmax=len(colors),
                                             ax=ax, add_colorbar=False)

        gdf.boundary.plot(ax=ax, linewidth=1, edgecolor='black', alpha=0.85)
        formatter = FuncFormatter(lambda x, pos: f'{x:.1f}')
        ax.xaxis.set_major_formatter(formatter)
        ax.yaxis.set_major_formatter(formatter)

        ax.set_xticks(np.linspace(bounds[0], bounds[2], num=5))
        ax.set_yticks(np.linspace(bounds[1], bounds[3], num=5))
        ax.tick_params(axis='both', labelsize=10, colors='grey')
        ax.set_xlim(bounds[0] - 0.15, bounds[2] + 0.15)
        ax.set_ylim(bounds[1] - 0.1, bounds[3] + 0.1)
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_title('')
        ax.text(149.93, -33.05, f'{year}', 
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.9),
                fontsize=14, fontweight='bold')

    # Hide unused subplots
    for j in range(len(years), len(axes)):
        axes[j].axis('off')

    # Colorbar
    divider = make_axes_locatable(axes[-2])
    cax = divider.append_axes("left", size="10%", pad=0.5)
    norm = mpl.colors.BoundaryNorm(np.arange(1, len(colors) + 2) - 0.5, cmap1.N)
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap1), cax=cax, orientation='vertical')
    cbar.set_ticks(np.arange(1, len(colors) + 1))
    cbar.set_ticklabels(cb_labels, fontsize=13)

    # Save output
    os.makedirs(output_dir, exist_ok=True)
    fig_path = os.path.join(output_dir, output_filename)
    plt.savefig(fig_path, dpi=dpi, bbox_inches='tight')
    plt.show()
    plt.close('all')


# -----------------------------
# Example Usage (Edit Paths)
# -----------------------------
if __name__ == "__main__":
    # Example placeholders — replace with your own file paths
    years = [1990, 1995, 2000, 2005, 2010, 2015, 2020]
    tiff_paths = [f"data/LCZ_{year}.tif" for year in years]
    shapefile_path = "data/study_area_boundary.shp"
    output_dir = "figures/"

    plot_lczmap_multi_year(tiff_paths, shapefile_path, output_dir, years)
