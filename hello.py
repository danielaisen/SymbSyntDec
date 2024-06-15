import aiger

x, y, z, w = aiger.atoms('x', 'y', 'z', 'w')

expr1 = z.implies(x & y)
expr2 = z & w

circ1 = expr1.with_output('z').aig    # Get AIG for expr1 with output 'z'.aig
#circ2 = circ1 >> circ2                # Feed outputs of circ1 into circ2.
########## HERE ##########

import aiger
x, y, z = aiger.atoms('x', 'y', 'z')
expr1 = x & y  # circuit with inputs 'x', 'y' and 1 output computing x AND y.
expr2 = x | y  # logical or.
expr3 = x ^ y  # logical xor.
expr4 = x == y  # logical ==, xnor.
expr5 = x.implies(y)
expr6 = ~x  # logical negation.
expr7 = aiger.ite(x, y, z)  # if x then y else z.

# Atoms can be constants.
expr8 = x & True  # Equivalent to just x.
expr9 = x & False # Equivalent to const False.

# Specifying output name of boolean expression.
# - Output is a long uuid otherwise.
expr10 = expr5.with_output('x_implies_y')
assert expr10.output == 'x_implies_y'

# And you can inspect the AIG if needed.
circ = x.aig

# And of course, you can get a BoolExpr from a single output aig.
expr10 = aiger.BoolExpr(circ)



import aiger
#from aiger import utils

# Parser for ascii AIGER format.
aig1 = aiger.load("and.aag")
aig2 = aiger.load("ex1.aag")
a1ig2 = aiger.load("unr.aag")

a1ig1 = aiger.load("unr1.aag")
a1ig2 = aiger.load("unr2.aag")
a1ig3 = aiger.load("unr3.aag")

aig3 = aig1 >> aig2
aig33 = aig1 >> aig1

aig4 = aig1 | aig2

# Connect output y to input x with delay, initialized to True.
# (Default initialization is False.)
#aig5 = aig1.loopback({   "input": "x", "output": "y", })

########## HERE ##########

'''aig6 = aig1.loopback({
  "input": "x", "output": "y",
}, {
  "input": "z", "output": "z", "latch": "z_latch",
  "init": False, "keep_outputs": False
})
'''
########## HERE ##########



# Relabel input 'x' to 'z'.
aig1['i', {'x': 'z'}]
aig1.relabel('input', {'x': 'z'})

# Relabel output 'y' to 'w'.
aig1['o', {'y': 'w'}]
aig1.relabel('output', {'y': 'w'})

# Relabel latches 'l1' to 'l2'.
aig1['l', {'l1': 'l2'}]
aig1.relabel('latch', {'l1': 'l2'})



# Combinatoric evaluation.
#aig3(inputs={'x':True, 'y':False})

# Sequential evaluation.
'''sim = aig3.simulate([{'x': 0, 'y': 0}, 
                    {'x': 1, 'y': 2},
                    {'x': 3, 'y': 4}])

'''
########## HERE ##########

# Simulation Coroutine
sim = aig3.simulator()  # Coroutine
next(sim)  # Initialize
#print(sim.send({'x': 0, 'y': 0}))
#print(sim.send({'x': 1, 'y': 2}))
#print(sim.send({'x': 3, 'y': 4}))


# Unroll
#aig4 = aig3.unroll(steps=10, init=True)
########## HERE ##########


# Fix input x to be False.
aig4 = aiger.source({'x': False}) >> aig3

# Remove output y. 
aig4 = aig3 >> aiger.sink(['y'])

# Create duplicate w of output y.
aig4 = aig3 >> aiger.tee({'y': ['y', 'w']})

a2 = aiger.common.eval_order(aig1)  # Returns topological ordering of circuit gates.

# Convert object into an AIG from multiple formats including BoolExpr, AIG, str, and filepaths.
a1 = aiger.to_aig(aig1)

print("h")
