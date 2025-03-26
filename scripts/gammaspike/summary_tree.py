import newick
from nexus import NexusReader
import pandas as pd

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


if __name__ == '__main__':
    family = Italic()
    tree_nexus_file = get_summary_tree_nexus(family.name)
    data = visit_tree(tree_nexus_file, family)

    write_out_data(data, family.name)
