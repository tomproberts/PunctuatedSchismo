import newick
import pandas as pd
from nexus import NexusReader

from scripts.families.sino_tibetan import SinoTibetan
from scripts.families.uralic import Uralic
from scripts.families.utils import LanguageFamily
from scripts.families.uto_aztecan import UtoAztecan


def write_out_data(data, family_name) -> None:
    pd.DataFrame(data).to_csv(f'data/gammaspike/summarytree/{family_name}.csv', index=False)


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
        language_id = family.get_language_id_from_ascii(ascii_name)
        leaves_ascii.append(ascii_name)
        leaves_name.append(family.get_language_from_language_id(language_id))
        glottocode = family.get_glottocode_from_language_id(language_id)
        leaves_glottocode.append(glottocode)
        # scale bursts sizes for number of cognate sets
        leaves_weightedSpikes.append(family.n_sites / 2 * float(node.properties['weightedSpikes']))
        leaves_weightedSpikes_median.append(family.n_sites / 2 * float(node.properties['weightedSpikes_median']))

    # visit leaf nodes
    tree.visit(visitor, lambda node: node.is_leaf)

    return {'label': leaves_ascii,
            'Name': leaves_name,
            'Glottocode': leaves_glottocode,
            'weightedSpikes': leaves_weightedSpikes,
            'weightedSpikes_median': leaves_weightedSpikes_median}


def get_summary_tree_nexus(family_name) -> NexusReader:
    try:
        return NexusReader.from_file(f'data/gammaspike/summarytree/{family_name}.nex')
    except Exception as e:
        trace = str(e)
    raise NoSummaryTree(family_name, trace)


def summary_tree_cherries(family: LanguageFamily, as_glottocode=True) -> list[tuple[str, str]]:
    tree = get_summary_tree_nexus(family.name)
    assert tree
    taxa = tree.taxa.taxa
    tree = tree.trees[0].newick_tree
    cherries = []

    def nx_output(node_id: str) -> str:
        ascii = taxa[int(node_id) - 1]
        if as_glottocode:
            return family.get_glottocode_from_ascii(ascii)
        return ascii

    def for_node(node: newick.Node) -> None:
        leaves = [n.name for n in node.descendants if n.is_leaf]
        if len(leaves) > 1:
            assert len(leaves) == 2
            cherry: tuple[str, str] = nx_output(leaves[0]), nx_output(leaves[1])
            cherries.append(cherry)

    tree.visit(for_node)
    return cherries


def get_sorted_summary_tree_cherries_ascii(family: LanguageFamily) -> list[tuple[str, list[tuple[str, str]]]]:
    cherries = summary_tree_cherries(family, as_glottocode=False)
    possible_clades = family.get_clades()
    if not possible_clades:
        return [('Cherries', cherries)]
    # initialise clade sorting
    clade_dict = {}
    for clade in possible_clades:
        clade_dict[clade] = []
    clade_dict['Miscellaneous'] = []
    # sort cherries
    for (lang1, lang2) in cherries:
        clade = family.get_clade_from_ascii(lang1)
        if clade not in clade_dict:
            clade = 'Miscellaneous'
        clade_dict[clade].append((lang1, lang2))
    return list(clade_dict.items())


class NoSummaryTree(Exception):
    def __init__(self, family_name, error='no stacktrace'):
        super().__init__(f'No summary tree present for {family_name}\n({error})')


if __name__ == '__main__':
    family = Uralic()
    tree_nexus_file = get_summary_tree_nexus(family.name)
    data = visit_tree(tree_nexus_file, family)

    write_out_data(data, family.name)
