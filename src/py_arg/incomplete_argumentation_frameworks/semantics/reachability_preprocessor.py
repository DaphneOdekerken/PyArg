import clingo
import pathlib


PATH_TO_ENCODINGS = pathlib.Path('encodings')


class ReachabilityPreprocessor:
    def __init__(self):
        self.last_model = None

    def on_model(self, model):
        self.last_model = model.symbols(shown=True)

    def enumerate_reachable(self, iaf_file):
        control = clingo.Control()
        control.load(str(iaf_file))
        control.load(str(PATH_TO_ENCODINGS / 'reachable_preprocessing.dl'))
        control.ground([('base', [])], context=self)
        control.solve(on_model=self.on_model)
        with open('temp.lp', 'w') as writer:
            writer.write('topic(a0).\n')
            if self.last_model:
                for symbols in self.last_model:
                    writer.write(str(symbols)[2:] + '.\n')
        return 'temp.lp'
