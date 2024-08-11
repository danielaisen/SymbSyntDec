from pylogics_modalities.parsers import parse_pltl

from SymDFA2AIGER import SymDFA2AIGER


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


from snf import snf
from ground import ground
from pastSimple import past_simple_con, past_simple_env
from past import past_declare_pattern
from modify import modify
from closure import closure, Closure_set
from state_variables import state_variables, State_variables_simple_dict, complex_dic_atoms


def parse_pltl_PLTLAnd(formula1, formula2):
    if formula1 is None:
        return formula2
    if formula2 is None:
        return formula1
    else:
        return PLTLAnd(formula1, formula2)


def initial_state(state_variables_return_atoms) -> Formula:

    initial_state = None

    if "Yesterday" in state_variables_return_atoms:
        yesterday_formula = state_variables_return_atoms["Yesterday"]
        for form in yesterday_formula:
            sub = PLTLNot(PLTLAtomic(form))
            initial_state = parse_pltl_PLTLAnd(initial_state, sub)

    if "WeakYesterday" in state_variables_return_atoms:
        weak_yesterday_formula = state_variables_return_atoms["WeakYesterday"]
        for form in weak_yesterday_formula:
            sub = PLTLAtomic(form)
            initial_state = parse_pltl_PLTLAnd(initial_state, sub)

    return initial_state


def transition_relation(state_variables_return_atoms: dict, sigma) -> (dict, Formula):  # type: ignore
    transition_relation_dict = {}
    transition_relation_formula = None

    if "Yesterday" in state_variables_return_atoms:
        yesterday_formula = state_variables_return_atoms["Yesterday"]
        for form in yesterday_formula:
            transition_relation_formula = primed_var_calculation(
                transition_relation_formula, state_variables_return_atoms, sigma, transition_relation_dict, form)

    if "WeakYesterday" in state_variables_return_atoms:
        weak_yesterday_formula = state_variables_return_atoms["WeakYesterday"]
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


def SymbSyntDec(sigma_controlled_str: set[str], sigma_environment_str: set[str], specification_env_phiE_str: set[str],
                specification_con_phiC_str: set[str], file_name: str = "SymbSyntDec_master_thesis.aag"):

    print("Symbolic Synthesizer for DECLARE")

    action_environment_pltl = str_to_pltl(sigma_environment_str)
    psi_simple_env = past_declare_pattern(specification_env_phiE_str)
    psi_env = past_simple_env(action_environment_pltl)

    action_controller_pltl = str_to_pltl(sigma_controlled_str)
    psi_simple_con = past_declare_pattern(specification_con_phiC_str)
    psi_con = past_simple_con(action_controller_pltl)

    formula_pltl = PLTLAnd(psi_simple_con,
                           PLTLImplies(
                               PLTLAnd(psi_simple_env, psi_env),
                               psi_con))

    # formula_pltl = PLTLAnd(psi_simple_con, psi_simple_env, psi_con)
    # formula_pltl = psi_env
    '''
    # not working!!
    formula_pltl = PLTLAnd(psi_simple_con, psi_simple_env, psi_env)
    formula_pltl = PLTLAnd(psi_simple_con, psi_simple_env, psi_env, psi_con)
    formula_pltl = PLTLAnd(psi_simple_con,
                           PLTLImplies(
                               psi_env,
                               psi_con))
    formula_pltl = PLTLImplies(
        PLTLAnd(psi_simple_env, psi_env),
        psi_con)
        '''

    sigma = action_controller_pltl.union(action_environment_pltl)
    if len(sigma) != (len(action_controller_pltl) + len(action_environment_pltl)):
        raise NotImplementedError(
            f"The set of actions are not disjoint {sigma_controlled_str, sigma_environment_str}")

    formula_modified = modify(formula_pltl)

    closure_set_return = closure(formula_modified, sigma)

    state_variables_return_dict, state_variables_return_atoms = state_variables(
        closure_set_return)

    snf_formula_return = snf(formula_modified, sigma)

    t_c = closure(snf_formula_return, sigma)
    t_s1, ts2 = state_variables(t_c)

    ground_return = ground(snf_formula_return, state_variables_return_atoms)

    initial_state_form = initial_state(state_variables_return_atoms)
    print(f"Initial state formula: \n {initial_state_form} \n")

#    def final_state(formula, sigma, state_variables) -> Formula:
 #   snf_form = snf(formula, sigma)
  #  return ground(snf_form, state_variables)
#    final_state_form = final_state(formula_modified, sigma, state_variables_return_atoms)

    final_state_form = ground_return
    print(f"Final state formula: \n {final_state_form}\n")

    transition_relation_dict, transition_relation_form = transition_relation(
        state_variables_return_atoms, sigma)
    print(f"Transition state formula: \n {transition_relation_form}\n")
    print("done Symbolic DFA\n")

    sigma_controlled = action_controller_pltl
    sigma_environment = action_environment_pltl

    state_variables_input = set(list(state_variables_return_dict.keys()))
    state_variables_input = (list(state_variables_return_dict.keys()))

    initial_state_input = initial_state_form
    # transition_system_input = transition_relation_form
    transition_system_input = transition_relation_dict
    final_state_variable = final_state_form

    print("calling SymDFA2AIGER\n")
    SymDFA2AIGER(sigma_controlled, sigma_environment, state_variables_input,
                 initial_state_input, transition_system_input, final_state_variable, file_name, state_variables_return_dict)

    print("done SymDFA2AIGER\n")

    symbolicDFA = {}
    symbolicDFA["initial_state_form"] = initial_state_form
    symbolicDFA["transition_relation_form"] = transition_relation_form
    symbolicDFA["final_state_form"] = final_state_form

    return symbolicDFA
