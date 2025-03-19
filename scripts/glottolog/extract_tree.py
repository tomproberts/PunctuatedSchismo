import re
import unicodedata

from scripts.families.indo_european import Italic

GLOTTOLOG_TREES = 'data/glottolog/tree_glottolog_newick.txt'
GLOTTOCODES_OUT = 'data/glottolog/glottocodes/'
GLOTTONAMES_OUT = 'data/glottolog/names/'


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
                        pull_up = True
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


def get_glottolog_tree_string(family, ascii=True):
    with open(GLOTTOLOG_TREES) as f:
        all_trees = f.readlines()
    tree_string = all_trees[250]

    # change extended characters to ascii, e.g. ç to c, ā to a
    if ascii:
        tree_string = unicodedata.normalize('NFKD', tree_string).encode('ASCII', 'ignore').decode('ASCII')
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


if __name__ == '__main__':
    family = Italic()
    ie_tree = get_glottolog_tree_string('Indo-European')
    ie_tree = glottocodes_only_tree(ie_tree)
    keep = family.glottocodes

    # Prune tree
    pruned = prune_tree_string(ie_tree, keep)
    verify_correct(pruned, keep)

    print(pruned)
    with open(f'{GLOTTOCODES_OUT}{family.name}.newick', 'w') as f:
        f.write(pruned)
