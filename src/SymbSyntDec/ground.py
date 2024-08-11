
from functools import singledispatch

from pylogics_modalities.syntax.base import (
    And as PLTLAnd,
    Or as PLTLOr,
    Formula,
    Not as PLTLNot,
    _UnaryOp
)
from pylogics_modalities.syntax.pltl import (
    Atomic as PLTLAtomic,
    Before,
    WeakBefore,
    PropositionalFalse,
    PropositionalTrue
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
    return formula


@ground_operands.register
def ground_operands_prop_false(formula: PropositionalFalse) -> Formula:
    return formula


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


@ground_operands.register
def ground_operands_yesterday(formula: Before) -> Formula:
    var = PLTLAtomic(State_var.get(formula))
    return var


@ground_operands.register
def ground_operands_weak_yesterday(formula: WeakBefore) -> Formula:
    var = PLTLAtomic(State_var.get(formula))
    return var
