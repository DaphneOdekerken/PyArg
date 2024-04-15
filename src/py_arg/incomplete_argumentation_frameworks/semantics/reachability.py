import clingo
import pathlib


PATH_TO_ENCODINGS = pathlib.Path('encodings')


class ReachabilitySolver:
    def __init__(self):
        self.last_model = None

    def on_model(self, model):
        self.last_model = model.symbols(shown=True)

    def enumerate_reachable(self, iaf_file):
        control = clingo.Control()
        control.load(str(iaf_file))
        control.load(str(PATH_TO_ENCODINGS / 'reachable.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'reachable_filter.dl'))
        control.ground([('base', [])], context=self)
        control.solve(on_model=self.on_model)


if __name__ == '__main__':
    # example = pathlib.Path('examples') / 'ac.lp'
    example = pathlib.Path('generated') / 'IAF_200_300_30_args_atts_1.pl'
    solver = ReachabilitySolver()
    solver.enumerate_reachable(example)
    for symbols in solver.last_model:
        print(str(symbols))
