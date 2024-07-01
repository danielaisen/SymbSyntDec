
"""Modify the formula with base operators visitor."""
from pylogics_modalities.parsers import parse_pltl
from functools import singledispatch

from pylogics_modalities.syntax.base import And as PLTLAnd
from pylogics_modalities.syntax.base import Formula
from pylogics_modalities.syntax.base import Not as PLTLNot
from pylogics_modalities.syntax.base import Or as PLTLOr
from pylogics_modalities.syntax.base import _UnaryOp
from pylogics_modalities.syntax.pltl import Atomic as PLTLAtomic
from pylogics_modalities.syntax.pltl import (
    Before,
    WeakBefore,
    FalseFormula,
    PropositionalFalse,
    PropositionalTrue,
    Since,
    Triggers,
)
from modify import modify

Closure_set = set()


def clear_set():
    Closure_set.clear()


def closure_unaryop(formula: _UnaryOp):
    return closure_operands(formula.argument)


def closure(formula: object) -> set:
    Closure_set.add(formula)
    closure_operands(formula)
    return set(Closure_set)


@ singledispatch
def closure_operands(formula: object) -> Formula:
    raise NotImplementedError(
        f"Closure not implemented for object of type {type(formula)}"
    )


@closure_operands.register
def closure_prop_true(formula: PropositionalTrue) -> Formula:
    # TODO check if I should add true and negated formulas into the closure?
    return formula


@closure_operands.register
def closure_prop_false(formula: PropositionalFalse) -> Formula:
    # TODO check if I should add true and negated formulas into the closure?
    return formula


# @closure_operands.register
# def closure_false(formula: FalseFormula) -> Formula:
#    return formula


@closure_operands.register
def closure_atomic(formula: PLTLAtomic) -> Formula:
    Closure_set.add(formula)
    Closure_set.add(PLTLNot(formula))
    return formula


@closure_operands.register
def closure_and(formula: PLTLAnd) -> Formula:
    Closure_set.add(formula)
    sub = [closure_operands(f) for f in formula.operands]
    return PLTLAnd(*sub)


@closure_operands.register
def closure_or(formula: PLTLOr) -> Formula:
    Closure_set.add(formula)
    sub = [closure_operands(f) for f in formula.operands]
    return PLTLOr(*sub)


@closure_operands.register
def closure_not(formula: PLTLNot) -> Formula:
    Closure_set.add(formula)
    return PLTLNot(closure_unaryop(formula))


# @closure_operands.register
# def closure_implies(formula: PLTLImplies) -> Formula:
#    Closure_set.add(formula)
#    """Compute the base formula for an Implies formula. Returns A DNF formula"""
#    head = [PLTLNot(closure_operands(f)) for f in formula.operands[:-1]]
#    tail = formula.operands[-1]
#    return PLTLOr(*head, tail)


@closure_operands.register
def closure_yesterday(formula: Before) -> Formula:
    Closure_set.add(formula)
    """Compute the base formula for a Before (Yesterday) formula."""
    return Before(closure_unaryop(formula))


@closure_operands.register
def closure_weak_yesterday(formula: WeakBefore) -> Formula:
    Closure_set.add(formula)
    """Compute the base formula for a WeakBefore (Weak Yesterday) formula."""
    return WeakBefore(closure_unaryop(formula))


@closure_operands.register
def closure_since(formula: Since) -> Formula:
    """Compute the base formula for a Since formulas."""
    Closure_set.add(formula)
    if len(formula.operands) != 2:
        head = formula.operands[0]
        tail = Since(*formula.operands[1:])
        return closure(Since(head, tail))
    sub = [closure_operands(f) for f in formula.operands]
    since = Since(*sub)
    Closure_set.add(since)
    Closure_set.add(Before(since))
    return since


@closure_operands.register
def closure_since(formula: Triggers) -> Formula:
    Closure_set.add(formula)
    if len(formula.operands) != 2:
        head = formula.operands[0]
        tail = Triggers(*formula.operands[1:])
        return closure(Triggers(head, tail))
    sub = [closure_operands(f) for f in formula.operands]
    triggers = Triggers(*sub)
    Closure_set.add(triggers)
    Closure_set.add(WeakBefore(triggers))
    return triggers


# Once and Historically are undefined in the Closure definition we are using
'''
# Examples:
formula_str = "!a S H(a)"  # a T (Y b)
print(formula_str)
formula_pltl = parse_pltl(formula_str)
print(formula_pltl)
# should be modifies to  ( !a S (false T a))
# (since (not a) (triggers false a))
formula_modified = modify(formula_pltl)
print(formula_modified)
# should return: {a, !a, b, !b, a T (Y b) , Y b, Z (a T (Y b) ) }
closure_set_return = closure(formula_mogdified)

'''
