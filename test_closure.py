from pylogics_modalities.parsers import parse_pltl
from pylogics_modalities.syntax.base import (
    And as PLTLAnd,
    Or as PLTLOr,
    Formula,
    Implies as PLTLImplies,
    Not as PLTLNot,
    _UnaryOp
)
from pylogics_modalities.syntax.pltl import (
    Atomic as PLTLAtomic,
    Before,
    WeakBefore,
    FalseFormula,
    Historically,
    Once,
    PropositionalFalse,
    PropositionalTrue,
    Since,
    Triggers
)

import unittest
import coverage

from SymbSynDec.modify import modify
from SymbSynDec.closure import closure, clear_set

a = modify(PLTLAtomic("a"))
b = modify(PLTLAtomic("b"))
c = modify(PLTLAtomic("c"))
d = modify(PLTLAtomic("d"))
neg = modify(parse_pltl("!a"))
_and = modify(parse_pltl("a & b"))
_or = modify(parse_pltl("a | b"))
implies1 = modify(parse_pltl("a -> b"))
implies2 = modify(parse_pltl("(!a) | b"))
yesterday = modify(parse_pltl("Y a"))
weak_yesterday = modify(parse_pltl("Z a"))
historically = modify(parse_pltl("H a"))
once1 = modify(parse_pltl("O a"))
once2 = modify(parse_pltl("true S a"))
false = modify(parse_pltl("false"))
true = modify(parse_pltl("true"))
since = modify(parse_pltl("a S b"))
triggers = modify(parse_pltl("a T b"))


class TestModify(unittest.TestCase):

    def test_closure_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            closure(1)
        with self.assertRaises(NotImplementedError):
            closure("H a")
        with self.assertRaises(NotImplementedError):
            closure(parse_pltl("H a"))
        with self.assertRaises(NotImplementedError):
            closure(parse_pltl("O a"))
        with self.assertRaises(NotImplementedError):
            closure(1.0)

    def test_closure_since(self):
        clear_set()
        formula = Since(a, b)
        result = closure(formula)
        print(result)
        self.assertIsInstance(result, set)
        self.assertEqual(len(result), 6)
        set_elements = {a, PLTLNot(a), b, PLTLNot(
            b), formula, Before(formula)}
        self.assertSetEqual(result, set_elements)

    def test_closure_triggers(self):
        clear_set()
        formula = Triggers(a, b)
        result = closure(formula)
        self.assertIsInstance(result, set)
        self.assertEqual(len(result), 6)
        set_elements = {a, PLTLNot(a), b, PLTLNot(
            b), formula, WeakBefore(formula)}
        self.assertSetEqual(result, set_elements)
    '''
    def test_closure_true(self):
        self.assertTrue(closure(parse_pltl("true"))
                        == closure(parse_pltl("true")))

    def test_closure_false(self):
        self.assertTrue(closure(parse_pltl("false")) ==
                        closure(parse_pltl("false")))

    def test_closure_atomic(self):
        self.assertEqual(closure(a), a)

    def test_closure_and(self):
        formula = PLTLAnd(a, b)
        result = closure(formula)
        self.assertIsInstance(result, PLTLAnd)
        self.assertEqual(result.operands[0], a)
        self.assertEqual(result.operands[1], b)
        self.assertEqual(result, _and)
        self.assertEqual(parse_pltl("b & a"), parse_pltl("a & b"))

    def test_closure_or(self):
        formula = PLTLOr(a, b)
        result = closure(formula)
        self.assertIsInstance(result, PLTLOr)
        self.assertEqual(result.operands[0], a)
        self.assertEqual(result.operands[1], b)
        self.assertEqual(parse_pltl("b | a"), parse_pltl("a | b"))
        self.assertEqual(result, _or)

    def test_closure_not(self):
        formula = PLTLNot(a)
        result = closure(formula)
        self.assertIsInstance(result, PLTLNot)
        self.assertEqual(result.argument, a)
        self.assertEqual(neg, formula)

    def test_closure_implies(self):
        formula = PLTLImplies(a, b)
        self.assertEqual(formula, implies1)
        result = closure(formula)
        self.assertIsInstance(result, PLTLOr)
        self.assertIsInstance(result.operands[0], PLTLNot)
        self.assertEqual(result.operands[0].argument, a)
        self.assertEqual(result.operands[1], b)
        self.assertEqual(implies2, result)

    def test_closure_yesterday(self):
        formula = Before(a)
        result = closure(formula)
        self.assertIsInstance(result, Before)
        self.assertEqual(result.argument, a)
        self.assertEqual(formula, result)
        self.assertEqual(yesterday, result)

    def test_closure_weak_yesterday(self):
        formula = WeakBefore(a)
        result = closure(formula)
        self.assertIsInstance(result, WeakBefore)
        self.assertEqual(result.argument, a)
        self.assertEqual(formula, result)
        self.assertEqual(weak_yesterday, result)




    def test_closure_once(self):
        formula = Once(a)
        result = closure(formula)
        self.assertIsInstance(result, Since)
        self.assertEqual(result.operands[0], true)
        self.assertEqual(result.operands[1], a)
        self.assertNotEqual(formula, result)
        self.assertEqual(once2, result)

    def test_closure_historically(self):
        formula = Historically(a)
        result = closure(formula)
        self.assertIsInstance(result, Triggers)
        self.assertEqual(result.operands[0], false)
        self.assertEqual(result.operands[0], PropositionalFalse())
        self.assertEqual(result.operands[1], a)
        self.assertNotEqual(formula, result)

'''
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
