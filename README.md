# Mapping Urban Dynamics in Greater Sydney

This repository contains Python scripts used to generate the figures presented in the paper:  
**Mapping Urban Dynamics in Greater Sydney – A Scalable Multi-Decadal Local Climate Zone Classification Approach.**

The scripts focus on post-classification analysis of Local Climate Zone (LCZ) maps from 1990 to 2020 across Greater Sydney. They include spatial transition analysis, pixel-level reversion tracking, and figure generation.

---

## 📁 Repository Structure

### `plot_multi_year_lczmap.py`
Generates a multi-panel figure displaying Local Climate Zone (LCZ) classification maps across multiple years (e.g., 1990–2020). Key features include:
- WUDAPT-compliant LCZ color schemes and labels.
- Overlaying clipped raster outputs on a district-level shapefile.
- Adding year annotations, scale-appropriate tick labels, and a customized vertical colorbar.
- Producing a high-resolution composite image suitable for publication.

📌 **Dependencies**: `rioxarray`, `geopandas`, `matplotlib`, and `mpl_toolkits`.

---

### `transition_matrix_analysis.py`
Calculates the transition matrix between LCZ classifications for specified time intervals. The output is a CSV file summarizing transitions between LCZ classes.

📌 **Dependencies**: `numpy`, `pandas`, and `rasterio`.

---

## 🗂 Example Usage

### `plot_multi_year_lczmap.py`
Update the file paths in the `if __name__ == "__main__"` section:

```python
tiff_paths = ["data/LCZ_1990.tif", ..., "data/LCZ_2020.tif"]
shapefile_path = "data/study_area_boundary.shp"
```

### `transition_matrix_analysis.py`
Update the file paths in the `if __name__ == "__main__"` section:

```python
tiff_files = ["data/LCZ_1990.tif", "data/LCZ_2000.tif", "data/LCZ_2010.tif"]
output_csv = "results/lcz_transition_matrix_1990_2010.csv"
```

---

Feel free to explore and adapt the scripts for your specific research needs. Contributions and feedback are welcome!

