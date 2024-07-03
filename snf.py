
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

# SNF_formula = parse_pltl("true")
closure_set = None


def snf_unaryop(formula: _UnaryOp):
    return snf_operands(formula.argument)


def snf(formula: object, closure: set) -> Formula:
    global closure_set
    closure_set = closure
    return snf_operands(formula)


@ singledispatch
def snf_operands(formula: object) -> Formula:
    raise NotImplementedError(
        f"State_variables not implemented for object of type {type(formula)}"
    )


@snf_operands.register
def snf_prop_true(formula: PropositionalTrue) -> Formula:
    # TODO check if I should add true and negated formulas into the snf?
    return formula


@snf_operands.register
def snf_prop_false(formula: PropositionalFalse) -> Formula:
    # TODO check if I should add true and negated formulas into the snf?
    return formula


# @snf_operands.register
# def snf_false(formula: FalseFormula) -> Formula:
#    return formula


@snf_operands.register
def snf_atomic(formula: PLTLAtomic) -> Formula:
    if formula in closure_set:
        # global SNF_formula
        # SNF_formula = PLTLAnd(SNF_formula, formula)
        return formula
    return None


@snf_operands.register
def snf_and(formula: PLTLAnd) -> Formula:
    sub = [snf_operands(f) for f in formula.operands]
    return PLTLAnd(*sub)


@snf_operands.register
def snf_or(formula: PLTLOr) -> Formula:
    sub = [snf_operands(f) for f in formula.operands]
    return PLTLOr(*sub)


@snf_operands.register
def snf_not(formula: PLTLNot) -> Formula:
    return PLTLNot(snf_unaryop(formula))


@snf_operands.register
def snf_implies(formula: PLTLImplies) -> Formula:
    """Compute the base formula for an Implies formula. Returns A DNF formula"""
    head = [PLTLNot(snf_operands(f))
            for f in formula.operands[:-1]]
    tail = formula.operands[-1]
    return PLTLOr(*head, tail)


@snf_operands.register
def snf_yesterday(formula: Before) -> Formula:
    """Compute the base formula for a Before (Yesterday) formula."""
    return Before(snf_unaryop(formula))


@snf_operands.register
def snf_weak_yesterday(formula: WeakBefore) -> Formula:
    """Compute the base formula for a WeakBefore (Weak Yesterday) formula."""
    return WeakBefore(snf_unaryop(formula))


@snf_operands.register
def snf_since(formula: Since) -> Formula:
    """Compute the base formula for a Since formulas."""
    # if len(formula.operands) != 2:
    #    head = formula.operands[0]
    #    tail = Since(*formula.operands[1:])
    #    return snf_operands(Since(head, tail))
    # sub = [snf_operands(f) for f in formula.operands]
    # return Since(*sub)
    sub1 = snf_operands(formula.operands[0])
    sub2 = snf_operands(formula.operands[1])
    sub3 = Before(formula)
    return (PLTLOr(sub2, (PLTLAnd(sub1, sub3))))


@snf_operands.register
def snf_since(formula: Triggers) -> Formula:
    sub1 = snf_operands(formula.operands[0])
    sub2 = snf_operands(formula.operands[1])
    sub3 = WeakBefore(formula)
    return (PLTLAnd(sub2, (PLTLOr(sub1, sub3))))
    # if len(formula.operands) != 2:
    #    head = formula.operands[0]
    #    tail = Triggers(*formula.operands[1:])
    #    return snf_operands(Triggers(head, tail))
    # sub = [snf_operands(f) for f in formula.operands]
    # return Triggers(*sub)


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
snf_set_return = snf(formula_mogdified)

'''
