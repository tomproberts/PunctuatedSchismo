import re

from scripts.families.indo_european import IndoEuropean, Italic
from scripts.glottolog.trees import GlottologTreeType, write_out_glottolog_tree, ALL_TREES
from scripts.utils import asciify

def prune_tree_string(tree_string, keep):
    tokenised = tokenise(tree_string)
    stack = []
    prev = None
    i = 0
    while i < len(tokenised):
        token = tokenised[i]
        if token == '(':
            stack.append(token)
        elif token[0].isalpha():
            prev = token
        elif token == ',' or token == ')':
            if prev:
                if prev in keep:
                    stack.append(prev)
                prev = None
            if token == ')':
                token_next = tokenised[i + 1]
                tmp = []
                if token_next[0].isalpha():
                    i = i + 1
                    if token_next in keep:
                        tmp = [token_next]
                while stack and stack[-1] != '(':
                    tmp.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
                if len(tmp) > 1:
                    stack.append(f'({','.join(reversed(tmp))})')
                elif len(tmp) == 1:
                    stack.append(tmp[0])
        i = i + 1
    assert stack
    return f'{stack[0]};'


def tokenise(tree_string):
    return re.findall(r'([\(\),]|[a-z]{4}[0-9]{4})', tree_string)


def get_glottolog_tree_string(family_glottocode):
    tree_line = 0
    tree_string = ''
    with open(ALL_TREES) as f:
        i = 0
        for line in f:
            if family_glottocode in line:
                tree_line = i
                tree_string = line
            i = i + 1

    # change extended characters to ascii, e.g. ç to c, ā to a
    tree_string = asciify(tree_string)
    return tree_string


def glottocodes_only_tree(tree_string):
    return re.sub(r'\'[A-Z][^[]*\[([a-z]{4}[0-9]{4})\][^\']*\'', r'\1', tree_string)


def verify_correct(pruned, keep):
    # Check no duplicates
    pruned_glottocodes = re.findall(r'([a-z]{4}[0-9]{4})', pruned)
    assert len(pruned_glottocodes) == len(set(pruned_glottocodes))

    # Check all required languages are still present in pruned tree
    missing = set(keep) - set(pruned_glottocodes)
    assert len(missing) == 0

    # Assert valid tree
    from newick import loads
    tree = loads(pruned)
    assert tree
    tree = tree[0]

    assert len(tree.get_leaves()) == len(set(keep))


def remove_grouping(pruned, lang1, lang2):
    pruned = pruned.replace(f"({lang1},{lang2})", f"{lang1},{lang2}")
    pruned = pruned.replace(f"({lang2},{lang1})", f"{lang2},{lang1}")
    return pruned


def tree_convert_glottocodes_to_labels(tree_string, family, ascii=False):
    # TODO: Make more efficient? Technically doesn't matter
    for family_glottocode in family.glottocodes:
        if ascii:
            language = family.get_language_ascii(family_glottocode)
        else:
            language = f"'{family.get_language(family_glottocode)}'"
        tree_string = tree_string.replace(family_glottocode, language)
    return tree_string


def fix_problematic_groupings(tree_string, family):
    if family.name == 'Italic' or family.name == 'IndoEuropean':
        tree_string = remove_grouping(tree_string, 'stan1290', 'angl1258')
    if family.name == 'IndoEuropean':
        tree_string = remove_grouping(tree_string, 'faro1244', 'icel1247')
        tree_string = remove_grouping(tree_string, 'czec1258', 'oldc1253')

    return tree_string


def generate_glottolog_trees(family):
    tree = get_glottolog_tree_string(family.family_glottocode)
    tree = glottocodes_only_tree(tree)
    select = family.glottocodes

    # Prune tree
    pruned = prune_tree_string(tree, select)
    pruned = fix_problematic_groupings(pruned, family)
    verify_correct(pruned, select)

    # Generate labelled version for plots
    labelled = tree_convert_glottocodes_to_labels(pruned, family)

    # Generate ascii version for beast
    labelled_ascii = tree_convert_glottocodes_to_labels(pruned, family, ascii=True)

    # Export
    write_out_glottolog_tree(pruned, family.name, GlottologTreeType.GLOTTOCODES)
    write_out_glottolog_tree(labelled, family.name, GlottologTreeType.NAMES)
    write_out_glottolog_tree(labelled_ascii, family.name, GlottologTreeType.ASCII)


if __name__ == '__main__':
    family = Italic()
    generate_glottolog_trees(family)
