from pylogics_modalities.parsers import parse_pltl
from pylogics_modalities.syntax.base import (
    And as PLTLAnd,
    Or as PLTLOr,
    Implies as PLTLImplies,
    Not as PLTLNot
)
from pylogics_modalities.syntax.pltl import (
    Atomic as PLTLAtomic,
    Before,
    WeakBefore,
    Historically,
    Once,
    PropositionalFalse,
    Since,
    Triggers
)

import unittest
import coverage
from modify import modify


a = PLTLAtomic("a")
b = PLTLAtomic("b")
c = PLTLAtomic("c")
d = PLTLAtomic("d")
neg = parse_pltl("!a")
_and = parse_pltl("a & b")
_or = parse_pltl("a | b")
implies1 = parse_pltl("a -> b")
implies2 = parse_pltl("(!a) | b")
yesterday = parse_pltl("Y a")
weak_yesterday = parse_pltl("Z a")
historically = parse_pltl("H a")
once1 = parse_pltl("O a")
once2 = parse_pltl("true S a")
false = parse_pltl("false")
true = parse_pltl("true")
since = parse_pltl("a S b")
triggers = parse_pltl("a T b")


class TestModify(unittest.TestCase):

    def test_modify_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            modify(1)
        with self.assertRaises(NotImplementedError):
            modify("H a")
        with self.assertRaises(NotImplementedError):
            modify(1.0)

    def test_modify_true(self):
        self.assertTrue(modify(parse_pltl("true"))
                        == modify(parse_pltl("true")))

    def test_modify_false(self):
        self.assertTrue(modify(parse_pltl("false")) ==
                        modify(parse_pltl("false")))

    def test_modify_atomic(self):
        self.assertEqual(modify(a), a)

    def test_modify_and(self):
        formula = PLTLAnd(a, b)
        result = modify(formula)
        self.assertIsInstance(result, PLTLAnd)
        self.assertEqual(result.operands[0], a)
        self.assertEqual(result.operands[1], b)
        self.assertEqual(result, _and)
        self.assertEqual(parse_pltl("b & a"), parse_pltl("a & b"))

    def test_modify_or(self):
        formula = PLTLOr(a, b)
        result = modify(formula)
        self.assertIsInstance(result, PLTLOr)
        self.assertEqual(result.operands[0], a)
        self.assertEqual(result.operands[1], b)
        self.assertEqual(parse_pltl("b | a"), parse_pltl("a | b"))
        self.assertEqual(result, _or)

    def test_modify_not(self):
        formula = PLTLNot(a)
        result = modify(formula)
        self.assertIsInstance(result, PLTLNot)
        self.assertEqual(result.argument, a)
        self.assertEqual(neg, formula)

    def test_modify_implies(self):
        formula = PLTLImplies(a, b)
        self.assertEqual(formula, implies1)
        result = modify(formula)
        self.assertIsInstance(result, PLTLOr)
        self.assertIsInstance(result.operands[0], PLTLNot)
        self.assertEqual(result.operands[0].argument, a)
        self.assertEqual(result.operands[1], b)
        self.assertEqual(implies2, result)

    def test_modify_yesterday(self):
        formula = Before(a)
        result = modify(formula)
        self.assertIsInstance(result, Before)
        self.assertEqual(result.argument, a)
        self.assertEqual(formula, result)
        self.assertEqual(yesterday, result)

    def test_modify_weak_yesterday(self):
        formula = WeakBefore(a)
        result = modify(formula)
        self.assertIsInstance(result, WeakBefore)
        self.assertEqual(result.argument, a)
        self.assertEqual(formula, result)
        self.assertEqual(weak_yesterday, result)

    def test_modify_since(self):
        formula = Since(a, b)
        result = modify(formula)
        self.assertIsInstance(result, Since)
        self.assertEqual(result.operands[0], a)
        self.assertEqual(result.operands[1], b)
        self.assertEqual(formula, result)
        self.assertEqual(since, result)

    def test_modify_triggers(self):
        formula = Triggers(a, b)
        result = modify(formula)
        self.assertIsInstance(result, Triggers)
        self.assertEqual(result.operands[0], a)
        self.assertEqual(result.operands[1], b)
        self.assertEqual(formula, result)
        self.assertEqual(triggers, result)

    def test_modify_once(self):
        formula = Once(a)
        result = modify(formula)
        self.assertIsInstance(result, Since)
        self.assertEqual(result.operands[0], true)
        self.assertEqual(result.operands[1], a)
        self.assertNotEqual(formula, result)
        self.assertEqual(once2, result)

    def test_modify_historically(self):
        formula = Historically(a)
        result = modify(formula)
        self.assertIsInstance(result, Triggers)
        self.assertEqual(result.operands[0], false)
        self.assertEqual(result.operands[0], PropositionalFalse())
        self.assertEqual(result.operands[1], a)
        self.assertNotEqual(formula, result)


# if __name__ == '__main__':
#    unittest.main()


if __name__ == '__main__':
    cov = coverage.Coverage()
    cov.start()

    try:
        unittest.main()
    except:  # catch-all except clause
        pass

    cov.stop()
    cov.save()

    cov.html_report()
    print("Done.")
    # python3 -m coverage report
    # python3 -m coverage html
