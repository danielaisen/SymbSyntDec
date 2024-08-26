from src.SymbSyntDec.main import SymbSyntDec

sigma_controlled_str = {"set", "pay", "cancel"}

sigma_environment_str = {"ship", "refund"}

specification_con_phiC_str = {"absence2(pay)", "absence2(cancel)", "resp-existence(pay,set)",
                              "neg-succession(ship,cancel)", "neg-succession(ship,set)"}

specification_env_phiE_str = {
    "precedence(set, ship)", "precedence(pay, ship)", "precedence(pay, refund)",
    "response(pay, ship | refund)", "neg-succession(cancel, ship)"
}

symbolicDFA = SymbSyntDec(sigma_controlled_str, sigma_environment_str,
                          specification_env_phiE_str, specification_con_phiC_str, "main_experiment_flipped")

print("The symbolic DFA is found to be:")
for key in symbolicDFA:
    print(f"{key}:\n{symbolicDFA[key]}\n\n")
