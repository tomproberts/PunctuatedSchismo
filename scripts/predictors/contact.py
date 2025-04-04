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


def find_closest_point(start, polygon):
    polygon = polygon['geometry']
    if polygon.contains(start).iloc[0]:
        return start
    p1, _ = nearest_points(polygon, start)
    return p1.geometry.iloc[0]
    # return Point(1575000, 5172177)


if __name__ == '__main__':
    family = Italic()
    cherries = glottolog_cherries(family)
    (oscan_glottocode, umbrian_glottocode) = cherries[-1]

    glottography = Glottography(get_config(family.name))
    oscan = glottography.get_polygon(oscan_glottocode)
    umbrian = glottography.get_polygon(umbrian_glottocode)

    combined = pd.concat([oscan, umbrian])
    base = combined.plot(color='white', edgecolor='black')
    combined.apply(lambda x: base.annotate(text=x['name'], xy=x.geometry.centroid.coords[0], ha='center'), axis=1)
    umbrian_points = umbrian.sample_points(10, rng=10).explode(index_parts=True)
    # oscan_points = oscan.sample_points(100)
    umbrian_points.plot(ax=base, markersize=1)

    # point = Point(1600000, 5152177)
    distances = []
    for i in range(len(umbrian_points)):
        point = umbrian_points.geometry.iloc[i]
        end = find_closest_point(point, oscan)
        distance = LineString([point, end])
        distances.append(distance)
    lines = geopandas.GeoDataFrame(index=list(range(len(distances))), geometry=distances)
    lines.plot(ax=base, color='red')

    plt.show()
