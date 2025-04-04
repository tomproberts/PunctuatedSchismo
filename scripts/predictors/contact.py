from statistics import median, mean

import geopandas
import pandas as pd
from matplotlib import pyplot as plt
from shapely.geometry.linestring import LineString
from shapely.geometry.point import Point
from shapely.ops import nearest_points

from scripts.families.indo_european import Italic
from scripts.glottolog.trees import glottolog_cherries
from scripts.predictors.polygons.glottography import Glottography
from scripts.predictors.polygons.glottography_config import get_config
from scripts.predictors.utils import write_out_df

CONTACT_DIR = 'contact'

SEED = None
N_POINTS = 50
GRAPH = False


def find_closest_point(start, polygon) -> Point:
    polygon = polygon.geometry.values[0]
    if polygon.contains(start):
        return start
    p1, _ = nearest_points(polygon, start)
    return p1


def graph_base_polygons(polygon_1, polygon_2):
    combined = pd.concat([polygon_1, polygon_2])
    base = combined.plot(color='white', edgecolor='black')
    combined.apply(lambda x: base.annotate(text=x['name'], xy=x.geometry.centroid.coords[0], ha='center'), axis=1)
    return base


def plot_points(polygon_points, base):
    polygon_points.plot(ax=base, markersize=1)


def draw_lines(distances, base):
    lines = geopandas.GeoDataFrame(index=list(range(len(distances))), geometry=distances)
    lines.plot(ax=base, color='red')


def calculate_lines(points, other_polygon) -> [LineString]:
    distances = []
    geometry = points.geometry
    for i in range(len(points)):
        point = geometry.values[i]
        end = find_closest_point(point, other_polygon)
        distance = LineString([point, end])
        distances.append(distance)
    return distances


def sample_points(polygon):
    return polygon.sample_points(N_POINTS, rng=SEED).explode(index_parts=True)


def write_out_contact(family_name, cherries, mean_distances, median_distances):
    file_name = f'{family_name}.contact'
    assert len(cherries) == len(median_distances) == len(median_distances)
    dataframe = pd.DataFrame(data={
        'language_1': [ls[0] for ls in cherries],
        'language_2': [ls[1] for ls in cherries],
        'median_contact': median_distances,
        'mean_contact': mean_distances
    })
    write_out_df(CONTACT_DIR, file_name, dataframe)


if __name__ == '__main__':
    family = Italic()
    cherries = glottolog_cherries(family)
    cherries = [cherries[-1], cherries[2], cherries[-2]]

    glottography = Glottography(get_config(family.name))
    mean_distances = []
    median_distances = []
    for (language_1, language_2) in cherries:
        polygon_1 = glottography.get_polygon(language_1)
        polygon_2 = glottography.get_polygon(language_2)

        umbrian_points = sample_points(polygon_2)

        paths = calculate_lines(umbrian_points, polygon_1)
        distances = [p.length for p in paths]

        median_distances.append(median(distances))
        mean_distances.append(mean(distances))

        if GRAPH:
            base = graph_base_polygons(polygon_1, polygon_2)
            # plot_points(umbrian_points, base)
            draw_lines(paths, base)
            plt.show()

    write_out_contact(family.name, cherries, mean_distances, median_distances)
