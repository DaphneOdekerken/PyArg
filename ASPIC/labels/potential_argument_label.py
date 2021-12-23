from ASPIC.labels.label import Label


class PotentialArgumentLabel(Label):
    def __init__(self, in_arguments: bool = False, in_necessary_grounded_extension: bool = False,
                 in_possible_grounded_extension: bool = False, defeated_by_necessary_grounded_extension: bool = False,
                 defeated_by_possible_grounded_extension: bool = False):
        super().__init__()
        self.in_arguments = in_arguments
        self.in_necessary_grounded_extension = in_necessary_grounded_extension
        self.in_possible_grounded_extension = in_possible_grounded_extension
        self.defeated_by_necessary_grounded_extension = defeated_by_necessary_grounded_extension
        self.defeated_by_possible_grounded_extension = defeated_by_possible_grounded_extension

    def __str__(self):
        s1 = '(A:{0}, NG:{1}, PG:{2}, ANG:{3}, PNG:{4})'.format(
            str(self.in_arguments),
            str(self.in_necessary_grounded_extension),
            str(self.in_possible_grounded_extension),
            str(self.defeated_by_necessary_grounded_extension),
            str(self.defeated_by_possible_grounded_extension))
        return s1

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return str(self) == str(other)

    def __copy__(self):
        return PotentialArgumentLabel(self.in_arguments, self.in_necessary_grounded_extension,
                                      self.in_possible_grounded_extension,
                                      self.defeated_by_necessary_grounded_extension,
                                      self.defeated_by_possible_grounded_extension)
