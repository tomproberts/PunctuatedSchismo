import os.path
import time
from statistics import median, mean

import geopandas
import pandas as pd
from tqdm import tqdm

from scripts.families.indo_european import IndoEuropean
from scripts.families.pama_nyungan import PamaNyungan
from scripts.families.uto_aztecan import UtoAztecan
from scripts.predictors.contact import sample_points
from scripts.predictors.polygons.australia.pama_nyungan_polygons import PamaNyunganPolygons
from scripts.predictors.polygons.glottography import LiterallyNoPolygonException, Glottography
from scripts.predictors.polygons.glottography_config import get_config

N_POINTS = 50

CRS_CONIC = 'ESRI:53027'
CRS_CYLINDRICAL = 'EPSG:4087'
CRS_AUSTRALIAN = 'EPSG:4283'
WATER_DIR = 'data/water'

AUSTRALIA_LINES = 'SurfaceHydrologyLinesNational.gdb'
AUSTRALIA_POLYS = 'SurfaceHydrologyPolygonsNational.gdb'


def get_super_polygon(family, glottography, save_super=False):
    start = time.time()
    dataframesList = []
    for ascii in family.languages_ascii:
        try:
            p = glottography.get_polygon_from_ascii(family, ascii)
            p.loc[p.index[0], 'geometry'] = p.make_valid(method='structure').iloc[0]
            dataframesList.append(p)
        except Exception as e:
            print(e)

    concatted = pd.concat(dataframesList, ignore_index=True)
    polygons = geopandas.GeoDataFrame(concatted, crs=dataframesList[0].crs, geometry='geometry')
    if 'description' in polygons.columns.values:  # fails to write pama-nyungan polygons to file with this column
        polygons = polygons.drop('description', axis=1)
    if save_super:
        polygons.to_file(f'{WATER_DIR}/tmpPolygons.{family.name}.gpkg', driver='GPKG')

    super_polygon = polygons.dissolve(as_index=False).to_crs('EPSG:3857')
    if save_super:
        super_polygon.to_file(f'{WATER_DIR}/tmpSuper.{family.name}.geojson', driver='GeoJSON')

    print(f'Constructed super polygon in {time.time() - start} seconds!')
    return super_polygon


def read_australia_water(super_polygon, polygons=True, lines=False):
    assert polygons or lines
    if polygons:
        print('Loading water polygon features for Australia...')
        start = time.time()
        water = geopandas.read_file(f'{WATER_DIR}/{AUSTRALIA_POLYS}', mask=super_polygon)
        water_polys = water[water['PERENNIALITY'] != 'Non Perennial']
        water_polys = water_polys.to_crs(CRS_AUSTRALIAN)

        print(f'Loaded water polygons in {time.time() - start} seconds. Saving to file...')
        start = time.time()
        water_polys.to_file(f'{WATER_DIR}/{temp_river_gpkg_name(family, polygons=True, lines=False)}', driver='GPKG')
        print(f'Saved water polygons in {time.time() - start} seconds.')
        if not lines:
            return water_polys
    if lines:
        print('Loading water line features for Australia...')
        start = time.time()
        water = geopandas.read_file(f'{WATER_DIR}/{AUSTRALIA_LINES}', mask=super_polygon)
        water_lines = water[water['PERENNIALITY'] != 'Non Perennial']
        water_lines = water_lines.to_crs(CRS_AUSTRALIAN)

        print(f'Loaded water lines in {time.time() - start} seconds. Saving to file...')
        start = time.time()
        water_lines.to_file(f'{WATER_DIR}/{temp_river_gpkg_name(family, polygons=False, lines=True)}', driver='GPKG')
        print(f'Saved water lines in {time.time() - start} seconds.')
        if not polygons:
            return water_lines

    print('Merging polygon features and line features...')
    start = time.time()
    water = geopandas.GeoDataFrame(pd.concat([water_polys, water_lines], ignore_index=True), crs=CRS_AUSTRALIAN)
    print(f'Merged water in {time.time() - start} seconds')

    print('Saving water features...')
    start = time.time()
    water.to_file(f'{WATER_DIR}/{temp_river_gpkg_name(family, polygons=True, lines=True)}', driver='GPKG')
    print(f'Saved all water features in {time.time() - start} seconds')

    return water


def read_osm_water(super_polygon, polygons=True, lines=False, save=True, make_valid=True):
    assert polygons and not lines
    print('Loading OSM water layer, this may take ~15 minutes...')
    start = time.time()
    water_file = 'OSM_WaterLayer.pbf'
    water = geopandas.read_file(f'{WATER_DIR}/{water_file}', layer='multipolygons', mask=super_polygon)
    print(f'Loaded water in {time.time() - start} seconds')

    print('Projecting to CONIC...')
    start = time.time()
    water = water.to_crs(CRS_CONIC)
    print(f'Projected to CONIC in {time.time() - start} seconds.')

    if make_valid:
        print('Forcing OSM water features to valid geometries...')
        start = time.time()
        valid = water.make_valid(method='structure')
        assert len(valid) == len(water)
        water['geometry'] = valid
        print(f'Made geometries valid in {time.time() - start} seconds')

    if save:
        print(f'Saving masked OSM water...')
        start = time.time()
        water.to_file(f'{WATER_DIR}/{temp_river_gpkg_name(family, polygons, lines)}', driver='GPKG')
        print(f'Wrote masked OSM in {time.time() - start} seconds')

    return water


def get_subset_type(polygons=True, lines=False):
    assert polygons or lines
    if polygons:
        return 'all' if lines else 'polygons'
    else:
        return 'lines'


def temp_river_gpkg_name(family, polygons=True, lines=False):
    assert polygons or lines
    return f'tmpFiltered.{family.name}.{get_subset_type(polygons, lines)}.gpkg'


def load_cached_water(family, polygons=True, lines=True):
    assert polygons or lines
    filename = f'{WATER_DIR}/{temp_river_gpkg_name(family, polygons, lines)}'
    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)

    masked_rivers_file = temp_river_gpkg_name(family, polygons, lines)
    print(f'Loading cached water (masked) from {masked_rivers_file}...')
    start = time.time()
    water = geopandas.read_file(f'{WATER_DIR}/{masked_rivers_file}')
    print(f'Loaded water in {time.time() - start} seconds!')
    return water


if __name__ == '__main__':
    USE_POLYGONS = True
    USE_LINES = True
    PROJECTION = CRS_CONIC

    family = PamaNyungan()
    # glottography = Glottography(get_config(family.name))
    glottography = PamaNyunganPolygons()

    try:
        water = load_cached_water(family, USE_POLYGONS, USE_LINES)
    except FileNotFoundError:
        super_polygon = get_super_polygon(family, glottography, save_super=True)
        if family.name == 'PamaNyungan':
            water = read_australia_water(super_polygon, USE_POLYGONS, USE_LINES)
        else:
            water = read_osm_water(super_polygon, USE_POLYGONS, USE_LINES)

    print(f'Reprojecting to {PROJECTION}...')
    start = time.time()
    water = water.to_crs(PROJECTION)
    print(f'Took {time.time() - start} seconds to reproject to {PROJECTION}')

    file_name = f'{family.name}.water.{get_subset_type(USE_POLYGONS, USE_LINES)}.{N_POINTS}'
    path = f'data/predictors/water/{file_name}.csv'

    asciis_to_calculate = family.languages_ascii
    try:
        df = pd.read_csv(path)
        already_done = set(df['lang'])
        asciis_to_calculate = list(set(asciis_to_calculate) - already_done)
    except FileNotFoundError:
        df = pd.DataFrame({
            'lang': [],
            'mean_distance': [],
            'median_distance': []
        })
        df.to_csv(path, index=False, header=True)

    print(f'Calculating water distance for {len(asciis_to_calculate)} languages...')
    start = time.time()
    for ascii in tqdm(asciis_to_calculate):
        # todo: multi-thread this
        try:
            p = glottography.get_polygon_from_ascii(family, ascii).to_crs(PROJECTION)
            p = p.make_valid(method='structure')
            intersecting = geopandas.clip(water, mask=p, keep_geom_type=False)
            # intersecting = p.overlay(water, how='intersection', keep_geom_type=False)
            merged = intersecting.dissolve(as_index=False).to_crs(PROJECTION)
            merged = merged.filter(['Name', 'geometry'])

            points = sample_points(p, N_POINTS)

            d = points.apply(lambda point: merged.distance(point))[0]
            mean_dist = mean(d)
            median_dist = median(d)
            df = pd.DataFrame({
                'lang': [ascii],
                'mean_distance': [round(mean_dist, 3)],
                'median_distance': [round(median_dist, 3)]
            })
            df.to_csv(path, mode='a', index=False, header=False)
            merged['mean_water_distance'] = mean_dist
            merged['median_water_distance'] = median_dist
            # dataframesList.append(merged)
        except LiterallyNoPolygonException:
            pass
        except Exception as e:
            print(f'Failed for {ascii}: {e}')  # error '0' means there's no water in the polygon

    print(f'Sorted polygons and calculated distances in {time.time() - start} seconds. Writing out to file...')
    # rdf = geopandas.GeoDataFrame(pd.concat(dataframesList, ignore_index=True), crs=dataframesList[0].crs)
    # rdf.to_file(f'{WATER_DIR}/tmpSorted.{family.name}.{filter_type}.gpkg', driver='GPKG')
    # print('Wrote sorted rivers to file.')

    print(f'Wrote out csv to {path}')
