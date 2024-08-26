# This files calls only some subsection of the main algorithm.


from src.SymbSyntDec.main import SymbSyntDec

sigma_controlled_str = {"a"}
sigma_environment_str = {"b"}


specification_con_phiC_str = {}
specification_env_phiE_str = {"precedence(a, b)"}


symbolicDFA = SymbSyntDec(sigma_controlled_str, sigma_environment_str,
                          specification_env_phiE_str, specification_con_phiC_str, "SymbSyntDec_master_thesis")

print("The symbolic DFA is found to be:")
for key in symbolicDFA:
    print(f"{key}:\n{symbolicDFA[key]}\n\n")
