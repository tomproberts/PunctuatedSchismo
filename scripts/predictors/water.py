import time
from statistics import median

import geopandas
import pandas as pd
from pyogrio.errors import DataSourceError
from tqdm import tqdm

from scripts.families.pama_nyungan import PamaNyungan
from scripts.predictors.contact import sample_points
from scripts.predictors.polygons.australia.pama_nyungan_polygons import PamaNyunganPolygons
from scripts.predictors.polygons.glottography import LiterallyNoPolygonException

N_POINTS = 50


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
    relevant = water.overlay(super_polygon, how='intersection').to_crs('EPSG:32633')
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
    for ascii in tqdm(family.languages_ascii):
        try:
            p = glottography.get_polygon_from_ascii(family, ascii).to_crs('EPSG:32633')
            intersecting = p.overlay(relevant, how='intersection', keep_geom_type=False)
            merged = intersecting.dissolve(as_index=False).to_crs('EPSG:32633')
            merged = merged.filter(['Name', 'geometry'])

            points = sample_points(p, N_POINTS)

            d = points.apply(lambda point: merged.disance(point))[0]
            median_dist = median(d)
            df_dict.append({
                'ascii': ascii,
                'distance': median_dist
            })
            merged['waterdistance'] = median_dist
            dataframesList.append(merged)
        except LiterallyNoPolygonException:
            pass
        except Exception as e:
            print(e)

    rdf = geopandas.GeoDataFrame(pd.concat(dataframesList, ignore_index=True), crs=dataframesList[0].crs)
    rdf.to_file('data/water/LanguageMapRiver.gpkg', driver='GPKG')

    df = pd.DataFrame.from_records(df_dict)
    file_name = f'{family.name}.water.all'
    df.to_csv(f'data/water/{file_name}.csv', index=False, header=True)
