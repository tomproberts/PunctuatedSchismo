import newick
from nexus import NexusReader
import pandas as pd

from scripts.families.dravidian import Dravidian
from scripts.families.indo_european import Italic
from scripts.families.utils import LanguageFamily


def write_out_data(data, family_name) -> None:
    pd.DataFrame(data).to_csv(f'data/gammaspike/{family_name}.csv', index=False)


def visit_tree(tree_nexus_file, family: LanguageFamily) -> dict:
    translate = tree_nexus_file.trees.translators
    tree: newick.Node = tree_nexus_file.trees.trees[0].newick_tree

    leaves_ascii = []
    leaves_name = []
    leaves_glottocode = []
    leaves_weightedSpikes = []
    leaves_weightedSpikes_median = []

    def visitor(node: newick.Node) -> None:
        ascii_name = translate[node.name]
        glottocode = family.get_glottocode_from_ascii(ascii_name)
        leaves_ascii.append(ascii_name)
        leaves_name.append(family.get_language(glottocode))
        leaves_glottocode.append(glottocode)
        # scale bursts sizes for number of cognate sets
        leaves_weightedSpikes.append(family.n_taxa * float(node.properties['weightedSpikes']))
        leaves_weightedSpikes_median.append(family.n_taxa * float(node.properties['weightedSpikes_median']))

    # visit leaf nodes
    tree.visit(visitor, lambda node: node.is_leaf)

    return {'label': leaves_ascii,
            'Name': leaves_name,
            'Glottocode': leaves_glottocode,
            'weightedSpikes': leaves_weightedSpikes,
            'weightedSpikes_median': leaves_weightedSpikes_median}


def get_summary_tree_nexus(family_name) -> NexusReader:
    return NexusReader.from_file(f'data/summarytree/{family_name}.nex')


def summary_tree_cherries(family: LanguageFamily) -> [(str, str)]:
    tree = get_summary_tree_nexus(family.name)
    assert tree
    taxa = tree.taxa.taxa
    tree = tree.trees[0].newick_tree
    cherries = []


    def nx_glottocode(node_id: str) -> str:
        ascii = taxa[int(node_id)]
        return family.get_glottocode_from_ascii(ascii)


    def for_node(node: newick.Node) -> None:
        leaves = [n.name for n in node.descendants if n.is_leaf]
        if len(leaves) > 1:
            assert len(leaves) == 2
            cherry = nx_glottocode(leaves[0]), nx_glottocode(leaves[1])
            cherries.append(cherry)


    tree.visit(for_node)
    return cherries


if __name__ == '__main__':
    family = Dravidian()
    tree_nexus_file = get_summary_tree_nexus(family.name)
    data = visit_tree(tree_nexus_file, family)

    write_out_data(data, family.name)
