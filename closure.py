
"""Modify the formula with base operators visitor."""
from pylogics_modalities.parsers import parse_pltl
from functools import singledispatch

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
from functools import singledispatch
# from modify import modify

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
    True


@closure_operands.register
def closure_prop_false(formula: PropositionalFalse) -> Formula:
    # TODO check if I should add true and negated formulas into the closure?
    True


# @closure_operands.register
# def closure_false(formula: FalseFormula) -> Formula:
#    return formula


@closure_operands.register
def closure_atomic(formula: PLTLAtomic) -> Formula:
    Closure_set.add(formula)
    Closure_set.add(PLTLNot(formula))


@closure_operands.register
def closure_and(formula: PLTLAnd) -> Formula:
    Closure_set.add(formula)
    sub = [closure_operands(f) for f in formula.operands]


@closure_operands.register
def closure_or(formula: PLTLOr) -> Formula:
    Closure_set.add(formula)
    sub = [closure_operands(f) for f in formula.operands]


@closure_operands.register
def closure_not(formula: PLTLNot) -> Formula:
    Closure_set.add(formula)
    closure_unaryop(formula)


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
    closure_unaryop(formula)


@closure_operands.register
def closure_weak_yesterday(formula: WeakBefore) -> Formula:
    Closure_set.add(formula)
    """Compute the base formula for a WeakBefore (Weak Yesterday) formula."""
    closure_unaryop(formula)


@closure_operands.register
def closure_since(formula: Since) -> Formula:
    """Compute the base formula for a Since formulas."""
    Closure_set.add(Before(formula))
    for form in formula.operands:
        closure_operands(form)


@closure_operands.register
def closure_since(formula: Triggers) -> Formula:
    Closure_set.add(WeakBefore(formula))
    for form in formula.operands:
        closure_operands(form)


'''
# Once and Historically are undefined in the Closure definition we are using
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
