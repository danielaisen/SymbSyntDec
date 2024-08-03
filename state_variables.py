
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


State_variables_simple_dict = {}
State_variables_set_atoms = {}
index = 1


def state_variables_unaryop(formula: _UnaryOp):
    return state_variables_operands(formula.argument)


def state_variables(formula: set) -> (set, dict):  # type: ignore
    for form in formula:
        state_variables_operands(form)
    return State_variables_simple_dict, (State_variables_set_atoms)


@ singledispatch
def state_variables_operands(formula: object) -> Formula:
    raise NotImplementedError(
        f"State_variables not implemented for object of type {type(formula)}"
    )


@state_variables_operands.register
def state_variables_prop_true(formula: PropositionalTrue):
    True


@state_variables_operands.register
def state_variables_prop_false(formula: PropositionalFalse):
    True


@state_variables_operands.register
def state_variables_atomic(formula: PLTLAtomic):
    True


@state_variables_operands.register
def state_variables_and(formula: PLTLAnd):
    True


@state_variables_operands.register
def state_variables_or(formula: PLTLOr):
    True


@state_variables_operands.register
def state_variables_not(formula: PLTLNot):
    True


@state_variables_operands.register
def state_variables_implies(formula: PLTLImplies):
    True


@state_variables_operands.register
def state_variables_yesterday(formula: Before) -> Formula:
    """Compute the base formula for a Before (Yesterday) formula."""
    add_variable(formula, "Yesterday")
    state_variables_unaryop(formula)


@state_variables_operands.register
def state_variables_weak_yesterday(formula: WeakBefore) -> Formula:
    """Compute the base formula for a WeakBefore (Weak Yesterday) formula."""
    add_variable(formula, "WeakYesterday")
    state_variables_unaryop(formula)


def add_variable(formula, modality):
    global State_variables_set_atoms
    if not (formula in State_variables_set_atoms):
        global index
        State_variables_set_atoms['x_var' + str(index)] = formula
        State_variables_set_atoms[formula] = 'x_var' + str(index)
        State_variables_simple_dict['x_var' + str(index)] = formula
        if not (modality in State_variables_set_atoms):
            State_variables_set_atoms[modality] = ['x_var' + str(index)]
        else:
            State_variables_set_atoms[modality] = State_variables_set_atoms[modality] + [
                'x_var' + str(index)]
        index += 1
    # it already exists and we do not want duplications


@state_variables_operands.register
def state_variables_since(formula: Since):
    True


@state_variables_operands.register
def state_variables_since(formula: Triggers):
    True
