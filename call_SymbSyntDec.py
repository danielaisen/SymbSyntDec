from SymbSyntDec import SymbSyntDec

sigma_controlled_str = {"ship", "skip"}
sigma_environment_str = {"open", "pay", "regaddr", "reqc"}

# specification_env_phiE_str = {"resp-existence(open,pay)"}
# sigma_environment_str = {"open", "nothing", "regaddr"}


# sigma_controlled_str = {"ship", "skip"}
# sigma_environment_str = {"open"}
# sigma_environment_str = {"open", "regaddr", "pay"}


specification_con_phiC_str = {"succession(pay,ship)"}
specification_env_phiE_str = {
    "resp-existence(open,regaddr)", "resp-existence(open,pay)", "succession(open,pay)"}


symbolicDFA = SymbSyntDec(sigma_controlled_str, sigma_environment_str,
                          specification_env_phiE_str, specification_con_phiC_str, "SymbSyntDec_master_thesis")

print("The symbolic DFA is found to be:")
for key in symbolicDFA:
    print(f"{key}:\n{symbolicDFA[key]}\n\n")
