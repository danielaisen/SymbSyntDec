from pylogics_modalities.parsers import parse_pltl

from pylogics_modalities.syntax.base import Formula
import re


def past_declare_pattern(declare_pattern) -> Formula:
    transformations = {
        "existence\((\w+)\)": "O({p})",
        "absence2\((\w+)\)": "H({p} -> ZH(!{p}))",
        "choice\((\w+), (\w+)\)": "O({p} | {q})",
        "exc-choice\((\w+), (\w+)\)": "O({p} | {q}) & (H(!{p}) | H(!{q}))",
        "resp-existence\((\w+), (\w+)\)": "H(!{p}) | O({q})",
        "coexistence\((\w+), (\w+)\)": "(H(!{p}) | O({q})) & (H(!{q}) | O({p}))",
        "response\((\w+), (\w+)\)": "{q} T (!{p} | {q})",
        "precedence\((\w+), (\w+)\)": "H({q} -> O({p}))",
        "succession\((\w+), (\w+)\)": "{p} T (!{p} | {q}) & H({q} -> O({p}))",
        "alt-response\((\w+), (\w+)\)": "({p} | {q}) T (!{p}) & H({q} -> Z({q} T (({p}|!{q})&Z({q} T (!{p})))))",
        "alt-precedence\((\w+), (\w+)\)": "H({q} -> O({p})) & H({q} & !{p} -> Z({q} T ({q} & !{p})))",
        "alt-succession\((\w+), (\w+)\)": "( ({p} | {q}) T (!{p}) & H({q} -> Z({q} T (({p}|!{q})&Z({q} T (!{p}))))) ) & ( H({q} -> O({p})) & H({q} & !{p} -> Z({q} T ({q} & !{p}))) )",
        "chain-response\((\w+), (\w+)\)": "!{p} & H(!{q} | ({p} -> {q}))",
        "chain-precedence\((\w+), (\w+)\)": "H({q} -> Z({p}))",
        "chain-succession\((\w+), (\w+)\)": "(!{p} & H(!{q} | ({p} -> {q}))) & (H({q} -> Z({p})))",
        "not-coexistence\((\w+), (\w+)\)": "H(!{p} | H(!{q}))",
        "neg-succession\((\w+), (\w+)\)": "H(!{p} | {q}) S ({p} & !{q} & Z H(!{p}))",
        "neg-chain-succession\((\w+), (\w+)\)": "H(Y({q} -> !{q}) & H(Y({q} -> !{p})))"
    }

    for pattern, template in transformations.items():
        match = re.fullmatch(pattern, declare_pattern)
        if match:
            return parse_pltl(template.format(p=match.group(1), q=match.group(2) if len(match.groups()) > 1 else None))

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
   pastified = past_declare_pattern(declare_pattern)
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
