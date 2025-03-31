# Mapping Urban Dynamics in Greater Sydney

This repository contains the Python code used to generate the figures presented in the paper:  
**Mapping Urban Dynamics in Greater Sydney – A Scalable Multi-Decadal Local Climate Zone Classification Approach.**

The included scripts focus on the post-classification analysis of Local Climate Zone (LCZ) maps from 1990 to 2020 across Greater Sydney. They cover spatial transition analysis, pixel-level reversion tracking, and figure generation.

---

## 📁 Repository Structure



### `plot_multi_year_lczmap.py`
Generates a multi-panel figure displaying Local Climate Zone (LCZ) classification maps across multiple years (e.g., 1990–2020). This script:
- Applies WUDAPT-compliant LCZ color schemes and labels.
- Plots clipped raster outputs over a district-level shapefile.
- Adds year annotations, scale-appropriate tick labels, and a customized vertical colorbar.
- Produces a final high-resolution composite image suitable for publication.

📌 Note: The script uses `rioxarray`, `geopandas`, `matplotlib`, and `mpl_toolkits` for geospatial and visual layout.


