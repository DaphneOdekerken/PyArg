from distutils.util import strtobool

from parse import parse

from py_arg.labels.label import Label


class FourBoolStabilityLabel(Label):
    def __init__(self, unsatisfiable: bool, defended: bool, out: bool, blocked: bool):
        super().__init__()
        self.unsatisfiable = unsatisfiable
        self.defended = defended
        self.out = out
        self.blocked = blocked

    def __str__(self):
        s1 = '(U:{0}, D:{1}, O:{2}, B:{3})'.format(str(self.unsatisfiable), str(self.defended), str(self.out),
                                                   str(self.blocked))
        return s1

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.unsatisfiable == other.unsatisfiable and self.defended == other.defended and \
               self.out == other.out and self.blocked == other.blocked

    def __copy__(self):
        return FourBoolStabilityLabel(self.unsatisfiable, self.defended, self.out, self.blocked)

    def __add__(self, other: 'FourBoolStabilityLabel'):
        unsatisfiable = self.unsatisfiable or other.unsatisfiable
        defended = self.defended or other.defended
        out = self.out or other.out
        blocked = self.blocked or other.blocked
        return FourBoolStabilityLabel(unsatisfiable, defended, out, blocked)

    @property
    def is_stable(self):
        return sum([self.unsatisfiable, self.defended, self.out, self.blocked]) == 1

    @property
    def is_stable_defended(self):
        return self.is_stable and self.defended

    @property
    def is_contested_stable(self):
        if self.defended and (self.unsatisfiable or self.out or self.blocked):
            return False
        return True

    @classmethod
    def from_str(cls, label_str: str):
        parse_result_str_list = parse('(U:{0}, D:{1}, O:{2}, B:{3})', label_str).fixed
        parse_result_bool_list = [strtobool(s) for s in parse_result_str_list]
        return FourBoolStabilityLabel(*parse_result_bool_list)
