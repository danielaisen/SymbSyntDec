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
from past import past_declare_pattern


def parse_pltl_PLTLAnd(formula1, formula2):
    if formula1 is None:
        return formula2
    if formula2 is None:
        return formula1
    else:
        return PLTLAnd(formula1, formula2)


def initial_state(state_variables_return_atoms) -> Formula:
    yesterday_formula = state_variables_return_atoms["Yesterday"]
    weak_yesterday_formula = state_variables_return_atoms["WeakYesterday"]

    # initial_state = parse_pltl("true")
    initial_state = None
    for form in yesterday_formula:
        sub = PLTLNot(PLTLAtomic(form))
        initial_state = parse_pltl_PLTLAnd(initial_state, sub)

    for form in weak_yesterday_formula:
        sub = PLTLAtomic(form)
        initial_state = parse_pltl_PLTLAnd(initial_state, sub)

    return initial_state


def final_state(formula, sigma, state_variables) -> Formula:
    snf_form = snf(formula, sigma)
    return ground(snf_form, state_variables)


def transition_relation(state_variables_return_atoms: dict, sigma) -> (dict, Formula):  # type: ignore
    yesterday_formula = state_variables_return_atoms["Yesterday"]
    weak_yesterday_formula = state_variables_return_atoms["WeakYesterday"]
    transition_relation_dict = {}
    # transition_relation_formula = parse_pltl("true")
    transition_relation_formula = None

    for form in yesterday_formula:
        transition_relation_formula = primed_var_calculation(
            transition_relation_formula, state_variables_return_atoms, sigma, transition_relation_dict, form)

    for form in weak_yesterday_formula:
        transition_relation_formula = primed_var_calculation(
            transition_relation_formula, state_variables_return_atoms, sigma, transition_relation_dict, form)

    return transition_relation_dict, transition_relation_formula


def primed_var_calculation(transition_relation_formula, state_variables_return_atoms, sigma, transition_relation_dict, form):
    sub = state_variables_return_atoms.get(form).argument
    snf_transition = snf(sub, sigma)
    transition = ground(snf_transition, state_variables_return_atoms)
    transition_relation_dict[form+'_prime'] = transition
    formula = PLTLEquivalence(parse_pltl(form+'_prime'), sub)
    transition_relation_formula = parse_pltl_PLTLAnd(
        transition_relation_formula, formula)

    return transition_relation_formula


def str_to_pltl(set_string):
    list_elements = []
    for element in set_string:
        list_elements.append(parse_pltl(element))
    return set(list_elements)


def main():
    print("Symbolic Synthesizer for DECLARE")

    phi_env = ["resp-existence(open,regaddr)"]
    psi_simple_env = past_declare_pattern(phi_env)

    # phi_con = ["precedence(regaddr,ship)", "succession(pay,ship)"]
    phi_con = ["succession(pay,ship)"]
    psi_simple_con = past_declare_pattern(phi_con)

    action_environment_str = set(["open", "regaddr", "pay"])
    action_environment_pltl = str_to_pltl(action_environment_str)
    psi_env = past_simple_env(action_environment_pltl)

    action_controller_str = set(["ship", "skip"])

    action_controller_pltl = str_to_pltl(action_controller_str)
    psi_con = past_simple_con(action_controller_pltl)

    formula_pltl = PLTLAnd(psi_simple_con,
                           PLTLImplies(
                               PLTLAnd(psi_simple_env, psi_env),
                               psi_con))

    sigma = action_controller_pltl.union(action_environment_pltl)
    if len(sigma) != (len(action_controller_pltl) + len(action_environment_pltl)):
        raise NotImplementedError(
            f"The set of actions are not disjoint {action_controller_str, action_environment_str}")

    # formula_str = "H(b -> O(a))"  # precedence(a,b)
    # #print(formula_str)
    # formula_pltl = parse_pltl(formula_str)
    # #print(formula_pltl)
    formula_modified = modify(formula_pltl)
    # print(formula_modified)
    # print()

    closure_set_return = closure(formula_modified)
    # print(closure_set_return)
    # print(Closure_set)
    # print()

    state_variables_return, state_variables_return_atoms = state_variables(
        closure_set_return)
    # print(state_variables_return)
    # print(State_variables_set)
    # print()

    snf_formula_return = snf(formula_modified, sigma)
    # print(snf_formula_return)
    # #print(SNF_formula)
    # print()

    ground_return = ground(snf_formula_return, state_variables_return_atoms)
    # print(ground_return)

    initial_state_form = initial_state(state_variables_return_atoms)
    print(initial_state_form)

    final_state_form = final_state(
        formula_modified, sigma, state_variables_return_atoms)
    print(final_state_form)

    transition_relation_dict, transition_relation_form = transition_relation(
        state_variables_return_atoms, sigma)

    print("HERE WE GO!!!")


if __name__ == "__main__":
    main()
