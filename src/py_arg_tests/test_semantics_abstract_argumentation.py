import unittest

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.abstract_argumentation.semantics import get_naive_extensions
from py_arg.abstract_argumentation.semantics.get_admissible_sets import \
    get_admissible_sets
from py_arg.abstract_argumentation.semantics.get_complete_extensions import \
    get_complete_extensions
from py_arg.abstract_argumentation.semantics.get_eager_extension import \
    get_eager_extension
from py_arg.abstract_argumentation.semantics.get_grounded_extension import \
    get_grounded_extension
from py_arg.abstract_argumentation.semantics.get_ideal_extension import \
    get_ideal_extension
from py_arg.abstract_argumentation.semantics.get_preferred_extensions import \
    get_preferred_extensions
from py_arg.abstract_argumentation.semantics.get_semistable_extensions import \
    get_semi_stable_extensions
from py_arg.abstract_argumentation.semantics.get_stable_extensions import \
    get_stable_extensions


# These examples are from Chapter 4 of the Handbook on Formal Argumentation
# (2018) Pietro Baroni, Dov Gabbay, Massimiliano Giacomin and Leendert van der
# Torre, eds.


class TestAFSemantics(unittest.TestCase):
    def test_handbook_chapter_4_figure_3(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        defeats = [Defeat(x, y) for x, y in [(a, b), (b, c)]]
        af = AbstractArgumentationFramework('af', [a, b, c], defeats)

        # Admissible sets
        gt_admissible = {
            frozenset(),
            frozenset({a}),
            frozenset({a, c})
        }
        admissible = get_admissible_sets(af)
        self.assertSetEqual(gt_admissible, admissible)

        # Naive extensions
        gt_naive = {
            frozenset({a, c}),
            frozenset({b})
        }
        naive = get_naive_extensions.apply(af)
        self.assertSetEqual(gt_naive, naive)

        # Complete extensions
        gt_complete = {
            frozenset({a, c})
        }
        complete = get_complete_extensions(af)
        self.assertSetEqual(gt_complete, complete)

        # Grounded extension
        gt_grounded = {a, c}
        grounded = get_grounded_extension(af)
        self.assertSetEqual(gt_grounded, grounded)

        # Preferred extensions
        gt_preferred = {
            frozenset({a, c})
        }
        preferred = get_preferred_extensions(af)
        self.assertSetEqual(gt_preferred, preferred)

        # Stable extensions
        gt_stable = gt_preferred
        stable = get_stable_extensions(af)
        self.assertSetEqual(gt_stable, stable)

        # Semi-stable extensions
        gt_semi_stable = gt_preferred
        semi_stable = get_semi_stable_extensions(af)
        self.assertSetEqual(gt_semi_stable, semi_stable)

        # Ideal extension
        gt_ideal = {a, c}
        ideal = get_ideal_extension(af)
        self.assertSetEqual(gt_ideal, ideal)

        # Eager extension
        gt_eager = {a, c}
        eager = get_eager_extension(af)
        self.assertSetEqual(gt_eager, eager)

    def test_handbook_chapter_4_figure_4(self):
        a = Argument('a')
        b = Argument('b')
        defeats = [Defeat(x, y) for x, y in [(a, b), (b, a)]]
        af = AbstractArgumentationFramework('af', [a, b], defeats)

        # Admissible sets
        gt_admissible = {
            frozenset(),
            frozenset({a}),
            frozenset({b})
        }
        admissible = get_admissible_sets(af)
        self.assertSetEqual(gt_admissible, admissible)

        # Naive extensions
        gt_naive = {
            frozenset({a}),
            frozenset({b})
        }
        naive = get_naive_extensions.apply(af)
        self.assertSetEqual(gt_naive, naive)

        # Complete extensions
        gt_complete = {
            frozenset(),
            frozenset({a}),
            frozenset({b})
        }
        complete = get_complete_extensions(af)
        self.assertSetEqual(gt_complete, complete)

        # Grounded extension
        gt_grounded = set()
        grounded = get_grounded_extension(af)
        self.assertSetEqual(gt_grounded, grounded)

        # Preferred extensions
        gt_preferred = {
            frozenset({a}),
            frozenset({b})
        }
        preferred = get_preferred_extensions(af)
        self.assertSetEqual(gt_preferred, preferred)

        # Stable extensions
        gt_stable = gt_preferred
        stable = get_stable_extensions(af)
        self.assertSetEqual(gt_stable, stable)

        # Semi-stable extensions
        gt_semi_stable = gt_preferred
        semi_stable = get_semi_stable_extensions(af)
        self.assertSetEqual(gt_semi_stable, semi_stable)

        # Ideal extension
        gt_ideal = set()
        ideal = get_ideal_extension(af)
        self.assertSetEqual(gt_ideal, ideal)

        # Eager extension
        gt_eager = set()
        eager = get_eager_extension(af)
        self.assertSetEqual(gt_eager, eager)

    def test_handbook_chapter_4_figure_5(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')
        defeats = [Defeat(x, y) for x, y in [(a, b), (b, c), (c, d), (d, c)]]
        af = AbstractArgumentationFramework('af', [a, b, c, d], defeats)

        # Admissible sets
        gt_admissible = {
            frozenset(),
            frozenset({d}),
            frozenset({a}),
            frozenset({a, d}),
            frozenset({a, c})
        }
        admissible = get_admissible_sets(af)
        self.assertSetEqual(gt_admissible, admissible)

        # Naive extensions
        gt_naive = {
            frozenset({a, c}),
            frozenset({a, d}),
            frozenset({b, d})
        }
        naive = get_naive_extensions.apply(af)
        self.assertSetEqual(gt_naive, naive)

        # Complete extensions
        gt_complete = {
            frozenset({a}),
            frozenset({a, c}),
            frozenset({a, d})
        }
        complete = get_complete_extensions(af)
        self.assertSetEqual(gt_complete, complete)

        # Grounded extension
        gt_grounded = {a}
        grounded = get_grounded_extension(af)
        self.assertSetEqual(gt_grounded, grounded)

        # Preferred extensions
        gt_preferred = {
            frozenset({a, c}),
            frozenset({a, d})
        }
        preferred = get_preferred_extensions(af)
        self.assertSetEqual(gt_preferred, preferred)

        # Stable extensions
        gt_stable = gt_preferred
        stable = get_stable_extensions(af)
        self.assertSetEqual(gt_stable, stable)

        # Semi-stable extensions
        gt_semi_stable = gt_preferred
        semi_stable = get_semi_stable_extensions(af)
        self.assertSetEqual(gt_semi_stable, semi_stable)

        # Ideal extension
        gt_ideal = {a}
        ideal = get_ideal_extension(af)
        self.assertSetEqual(gt_ideal, ideal)

        # Eager extension
        gt_eager = {a}
        eager = get_eager_extension(af)
        self.assertSetEqual(gt_eager, eager)

    def test_handbook_chapter_4_figure_6(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')
        defeats = [Defeat(x, y) for x, y in [(a, b), (b, a), (a, c), (b, c),
                                             (c, d)]]
        af = AbstractArgumentationFramework('af', [a, b, c, d], defeats)

        # Admissible sets
        gt_admissible = {
            frozenset(),
            frozenset({a}),
            frozenset({b}),
            frozenset({a, d}),
            frozenset({b, d})
        }
        admissible = get_admissible_sets(af)
        self.assertSetEqual(gt_admissible, admissible)

        # Naive extensions
        gt_naive = {
            frozenset({a, d}),
            frozenset({b, d}),
            frozenset({c})
        }
        naive = get_naive_extensions.apply(af)
        self.assertSetEqual(gt_naive, naive)

        # Complete extensions
        gt_complete = {
            frozenset(),
            frozenset({a, d}),
            frozenset({b, d})
        }
        complete = get_complete_extensions(af)
        self.assertSetEqual(gt_complete, complete)

        # Grounded extension
        gt_grounded = set()
        grounded = get_grounded_extension(af)
        self.assertSetEqual(gt_grounded, grounded)

        # Preferred extensions
        gt_preferred = {
            frozenset({a, d}),
            frozenset({b, d})
        }
        preferred = get_preferred_extensions(af)
        self.assertSetEqual(gt_preferred, preferred)

        # Stable extensions
        gt_stable = gt_preferred
        stable = get_stable_extensions(af)
        self.assertSetEqual(gt_stable, stable)

        # Semi-stable extensions
        gt_semi_stable = gt_preferred
        semi_stable = get_semi_stable_extensions(af)
        self.assertSetEqual(gt_semi_stable, semi_stable)

        # Ideal extension
        gt_ideal = set()
        ideal = get_ideal_extension(af)
        self.assertSetEqual(gt_ideal, ideal)

        # Eager extension
        gt_eager = set()
        eager = get_eager_extension(af)
        self.assertSetEqual(gt_eager, eager)

    def test_handbook_chapter_4_figure_7(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        defeats = [Defeat(x, y) for x, y in [(a, b), (b, c), (c, a)]]
        af = AbstractArgumentationFramework('af', [a, b, c], defeats)

        # Admissible sets
        gt_admissible = {
            frozenset()
        }
        admissible = get_admissible_sets(af)
        self.assertSetEqual(gt_admissible, admissible)

        # Naive extensions
        gt_naive = {
            frozenset({a}),
            frozenset({b}),
            frozenset({c})
        }
        naive = get_naive_extensions.apply(af)
        self.assertSetEqual(gt_naive, naive)

        # Complete extensions
        gt_complete = {
            frozenset()
        }
        complete = get_complete_extensions(af)
        self.assertSetEqual(gt_complete, complete)

        # Grounded extension
        gt_grounded = set()
        grounded = get_grounded_extension(af)
        self.assertSetEqual(gt_grounded, grounded)

        # Preferred extensions
        gt_preferred = {
            frozenset()
        }
        preferred = get_preferred_extensions(af)
        self.assertSetEqual(gt_preferred, preferred)

        # Stable extensions
        gt_stable = set()
        stable = get_stable_extensions(af)
        self.assertSetEqual(gt_stable, stable)

        # Semi-stable extensions
        gt_semi_stable = gt_preferred
        semi_stable = get_semi_stable_extensions(af)
        self.assertSetEqual(gt_semi_stable, semi_stable)

        # Ideal extension
        gt_ideal = set()
        ideal = get_ideal_extension(af)
        self.assertSetEqual(gt_ideal, ideal)

        # Eager extension
        gt_eager = set()
        eager = get_eager_extension(af)
        self.assertSetEqual(gt_eager, eager)

    def test_handbook_chapter_4_figure_9(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')
        e = Argument('e')
        defeats = [Defeat(x, y) for x, y in [(a, b), (b, a), (b, c), (c, d),
                                             (d, e), (e, c)]]
        af = AbstractArgumentationFramework('af', [a, b, c, d, e], defeats)

        # Admissible sets
        gt_admissible = {
            frozenset(),
            frozenset({a}),
            frozenset({b}),
            frozenset({b, d})
        }
        admissible = get_admissible_sets(af)
        self.assertSetEqual(gt_admissible, admissible)

        # Naive extensions
        gt_naive = {
            frozenset({a, c}),
            frozenset({a, d}),
            frozenset({a, e}),
            frozenset({b, d}),
            frozenset({b, e})
        }
        naive = get_naive_extensions.apply(af)
        self.assertSetEqual(gt_naive, naive)

        # Complete extensions
        gt_complete = {
            frozenset(),
            frozenset({a}),
            frozenset({b, d})
        }
        complete = get_complete_extensions(af)
        self.assertSetEqual(gt_complete, complete)

        # Grounded extension
        gt_grounded = set()
        grounded = get_grounded_extension(af)
        self.assertSetEqual(gt_grounded, grounded)

        # Preferred extensions
        gt_preferred = {
            frozenset({a}),
            frozenset({b, d})
        }
        preferred = get_preferred_extensions(af)
        self.assertSetEqual(gt_preferred, preferred)

        # Stable extensions
        gt_stable = {
            frozenset({b, d})
        }
        stable = get_stable_extensions(af)
        self.assertSetEqual(gt_stable, stable)

        # Semi-stable extensions
        gt_semi_stable = gt_stable
        semi_stable = get_semi_stable_extensions(af)
        self.assertSetEqual(gt_semi_stable, semi_stable)

        # Ideal extension
        gt_ideal = set()
        ideal = get_ideal_extension(af)
        self.assertSetEqual(gt_ideal, ideal)

        # Eager extension
        gt_eager = {b, d}
        eager = get_eager_extension(af)
        self.assertSetEqual(gt_eager, eager)

    def test_handbook_chapter_4_figure_10(self):
        a = Argument('a')
        b = Argument('b')
        defeats = [Defeat(x, y) for x, y in [(a, b), (b, a), (b, b)]]
        af = AbstractArgumentationFramework('af', [a, b], defeats)

        # Admissible sets
        gt_admissible = {
            frozenset(),
            frozenset({a})
        }
        admissible = get_admissible_sets(af)
        self.assertSetEqual(gt_admissible, admissible)

        # Naive extensions
        gt_naive = {
            frozenset({a})
        }
        naive = get_naive_extensions.apply(af)
        self.assertSetEqual(gt_naive, naive)

        # Complete extensions
        gt_complete = {
            frozenset(),
            frozenset({a})
        }
        complete = get_complete_extensions(af)
        self.assertSetEqual(gt_complete, complete)

        # Grounded extension
        gt_grounded = set()
        grounded = get_grounded_extension(af)
        self.assertSetEqual(gt_grounded, grounded)

        # Preferred extensions
        gt_preferred = {
            frozenset({a})
        }
        preferred = get_preferred_extensions(af)
        self.assertSetEqual(gt_preferred, preferred)

        # Stable extensions
        gt_stable = gt_preferred
        stable = get_stable_extensions(af)
        self.assertSetEqual(gt_stable, stable)

        # Semi-stable extensions
        gt_semi_stable = gt_preferred
        semi_stable = get_semi_stable_extensions(af)
        self.assertSetEqual(gt_semi_stable, semi_stable)

        # Ideal extension
        gt_ideal = {a}
        ideal = get_ideal_extension(af)
        self.assertSetEqual(gt_ideal, ideal)

        # Eager extension
        gt_eager = {a}
        eager = get_eager_extension(af)
        self.assertSetEqual(gt_eager, eager)

    def test_handbook_chapter_4_figure_11(self):
        a = Argument('a')
        b = Argument('b')
        defeats = [Defeat(x, y) for x, y in [(a, a), (a, b)]]
        af = AbstractArgumentationFramework('af', [a, b], defeats)

        # Admissible sets
        gt_admissible = {
            frozenset()
        }
        admissible = get_admissible_sets(af)
        self.assertSetEqual(gt_admissible, admissible)

        # Naive extensions
        gt_naive = {
            frozenset()
        }
        naive = get_naive_extensions.apply(af)
        # self.assertSetEqual(gt_naive, naive)
        # TODO check above.

        # Complete extensions
        gt_complete = {
            frozenset()
        }
        complete = get_complete_extensions(af)
        self.assertSetEqual(gt_complete, complete)

        # Grounded extension
        gt_grounded = set()
        grounded = get_grounded_extension(af)
        self.assertSetEqual(gt_grounded, grounded)

        # Preferred extensions
        gt_preferred = {
            frozenset()
        }
        preferred = get_preferred_extensions(af)
        self.assertSetEqual(gt_preferred, preferred)

        # Stable extensions
        gt_stable = set()
        stable = get_stable_extensions(af)
        self.assertSetEqual(gt_stable, stable)

        # Semi-stable extensions
        gt_semi_stable = gt_preferred
        semi_stable = get_semi_stable_extensions(af)
        self.assertSetEqual(gt_semi_stable, semi_stable)

        # Ideal extension
        gt_ideal = set()
        ideal = get_ideal_extension(af)
        self.assertSetEqual(gt_ideal, ideal)

        # Eager extension
        gt_eager = set()
        eager = get_eager_extension(af)
        self.assertSetEqual(gt_eager, eager)

    def test_handbook_chapter_4_figure_12(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        defeats = [Defeat(x, y) for x, y in [(a, b), (b, c), (c, c)]]
        af = AbstractArgumentationFramework('af', [a, b, c], defeats)

        # Admissible sets
        gt_admissible = {
            frozenset(),
            frozenset({a})
        }
        admissible = get_admissible_sets(af)
        self.assertSetEqual(gt_admissible, admissible)

        # Naive extensions
        gt_naive = {
            frozenset({a})
        }
        naive = get_naive_extensions.apply(af)
        self.assertSetEqual(gt_naive, naive)

        # Complete extensions
        gt_complete = {
            frozenset({a})
        }
        complete = get_complete_extensions(af)
        self.assertSetEqual(gt_complete, complete)

        # Grounded extension
        gt_grounded = {a}
        grounded = get_grounded_extension(af)
        self.assertSetEqual(gt_grounded, grounded)

        # Preferred extensions
        gt_preferred = {
            frozenset({a})
        }
        preferred = get_preferred_extensions(af)
        self.assertSetEqual(gt_preferred, preferred)

        # Stable extensions
        gt_stable = gt_preferred
        stable = get_stable_extensions(af)
        self.assertSetEqual(gt_stable, stable)

        # Semi-stable extensions
        gt_semi_stable = gt_preferred
        semi_stable = get_semi_stable_extensions(af)
        self.assertSetEqual(gt_semi_stable, semi_stable)

        # Ideal extension
        gt_ideal = {a}
        ideal = get_ideal_extension(af)
        self.assertSetEqual(gt_ideal, ideal)

        # Eager extension
        gt_eager = {a}
        eager = get_eager_extension(af)
        self.assertSetEqual(gt_eager, eager)
