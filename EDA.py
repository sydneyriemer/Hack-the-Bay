import geopandas
import matplotlib.pyplot as plt
import pandas as pd
import shapely
from shapely.geometry import Point, Polygon
import seaborn as sns
from geopandas.tools import sjoin
import numpy as np
import scipy.stats
from itertools import permutations

geo_md = geopandas.read_file('lithogeomd_polygon.shp')  # geolitholohies in MD
geo_va = geopandas.read_file('lithogeova_polygon.shp')  # geolithologies in VA
meta = pd.read_csv('lithtbl.txt')  # lithological characteristics

geo_md = geo_md.drop(geo_md[geo_md.LITH_CODE=='water'].index)
geo_md = geo_md.drop(geo_md[geo_md.LITH_CODE=='no_geol'].index)
geo_va = geo_va.drop(geo_va[geo_va.LITH_CODE=='water'].index)
geo_va = geo_va.drop(geo_va[geo_va.LITH_CODE=='no_geol'].index)

geo_md = geo_md.merge(meta,how='left',on='LITH_CODE')
geo_va = geo_va.merge(meta,how='left',on='LITH_CODE')
geology = pd.concat([geo_md,geo_va],axis=0)

nitrate1 = pd.read_csv('nitrate.csv')
nitrate1['Point'] = nitrate1['Point'].apply(shapely.wkt.loads)
nitrate = geopandas.GeoDataFrame(nitrate1,crs='EPSG:4269',geometry='Point')
joined = sjoin(geology,nitrate,how='inner',op='contains')

column = 'WATER_CHEMISTRY'
types = joined[column].unique()
df = joined.groupby('LITH_CODE').nunique()
print(df['MeasureValue'])

def ttest_run(d,c1, c2):
    results = scipy.stats.mannwhitneyu(d.loc[joined[column]==c1, 'MeasureValue'], d.loc[joined[column]==c2, 'MeasureValue'],alternative='two-sided')
    df3 = pd.DataFrame({'1': c1,
                       '2': c2,
                       'pvalue': results.pvalue},
                       index = [0])
    return df3

df_list = [ttest_run(joined,i, j) for i, j in permutations(joined[column].unique().tolist(), 2)]
final_df = pd.concat(df_list, ignore_index = True)
doubles = [ttest_run(joined,i,i) for i in types]
doubles_df = pd.concat(doubles, ignore_index=True)
f= final_df.append(doubles_df, ignore_index=True)
pivoted_table = f.pivot(index='1', columns='2', values='pvalue')

#ax=joined.boxplot(by=column, column=['MeasureValue'], grid=False,rot=10)
#ax.set_ylabel('Nitrate concentration (mg/L)')
ax = sns.heatmap(pivoted_table, cmap="RdBu_r",square=True,cbar_kws={'label': 'p-value'},linewidths=.5,annot=True, xticklabels=False)
ax.set_xlabel('')
ax.set_ylabel('')

plt.xticks(wrap=True,rotation=10)
plt.show()

