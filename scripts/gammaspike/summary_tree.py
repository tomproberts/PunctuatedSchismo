import newick
from nexus import NexusReader
import pandas as pd

from scripts.families.indo_european import Italic

family = Italic()
tree_nexus_file = NexusReader.from_file('/home/thomas/R/tree-analysis/trees/italic.ccd0')
translate = tree_nexus_file.trees.translators
tree2: newick.Node = tree_nexus_file.trees.trees[0].newick_tree

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
    leaves_weightedSpikes.append(4958 * float(node.properties['weightedSpikes']))
    leaves_weightedSpikes_median.append(4958 * float(node.properties['weightedSpikes_median']))


tree2.visit(visitor, lambda node: node.is_leaf)
data = {'label': leaves_ascii,
        'Name': leaves_name,
        'Glottocode': leaves_glottocode,
        'weightedSpikes': leaves_weightedSpikes,
        'weightedSpikes_median': leaves_weightedSpikes_median}

pd.DataFrame(data).to_csv('data/gammaspike/Italic.csv', index=False)

# print(tree2.ascii_art())
