# SymbSyntDec

## Description

SymbSyntDec is a tool designed to convert a DECLARE specification of a system into an AIGER file (.aag). This conversion is achieved through a novel transformation into a symbolic deterministic finite automaton (SDFA), which is then used as input for the `SymDFA2AIGER` tool. 
The main function provided is `SymbSyntDec`. 
An example input file is included in this directory to demonstrate the expected format for the function.

#### Personal Note

This tool was created by Daniel Bachmann Aisen as part of his master’s thesis. 
In 2024, amidst challenging times, this project is dedicated to the safe return of all hostages, to the soldiers safeguarding my friends, family, and me, and in memory of those who have fallen. 
May we look forward to better days.

## Inputs

The tool requires four inputs corresponding to full DECLARE specification of a system:

- `sigma_controlled_str`: `set[str]`
- `sigma_environment_str`: `set[str]`
- `specification_env_phiE_str`: `set[str]`
- `specification_con_phiC_str`: `set[str]`

### Optional Inputs

- `file_name`: `str` (default: `"SymbSyntDec_master_thesis.aag"`)


### Example Usage

```python
sigma_environment_str = {"set", "pay", "cancel"}
sigma_controlled_str = {"ship", "refund"}

specification_env_phiE_str = {"absence2(pay)", "absence2(cancel)", "resp-existence(pay,set)", "neg-succession(ship,cancel)", "neg-succession(ship,set)"}
specification_con_phiC_str = {"precedence(set, ship)", "precedence(pay, ship)", "precedence(pay, refund)", "response(pay, ship | refund)", "neg-succession(cancel, ship)"
}

symbolicDFA = SymbSyntDec(sigma_controlled_str, sigma_environment_str, specification_env_phiE_str, specification_con_phiC_str, "SymbSyntDec_master_thesis.aag")
```

## Installation and Dependencies

This tool requires three external libraries: [pylogics_modalities](https://github.com/danielaisen/pylogics_modalities), [SymDFA2Aiger](https://github.com/danielaisen/SymDFA2Aiger) and `multipledispatch`.

- **pylogics_modalities**: This library extends the pylogics library by whitemech. To install it, use the `.whl` file provided in the `dependencies` folder.

`pip install dependencies/pylogics_modalities-0.2.2-py3-none-any.whl`
`pip install SymDFA2Aiger`
`pip install multipledispatch`

```bash
pip install SymbSyntDec