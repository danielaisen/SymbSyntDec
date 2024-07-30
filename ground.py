
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


State_var = {}


def ground(formula: object, state_var: dict) -> Formula:
    global State_var
    State_var = state_var
    return ground_operands(formula)


def ground_operands_unaryop(formula: _UnaryOp):
    return ground_operands(formula.argument)


@ singledispatch
def ground_operands(formula: object) -> Formula:
    raise NotImplementedError(
        f"Ground not implemented for object of type {type(formula)}"
    )


@ground_operands.register
def ground_operands_prop_true(formula: PropositionalTrue) -> Formula:
    # TODO check if I should add true and negated formulas into the ground_operands?
    return formula


@ground_operands.register
def ground_operands_prop_false(formula: PropositionalFalse) -> Formula:
    # TODO check if I should add true and negated formulas into the ground_operands?
    return formula


# @ground_operands.register
# def ground_operands_false(formula: FalseFormula) -> Formula:
#    return formula


@ground_operands.register
def ground_operands_atomic(formula: PLTLAtomic) -> Formula:
    return formula


@ground_operands.register
def ground_operands_and(formula: PLTLAnd) -> Formula:
    sub = [ground_operands(f) for f in formula.operands]
    return PLTLAnd(*sub)


@ground_operands.register
def ground_operands_or(formula: PLTLOr) -> Formula:
    sub = [ground_operands(f) for f in formula.operands]
    return PLTLOr(*sub)


@ground_operands.register
def ground_operands_not(formula: PLTLNot) -> Formula:
    return PLTLNot(ground_operands_unaryop(formula))


'''
@ground_operands.register
def ground_operands_implies(formula: PLTLImplies) -> Formula:
    """Compute the base formula for an Implies formula. Returns A DNF formula"""
    head = [PLTLNot(ground_operands(f))
            for f in formula.operands[:-1]]
    tail = formula.operands[-1]
    return PLTLOr(*head, tail)
'''


@ground_operands.register
def ground_operands_yesterday(formula: Before) -> Formula:
    var = PLTLAtomic(State_var.get(formula))
    return var
    sub = ground_operands_unaryop(formula)
    return PLTLAnd(var, sub)


@ground_operands.register
def ground_operands_weak_yesterday(formula: WeakBefore) -> Formula:
    var = PLTLAtomic(State_var.get(formula))
    return var
    # sub = ground_operands_unaryop(formula)
    # return PLTLAnd(var, sub)


'''
@ground_operands.register
def ground_operands_since(formula: Since) -> Formula:
    """Compute the base formula for a Since formulas."""
    if len(formula.operands) != 2:
        head = formula.operands[0]
        tail = Since(*formula.operands[1:])
        return ground_operands(Since(head, tail))
    sub = [ground_operands(f) for f in formula.operands]
    return Since(*sub)


@ground_operands.register
def ground_operands_since(formula: Triggers) -> Formula:
    if len(formula.operands) != 2:
        head = formula.operands[0]
        tail = Triggers(*formula.operands[1:])
        return ground_operands(Triggers(head, tail))
    sub = [ground_operands(f) for f in formula.operands]
    return Triggers(*sub)
'''
