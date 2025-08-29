import os

import geopandas
import pandas as pd

polys = '~/gis/missingPolygons/polys/'
CRS = 'EPSG:4326'
citation = 'roberts2026schismo'
glottography = 'data/glottography'

if __name__ == '__main__':
    packages = [f for f in os.listdir(os.path.expanduser(polys)) if f.endswith('.gpkg')]
    dataframes = []
    for package in packages:
        curr_dataframe = geopandas.read_file(f'{polys}{package}')
        if curr_dataframe.crs != CRS:
            print(f'{package} using some other CRS than {CRS}')
            # curr_dataframe.to_crs(CRS, inplace=True)
            continue
        dataframes.append(curr_dataframe)
    data = geopandas.GeoDataFrame(pd.concat(dataframes, ignore_index=True), crs=CRS)
    data.id = list(data.index + 1)

    # Writing a GeoPackage file
    data.to_file(f'{glottography}/{citation}_raw.gpkg', driver='GPKG')
    (data[['id', 'name', 'map_name_full', 'year', 'glottocode', 'note']]
     .rename(columns={'id': 'polygon_id'})
     .to_csv(f'{glottography}/{citation}_glottocode_to_polygons.csv', index=False))
