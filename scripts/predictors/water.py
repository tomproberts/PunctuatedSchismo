import time

import geopandas
import pandas as pd
from pyogrio.errors import DataSourceError
from tqdm import tqdm

from scripts.families.pama_nyungan import PamaNyungan
from scripts.predictors.polygons.australia.pama_nyungan_polygons import PamaNyunganPolygons


def read_or_create_relevant_water(family, glottography):
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
            pass

    crs = dataframesList[0].crs
    polygons = geopandas.GeoDataFrame(pd.concat(dataframesList, ignore_index=True), crs=crs)
    polygons = polygons.make_valid()
    polygons = geopandas.GeoDataFrame(geometry=polygons, crs=crs)
    super_polygon = polygons.dissolve(as_index=False).to_crs('EPSG:4283')
    # super_polygon.to_file('data/water/PamaNyunganSuper.geojson', driver='GeoJSON')
    print('Constructed super polygon!')

    water = geopandas.read_file('data/water/SurfaceHydrologyPolygonsNational.gdb')
    print('Loaded water')
    relevant = water.overlay(super_polygon, how='intersection')
    print('Calculated intersection')
    relevant.to_file('data/water/PamaNyunganWaterIntersect.gpkg', driver='GPKG')
    print('Wrote out intersection')
    print(f'Filtered water in language areas in {time.time() - start} seconds')

    return relevant


if __name__ == '__main__':
    family = PamaNyungan()
    glottography = PamaNyunganPolygons()

    relevant = read_or_create_relevant_water(family, glottography)

    dataframesList = []
    for ascii in tqdm(family.languages_ascii):
        try:
            p = glottography.get_polygon_from_ascii(family, ascii).to_crs('EPSG:4283')
            intersecting = p.overlay(relevant, how='intersection')
            merged = intersecting.dissolve(as_index=False).to_crs('EPSG:4283')
            dataframesList.append(merged.filter(['Name', 'geometry']))
        except Exception as e:
            pass

    rdf = geopandas.GeoDataFrame(pd.concat(dataframesList, ignore_index=True), crs=dataframesList[0].crs)
    rdf.to_file('data/water/LanguageMapRiver.gpkg', driver='GPKG')
