from py_arg.incomplete_aspic.algorithms.stability.stability_label import \
    StabilityLabel
from py_arg.incomplete_aspic.algorithms.stability.stability_labels import \
    StabilityLabels
from py_arg.incomplete_aspic.classes.incomplete_argumentation_theory import \
    IncompleteArgumentationTheory


class SatisfiabilityLabeler:
    def __init__(self):
        pass

    @staticmethod
    def _preprocess_visit(rule, labels):
        if labels.rule_labeling[rule].defended:
            return False
        if all([labels.literal_labeling[literal].defended for literal in
                rule.antecedents]):
            labels.rule_labeling[rule] = StabilityLabel(True, True, True, True)
            labels.literal_labeling[rule.consequent] = StabilityLabel(
                True, True, True, True)
            return True
        return False

    def label(
            self,
            incomplete_argumentation_theory: IncompleteArgumentationTheory) \
            -> StabilityLabels:
        labels = StabilityLabels(dict(), dict())

        for literal in incomplete_argumentation_theory.argumentation_system.\
                language.values():
            if incomplete_argumentation_theory.is_queryable(literal) and \
                    all([
                        contrary not in
                        incomplete_argumentation_theory.knowledge_base
                        for contrary in
                        literal.contraries_and_contradictories]):
                labels.literal_labeling[literal] = StabilityLabel(
                    True, True, True, True)
            else:
                labels.literal_labeling[literal] = StabilityLabel(
                    True, False, False, False)

        for rule in incomplete_argumentation_theory.argumentation_system.rules:
            labels.rule_labeling[rule] = StabilityLabel(
                True, False, False, False)

        label_added = True
        while label_added:
            label_added = False
            for rule in incomplete_argumentation_theory.argumentation_system.\
                    rules:
                label_added = \
                    self._preprocess_visit(rule, labels) or label_added

        return labels
