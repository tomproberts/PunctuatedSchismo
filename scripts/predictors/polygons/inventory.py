from scripts.families.indo_european import IndoEuropean
from scripts.gammaspike.summary_tree import summary_tree_cherries
from scripts.predictors.polygons.glottography import Glottography, LiterallyNoPolygonException
from scripts.predictors.polygons.glottography_config import get_config

if __name__ == '__main__':
    family = IndoEuropean()
    glottography = Glottography(get_config(family.name))

    # Find missing
    not_present = []
    for glottocode in family.glottocodes:
        try:
            _ = glottography.get_polygon(glottocode)
        except LiterallyNoPolygonException:
            not_present.append(glottocode)

    # Find consequences
    half_cherries = []
    both_missing = []
    for (l1, l2) in summary_tree_cherries(family):
        if l1 in not_present:
            if l2 not in not_present:
                half_cherries.append(l1)
            else:
                both_missing.append((l1, l2))
        elif l2 in not_present:
            half_cherries.append(l2)

    # Output consequences
    if len(half_cherries) > 0:
        print(f'{len(half_cherries)} broken cherries (only one polygon out of two):')
        half_cherries = set(half_cherries)
        for l in half_cherries:
            print(f'- †cherry, because {family.get_language(l)} ({l}) missing')

    if len(both_missing) > 0:
        print(f'{len(both_missing)} dead cherries (neither polygon present):')
        for (l1, l2) in both_missing:
            print(f'- †cherry, because both {family.get_language(l1)} ({l1}) and {family.get_language(l2)} ({l2}) missing')
