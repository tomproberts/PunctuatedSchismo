import geopandas
import pandas as pd


class Glottography:
    def __init__(self, settings, geodesic=True):
        self.settings = settings
        self.glottocode_map = self.init_glottocode_map(settings.sources)
        self.raw_polygons = self.init_polygons(settings.sources, geodesic)

    @staticmethod
    def init_glottocode_map(sources):
        glottocode_map = []
        for source in sources:
            glottocode_map.append(pd.read_csv(
                f'data/glottography/{source}_glottocode_to_polygons.csv',
                index_col=0)[['name', 'glottocode', 'year']])
        return glottocode_map

    @staticmethod
    def init_polygons(sources, geodesic=True):
        polygons = []
        for source in sources:
            all = geopandas.read_file(f'data/glottography/{source}_raw.gpkg')
            if geodesic:
                all = all.to_crs("EPSG:32633")
            polygons.append(all)
        return polygons

    def get_polygon(self, glottocode, verbose=False):
        # Check patches
        if glottocode in self.settings.patches.keys():
            s, index = self.settings.patches[glottocode]
            raws = self.raw_polygons[s]
            polygon = raws[raws.polygon_id == index]
            if len(polygon) > 0:
                return polygon
            raise PolygonNotFoundException(index)

        # Loop through all sources
        for (glottocodes, raw_polygons) in zip(self.glottocode_map, self.raw_polygons):
            polygon_glottocodes = list(glottocodes.glottocode)
            if glottocode in polygon_glottocodes:
                row = glottocodes[glottocodes.glottocode == glottocode]
                if verbose: print(row)
                if len(row) > 1:
                    raise MultiplePolygonException(glottocode)
                index = row.index.values[0]
                polygon = raw_polygons[raw_polygons.polygon_id == index]
                if len(polygon) > 0:
                    return polygon
                raise PolygonNotFoundException(index)

        # Otherwise not present
        raise LiterallyNoPolygonException(glottocode)

    def get_source(self, glottocode):
        # Check patches
        if glottocode in self.settings.patches.keys():
            s, index = self.settings.patches[glottocode]
            raws = self.raw_polygons[s]
            polygon = raws[raws.polygon_id == index]
            if len(polygon) > 0:
                return self.settings.sources[s]
            raise PolygonNotFoundException(index)

        # Loop through all sources
        for (s, glottocodes) in zip(self.settings.sources, self.glottocode_map):
            polygon_glottocodes = list(glottocodes.glottocode)
            if glottocode in polygon_glottocodes:
                return s
        return None


class GlottographyConfig:
    def __init__(self, sources: list[str], patches: dict[str, tuple[int, int]] = None):
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


class PolygonNotFoundException(Exception):
    def __init__(self, polygon_id, source=None):
        if source is None:
            msg = f"Polygon with id '{polygon_id}' not found"
        else:
            msg = f"Polygon with id '{polygon_id}' not found in source '{source}'"
        super().__init__(msg)
