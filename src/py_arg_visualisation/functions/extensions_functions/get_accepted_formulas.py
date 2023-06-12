def get_accepted_formulas(extensions, strategy_specification: str):
    """
    Calculate the set of accepted formulas from a set of extensions (sets of arguments) and evaluation strategy

    :param extensions: The extensions (sets of collectively accepted arguments).
    :param strategy_specification: The evaluation strategy (e.g., skeptical or credulous).
    """
    if strategy_specification == 'Skeptical':
        accepted_arguments = set.intersection(*extensions)
        return set(arg.conclusion for arg in accepted_arguments)
    if strategy_specification == 'Credulous':
        accepted_arguments = set.union(*extensions)
        return set(arg.conclusion for arg in accepted_arguments)
    elif strategy_specification == 'WeaklySkeptical':
        extension_formulas = [{arg.conclusion for arg in extension} for extension in extensions]
        return set.intersection(*extension_formulas)
