from pylogics_modalities.parsers import parse_pltl

from pylogics_modalities.syntax.base import (Formula, And as PLTLAnd)
import re


def past_declare_pattern(declare_pattern_set) -> Formula:
    pltl_formula = None
    for element in declare_pattern_set:
        if pltl_formula is None:
            pltl_formula = past_declare_pattern_call(element)
        else:
            pltl_formula = PLTLAnd(
                pltl_formula, past_declare_pattern_call(element))

    return pltl_formula


def past_declare_pattern_call(declare_pattern) -> str:
    transformations = {
        r"existence\(\s*(.+?)\s*\)": "O({p})",
        r"absence2\(\s*(.+?)\s*\)": "H({p} -> Z H(!{p}))",
        r"choice\(\s*(.+?)\s*,\s*(.+?)\s*\)": "O({p} | {q})",
        r"exc-choice\(\s*(.+?)\s*,\s*(.+?)\s*\)": "O({p} | {q}) & (H(!{p}) | H(!{q}))",
        r"resp-existence\(\s*(.+?)\s*,\s*(.+?)\s*\)": "H(!{p}) | O({q})",
        r"coexistence\(\s*(.+?)\s*,\s*(.+?)\s*\)": "(H(!{p}) | O({q})) & (H(!{q}) | O({p}))",
        r"response\(\s*(.+?)\s*,\s*(.+?)\s*\)": "{q} T (!{p} | {q})",
        r"precedence\(\s*(.+?)\s*,\s*(.+?)\s*\)": "H({q} -> O({p}))",
        r"succession\(\s*(.+?)\s*,\s*(.+?)\s*\)": "{p} T (!{p} | {q}) & H({q} -> O({p}))",
        r"alt-response\(\s*(.+?)\s*,\s*(.+?)\s*\)": "({p} | {q}) T (!{p}) & H({q} -> Z({q} T (({p}|!{q})&Z({q} T (!{p})))))",
        r"alt-precedence\(\s*(.+?)\s*,\s*(.+?)\s*\)": "H({q} -> O({p})) & H({q} & !{p} -> Z({q} T ({q} & !{p})))",
        r"alt-succession\(\s*(.+?)\s*,\s*(.+?)\s*\)": "( ({p} | {q}) T (!{p}) & H({q} -> Z({q} T (({p}|!{q})&Z({q} T (!{p}))))) ) & ( H({q} -> O({p})) & H({q} & !{p} -> Z({q} T ({q} & !{p}))) )",
        r"chain-response\(\s*(.+?)\s*,\s*(.+?)\s*\)": "!{p} & H(!{q} | ({p} -> {q}))",
        r"chain-precedence\(\s*(.+?)\s*,\s*(.+?)\s*\)": "H({q} -> Z({p}))",
        r"chain-succession\(\s*(.+?)\s*,\s*(.+?)\s*\)": "(!{p} & H(!{q} | ({p} -> {q}))) & (H({q} -> Z({p})))",
        r"not-coexistence\(\s*(.+?)\s*,\s*(.+?)\s*\)": "H(!{p} | H(!{q}))",
        r"neg-succession\(\s*(.+?)\s*,\s*(.+?)\s*\)": "H(!{p} | {q}) S ({p} & !{q} & Z H(!{p}))",
        r"neg-chain-succession\(\s*(.+?)\s*,\s*(.+?)\s*\)": "H(Y({q} -> !{q}) & H(Y({q} -> !{p})))"
    }

    for pattern, template in transformations.items():
        match = re.fullmatch(pattern, declare_pattern)
        if match:
            formatted_template = template.format(p=match.group(
                1), q=match.group(2) if len(match.groups()) > 1 else None)
            return parse_pltl(formatted_template)

    return "Unknown pattern"


'''
declare_patterns = [
    "existence(p1)",
    "neg-chain-succession(p1, q2)",
    "succession(p1, q2)",
    "response(p1, q2)",
    "precedence(p1, q2)",
    "alt-response(p1, q2)",
    "alt-precedence(p1, q2)",
    "alt-succession(p1, q2)",
    "chain-response(p1, q2)",
    "chain-precedence(p1, q2)",
    "chain-succession(p1, q2)",
    "not-coexistence(p1, q2)",
    "neg-succession(p1, q2)"
]

# Transformations
for declare_pattern in declare_patterns:
    pastified = past_declare_pattern({declare_pattern})
    print(f"{declare_pattern:<24}-> {pastified}")


# Examples
declare_patterns = [
    "existence(p1)",
    "neg-chain-succession(p1, q2)",
    "succession(p1, q2)",
    "response(p1, q2)",
    "precedence(p1, q2)",
    "alt-response(p1, q2)",
    "alt-precedence(p1, q2)",
    "alt-succession(p1, q2)",
    "chain-response(p1, q2)",
    "chain-precedence(p1, q2)",
    "chain-succession(p1, q2)",
    "not-coexistence(p1, q2)",
    "neg-succession(p1, q2)"
]

# Transformations
for declare_pattern in declare_patterns:
    pastified = past_declare_pattern(declare_pattern)
    print(pastified)
    p1 = parse_pltl(pastified)
    print(p1)

'''
