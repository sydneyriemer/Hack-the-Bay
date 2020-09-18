import geopandas
import matplotlib.pyplot as plt
import pandas as pd
import shapely
from shapely.geometry import Point, Polygon

geo_md = geopandas.read_file('lithogeomd_polygon.shp')  # geolitholohies in MD
geo_va = geopandas.read_file('lithogeova_polygon.shp')  # geolithologies in VA
meta = pd.read_csv('lithtbl.txt')  # lithological characteristics

geo_md = geo_md.drop(geo_md[geo_md.LITH_CODE=='water'].index)
geo_md = geo_md.drop(geo_md[geo_md.LITH_CODE=='no_geol'].index)
geo_va = geo_va.drop(geo_va[geo_va.LITH_CODE=='water'].index)
geo_va = geo_va.drop(geo_va[geo_va.LITH_CODE=='no_geol'].index)

geo_md = geo_md.merge(meta,how='left',on='LITH_CODE')
geo_va = geo_va.merge(meta,how='left',on='LITH_CODE')

water1 = pd.read_csv('water_combined.csv')
water1['Point'] = water1['Point'].apply(shapely.wkt.loads)
water = geopandas.GeoDataFrame(water1,crs='EPSG:4269',geometry='Point')

ax = geo_md.plot(geo_md['LITH_CODE'])
geo_va.plot(geo_va['LITH_CODE'],ax=ax)
water.plot(ax=ax,markersize=5,color='black', alpha=0.5)

plt.show()