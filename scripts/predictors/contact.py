from statistics import median, mean

import geopandas
import pandas as pd
from matplotlib import pyplot as plt
from shapely.geometry.linestring import LineString
from shapely.geometry.point import Point
from shapely.ops import nearest_points

from scripts.families.uralic import Uralic
from scripts.glottolog.trees import glottolog_cherries
from scripts.predictors.polygons.glottography import Glottography, LiterallyNoPolygonException
from scripts.predictors.polygons.glottography_config import get_config
from scripts.predictors.utils import write_out_df

CONTACT_DIR = 'contact'

SEED = 1
N_POINTS = 500


def find_closest_point(start, polygon) -> Point:
    polygon = polygon.geometry.values[0]
    if polygon.contains(start):
        return start
    p1, _ = nearest_points(polygon, start)
    return p1


def calculate_lines(points, other_polygon) -> [LineString]:
    distances = []
    geometry = points.geometry
    for i in range(len(points)):
        point = geometry.values[i]
        end = find_closest_point(point, other_polygon)
        distance = LineString([point, end])
        distances.append(distance)
    return distances


def sample_points(polygon, n_points=N_POINTS):
    return polygon.sample_points(n_points, rng=SEED).explode(index_parts=True)


def write_out_contact(family_name, cherries, mean_distances, median_distances):
    file_name = f'{family_name}.contact.euclidean'
    assert len(cherries) == len(median_distances) == len(median_distances)
    dataframe = pd.DataFrame(data={
        'language_1': [ls[0] for ls in cherries],
        'language_2': [ls[1] for ls in cherries],
        'median_distance': median_distances,
        'mean_distance': mean_distances
    })
    write_out_df(CONTACT_DIR, file_name, dataframe)


def calculate_euclidean_distances(cherries, glottography):
    mean_distances = []
    median_distances = []
    new_cherries = []
    for (language_1, language_2) in cherries:
        try:
            polygon_1 = glottography.get_polygon(language_1)
            polygon_2 = glottography.get_polygon(language_2)
        except LiterallyNoPolygonException as e:
            print(f'Warning: {e} (skipping)')
            continue

        sampled_points = sample_points(polygon_1)

        paths = calculate_lines(sampled_points, polygon_2)
        distances = [p.length for p in paths]

        new_cherries.append((language_1, language_2))
        median_distances.append(median(distances))
        mean_distances.append(mean(distances))

    return new_cherries, mean_distances, median_distances


def double_reverse(cherries):
    reversed_cherries = [c[::-1] for c in cherries]
    return cherries + reversed_cherries


def plot_contact(language_1, language_2, glottography, n_points):
    # Calculate polygons and lines
    polygon_1 = glottography.get_polygon(language_1)
    polygon_2 = glottography.get_polygon(language_2)
    sampled_points = sample_points(polygon_2, n_points)
    paths = calculate_lines(sampled_points, polygon_1)

    # Graph base polygons
    combined = pd.concat([polygon_2, polygon_1])
    base = combined.plot(color='white', edgecolor='black')
    combined.apply(lambda x: base.annotate(text=x['name'], xy=x.geometry.centroid.coords[0], ha='center'), axis=1)

    # Plot individual points
    sampled_points.plot(ax=base, markersize=1)

    # Draw lines
    lines = geopandas.GeoDataFrame(index=list(range(len(paths))), geometry=paths)
    lines.plot(ax=base, color='red')
    plt.show()


if __name__ == '__main__':
    family = Uralic()
    cherries = glottolog_cherries(family)
    cherries = double_reverse(cherries)

    glottography = Glottography(get_config(family.name))
    cherries, mean_distances, median_distances = calculate_euclidean_distances(cherries, glottography)
    # TODO: include language IDs
    write_out_contact(family.name, cherries, mean_distances, median_distances)
    print(f'Wrote out contact distances for {family.name}')

    cherry = ('west2391', 'esto1258')
    plot_contact(cherry[0], cherry[1], glottography, 50)
    plot_contact(cherry[1], cherry[0], glottography, 50)
