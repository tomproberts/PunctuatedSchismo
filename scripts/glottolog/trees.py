from enum import Enum

from scripts.families.utils import LanguageFamily

GLOTTOLOG_DIR = 'data/glottolog'
ALL_TREES = f'{GLOTTOLOG_DIR}/tree_glottolog_newick.txt'


class GlottologTreeType(Enum):
    GLOTTOCODES = 'glottocodes'
    NAMES = 'names'
    ASCII = 'ascii'


def write_out_glottolog_tree(tree_string: str, family_name: str, type: GlottologTreeType) -> None:
    with open(glottolog_tree_file(type, family_name), 'w') as f:
        f.write(tree_string)


def glottolog_tree_file(type: GlottologTreeType, family_name: str) -> str:
    return f'{GLOTTOLOG_DIR}/{type.value}/{family_name}.newick'


def glottolog_cherries(family: LanguageFamily):
    if family.name == 'Italic':
        return [('port1283', 'braz1246'),
                ('stan1288', 'olds1249'),
                ('oldc1251', 'stan1289'),
                ('stan1290', 'fran1269'),
                ('ladi1250', 'friu1240'),
                ('neap1235', 'ital1282'),
                ('sout2614', 'barb1262'),
                ('roma1327', 'megl1237'),
                ('umbr1253', 'osca1245')]
    raise NotImplementedError(f'glottolog cherries not implemented for {family.name}')
