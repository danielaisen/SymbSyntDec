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
from typing import Set


def past_simple_env(formula: Set[PLTLAtomic]) -> Formula:
    true_var = parse_pltl("true")
    false_var = parse_pltl("false")
    or_u = false_var
    and_neg_u = true_var
    and_not_u1_and_u2 = true_var
    phi1 = true_var
    for u1 in formula:
        or_u = PLTLOr(or_u, u1)
        and_neg_u = PLTLAnd(and_neg_u, PLTLNot(u1))
        if len(formula) == 1:
            and_not_u1_and_u2 = PLTLNot(u1)
            phi1 = PLTLImplies(or_u, and_not_u1_and_u2)
        else:
            for u2 in formula:
                if not u1.__eq__(u2):
                    phi_temp = PLTLNot(PLTLAnd(u1, u2))
                    and_not_u1_and_u2 = PLTLAnd(and_not_u1_and_u2, phi_temp)
            phi_temp = PLTLImplies(or_u, and_not_u1_and_u2)
            phi1 = PLTLAnd(phi1, phi_temp)
    phi2 = PLTLImplies(Before(or_u), and_neg_u)
    phi3 = PLTLImplies(Before(Before(or_u)), or_u)

    left = Once(PLTLAnd
                (WeakBefore(false_var), or_u))
    right = Historically(
        PLTLAnd(phi1, PLTLAnd(phi2, phi3)))

    return PLTLAnd(left, right)


def past_simple_con(formula: Set[PLTLAtomic]) -> Formula:
    true_var = parse_pltl("true")
    false_var = parse_pltl("false")
    or_c = false_var
    and_neg_c = true_var
    and_not_c1_and_c2 = true_var
    phi1 = true_var
    for c1 in formula:
        or_c = PLTLOr(or_c, c1)
        and_neg_c = PLTLAnd(and_neg_c, PLTLNot(c1))
        if len(formula) == 1:
            and_not_c1_and_c2 = PLTLNot(c1)
            phi1 = PLTLImplies(Before(and_neg_c),
                               PLTLAnd(or_c, and_not_c1_and_c2))
        else:
            for c2 in formula:
                if not c1.__eq__(c2):
                    phi_temp = PLTLNot(PLTLAnd(c1, c2))
                    and_not_c1_and_c2 = PLTLAnd(and_not_c1_and_c2, phi_temp)

            phi_temp = PLTLImplies(
                Before(or_c), PLTLAnd(or_c, and_not_c1_and_c2))
            phi1 = PLTLAnd(phi1, phi_temp)

    phi2 = PLTLImplies(Before(Before(and_neg_c)), and_neg_c)

    left = Once(PLTLAnd
                (WeakBefore(false_var), or_c))
    right = Historically(
        PLTLAnd(phi1, phi2))

    return PLTLAnd(left, right)


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
