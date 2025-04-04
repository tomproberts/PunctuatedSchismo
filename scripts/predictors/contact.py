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

SEED = None
N_POINTS = 50


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


if __name__ == '__main__':
    family = Italic()
    cherries = glottolog_cherries(family)
    (oscan_glottocode, umbrian_glottocode) = cherries[-1]

    glottography = Glottography(get_config(family.name))
    oscan = glottography.get_polygon(oscan_glottocode)
    umbrian = glottography.get_polygon(umbrian_glottocode)

    base = graph_base_polygons(oscan, umbrian)
    umbrian_points = sample_points(umbrian)

    # plot_points(umbrian_points, base)
    distances = calculate_lines(umbrian_points, oscan)

    draw_lines(distances, base)
    plt.show()
