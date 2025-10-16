import pandas as pd
from thefuzz import process, fuzz

from scripts.families.pama_nyungan import CHIRILA_LANGUAGES_CSV

AUSTRALIA = 'data/glottography/australia/'
AUSTRALIAN_POLYGONS = 'AustralianPolygons.kml'
SNAPPED_LANGS = 'SnappedLangs.gpkg'
OUT_CSV = 'pamanyungan-polygons.csv'

THRESHOLD = 85  # out of 100
scorer = fuzz.token_sort_ratio

if __name__ == '__main__':
    # languages in Pama-Nyungan dataset
    languages = pd.read_csv(CHIRILA_LANGUAGES_CSV, na_filter=False)
    languages = list(zip(languages.ID, languages.Glottocode, languages.Glottolog_Name))
    # potential polygons
    australian_polygon_names = list(pd.read_csv(f'{AUSTRALIA}{AUSTRALIAN_POLYGONS}.csv').name)
    snapped_langs_names = list(pd.read_csv(f'{AUSTRALIA}{SNAPPED_LANGS}.csv').name)

    found = []
    not_found = []
    snapped_count = 0
    for (name, glottocode, glottolog_name) in languages:
        # normal name in `AustralianPolygons.kml`
        polygon, s = process.extractOne(name, australian_polygon_names, scorer=scorer)
        if s >= THRESHOLD:
            # found.append(f"{name} → '{polygon}' ({s} points)")
            found.append({
                "language_id": name,
                "glottocode": glottocode,
                "glottolog_name": glottolog_name,
                "polygon_file": AUSTRALIAN_POLYGONS,
                "polygon_name": polygon,
                "fuzzy_score": s,
                "polygon_group": ""
            })
            continue

        # glottolog name in `AustralianPolygons.kml`
        if glottolog_name != '':
            polygon, s = process.extractOne(glottolog_name, australian_polygon_names, scorer=scorer)
            if s >= THRESHOLD:
                # found.append(f"{name} ({glottolog_name}) → '{polygon}' ({s} points)")
                found.append({
                    "language_id": name,
                    "glottocode": glottocode,
                    "glottolog_name": glottolog_name,
                    "polygon_file": AUSTRALIAN_POLYGONS,
                    "polygon_name": polygon,
                    "fuzzy_score": s,
                    "polygon_group": ""
                })
                continue

        # normal name in `SnappedLangs.gpkg`
        polygon, s = process.extractOne(name, snapped_langs_names, scorer=scorer)
        if s >= THRESHOLD:
            # found.append(f"{name} → '{polygon}' ({s} points) in snappedLangs")
            found.append({
                "language_id": name,
                "glottocode": glottocode,
                "glottolog_name": glottolog_name,
                "polygon_file": SNAPPED_LANGS,
                "polygon_name": polygon,
                "fuzzy_score": s,
                "polygon_group": ""
            })
            snapped_count += 1
            continue

        # glottolog name in `SnappedLangs.gpkg`
        if glottolog_name != '':
            polygon, s = process.extractOne(glottolog_name, snapped_langs_names, scorer=scorer)
            if s >= THRESHOLD:
                # found.append(f"{name} ({glottolog_name}) → '{polygon}' ({s} points) in snappedLangs")
                found.append({
                    "language_id": name,
                    "glottocode": glottocode,
                    "glottolog_name": glottolog_name,
                    "polygon_file": SNAPPED_LANGS,
                    "polygon_name": polygon,
                    "fuzzy_score": s,
                    "polygon_group": ""
                })
                snapped_count += 1
                continue

        # not found
        not_found.append(f"{name} ({glottolog_name}) → '{polygon}' ({s} points)")

    print(f'Found {len(found)} polygons for {len(languages)} total languages ({snapped_count} in `{SNAPPED_LANGS}`)')

    # Convert to dataframe, write out to csv
    out_file = f'{AUSTRALIA}{OUT_CSV}'
    df = pd.DataFrame.from_records(found)
    df.to_csv(out_file, index=False)
    print(f'Wrote {len(found)} rows to {out_file}')
