import time
from statistics import median, mean

import geopandas
import pandas as pd
from pyogrio.errors import DataSourceError
from tqdm import tqdm

from scripts.families.indo_european import IndoEuropean
from scripts.predictors.contact import sample_points
from scripts.predictors.polygons.glottography import LiterallyNoPolygonException, Glottography
from scripts.predictors.polygons.glottography_config import get_config

N_POINTS = 50

GEODESIC = 'EPSG:32633'
LONGLAT = 'EPSG:4087'
filter_type = 'perennial'

def read_or_create_relevant_water(family, glottography, water_file):
    print('Loading water features in language areas...')
    relevant_file = f'data/water/tmpFiltered.{family.name}.{filter_type}.gpkg'
    try:
        start = time.time()
        relevant = geopandas.read_file(relevant_file)
        print(f'Loaded intersection in {time.time() - start} seconds')
        return relevant
    except DataSourceError as _:
        print('No cached file found for water filtered to language areas')

    super_polygon = get_super_polygon(family, glottography)
    print('Loading water features...')

    start = time.time()
    water = geopandas.read_file(f'data/water/{water_file}')
    if filter_type == 'perennial':
        # filter for perennial
        print('Filtering for perennial...')
        water = water[water['PERENNIALITY'] != 'Non Perennial']
    print('Loaded water. Calculating intersection...')

    relevant = water.overlay(super_polygon, how='intersection').to_crs(GEODESIC)
    print('Calculated intersection. Writing to file...')
    relevant.to_file(relevant_file, driver='GPKG')
    print('Wrote out intersection')
    print(f'Filtered water in language areas in {time.time() - start} seconds')

    return relevant


def get_super_polygon(family, glottography, save_super=False):
    start = time.time()
    dataframesList = []
    for ascii in family.languages_ascii:
        try:
            p = glottography.get_polygon_from_ascii(family, ascii)
            p.loc[p.index[0], 'geometry'] = p.make_valid(method="structure").iloc[0]
            dataframesList.append(p)
        except Exception as e:
            print(e)

    concatted = pd.concat(dataframesList, ignore_index=True)
    polygons = geopandas.GeoDataFrame(concatted, crs=dataframesList[0].crs, geometry='geometry')
    if 'description' in polygons.columns.values:  # fails to write pama-nyungan polygons to file with this column
        polygons = polygons.drop('description', axis=1)
    if save_super:
        polygons.to_file(f'data/water/tmpAll.{family.name}.gpkg', driver='GPKG')

    super_polygon = polygons.dissolve(as_index=False).to_crs('EPSG:3857')
    if save_super:
        super_polygon.to_file(f'data/water/tmpSuper.{family.name}.geojson', driver='GeoJSON')

    print(f'Constructed super polygon in {time.time() - start} seconds!')
    return super_polygon


if __name__ == '__main__':
    family = IndoEuropean()
    glottography = Glottography(get_config(family.name))
    # glottography = PamaNyunganPolygons()

    water_file = 'OSM_WaterLayer.pbf'
    # water_file = 'SurfaceHydrologyPolygonsNational.gdb'

    # super_polygon = get_super_polygon(family, glottography, save_super=True)
    # start = time.time()
    # water = geopandas.read_file(f'data/water/{water_file}', layer='multipolygons', mask=super_polygon)  # takes 1042 seconds
    # print(f'Loaded water in {time.time() - start} seconds')
    start = time.time()
    # filter to `water='natural'` etc.
    water = geopandas.read_file(f'data/water/tmpFiltered.{family.name}.natural.gpkg')
    print(f'Loaded water in {time.time() - start} seconds')

    # start = time.time()
    # water = water[water['natural'] == 'water']
    # print(f'Filtered water in {time.time() - start} seconds')
    #
    # start = time.time()
    # water.to_file(f'data/water/tmpFiltered.{family.name}.natural.gpkg', driver='GPKG')
    # print(f'Saved water in {time.time() - start} seconds')

    # relevant = read_or_create_relevant_water(family, glottography, water_file)
    relevant = water.to_crs(LONGLAT)
    dataframesList = []
    df_dict = []
    start = time.time()
    for ascii in tqdm(family.languages_ascii):
        try:
            p = glottography.get_polygon_from_ascii(family, ascii).to_crs(LONGLAT)
            start_sub = time.time()
            intersecting = p.overlay(relevant, how='intersection', keep_geom_type=False)
            merged = intersecting.dissolve(as_index=False).to_crs(LONGLAT)
            merged = merged.filter(['Name', 'geometry'])
            print(f'Subset rivers for {ascii} in {time.time() - start_sub} seconds')

            start_sub = time.time()
            points = sample_points(p, N_POINTS)

            d = points.apply(lambda point: merged.distance(point))[0]
            print(f'calculated distances for {ascii} in {time.time() - start_sub} seconds')
            mean_dist = mean(d)
            median_dist = median(d)
            df_dict.append({
                'lang': ascii,
                'mean_distance': round(mean_dist, 3),
                'median_distance': round(median_dist, 3)
            })
            merged['mean_water_distance'] = mean_dist
            merged['median_water_distance'] = median_dist
            dataframesList.append(merged)
        except LiterallyNoPolygonException:
            pass
        except Exception as e:
            print(f'Failed for {ascii}: {e}')  # error '0' means there's no water in the polygon

    print(f'Sorted polygons and calculated distances in {time.time() - start} seconds. Writing out to file...')
    rdf = geopandas.GeoDataFrame(pd.concat(dataframesList, ignore_index=True), crs=dataframesList[0].crs)
    rdf.to_file(f'data/water/tmpSorted.{family.name}.{filter_type}.gpkg', driver='GPKG')
    print('Wrote sorted rivers to file.')

    df = pd.DataFrame.from_records(df_dict)
    file_name = f'{family.name}.water.{filter_type}.{N_POINTS}'
    path = f'data/predictors/water/{file_name}.csv'
    df.to_csv(path, index=False, header=True)
    print(f'Wrote out csv to {path}')
