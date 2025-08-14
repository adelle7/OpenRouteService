## Duration Comparisons Using Open Route Service and Google Maps API  
**Author:** Adelle Melnikov  

---

### Includes:

#### `src/`  
- `ors_construct.py`  
- `ors_convert.py`  
- `maps_construct.py`  

#### `data/`  
**CSV files**:  
- `inputs`: sources and targets with `"Longitude, Latitude"` coordinates  
- `matrices`: duration matrices of specified sources and targets from OpenRouteService and Google Maps API 
- `directions`: path of intervals seperated by waycategory (1 = highway, 0 = residential) for each source and target pair 

**JSON files**:  
- Polygon coordinates for enclosed areas in:
  - Drexel Hill  
  - Mount Airy & Germantown  
  - Northeast Philadelphia  
  - Center City Philadelphia  
  *(drawn using [geojson.io](https://geojson.io/#map=2/0/20))*

- Coordinates of nodes representing:
  - Residential areas not in the city  
  - Places of work in the city  
  *(queried from [Overpass Turbo](https://overpass-turbo.eu/))*

#### `ors-docker/`  
Materials for the Docker container used to run OpenRouteService and draw graphs  
[OpenRouteService GitHub](https://github.com/GIScience/openrouteservice)

---

## Goal:  
**Determine and Improve Inaccuracies in Open Street Map.**  
* We do this by comparing the open-source durations to Google Maps durations, which account for **time of day**.

---

## Steps:

1. Use [geojson.io](https://geojson.io/#map=2/0/20) to draw desired polygon areas. 
<br>
  <img src="images/geojson_center-city_philadelphia.png" alt="center-city" width="450"/> 
  <img src="images/geojson_drexel-hill.png" alt="center-city" width="450"/> 

    In total, four polygons are drawn oustside Center City Philadelphia: Northeast area, Mount Airy and Germantown, and Drexel Hill suburbs. The fifth polygon is drawn directly in Center City, Philadelphia. Their coordinates are in data/json/polygon.json 

2. Pass the polygon coordinates into [Overpass Turbo](https://overpass-turbo.eu/) to query nodes mapped on OpenRouteService. 
<br>
3. Run `ors_convert.py` to get CSV files formatted as `"Longitude, Latitude"`—these are node coordinates output by Overpass Turbo that serve as sources and targets. All source and target node coordinates are located in data/csv/inputs.
<br>
4. Run `ors_construct.py` (within a virtual environment) through a Docker container to generate output matrix files of duration times between specified sources and targets. 
   Run `maps_construct.py` to get **duration matrices** for the same sources and targets using Google Maps.  
<br>
5. Run `compare.py` to generate **histograms** of the differences:  
   `google_maps_durations - ors_durations`  
   *(all values are in seconds)*  
  <img src="histograms/07_29_8:00/drexel-hill_morning_diff_histogram.png" alt="histogram" width="375"/> 
  <img src="histograms/07_29_13:30/drexel-hill_afternoon_diff_histogram.png" alt="histogram" width="375"/> 
  <img src="histograms/07_29_17:00/drexel-hill_evening_diff_histogram.png" alt="histogram" width="375"/> 


<div>
<h4>6. Run <code>ors_cluster.py</code> to get highway segments that act as centroids of all highway segments in the paths inbound to Center City Philadelphia.</h4>


<style>
  .image-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(375px, 1fr));
    gap: 10px;
    justify-items: center;
  }
  .image-grid img {
    max-width: 100%;
    height: auto;
  }
</style>

<div class="image-grid">
  <img src="images/-75.073642  40.007374 -75.142028  39.957202.png" alt="center-city">
  <img src="images/-75.178456  40.014653 -75.176745  39.959053.png" alt="center-city">
  <img src="images/-75.178456  40.014653 -75.181218  39.956899.png" alt="center-city">
  <img src="images/-75.187634  39.947453 -75.149154  39.956189.png" alt="center-city">
  <img src="images/-75.187634  39.947453 -75.175561  39.959203.png" alt="center-city">
  <img src="images/-75.198346  39.974789 -75.149154  39.956189.png" alt="center-city">
  <img src="images/-75.198346  39.974789 -75.164204  39.957732.png" alt="center-city">
  <img src="images/-75.198346  39.974789 -75.175561  39.959203.png" alt="center-city">

</div>

Directions for the paths and a corresponding matrix containing which paths have a highway will also be output to files. The following descriptions can be found in `data/csv/matrices`  
- differeces: a matrix for area of sources, where each cell is the difference in seconds between the google maps api duration time and openrouteservice duration time 
- geometry: coordinates of points making up each shortest path, and their waycategory 
- waycategory: a matrix for each area of sources, where each cell is marked 1 is a highway is present somewhere in the path between the source and target and 0 if no highway is present


## Results:


The differences between google maps duration times and openrouteservice duration times have a negative difference for Mount Airy and Germantown suburbs, inbound to Center City Philadelphia




  
