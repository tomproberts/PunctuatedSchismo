from enum import Enum

import newick
from itertools import combinations

from scripts.families.indo_european import Italic
from scripts.families.utils import LanguageFamily

GLOTTOLOG_DIR = 'data/glottolog'
ALL_TREES = f'{GLOTTOLOG_DIR}/tree_glottolog_newick.txt'


class GlottologTreeType(Enum):
    GLOTTOCODES = 'glottocodes'
    NAMES = 'names'
    ASCII = 'ascii'
    ID = 'id'


def write_out_glottolog_tree(tree_string: str, family_name: str, type: GlottologTreeType) -> None:
    with open(glottolog_tree_file(type, family_name), 'w') as f:
        f.write(tree_string)


def glottolog_tree_file(type: GlottologTreeType, family_name: str) -> str:
    return f'{GLOTTOLOG_DIR}/{type.value}.{family_name}.newick'


def glottolog_cherries(family: LanguageFamily, type: GlottologTreeType = GlottologTreeType.GLOTTOCODES) -> list[tuple[str, str]]:
    file_name = glottolog_tree_file(type, family.name)
    tree = newick.read(file_name)
    assert tree
    tree = tree[0]
    cherries = []

    def for_node(node: newick.Node) -> None:
        # Get leaf babies of node
        leaves = [n.name for n in node.descendants if n.is_leaf]
        if len(leaves) > 1:
            # Add all possible binary cherries compatible with Glottolog topology
            for p in combinations(leaves, 2):
                cherries.append(p)

    tree.visit(for_node)
    return cherries


if __name__ == '__main__':
    cherries = glottolog_cherries(Italic())
    print(cherries)
