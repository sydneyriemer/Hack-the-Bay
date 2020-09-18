# Hack-the-Bay
My solution to Booz Allen Hamilton's Hack the Bay challenge

# Python files:
-data_exploration_geo.py: loads in USGS shapefiles (Peper et al., 2001) of lithogeochemical map and plots water quality data on top of map

-EDA.py: spatially joins geology data and water quality data and performs exploratory data analysis of the water quality data (boxplots and hypothesis testing)

-nontidal_water.py: extracts the CBP and CMC data points that only lie on land and in the states of Maryland and Virginia

# Geospatial data
Shapefiles for the geospatial data I used are contained in the folder called 'geospatial_data'. 

-lithogeomd_polygon.shp: shapefile for lithogeochemical data of Maryland from Peper et al. (2001)

-lithogeova_polygon.shp: shapefile for lithogeochemical data of Maryland from Peper et al. (2001)

-states.shp: shapefile for USA state borders used to select CBP and CMC water quality data points in Maryland and Virginia only. Data from ArcGis (https://www.arcgis.com/home/item.html?id=b07a9393ecbd430795a6f6218443dccc)
