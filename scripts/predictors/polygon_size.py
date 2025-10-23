import pandas as pd
from tqdm import tqdm

from scripts.families.pama_nyungan import PamaNyungan
from scripts.predictors.polygons.australia.pama_nyungan_polygons import PamaNyunganPolygons
from scripts.predictors.polygons.glottography import LiterallyNoPolygonException, MultiplePolygonException, \
    PolygonNotFoundException
from scripts.predictors.utils import write_out_df

POLYGON_SIZE = 'area'


def area_of_polygon(polygon_df_row):
    return round(polygon_df_row.area.iloc[0] / 1e6, 0)


def write_out_polygon_size(dataframe, family_name, type):
    file_name = f'{family_name}.{type}'
    write_out_df(POLYGON_SIZE, file_name, dataframe)


def calculate_areas(glottography, asciis):
    df_data = []
    errors = []
    for lang in tqdm(asciis):
        try:
            # Collect polygon and lang meta
            code = family.get_glottocode_from_ascii(lang)
            polygon = glottography.get_polygon_from_ascii(family, lang)
            area = area_of_polygon(polygon)
            # Add to list
            df_data.append({'lang': lang, 'glottocode': code, 'area': area})
        except (LiterallyNoPolygonException, MultiplePolygonException, PolygonNotFoundException) as e:
            errors.append(f'{e} ({family.get_language_from_ascii(lang)})')

    # Display errors
    print('\n'.join(errors))
    return pd.DataFrame.from_records(df_data)


if __name__ == '__main__':
    # Get family and glottography setup
    family = PamaNyungan()
    # glottography = Glottography(get_config(family.name), geodesic=True)
    glottography = PamaNyunganPolygons(geodesic=True)

    # Calculate and save as csv the polygon areas
    df = calculate_areas(glottography, family.languages_ascii)
    write_out_polygon_size(df, family.name, type='geodesic')
    print(f'Wrote out polygon sizes for {family.name}')
