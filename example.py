from SymbSyntDec import SymbSyntDec

sigma_controlled_str = {"ship"}
# sigma_controlled_str = {"ship", "skip"}
sigma_environment_str = {"open", "pay"}
# sigma_environment_str = {"open", "regaddr", "pay"}
specification_env_phiE_str = {"resp-existence(open,pay)"}
# specification_env_phiE_str = {"resp-existence(open,regaddr)"}
specification_con_phiC_str = {"succession(pay,ship)"}


symbolicDFA = SymbSyntDec(sigma_controlled_str, sigma_environment_str,
                          specification_env_phiE_str, specification_con_phiC_str)

print()
print("The symbolic DFA is found to be:")
for key in symbolicDFA:
    print(f"{key}:\n{symbolicDFA[key]}\n\n")
