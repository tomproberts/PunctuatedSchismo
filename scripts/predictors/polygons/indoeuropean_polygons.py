import geopandas

from scripts.predictors.polygons.poly_utils import PolygonSource, PolygonNotFoundException, \
    MultiplePolygonException, POLYGON_DIR


class IndoEuropeanPolygons(PolygonSource):
    family = 'IndoEuropean'
    geojson = f'{POLYGON_DIR}/indoeuropean/features.geojson'

    def __init__(self):
        self.polygons = geopandas.read_file(self.geojson).to_crs('EPSG:32633')

    def get_polygon_from_ascii(self, ascii):
        row = self.polygons[self.polygons.ascii == ascii]
        if row.empty:
            raise PolygonNotFoundException(ascii, self.geojson)
        if len(row) > 1:
            raise MultiplePolygonException(ascii)
        return row
