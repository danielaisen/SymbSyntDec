import json


def formula_to_dict(formula):
    # Convert the formula object to a dictionary (example, you need to implement this)
    return formula.__dict__


def save_formulas_to_json(filename, initial_state_form, final_state_form, transition_relation_form):
    data = {
        'initial_state_form': formula_to_dict(initial_state_form),
        'final_state_form': formula_to_dict(final_state_form),
        'transition_relation_form': formula_to_dict(transition_relation_form)
    }
    with open(filename, 'w') as f:
        json.dump(data, f)


def save_formulas_to_json(filename, initial_state_form, final_state_form, transition_relation_form):
    data = {
        'initial_state_form': formula_to_dict(initial_state_form),
        'final_state_form': formula_to_dict(final_state_form),
        'transition_relation_form': formula_to_dict(transition_relation_form)
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_formulas_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return (dict_to_formula(data['initial_state_form']),
            dict_to_formula(data['final_state_form']),
            dict_to_formula(data['transition_relation_form']))
