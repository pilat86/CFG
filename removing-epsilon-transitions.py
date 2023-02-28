from typing import Set, Dict


def make_permutations(rule: str, nonterm: str) -> Dict[str, Set[str]]:
    rule_lst = []
    alredy_added = []
    count = 0
    new_set = set()

    for letter in rule:
        if letter != nonterm:
            rule_lst.append(letter)
        elif letter == nonterm:
            rule_lst.append(letter)
            count += 1

    if count == 1 and nonterm in rule_lst:
        original = "".join(rule_lst)
        making = [x for x in rule_lst if x != nonterm]
        new = "".join(making)
        alredy_added.append(new)
        alredy_added.append(original)
        new_set.add(original)
        new_set.add(new)

    if count == 0 and nonterm not in rule_lst:
        making = [x for x in rule_lst if x != nonterm]
        new = "".join(making)
        alredy_added.append(new)
        new_set.add(new)

    if count == len(rule_lst):
        new_set.add("")
        original = "".join(rule_lst)
        alredy_added.append(original)
        new_set.add(original)
        for i in range(count):
            new = i*nonterm
            if new not in alredy_added:
                alredy_added.append(new)
                new_set.add(new)

    if count > 1:

        original = "".join(rule_lst)
        alredy_added.append(original)
        new_set.add(original)

        without_nonterminals = "".join([x for x in rule_lst if x != nonterm])
        alredy_added.append(without_nonterminals)
        new_set.add(without_nonterminals)

        index = 0
        for i in rule_lst:
            if i == nonterm:
                before = "".join(rule_lst[:index])
                if before == "":
                    before = ''
                after = "".join(rule_lst[index+1:])
                new = before + after
                if new not in alredy_added:
                    alredy_added.append(new)
                    new_set.add(new)

                before = "".join([x for x in rule_lst[:index] if x != nonterm])
                after = "".join(
                    [x for x in rule_lst[index+1:] if x != nonterm])

                new = before + nonterm + after
                if new not in alredy_added:
                    alredy_added.append(new)
                    new_set.add(new)

                index += 1
            if i != nonterm:
                index += 1

    return new_set


def del_epsilon_from(grammar: Dict[str, Set[str]], nonterm: str) \
        -> Dict[str, Set[str]]:

    gram = copy_grammar(grammar)

    for key in gram:
        for value in list(gram[key]):
            if nonterm in value:
                new_value = make_permutations(value, nonterm)
                peek(nonterm)
                for i in new_value:
                    if i not in gram[key]:
                        gram[key].add(i)

    if "" in gram[nonterm]:
        gram[nonterm].remove("")

    return gram


def del_epsilon(grammar: Dict[str, Set[str]]) -> Set[str]:
    gram = copy_grammar(grammar)

    keys = []
    for key in gram:
        if key != "S":
            keys.append(key)

    for key in keys:
        if "" not in list(gram[key]):
            continue
        nonterm = key
        for key in list(gram.keys()):
            for value in list(gram[key]):
                if nonterm in value:
                    new_value = make_permutations(value, nonterm)
                    for i in new_value:
                        if i not in gram[key]:
                            gram[key].add(i)

        if "" in gram[nonterm]:
            gram[nonterm].remove("")

    for key in gram:
        if key == "S":
            continue
        for value in list(gram[key]):
            if value == "":
                if peek(key):
                    gram[key].remove("")

    return gram


def peek(nonterminal):
    xd = []
    if nonterminal not in xd:
        xd.append(nonterminal)
        return True
    return False


def copy_grammar(grammar: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    gramm = dict()
    for nonterm, rule in grammar.items():
        gramm[nonterm] = rule.copy()
    return gramm


def test():
    print(make_permutations("aaaAb", "A"))      # {"aaab", "aaaAb"}
    print(make_permutations("aaaAb", "B"))      # {"aaaAb"}
    print(make_permutations("B", "B"))          # {"B", ""}
    print(make_permutations("XX", "X"))         # {"XX", "X", ""}
    print(make_permutations("XdX", "X"))        # {"XdX", "dX", "Xd", "d"}

    grammar = {
        "S": {"ab", "B", ""},
        "A": {"Ba", "Ab", ""},
        "B": {"Aa", "A", ""},
    }
    grammar_start = {
        "S": {"ab", "B", ""},
        "A": {"Ba", "Ab", ""},
        "B": {"Aa", "A", ""},
    }
    grammar_step = {
        "S": {"ab", "B", ""},
        "A": {"Ba", "Ab", "b"},
        "B": {"Aa", "A", "a", ""},
    }
    grammar_after = {
        "S": {"ab", "B", ""},
        "A": {"Ba", "Ab", "b", "a"},
        "B": {"Aa", "A", "a"},
    }

    grammar2 = {
        "S": {"aAb"},
        "A": {"B", "ab", "aAb"},
        "B": {"ACD"},
        "C": {"", "d"},
        "D": {"c", ""},
    }
    grammar2_start = {
        "S": {"aAb"},
        "A": {"B", "ab", "aAb"},
        "B": {"ACD"},
        "C": {"", "d"},
        "D": {"c", ""},
    }
    grammar2_step = {
        "S": {"aAb"},
        "A": {"B", "ab", "aAb"},
        "B": {"ACD", "AD"},
        "C": {"d"},
        "D": {"c", ""},
    }
    grammar2_after = {
        "S": {"aAb"},
        "A": {"B", "ab", "aAb"},
        "B": {"ACD", "AC", "AD", "A"},
        "C": {"d"},
        "D": {"c"},
    }
    grammar10 = {
        'S': {'BA', 'A', 'B'},
        'A': {'', "B"},
        'B': {""},
        'C': {'x'}
    }
    grammar11 = {
        'S': {'', 'A', 'B', 'BA'},
        'A': {'B'},
        'B': set(),
        'C': {'x'}
    }

    grammar100 = {
        'S': {'A'},
        'A': {'C', ''},
        'C': {'x', 'A', ''}
    }

    grammar200 = {
        'S': {'', 'A'},
        'A': {'C'},
        'C': {'x', 'A'}
    }

    grammar = del_epsilon_from(grammar, "A")
    print(grammar == grammar_step)                       # True
    grammar = del_epsilon_from(grammar, "B")
    print(grammar == grammar_after)                      # True

    grammar2 = del_epsilon_from(grammar2, "C")
    print(grammar2 == grammar2_step)                     # True
    grammar2 = del_epsilon_from(grammar2, "D")
    print(grammar2 == grammar2_after)                    # True

    print(del_epsilon(grammar_start) == grammar_after)   # True
    print(del_epsilon(grammar2_start) == grammar2_after)  # True

    print(del_epsilon(grammar10) == grammar11)  # True

    print(del_epsilon(grammar100) == grammar200)  # True


test()
