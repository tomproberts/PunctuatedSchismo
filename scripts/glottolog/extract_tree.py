import re
import unicodedata

from scripts.families.indo_european import Italic

GLOTTOLOG_TREES = 'data/glottolog/tree_glottolog_newick.txt'


def prune_tokenised_tree(tokenised, keep):
    print(tokenised)

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
                    # print(list(reversed(tmp)))
                    stack.append(f'({','.join(reversed(tmp))})')
                elif len(tmp) == 1:
                    stack.append(tmp[0])
        i = i + 1
    assert stack
    return f'{stack[0]};'


if __name__ == '__main__':
    with open(GLOTTOLOG_TREES) as f:
        all_trees = f.readlines()

    ie_tree = all_trees[250]
    ie_tree = unicodedata.normalize('NFKD', ie_tree).encode('ASCII', 'ignore').decode('ASCII')
    ie_tree = re.sub(r'\'[A-Z][^[]*\[([a-z]{4}[0-9]{4})\][^\']*\'', r'\1', ie_tree)
    italic = Italic()
    keep = italic.glottocodes

    tokenised = re.findall(r'([\(\)]|[a-z]{4}[0-9]{4}|,)', ie_tree)
    pruned = prune_tokenised_tree(tokenised, keep)
    #print(pruned)

    # Check no duplicates
    pruned_glottocodes = re.findall(r'([a-z]{4}[0-9]{4})', pruned)
    assert len(pruned_glottocodes) == len(set(pruned_glottocodes))

    # Check all required languages are still present in pruned tree
    missing = set(keep) - set(pruned_glottocodes)
    assert len(missing) == 0

    # Assert valid tree
    from newick import loads
    tree = loads(pruned)[0]
    print(tree.ascii_art())
