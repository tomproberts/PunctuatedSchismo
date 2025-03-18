import re
import unicodedata
from newick import read, write, loads, dumps

from scripts.families.indo_european import Italic

GLOTTOLOG_TREES = 'data/glottolog/tree_glottolog_newick.txt'

if __name__ == '__main__':
    with open(GLOTTOLOG_TREES) as f:
        all_trees = f.readlines()

    ie_tree = all_trees[250]
    ie_tree = unicodedata.normalize('NFKD', ie_tree).encode('ASCII', 'ignore').decode('ASCII')
    ie_tree = re.sub(r'\'[A-Z][^[]*\[([a-z]{4}[0-9]{4})\][^\']*\'', r'\1', ie_tree)
    all_glottocodes = re.findall(r'[a-z]{4}[0-9]{4}', ie_tree)
    tree = loads(ie_tree)[0]
    italic = Italic()
    keep = italic.glottocodes

    # check glottocodes don't have duplicates?
    keep_set = set(keep)
    assert(len(keep) == len(keep_set))

    # check glottocodes are in tree
    missing_from_glottolog = keep_set - keep_set.intersection(all_glottocodes)
    assert(len(missing_from_glottolog) == 0)

    tree.prune_by_names(keep, inverse=True)
    print(dumps(tree))
    pruned_glottocodes = re.findall(r'[a-z]{4}[0-9]{4}', dumps(tree))

    # TODO: check glottocodes aren't constrained-ancestors, control for such cases
    ancestors = re.findall(r'\)([a-z]{4}[0-9]{4})', dumps(tree))
    ancestor_nodes = keep_set - set(ancestors)

    tree.remove_redundant_nodes(preserve_lengths=False, keep_leaf_name=True)
    final_glottocodes = re.findall(r'[a-z]{4}[0-9]{4}', dumps(tree))
    # remove lengths

    #print(tree.ascii_art())
