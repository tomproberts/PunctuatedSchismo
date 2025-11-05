import time
from statistics import median, mean

import geopandas
import pandas as pd
from pyogrio.errors import DataSourceError
from tqdm import tqdm

from scripts.families.pama_nyungan import PamaNyungan
from scripts.predictors.contact import sample_points
from scripts.predictors.polygons.australia.pama_nyungan_polygons import PamaNyunganPolygons
from scripts.predictors.polygons.glottography import LiterallyNoPolygonException

N_POINTS = 50

GEODESIC = 'EPSG:32633'


def read_or_create_relevant_water(family, glottography):
    print('Loading water features in language areas...')
    try:
        start = time.time()
        relevant = geopandas.read_file('data/water/PamaNyunganWaterIntersect.gpkg')
        print(f'Loaded intersection in {time.time() - start} seconds')
        return relevant
    except DataSourceError as _:
        print('No cached file found for water filtered to language areas')

    start = time.time()
    dataframesList = []
    for ascii in family.languages_ascii:
        try:
            p = glottography.get_polygon_from_ascii(family, ascii)
            dataframesList.append(p)
        except Exception as e:
            print(e)

    crs = dataframesList[0].crs
    polygons = geopandas.GeoDataFrame(pd.concat(dataframesList, ignore_index=True), crs=crs)
    polygons = polygons.make_valid()
    polygons = geopandas.GeoDataFrame(geometry=polygons, crs=crs)
    super_polygon = polygons.dissolve(as_index=False).to_crs('EPSG:4283')
    # super_polygon.to_file('data/water/PamaNyunganSuper.geojson', driver='GeoJSON')
    print('Constructed super polygon! Loading water features...')

    water = geopandas.read_file('data/water/SurfaceHydrologyPolygonsNational.gdb')
    print('Loaded water. Calculating intersection...')
    relevant = water.overlay(super_polygon, how='intersection').to_crs(GEODESIC)
    print('Calculated intersection. Writing to file...')
    relevant.to_file('data/water/PamaNyunganWaterIntersect.gpkg', driver='GPKG')
    print('Wrote out intersection')
    print(f'Filtered water in language areas in {time.time() - start} seconds')

    return relevant


if __name__ == '__main__':
    family = PamaNyungan()
    glottography = PamaNyunganPolygons()

    relevant = read_or_create_relevant_water(family, glottography)

    dataframesList = []
    df_dict = []
    start = time.time()
    for ascii in tqdm(family.languages_ascii):
        try:
            p = glottography.get_polygon_from_ascii(family, ascii).to_crs(GEODESIC)
            intersecting = p.overlay(relevant, how='intersection', keep_geom_type=False)
            merged = intersecting.dissolve(as_index=False).to_crs(GEODESIC)
            merged = merged.filter(['Name', 'geometry'])

            points = sample_points(p, N_POINTS)

            d = points.apply(lambda point: merged.distance(point))[0]
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
            print(f'Failed for {ascii}: {e}')

    print(f'Sorted polygons and calculated distances in {time.time() - start} seconds. Writing out to file...')
    rdf = geopandas.GeoDataFrame(pd.concat(dataframesList, ignore_index=True), crs=dataframesList[0].crs)
    rdf.to_file('data/water/LanguageMapRiver.gpkg', driver='GPKG')
    print('Wrote sorted rivers to file.')

    df = pd.DataFrame.from_records(df_dict)
    file_name = f'{family.name}.water.all.{N_POINTS}'
    path = f'data/predictors/water/{file_name}.csv'
    df.to_csv(path, index=False, header=True)
    print(f'Wrote out csv to {path}')
