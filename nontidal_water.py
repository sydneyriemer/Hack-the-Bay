import geopandas
import matplotlib.pyplot as plt
import pandas as pd
import shapely
from shapely.geometry import Point, Polygon, MultiPolygon
from geopandas.tools import sjoin

states = geopandas.read_file('states.shp')
water = pd.read_csv('Water_FINAL.csv',low_memory=False)
water['Point'] = water['Point'].apply(shapely.wkt.loads)
water_gdf = geopandas.GeoDataFrame(water, geometry='Point')
water_gdf.crs = "EPSG:4269"
water_gdf.to_crs(epsg=4269)
states = states.set_index("STATE_NAME", drop = False)
maryland = states[states['STATE_NAME'] == "Maryland"].geometry.squeeze()
#maryland = geopandas.GeoDataFrame(maryland1,crs='EPSG:4269',geometry=geometry)
virginia = states[states['STATE_NAME'] == "Virginia"].geometry.squeeze()
#virginia = geopandas.GeoDataFrame(virginia1,crs='EPSG:4269',geometry=geometry)


in_md= water_gdf.geometry.within(maryland)
in_va= water_gdf.geometry.within(virginia)

df_md = water_gdf[in_md]
df_va = water_gdf[in_va]

df_md.to_csv('maryland_water.csv')
df_va.to_csv('virginia_water.csv')
