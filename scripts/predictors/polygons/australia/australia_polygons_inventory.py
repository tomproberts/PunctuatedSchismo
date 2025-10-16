import pandas as pd
from thefuzz import process, fuzz

from scripts.families.pama_nyungan import CHIRILA_LANGUAGES_CSV

AUSTRALIAN_POLYGONS = 'data/glottography/australia/AustralianPolygons.kml.csv'
SNAPPED_LANGS = 'data/glottography/australia/SnappedLangs.gpkg.csv'
THRESHOLD = 80  # out of 100

if __name__ == '__main__':
    scorer = fuzz.token_sort_ratio
    # languages in Pama-Nyungan dataset
    languages = pd.read_csv(CHIRILA_LANGUAGES_CSV, na_filter=False)
    languages = list(zip(languages.ID, languages.Glottolog_Name))
    # potential polygons
    australian_polygon_names = list(pd.read_csv(AUSTRALIAN_POLYGONS).name)
    australian_polygon_names = [n.replace(' ', '') for n in australian_polygon_names]
    snapped_langs_names = list(pd.read_csv(SNAPPED_LANGS).name)

    found = []
    not_found = []
    snapped_langs_usefulness = 0
    for (name, glottolog_name) in languages:
        # normal name in `AustralianPolygons.kml`
        polygon, s = process.extractOne(name, australian_polygon_names, scorer=scorer)
        if s >= THRESHOLD:
            found.append(f"{name} → '{polygon}' ({s} points)")
            # found.append({})
            continue

        # glottolog name in `AustralianPolygons.kml`
        if glottolog_name != '':
            polygon, s = process.extractOne(glottolog_name, australian_polygon_names, scorer=scorer)
            if s >= THRESHOLD:
                found.append(f"{name} ({glottolog_name}) → '{polygon}' ({s} points)")
                continue

        # normal name in `SnappedLangs.gpkg`
        polygon, s = process.extractOne(name, snapped_langs_names, scorer=scorer)
        if s >= THRESHOLD:
            found.append(f"{name} → '{polygon}' ({s} points) in snappedLangs")
            snapped_langs_usefulness += 1
            continue

        # glottolog name in `SnappedLangs.gpkg`
        if glottolog_name != '':
            polygon, s = process.extractOne(glottolog_name, snapped_langs_names, scorer=scorer)
            if s >= THRESHOLD:
                found.append(f"{name} ({glottolog_name}) → '{polygon}' ({s} points) in snappedLangs")
                snapped_langs_usefulness += 1
                continue

        # not found
        not_found.append(f"{name} ({glottolog_name}) → '{polygon}' ({s} points)")

    print(f'Found {len(found)} polygons for {len(languages)} total languages ({snapped_langs_usefulness} of which are in `SnappedLangs.gpkg`)')
