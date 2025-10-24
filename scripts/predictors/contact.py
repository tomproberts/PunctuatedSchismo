from statistics import median, mean

import geopandas
import pandas as pd
from matplotlib import pyplot as plt
from shapely.geometry.linestring import LineString
from shapely.geometry.point import Point
from shapely.ops import nearest_points
from tqdm import tqdm

from scripts.families.utils import LanguageFamily
from scripts.families.uto_aztecan import UtoAztecan
from scripts.gammaspike.summary_tree import summary_tree_cherries
from scripts.predictors.polygons.glottography import Glottography
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


def calculate_lines(points, other_polygon) -> list[LineString]:
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


def write_out_contact(family_name, df):
    file_name = f'{family_name}.contact.{N_POINTS}'
    write_out_df(CONTACT_DIR, file_name, df)


def calculate_euclidean_distances(family, cherries, glottography) -> pd.DataFrame:
    errors = []
    records = []
    for (language_1, language_2) in tqdm(cherries):
        try:
            glottocode_1 = family.get_glottocode_from_ascii(language_1)
            glottocode_2 = family.get_glottocode_from_ascii(language_2)
            polygon_1 = glottography.get_polygon_from_ascii(family, language_1)
            polygon_2 = glottography.get_polygon_from_ascii(family, language_2)
        except Exception as e:
            errors.append(f'Warning: {e} ({language_1} / {language_2})')
            continue

        sampled_points = sample_points(polygon_1)

        paths = calculate_lines(sampled_points, polygon_2)
        distances = [p.length / 1e3 for p in paths]

        records.append({
            'language_1': language_1,
            'language_2': language_2,
            'glottocode_1': glottocode_1,
            'glottocode_2': glottocode_2,
            'median_distance': median(distances),
            'mean_distance': mean(distances)
        })

    # show skipped languages
    '\n'.join(errors)

    return pd.DataFrame.from_records(records)


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


def calculate_output_contact(family: LanguageFamily, glottography):
    # Cherries should be ascii names since they are unique
    cherries = summary_tree_cherries(family, as_glottocode=False)
    cherries = double_reverse(cherries)
    df = calculate_euclidean_distances(family, cherries, glottography)

    write_out_contact(family.name, df)
    print(f'Wrote out contact distances for {family.name}')


if __name__ == '__main__':
    family = UtoAztecan()
    glottography = Glottography(get_config(family.name))
    # glottography = PamaNyunganPolygons()

    # plot_contact('vlaa1240', 'dutc1256', glottography, 50)

    calculate_output_contact(family, glottography)
