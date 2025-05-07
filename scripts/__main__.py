from scripts.families.indo_european import Italic, IndoEuropean
from scripts.glottolog import trees
from scripts.predictors.phonological_distance import calculate_distances, MEAN
from scripts.predictors.utils import write_out_phonological_distance


def main():
    family = Italic()
    cherries = trees.glottolog_cherries(family)
    print('\n'.join([f'({family.get_language_from_glottocode(x)}, {family.get_language_from_glottocode(y)})' for (x, y) in cherries]))
    phon_distances = calculate_distances(family, cherries, MEAN)
    print(phon_distances)
    write_out_phonological_distance(family, cherries, phon_distances)


if __name__ == '__main__':
    main()
