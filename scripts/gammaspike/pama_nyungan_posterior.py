from statistics import mean, pstdev

from nexus import NexusReader
from tqdm import tqdm

if __name__ == '__main__':
    n = NexusReader.from_file('/home/thomas/phyloconfigs/pamanyungan/posterior.trees')
    trees = n.trees.trees
    rate_mean = []
    rate_SD = []

    for tree in tqdm(trees):
        t = tree.newick_tree
        rates = []
        t.visit(lambda n: rates.append(float(n.properties['rate'])))
        rates = rates[1:]
        rate_mean.append(mean(rates))
        rate_SD.append(pstdev(rates))

    print(f'Mean clock rate across {len(trees)} trees: {mean(rate_mean) * 1e3}/kya')
    print(f'Mean clock rate s.d. across {len(trees)} trees: {mean(rate_SD) * 1e3}/kya')
