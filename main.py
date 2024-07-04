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

from closure import closure, clear_set, Closure_set
from modify import modify
from state_variables import state_variables, State_variables_set, State_variables_set_atoms
from snf import snf
from ground import ground


def main():
    print("Symbolic Synthesizer for DECLARE")
    formula_str = "H(b -> O(a))"  # precedence(a,b)
    print(formula_str)
    formula_pltl = parse_pltl(formula_str)
    print(formula_pltl)
    formula_modified = modify(formula_pltl)
    print(formula_modified)
    print()

    closure_set_return = closure(formula_modified)
    print(closure_set_return)
    print(Closure_set)
    print()

    state_variables_return, state_variables_return_atoms = state_variables(
        closure_set_return)
    print(state_variables_return)
    print(State_variables_set)
    print()

    snf_formula_return = snf(formula_modified, closure_set_return)
    print(snf_formula_return)
    # print(SNF_formula)
    print()

    ground_return = ground(snf_formula_return, state_variables_return_atoms)
    print(ground_return)

    print("HERE WE GO!!!")


if __name__ == "__main__":
    main()


def initial_state(state_variables_return_atoms) -> Formula:
    yesterday_formula = state_variables_return_atoms["Yesterday"]
    weak_yesterday_formula = state_variables_return_atoms["WeakYesterday"]

    initial_state = parse_pltl("true")
    for form in yesterday_formula:
        initial_state = PLTLAnd(*form)

    return initial_state
