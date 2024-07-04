
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


State_variables_set = set()
State_variables_set_atoms = {}
index = 1


def clear_set():
    State_variables_set.clear()


def state_variables_unaryop(formula: _UnaryOp):
    return state_variables_operands(formula.argument)


def state_variables(formula: set) -> (set, dict):  # type: ignore
    for form in formula:
        state_variables_operands(form)
    return set(State_variables_set), (State_variables_set_atoms)


@ singledispatch
def state_variables_operands(formula: object) -> Formula:
    raise NotImplementedError(
        f"State_variables not implemented for object of type {type(formula)}"
    )


@state_variables_operands.register
def state_variables_prop_true(formula: PropositionalTrue) -> Formula:
    # TODO check if I should add true and negated formulas into the state_variables?
    return formula


@state_variables_operands.register
def state_variables_prop_false(formula: PropositionalFalse) -> Formula:
    # TODO check if I should add true and negated formulas into the state_variables?
    return formula


# @state_variables_operands.register
# def state_variables_false(formula: FalseFormula) -> Formula:
#    return formula


@state_variables_operands.register
def state_variables_atomic(formula: PLTLAtomic) -> Formula:
    return formula


@state_variables_operands.register
def state_variables_and(formula: PLTLAnd) -> Formula:

    sub = [state_variables_operands(f) for f in formula.operands]
    return PLTLAnd(*sub)


@state_variables_operands.register
def state_variables_or(formula: PLTLOr) -> Formula:

    sub = [state_variables_operands(f) for f in formula.operands]
    return PLTLOr(*sub)


@state_variables_operands.register
def state_variables_not(formula: PLTLNot) -> Formula:

    return PLTLNot(state_variables_unaryop(formula))


@state_variables_operands.register
def state_variables_implies(formula: PLTLImplies) -> Formula:
    """Compute the base formula for an Implies formula. Returns A DNF formula"""
    head = [PLTLNot(state_variables_operands(f))
            for f in formula.operands[:-1]]
    tail = formula.operands[-1]
    return PLTLOr(*head, tail)


@state_variables_operands.register
def state_variables_yesterday(formula: Before) -> Formula:
    """Compute the base formula for a Before (Yesterday) formula."""
    add_variable(formula, "Before")
    # State_variables_set.add(' '+str(formula))
    return Before(state_variables_unaryop(formula))


@state_variables_operands.register
def state_variables_weak_yesterday(formula: WeakBefore) -> Formula:
    """Compute the base formula for a WeakBefore (Weak Yesterday) formula."""
    add_variable(formula, "WeakBefore")
    # State_variables_set.add('_ '+str(formula))
    return WeakBefore(state_variables_unaryop(formula))


def add_variable(formula, modality):
    global State_variables_set_atoms
    State_variables_set.add(formula)
    if not (formula in State_variables_set_atoms):
        global index
        State_variables_set_atoms['x_var' + str(index)] = formula
        State_variables_set_atoms[formula] = 'x_var' + str(index)
        if not (modality in State_variables_set_atoms):
            State_variables_set_atoms[modality] = ['x_var' + str(index)]
        else:
            State_variables_set_atoms[modality] = State_variables_set_atoms[modality] + [
                'x_var' + str(index)]
        index += 1


@state_variables_operands.register
def state_variables_since(formula: Since) -> Formula:
    """Compute the base formula for a Since formulas."""

    if len(formula.operands) != 2:
        head = formula.operands[0]
        tail = Since(*formula.operands[1:])
        return state_variables(Since(head, tail))
    sub = [state_variables_operands(f) for f in formula.operands]
    return Since(*sub)


@state_variables_operands.register
def state_variables_since(formula: Triggers) -> Formula:

    if len(formula.operands) != 2:
        head = formula.operands[0]
        tail = Triggers(*formula.operands[1:])
        return state_variables(Triggers(head, tail))
    sub = [state_variables_operands(f) for f in formula.operands]
    return Triggers(*sub)


# Once and Historically are undefined in the State_variables definition we are using
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
state_variables_set_return = state_variables(formula_mogdified)

'''
