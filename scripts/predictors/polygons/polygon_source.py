from scripts.predictors.polygons.australia.pama_nyungan_polygons import PamaNyunganPolygons
from scripts.predictors.polygons.indoeuropean_polygons import IndoEuropeanPolygons

sources = [IndoEuropeanPolygons, PamaNyunganPolygons]


class Polygons:
    @staticmethod
    def get_source(family_name):
        for source in sources:
            if source.family == family_name:
                return source()
        raise Exception(f'Could not find source for family {family_name}, available: {[source.family for source in sources]}')
