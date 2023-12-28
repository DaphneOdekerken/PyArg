from py_arg.abstract_argumentation.semantics.acceptance_strategy import \
    AcceptanceStrategy


def get_acceptance_strategy(acceptance_strategy_specification: str) -> \
        AcceptanceStrategy:
    if acceptance_strategy_specification == 'Skeptical':
        return AcceptanceStrategy.SKEPTICAL
    if acceptance_strategy_specification == 'Credulous':
        return AcceptanceStrategy.CREDULOUS
    if acceptance_strategy_specification == 'WeaklySkeptical':
        return AcceptanceStrategy.WEAKLY_SKEPTICAL
