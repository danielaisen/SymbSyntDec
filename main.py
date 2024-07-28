from pylogics_modalities.parsers import parse_pltl
from pylogics_modalities.syntax.base import (
    And as PLTLAnd,
    Or as PLTLOr,
    Formula,
    Implies as PLTLImplies,
    Not as PLTLNot,
    _UnaryOp,
    Equivalence as PLTLEquivalence
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
from pastSimple import past_simple_con, past_simple_env


def initial_state(state_variables_return_atoms) -> Formula:
    yesterday_formula = state_variables_return_atoms["Yesterday"]
    weak_yesterday_formula = state_variables_return_atoms["WeakYesterday"]

    initial_state = parse_pltl("true")
    for form in yesterday_formula:
        sub = PLTLNot(PLTLAtomic(form))
        initial_state = PLTLAnd(initial_state, sub)

    for form in weak_yesterday_formula:
        sub = PLTLAtomic(form)
        initial_state = PLTLAnd(initial_state, sub)

    return initial_state


def final_state(formula, closure_set, state_variables) -> Formula:
    snf_form = snf(formula, closure_set)
    return ground(snf_form, state_variables)


def transition_relation(state_variables_return_atoms: dict, closure_set) -> (dict, Formula):  # type: ignore
    yesterday_formula = state_variables_return_atoms["Yesterday"]
    weak_yesterday_formula = state_variables_return_atoms["WeakYesterday"]
    transition_relation_dict = {}
    transition_relation_formula = parse_pltl("true")

    for form in yesterday_formula:
        transition_relation_formula = snf_for_primed_var(
            transition_relation_formula, state_variables_return_atoms, closure_set, transition_relation_dict, form)

    for form in weak_yesterday_formula:
        transition_relation_formula = snf_for_primed_var(
            transition_relation_formula, state_variables_return_atoms, closure_set, transition_relation_dict, form)

    return transition_relation_dict, transition_relation_formula


def snf_for_primed_var(transition_relation_formula, state_variables_return_atoms, closure_set, transition_relation_dict, form):
    sub = state_variables_return_atoms.get(form).argument
    transition = snf(sub, closure_set)
    transition_relation_dict[form+'_prime'] = transition
    formula = PLTLEquivalence(parse_pltl(form+'_prime'), sub)
    transition_relation_formula = PLTLAnd(
        transition_relation_formula, formula)

    return transition_relation_formula


def str_to_pltl(set_string):
    list_elements = []
    for element in set_string:
        list_elements.append(parse_pltl(element))
    return set(list_elements)


def main():
    print("Symbolic Synthesizer for DECLARE")

    action_environment_str = set(["a", "t"])
    action_environment_pltl = str_to_pltl(action_environment_str)
    psi_env = past_simple_env(action_environment_pltl)

    action_controller_str = set(["b", "c"])
    action_controller_pltl = str_to_pltl(action_controller_str)
    psi_con = past_simple_con(action_controller_pltl)

    psi_simple_env = ""
    psi_simple_con = ""

    formula = PLTLAnd(psi_simple_con,
                      PLTLImplies(
                          PLTLAnd(psi_simple_env, psi_env),
                          psi_con))

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

    initial_state_form = initial_state(state_variables_return_atoms)
    print(initial_state_form)

    final_state_form = final_state(
        formula_modified, closure_set_return, state_variables_return_atoms)
    print(final_state_form)

    transition_relation_dict, transition_relation_form = transition_relation(
        state_variables_return_atoms, closure_set_return)

    print("HERE WE GO!!!")


if __name__ == "__main__":
    main()
