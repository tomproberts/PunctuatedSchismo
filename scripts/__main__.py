from scripts.families.indo_european import Italic
from scripts.glottolog import trees


def main():
    family = Italic()
    cherries = trees.glottolog_cherries(family)
    print('\n'.join([f'({family.get_language(x)}, {family.get_language(y)})' for (x, y) in cherries]))
    # phon_distances = calculate_distances(family, cherries, MEAN)
    # print(phon_distances)
    # write_out_phonological_distance(family, cherries, phon_distances)


if __name__ == '__main__':
    main()
