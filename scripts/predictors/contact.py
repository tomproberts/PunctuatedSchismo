import geopandas
import pandas as pd
import shapely.plotting
from matplotlib import pyplot as plt
from shapely.geometry.point import Point

from scripts.families.indo_european import Italic
from scripts.glottolog.trees import glottolog_cherries
from scripts.predictors.polygons.glottography import Glottography
from scripts.predictors.polygons.glottography_config import get_config

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
    umbrian_points = umbrian.sample_points(100, rng=10)
    # oscan_points = oscan.sample_points(100)
    umbrian_points.plot(ax=base, markersize=1)

    point = Point(1500000, 5252177)
    geo_point = geopandas.GeoDataFrame(index=[0], geometry=[point])
    geo_point.plot(ax=base, color='red')

    plt.show()
