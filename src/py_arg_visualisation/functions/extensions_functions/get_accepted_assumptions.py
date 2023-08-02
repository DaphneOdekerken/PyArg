def apply(extensions, strategy_specification: str):
    """
    Calculate the set of accepted formulas from a set of extensions (sets of arguments) and evaluation strategy

    :param extensions: The extensions (sets of collectively accepted arguments).
    :param strategy_specification: The evaluation strategy (e.g., skeptical or credulous).
    """
    if strategy_specification == 'Skeptical':
        return frozenset().intersection(*extensions)
    if strategy_specification == 'Credulous':
        return frozenset().union(*extensions)
    return {}
