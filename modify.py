"""Modify the formulas to exclude the modalities: Once, Historically; and the logical operation implies."""

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


def modify_unaryop(formula: _UnaryOp):
    """Modify the sub-formulas for a given formula."""
    return modify(formula.argument)


@ singledispatch
def modify(formula: object) -> Formula:
    """Modify a formula."""
    raise NotImplementedError(
        f"Modify not implemented for object of type {type(formula)}"
    )


@modify.register
def modify_prop_true(formula: PropositionalTrue) -> Formula:
    return formula


@modify.register
def modify_prop_false(formula: PropositionalFalse) -> Formula:
    return formula


@modify.register
def modify_false(formula: FalseFormula) -> Formula:
    return formula


@modify.register
def modify_atomic(formula: PLTLAtomic) -> Formula:
    return formula


@modify.register
def modify_and(formula: PLTLAnd) -> Formula:
    """Compute the base formula for all sub-formulas combined with And relation."""
    sub = [modify(f) for f in formula.operands]
    return PLTLAnd(*sub)


@modify.register
def modify_or(formula: PLTLOr) -> Formula:
    """Compute the base formula for all sub-formulas combined with Or relation."""
    sub = [modify(f) for f in formula.operands]
    return PLTLOr(*sub)


@modify.register
def modify_not(formula: PLTLNot) -> Formula:
    """Compute the base formula of the negated formula."""
    return PLTLNot(modify_unaryop(formula))


@modify.register
def modify_implies(formula: PLTLImplies) -> Formula:
    """Compute the base formula for an Implies formula. Returns A DNF formula"""
    head = [PLTLNot(modify(f)) for f in formula.operands[:-1]]
    tail = formula.operands[-1]
    return PLTLOr(*head, tail)


@modify.register
def modify_yesterday(formula: Before) -> Formula:
    """Compute the base formula for a Before (Yesterday) formula."""
    return Before(modify_unaryop(formula))


@modify.register
def modify_weak_yesterday(formula: WeakBefore) -> Formula:
    """Compute the base formula for a WeakBefore (Weak Yesterday) formula."""
    return WeakBefore(modify_unaryop(formula))


@modify.register
def modify_since(formula: Since) -> Formula:
    """Compute the base formula for a Since formulas."""
    # if len(formula.operands) != 2:
    #    head = formula.operands[0]
    #    tail = Since(*formula.operands[1:])
    #    return modify(Since(head, tail))
    sub = [modify(f) for f in formula.operands]
    return Since(*sub)


@modify.register
def modify_since(formula: Triggers) -> Formula:
    """Compute the base formula for a Triggers formula."""
    # if len(formula.operands) != 2:
    #    head = formula.operands[0]
    #    tail = Triggers(*formula.operands[1:])
    #    return modify(Triggers(head, tail))
    sub = [modify(f) for f in formula.operands]
    return Triggers(*sub)


@modify.register
def modify_once(formula: Once) -> Formula:
    # Compute the base formula for a Once formula.
    """Modify the modality to Once with use of the computed base formula. Example: "O(a)" translated into "true S a"   """
    sub = [parse_pltl("true"), modify_unaryop(formula)]
    return Since(*sub)


@modify.register
def modify_historically(formula: Historically) -> Formula:
    """Modify the modality to Since with use of the computed base formula. Example: "H(a)" translated into "false T a"   """
    sub = [parse_pltl("false"), modify_unaryop(formula)]
    return Triggers(*sub)


'''
# Examples:
formula_str = "!a S H(a)"  # should be modifies to  ( !a S (false T a))
print(formula_str)
formula_pltl = parse_pltl(formula_str)
print(formula_pltl)
formula_modified = modify(formula_pltl)  # (since (not a) (triggers false a))
print(formula_modified)

formula_str = "O a"  # should be modifies to  (true S a)
print(formula_str)
formula_pltl = parse_pltl(formula_str)
print(formula_pltl)
# (since PropositionalTrue(Logic.PLTL) a)
formula_modified = modify(formula_pltl)
print(formula_modified)

'''
