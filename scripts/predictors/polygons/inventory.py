from scripts.families.sino_tibetan import SinoTibetan
from scripts.phylo.summary_tree import summary_tree_cherries, NoSummaryTree
from scripts.predictors.polygons.glottography import Glottography, LiterallyNoPolygonException
from scripts.predictors.polygons.glottography_config import get_config


def to_glottolink(glottocode):
    return f'[{glottocode}](https://glottolog.org/resource/languoid/id/{glottocode})'


if __name__ == '__main__':
    family = SinoTibetan()
    n_langs = len(family.languages)
    glottography = Glottography(get_config(family.name))

    # Find missing
    not_present = []
    for glottocode in family.glottocodes:
        try:
            _ = glottography.get_polygon(glottocode)
        except LiterallyNoPolygonException:
            not_present.append(glottocode)

    # Find broken cherries
    half_cherries = []
    both_missing = []
    summary_cherries = []
    try:
        summary_cherries = summary_tree_cherries(family)
        for (l1, l2) in summary_cherries:
            if l1 in not_present:
                if l2 not in not_present:
                    half_cherries.append(l1)
                else:
                    both_missing.append((l1, l2))
            elif l2 in not_present:
                half_cherries.append(l2)
    except NoSummaryTree:
        pass

    # Output consequences
    print(f'### *{family.name}* ({n_langs} taxa)')
    # Summary
    print('\nSummary:')
    if summary_cherries:
        n_complete_cherries = len(summary_cherries) - len(half_cherries) - len(both_missing)
        print(f'- {n_complete_cherries} out of {len(summary_cherries)} cherries present')
    else:
        print('- NO SUMMARY TREE FOUND = NO CHERRY INFORMATION')
    print(f'- {n_langs - len(not_present)} out of {n_langs} polygons present')

    # Mention duplicates
    duplicates = family.get_duplicate_glottocodes()
    if len(duplicates) > 0:
        for dup_glottocode in duplicates:
            language_names = family.get_languages_from_glottocode(dup_glottocode)
            print(f"- '{dup_glottocode}' ({", ".join(language_names)}) have the same polygon")

    if summary_cherries:
        # Half-broken cherries
        if len(half_cherries) > 0:
            print(f'\n{len(half_cherries)} broken cherries (only one polygon out of two):')
            half_cherries = set(half_cherries)
            for l in half_cherries:
                lang = family.get_languages_from_glottocode(l)
                display = lang[0] if len(lang) == 1 else f"({', '.join(lang)})"
                print(f'- †cherry, because {display} ({to_glottolink(l)}) missing')

        # Fully-broken cherries
        if len(both_missing) > 0:
            print(f'\n{len(both_missing)} dead cherries (neither polygon present):')
            for (l1, l2) in both_missing:
                lang = family.get_languages_from_glottocode(l1)
                display_1 = lang[0] if len(lang) == 1 else f"({', '.join(lang)})"
                lang = family.get_languages_from_glottocode(l2)
                display_2 = lang[0] if len(lang) == 1 else f"({', '.join(lang)})"
                print(
                    f'- †cherry, because both {display_1} ({to_glottolink(l1)}) and {display_2} ({to_glottolink(l2)}) missing')

    else:  # No tree, so just list missing polygons
        print(f'\n{len(not_present)} missing polygons:')
        for p in not_present:
            lang = family.get_languages_from_glottocode(p)
            display = lang[0] if len(lang) == 1 else f"({', '.join(lang)})"
            print(f'- {display} ({to_glottolink(p)})')
