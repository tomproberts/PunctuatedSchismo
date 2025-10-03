import re

from scripts.families.dravidian import Dravidian
from scripts.families.uto_aztecan import UtoAztecan
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
            # token is language, cache
            prev = token
        elif token == ',' or token == ')':
            if prev:
                # check if cached token is in our list
                if prev in keep:
                    stack.append(prev)
                prev = None
            if token == ')':
                token_next = tokenised[i + 1]
                tmp = []
                if token_next[0].isalpha():
                    # named internal node
                    i = i + 1
                    if token_next in keep:
                        tmp = [token_next]
                # Collapse stack:
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
    # only tokenises glottocodes, no other labels!
    return re.findall(r'([\(\),]|[a-z]{4}[0-9]{4})', tree_string)


def get_glottolog_tree_string(family_glottocode):
    tree_string = ''
    with open(ALL_TREES) as f:
        i = 0
        for line in f:
            if family_glottocode in line:
                tree_string = line
                break
            i = i + 1

    # change extended characters to ascii, e.g. ç to c, ā to a
    tree_string = asciify(tree_string)
    return tree_string


def glottocodes_only_tree(tree_string):
    return re.sub(r'\'[A-Z][^[]*\[([a-z]{4}[0-9]{4})\][^\']*\'', r'\1', tree_string)


def extract_all_glottocodes(glottocodes_tree):
    return re.findall(r'([a-z]{4}[0-9]{4})', glottocodes_tree)


def verify_correct(pruned, keep):
    # Check no duplicates
    pruned_glottocodes = extract_all_glottocodes(pruned)
    assert len(pruned_glottocodes) == len(set(pruned_glottocodes))

    # Check all required languages are still present in pruned tree
    missing = set(keep) - set(pruned_glottocodes)
    if len(missing) != 0:
        print(f'Missing glottocodes from tree: {', '.join(missing)}')
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


def escape_glottocodes(tree_string):
    return re.sub(r'([a-z]{4}[0-9]{4})', r'$\1$', tree_string)


def escape_ids(tree_string):
    return re.sub(r'([a-zA-Z0-9_]+)', r'$\1$', tree_string)


def tree_convert_ids_to_labels(tree_string, family):
    tree_string = escape_ids(tree_string)
    for lang_id, label in zip(family.language_ids, family.languages):
        tree_string = tree_string.replace(f'${lang_id}$', f"'{label}'")
    return tree_string


def tree_convert_ids_to_ascii(tree_string, family):
    tree_string = escape_ids(tree_string)
    for lang_id, label_ascii in zip(family.language_ids, family.languages_ascii):
        tree_string = tree_string.replace(f'${lang_id}$', label_ascii)
    return tree_string


def tree_convert_glottocodes_to_ids(tree_string, family):
    # Escape glottocodes in case ids are literally glottocodes and messed up
    tree_string = escape_glottocodes(tree_string)
    # Replace
    for family_glottocode in family.glottocodes:
        ids = family.get_language_ids_from_glottocode(family_glottocode)
        replace_text = ids[0] if len(ids) == 1 else ','.join(ids)
        tree_string = tree_string.replace(f'${family_glottocode}$', replace_text)
    return tree_string


def fix_problematic_groupings(tree_string, family):
    if family.name == 'Italic' or family.name == 'IndoEuropean':
        tree_string = remove_grouping(tree_string, 'stan1290', 'angl1258')
    if family.name == 'IndoEuropean':
        tree_string = remove_grouping(tree_string, 'faro1244', 'icel1247')
        tree_string = remove_grouping(tree_string, 'czec1258', 'oldc1253')
    if family.name == 'Uralic':
        tree_string = make_outgroup(tree_string, 'ural1272')
    if family.name == 'UtoAztecan':
        tree_string = make_outgroup(tree_string, '(kiow1266,sanj1276)', force=True)

    return tree_string


def make_outgroup(tree_string, lang, force=False):
    # TODO: Probably missed edge cases
    if lang in tree_string or force:
        moved = re.sub(f'{lang},', '', tree_string)
        if moved == tree_string:
            moved = re.sub(f',{lang}', '', tree_string)
        if force or moved:
            return f'({lang},{moved[0:-1]});'
    return tree_string


def generate_glottolog_trees(family):
    tree = get_glottolog_tree_string(family.family_glottocode)
    tree = glottocodes_only_tree(tree)
    select = set(family.glottocodes)

    # Check all glottocodes are in language family (according to Glottolog)
    missing = set(select) - set(extract_all_glottocodes(tree))
    if len(missing) > 0:
        print(f'Warning, glottolog tree for {family.name} is missing the following glottocodes: {', '.join(missing)}')

    # Prune tree
    pruned_glottocodes = prune_tree_string(tree, select)
    pruned_glottocodes = fix_problematic_groupings(pruned_glottocodes, family)
    try:
        verify_correct(pruned_glottocodes, select)
    except AssertionError as e:
        print(f'Tree: {tree}')
        raise e

    # Convert to IDs
    id_labelled = tree_convert_glottocodes_to_ids(pruned_glottocodes, family)

    # Generate labelled version for plots
    labelled = tree_convert_ids_to_labels(id_labelled, family)

    # Generate ascii version for beast
    labelled_ascii = tree_convert_ids_to_ascii(id_labelled, family)

    # Export
    write_out_glottolog_tree(pruned_glottocodes, family.name, GlottologTreeType.GLOTTOCODES)
    write_out_glottolog_tree(id_labelled, family.name, GlottologTreeType.ID)
    write_out_glottolog_tree(labelled, family.name, GlottologTreeType.NAMES)
    write_out_glottolog_tree(labelled_ascii, family.name, GlottologTreeType.ASCII)


if __name__ == '__main__':
    family = UtoAztecan()
    generate_glottolog_trees(family)
