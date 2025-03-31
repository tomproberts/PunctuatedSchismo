import geopandas
import pandas as pd


class Glottography:
    def __init__(self):
        self._glottocodes = None
        self._countries_gdf = None

    @property
    def glottocodes(self):
        if self._glottocodes is None:
            self._glottocodes = pd.read_csv(
                'data/glottography/bouckaert2012indoeuropean/glottocode_to_polygons.csv',
                index_col=0)[['name', 'glottocode', 'year']]
        return self._glottocodes

    @property
    def countries_gdf(self):
        if self._countries_gdf is None:
            self._countries_gdf = geopandas.read_file('data/glottography/bouckaert2012indoeuropean/raw.gpkg')
        return self._countries_gdf

    def get_polygon(self, glottocode):
        glottocodes = self.glottocodes
        countries_gdf = self.countries_gdf
        polygon_glottocodes = list(glottocodes.glottocode)
        if glottocode in polygon_glottocodes:
            row = glottocodes[glottocodes.glottocode == glottocode]
            if len(row) > 1:
                print(f'Multiple! {row}')
            id = row.index.values[0]
            return countries_gdf[countries_gdf.polygon_id == id]
        return None
