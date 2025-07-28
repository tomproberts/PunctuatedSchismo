from scripts.families.uralic import Uralic
from scripts.gammaspike.summary_tree import summary_tree_cherries
from scripts.predictors.polygons.glottography import Glottography
from scripts.predictors.polygons.glottography_config import get_config
from scripts.predictors.polygons.inventory import to_glottolink

if __name__ == '__main__':
    # Load family
    family = Uralic()
    glottography = Glottography(get_config(family.name))

    # Get cherries
    cherries = summary_tree_cherries(family, as_glottocode=False)
    lines = [f'## {family.name}\n']

    clades = ['Cherries']
    for clade in clades:
        lines.append(f'### {clade}')
        lines.append('| `lang1` | `lang2` | `polygon1` | `polygon2` |')
        lines.append('|---------|---------|------------|------------|')
        for (lang1, lang2) in cherries:
            # Get full language name
            name1 = family.get_language_from_ascii(lang1)
            name2 = family.get_language_from_ascii(lang2)
            # Get glottocode
            glotto1 = family.get_glottocode_from_ascii(lang1)
            glotto2 = family.get_glottocode_from_ascii(lang2)
            # Check polygons
            poly1 = glottography.get_source(glotto1)
            poly1 = '❌' if poly1 is None else f'✔ `{poly1}`'
            poly2 = glottography.get_source(glotto2)
            poly2 = '❌' if poly2 is None else f'✔ `{poly2}`'

            # Write line
            lines.append(f'| {name1} {to_glottolink(glotto1)} | {name2} {to_glottolink(glotto2)} | {poly1} | {poly2} |')

    # print(cherries)
    print('\n'.join(lines))
