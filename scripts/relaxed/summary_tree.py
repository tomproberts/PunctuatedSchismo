import newick
import pandas as pd
from nexus import NexusReader

from scripts.families.pama_nyungan import PamaNyungan
from scripts.families.utils import LanguageFamily


def write_out_data(data: pd.DataFrame, family_name) -> None:
    data.to_csv(f'data/relaxed/{family_name}.csv', index=False)


def visit_tree(tree_nexus_file, family: LanguageFamily) -> pd.DataFrame:
    tree: newick.Node = tree_nexus_file.trees.trees[0].newick_tree

    leaf_data = []

    def visitor(node: newick.Node) -> None:
        ascii_name = node.name
        language_id = family.get_language_id_from_ascii(ascii_name)
        glottocode = family.get_glottocode_from_language_id(language_id)

        leaf_data.append({
            'label': ascii_name,
            'name': family.get_language_from_language_id(language_id),
            'glottocode': glottocode,
            'rate': float(node.properties['rate']),
            'rate_median': float(node.properties['rate_median'])
        })

    # visit leaf nodes
    tree.visit(visitor, lambda node: node.is_leaf)

    return pd.DataFrame.from_records(leaf_data)


def get_summary_tree_nexus(family_name) -> NexusReader:
    try:
        return NexusReader.from_file(f'data/relaxed/{family_name}.nex')
    except Exception as e:
        trace = str(e)
    raise NoRelaxedSummaryTree(family_name, trace)


def relaxed_summary_tree_cherries(family: LanguageFamily, as_glottocode=True) -> list[tuple[str, str]]:
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
            cherry = nx_output(leaves[0]), nx_output(leaves[1])
            cherries.append(cherry)

    tree.visit(for_node)
    return cherries


class NoRelaxedSummaryTree(Exception):
    def __init__(self, family_name, error='no stacktrace'):
        super().__init__(f'No relaxed summary tree present for {family_name}\n({error})')


if __name__ == '__main__':
    family = PamaNyungan()
    tree_nexus_file = get_summary_tree_nexus(family.name)
    data = visit_tree(tree_nexus_file, family)

    write_out_data(data, family.name)
