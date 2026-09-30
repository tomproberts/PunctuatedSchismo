POLYGON_DIR = 'data/polygons'


class LiterallyNoPolygonException(Exception):
    def __init__(self, identifier):
        super().__init__(f"Could not find a polygon for '{identifier}'")


class MultiplePolygonException(Exception):
    def __init__(self, identifier):
        super().__init__(f"Multiple polygons for '{identifier}', please specify")


class PolygonNotFoundException(Exception):
    def __init__(self, polygon_id, source=None):
        if source is None:
            msg = f"Polygon with id '{polygon_id}' not found"
        else:
            msg = f"Polygon with id '{polygon_id}' not found in source '{source}'"
        super().__init__(msg)


class PolygonSource:
    family = 'AbstractPolygonSource'

    def get_polygon_from_ascii(self, ascii):
        raise NotImplemented(f'get_polygon_from_ascii has not been implemented for {self.family}')
