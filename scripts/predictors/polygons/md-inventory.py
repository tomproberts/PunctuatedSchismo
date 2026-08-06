from scripts.families.indo_european import IndoEuropean
from scripts.phylo.summary_tree import get_sorted_summary_tree_cherries_ascii
from scripts.predictors.polygons.glottography import Glottography
from scripts.predictors.polygons.glottography_config import get_config
from scripts.predictors.polygons.inventory import to_glottolink


def to_ie_cor(name, ascii):
    return f'[{name}](https://iecor.clld.org/languages/{ascii.lower()})'


def polygon_cherries_inventory_markdown(family, glottography):
    # Get cherries
    clades_cherries = get_sorted_summary_tree_cherries_ascii(family)

    lines = []
    missing = 0
    len_cherries = 0
    for (clade, cherries) in clades_cherries:
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
            poly2 = glottography.get_source(glotto2)
            if poly1 is None or poly2 is None: missing += 1

            # Stringify
            poly1 = '❌' if poly1 is None else f'✔ `{poly1}`'
            poly2 = '❌' if poly2 is None else f'✔ `{poly2}`'

            # If duplicate, don't count
            if glotto1 == glotto2:
                missing += 1
                poly2 = '?❌ (duplicate)'

            # Write line
            lines.append(f'| {name1} {to_glottolink(glotto1)} | {name2} {to_glottolink(glotto2)} | {poly1} | {poly2} |')

        len_cherries += len(cherries)
        lines.append('')

    # Header
    header = []
    header.append(f'## *{family.name}* ({len(family.languages)} taxa)')
    header.append('### Summary')
    header.append(f'- {len_cherries - missing} out of {len_cherries} cherries present')
    # Warn about duplicate polygons
    duplicates = sorted(family.get_duplicate_glottocodes())
    if len(duplicates) > 0:
        for dup_glottocode in duplicates:
            language_names = family.get_languages_from_glottocode(dup_glottocode)
            header.append(f"- '{dup_glottocode}' ({', '.join(language_names)}) have the same polygon")
    header.append('')

    # Write out
    lines = header + lines
    return '\n'.join(lines)


def all_polygon_inventory_markdown(family, glottography, all=False):
    langs = family.languages_ascii
    # initialise clade sorting
    clade_dict = {}
    for clade in family.get_clades():
        clade_dict[clade] = []
    clade_dict['Miscellaneous'] = []
    # sort into clades
    for ascii in langs:
        clade = family.get_clade_from_ascii(ascii)
        if clade not in clade_dict:
            clade = 'Miscellaneous'
        clade_dict[clade].append(ascii)

    # inventory
    lines = []
    for clade in clade_dict.keys():
        lines.append(f'\n### {clade}')
        for lang in clade_dict[clade]:
            name = family.get_language_from_ascii(lang)
            glottocode = family.get_glottocode_from_ascii(lang)
            poly = glottography.get_source(glottocode)
            status = ' ' if poly is None else 'x'
            if status == ' ' or all:
                lines.append(f'- [{status}] {to_ie_cor(name, lang)} ({to_glottolink(glottocode)})')

    # Header
    header = []
    header.append(f'## *{family.name}* ({len(family.languages)} taxa) Missing Polygons')

    lines = header + lines
    return '\n'.join(lines)


if __name__ == '__main__':
    # Load family
    family = IndoEuropean()
    glottography = Glottography(get_config(family.name))

    # Generate markdown report
    md = all_polygon_inventory_markdown(family, glottography, all=False)

    # Write out
    filename = f'data/glottography/AllPolygons{family.name}.md'
    with open(filename, 'w') as f:
        f.write(md)

    print(f'Wrote polygon inventory to {filename}')
