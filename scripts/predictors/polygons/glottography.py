import geopandas
import pandas as pd


class Glottography:
    def __init__(self, settings):
        self.settings = settings
        self._glottocodes = None
        self._raw_polygons = None

    @property
    def glottocodes(self):
        if self._glottocodes is None:
            self._glottocodes = pd.read_csv(
                f'data/glottography/{self.settings[0]}/glottocode_to_polygons.csv',
                index_col=0)[['name', 'glottocode', 'year']]
        return self._glottocodes

    @property
    def raw_polygons(self):
        if self._raw_polygons is None:
            self._raw_polygons = geopandas.read_file(f'data/glottography/{self.settings[0]}/raw.gpkg')
        return self._raw_polygons

    def get_polygon(self, glottocode):
        glottocodes = self.glottocodes
        raw_polygons = self.raw_polygons
        polygon_glottocodes = list(glottocodes.glottocode)

        index = None
        if glottocode in self.settings.patches.keys():
            _, index = self.settings.patches[glottocode]
        elif glottocode in polygon_glottocodes:
            row = glottocodes[glottocodes.glottocode == glottocode]
            if len(row) > 1:
                print(f'Multiple! {row}')
                raise MultiplePolygonException(glottocode)
            index = row.index.values[0]

        if index is not None:
            return raw_polygons[raw_polygons.polygon_id == index]
        raise LiterallyNoPolygonException(glottocode)


class GlottographyConfig:
    def __init__(self, sources: [str], patches: {str: (int, int)} = None):
        if patches is None:
            patches = {}
        self.patches = patches
        self.sources = sources

    def __getitem__(self, source_index: int):
        if len(self.sources) == 0:
            raise RuntimeError('No sources defined for Glottography config')
        if source_index < len(self.sources):
            return self.sources[source_index]
        else:
            raise IndexError(f'Index {source_index} is out of range for config sources')


class LiterallyNoPolygonException(Exception):
    def __init__(self, glottocode):
        super().__init__(f"Could not find a polygon for '{glottocode}'")


class MultiplePolygonException(Exception):
    def __init__(self, glottocode):
        super().__init__(f"Multiple polygons for '{glottocode}', please specify")
