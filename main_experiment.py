from src.SymbSyntDec import SymbSyntDec

sigma_environment_str = {"set", "pay", "cancel"}

sigma_controlled_str = {"ship", "refund"}

specification_env_phiE_str = {"absence2(pay)", "absence2(cancel)", "resp-existence(pay,set)",
                              "neg-succession(ship,cancel)", "neg-succession(ship,set)"}

specification_con_phiC_str = {
    "precedence(set, ship)", "precedence(pay, ship)", "precedence(pay, refund)",
    "response(pay, ship | refund)", "neg-succession(cancel, ship)"
}

symbolicDFA = SymbSyntDec(sigma_controlled_str, sigma_environment_str,
                          specification_env_phiE_str, specification_con_phiC_str, "main_experiment")

print("The symbolic DFA is found to be:")
for key in symbolicDFA:
    print(f"{key}:\n{symbolicDFA[key]}\n\n")
