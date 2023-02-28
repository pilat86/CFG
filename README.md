# **Removing epsilon transition from context-free grammar:**

***1. make_permutations***
- *this function takes a rule and a non-terminal and creates a set of rules such that it contains all possible combinations of replacing the given non-terminal with epsilon, or an empty string.*

***2. del_epsilon_from***
- *this function takes a grammar and a non-terminal, which is rewritten to epsilon and completes all the necessary rules for removing epsilon from this rule and then removes it as well.*

***3. del_epsilon***
- *this function takes a grammar and returns an equivalent rule-free grammar with epsilon, minus the initial non-terminal. This function must not modify the input     grammar, you can use the prescribed function copy_grammar() for a possible copy of the grammar.*
