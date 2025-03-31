updated_transition_matrix_code = '''"""
transition_matrix_analysis.py

Computes a land cover transition matrix between two LCZ-classified raster files,
tracking changes in pixel classes between time steps.

Author: Shankar Sharma/ shankar.sharma@unsw.edu.au
Affiliation: CCRC, UNSW
License: MIT (or appropriate)
"""

import os
import xarray as xr
import numpy as np
import rioxarray
import geopandas as gpd
from shapely.geometry import mapping
import pandas as pd

def count_pixels(lcz_tif_path, shapefile_path):
    da = rioxarray.open_rasterio(lcz_tif_path)
    shp = gpd.read_file(shapefile_path)

    if shp.crs != da.rio.crs:
        shp = shp.to_crs(da.rio.crs)
    if da.rio.crs.to_epsg() != 3857:
        da = da.rio.reproject("EPSG:3857")

    da_clipped = da.rio.clip(shp.geometry.apply(mapping), shp.crs, drop=True, all_touched=True)
    data_array = da_clipped.isel(band=0).values
    nodata_value = da_clipped.rio.nodata

    class_counts = {}
    for class_value in np.unique(data_array):
        if class_value == nodata_value or class_value == 0:
            continue
        mask = data_array == class_value
        class_counts[class_value] = int(np.sum(mask))

    return class_counts, data_array

def calculate_transition_matrix(tiff_files, shapefile_path):
    num_classes = 18  # Including 1–17 classes
    transition_matrix = np.zeros((num_classes, num_classes), dtype=int)

    previous_data_array = None
    pixel_counts = {}

    for tiff_file in tiff_files:
        class_counts, current_data_array = count_pixels(tiff_file, shapefile_path)
        year = os.path.splitext(os.path.basename(tiff_file))[0].split('_')[-1]
        pixel_counts[year] = class_counts

        if previous_data_array is not None:
            current_data_array_resampled = xr.DataArray(current_data_array, dims=["y", "x"]).interp(
                x=np.linspace(0, current_data_array.shape[1]-1, previous_data_array.shape[1]),
                y=np.linspace(0, current_data_array.shape[0]-1, previous_data_array.shape[0]),
                method="nearest"
            ).values

            for from_class in range(1, num_classes):
                for to_class in range(1, num_classes):
                    count = np.sum((previous_data_array == from_class) & (current_data_array_resampled == to_class))
                    transition_matrix[to_class, from_class] += count

        previous_data_array = current_data_array

    return transition_matrix, pixel_counts

def export_transition_matrix_simple(transition_matrix, pixel_counts, tiff_files, output_csv):
    num_classes = transition_matrix.shape[0]
    rows = []

    current_year = os.path.splitext(os.path.basename(tiff_files[0]))[0].split('_')[-1]
    next_year = os.path.splitext(os.path.basename(tiff_files[1]))[0].split('_')[-1]

    for class_id in range(1, num_classes):
        row = {
            "Class": class_id,
            "First_Year_Pixel_Count": pixel_counts[current_year].get(class_id, 0),
            "Second_Year_Pixel_Count": pixel_counts[next_year].get(class_id, 0)
        }
        for to_class in range(1, num_classes):
            row[f"To_Class_{to_class}"] = transition_matrix[class_id, to_class]
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(output_csv, index=False)
    print(f"Transition matrix exported to {output_csv}")

# Example usage (edit file paths as needed)
if __name__ == "__main__":
    tiff_files = ["data/LCZ_YEAR1.tif", "data/LCZ_YEAR2.tif"]
    # YEAR1 could be 2010, YEAR2 could be 2015
    shapefile_path = "data/study_area_boundary.shp"
    output_csv = "results/lcz_transition_matrix_YEAR1_YEAR2.csv"

    transition_matrix, pixel_counts = calculate_transition_matrix(tiff_files, shapefile_path)
    export_transition_matrix_simple(transition_matrix, pixel_counts, tiff_files, output_csv)
'''
updated_transition_matrix_code
