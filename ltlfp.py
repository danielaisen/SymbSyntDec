"""
module_name, package_name, ClassName, method_name, 
ExceptionName, function_name, GLOBAL_CONSTANT_NAME, 
global_var_name, instance_var_name, function_parameter_name, local_var_name.
"""

from ltlf2dfa.parser.pltlf import PLTLfParser
from ltlf2dfa.pltlf import (
    PLTLfAnd,
    PLTLfAtomic,
    PLTLfBefore,
    PLTLfEquivalence,
    PLTLfFalse,
    PLTLfHistorically,
    PLTLfImplies,
    PLTLfNot,
    PLTLfOnce,
    PLTLfOr,
    PLTLfPastRelease,
    PLTLfSince,
    PLTLfStart,
    PLTLfTrue,
    PLTLfWeakBefore,
)
from ltlf2dfa.pltlf import PLTLfFormula

parser = PLTLfParser()

def modify(formula) -> str:
    if not (special_instance(formula)):
        raise CustomError("the given formula is of a wrong type")
    elif isinstance(formula, PLTLfAtomic):
        return formula.s
    elif isinstance(formula, (PLTLfOnce)):
        return add_parentheses( "true S " + modify(formula.f))
    elif isinstance(formula, PLTLfHistorically):
        return add_parentheses( "false P " + modify(formula.f))
    elif isinstance(formula, (PLTLfImplies)):
        return add_parentheses("!" + modify(formula.formulas[0]) +' | '+ modify(formula.formulas[1]) )
    elif single_formula(formula):
        return add_parentheses(formula.operator_symbol +' '+  modify(formula.f))
    elif double_formulas(formula):
        if (len(formula.formulas)) ==2:
            return add_parentheses(modify(formula.formulas[0]) +' '+ formula.operator_symbol +' '+ modify(formula.formulas[1]) )
        else:
            return_formula = ""
            for f in formula.formulas:
                return_formula = return_formula + (' ' +  modify(f) + ' ' + formula.operator_symbol)
            return add_parentheses(return_formula[:-1])
    else:
        print("Unknown instance type")
        raise CustomError("the given formula is not of the two types")



closure_set = set()
def closure(string):
    global closure_set
    #closure_set.add(string)
    formula = parser(string)
    def recursive_closure(formula) -> str:
        print(formula)
        if not (special_instance(formula)):
            raise CustomError("the given formula is of a wrong type")
        elif isinstance(formula, PLTLfAtomic):
            closure_set.add(formula.s)
            closure_set.add('!' + formula.s)
            return formula.s
        elif single_formula(formula):
            phi = add_parentheses(formula.operator_symbol +' '+  recursive_closure(formula.f))
            closure_set.add(phi)
            return phi
        elif double_formulas(formula):
            if (len(formula.formulas)) ==2:
                phi1 =add_parentheses(recursive_closure(formula.formulas[0])) 
                closure_set.add(add_parentheses(recursive_closure(formula.formulas[0])))
                phi2 =add_parentheses(recursive_closure(formula.formulas[1])) 
                phi = phi1 +' '+ formula.operator_symbol +' '+ phi2
                closure_set.add(add_parentheses(phi))
                return phi
            else:
                return_formula = ""
                for f in formula.formulas:
                    phi1 = add_parentheses(recursive_closure(f))
                    closure_set.add(phi1)
                    return_formula = return_formula + (' ' +  phi1 + ' ' + formula.operator_symbol)
                phi = add_parentheses(return_formula[:-1])
                closure_set.add(phi)
                return phi
        else:
            print("Unknown instance type")
            raise CustomError("the given formula is not of the two types")

    recursive_closure(formula)
    return closure_set



class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def special_instance(formula) ->bool:
    instances = (PLTLfAnd,PLTLfAtomic, PLTLfBefore, PLTLfEquivalence, PLTLfFalse, PLTLfHistorically, PLTLfImplies, PLTLfNot, PLTLfOnce, PLTLfOr, PLTLfPastRelease, PLTLfSince, PLTLfStart, PLTLfTrue, PLTLfWeakBefore,)
    return isinstance(formula, instances)
    
def single_formula(formula) ->bool:
    #instances = (,, , , PLTLfFalse, , , , , , , , PLTLfStart, PLTLfTrue, ,)
    single_formula = (PLTLfAtomic, PLTLfBefore, PLTLfWeakBefore, PLTLfHistorically, PLTLfNot, PLTLfOnce)
    return isinstance(formula, single_formula)

def double_formulas(formula) ->bool:
    #instances = (,, , , PLTLfFalse, , , , , , , , PLTLfStart, PLTLfTrue, ,)
    two_formulas = (PLTLfAnd, PLTLfEquivalence, PLTLfImplies, PLTLfOr, PLTLfPastRelease, PLTLfSince)
    return isinstance(formula, two_formulas)
    

def add_parentheses(input_string):
    return f" ({input_string}) "

def run() -> None:

    
    p2 = modify(parser('true | (x -> x_xadsf) &x|y'))
    """
    from ltlf2dfa.parser.ltlf import LTLfParser

    formula_str = "G(a -> X b)"
    formula = parser(formula_str)       # returns an LTLfFormula 
    print(formula)                      # prints "G(a -> X (b))"

    """

    notX1 = "!x"
    notX2 = "~x"

    and1 = "x&y"
    and2 = "x&&y"

    or1 = "x|y"
    or2 = "x||y"

    imply1 = "x -> x_xadsf"
    imply2 = "x => y"

    iff = "a <-> b" #EQUIVALENCE: "<->" | "<=>"

    yesterday = "Y x"
    weakYesterday = "WY x"
    since = "y S x"
    triger = "y P x" #    PAST_RELEASE = "P"
    once = "O x"
    historically = "H x"

    x = " ( " + or1 + " ) & " + imply2

    extra = add_parentheses(imply1) +"&" + or1 
    true1 ="true"
    extra2 = true1 + " |" + extra

    precedence_a_b = " H (b -> O(a))"

    a = [notX1, notX2, and1, and2, or1, or2, imply1, imply2,
        yesterday, weakYesterday, since,triger, x, iff,
        once, historically, true1,  
            extra, extra2,(extra2 + "|" + "false") , ("H Y WY "+ extra2) ] 
    #a = [extra, extra2, (extra2 + "|" + "false") ]
    extra1 = parser(extra)


    for a1 in a: 
        print(a1)
        for1 = parser(a1)
        if not (special_instance(for1)):
            break
        special = modify(for1)
        print(special)
        p1 = parser(special)
        if not ((p1==for1)):
            if not (p1.operator_symbol == for1.operator_symbol):
                print("need work on:")
                print(for1, end=" =?=  ")
                print(p1)
                print(a1, end=" =?=  ")
                print(special)
        for2 = parser(a1)    
        print(for1)

    closure(modify(parser(precedence_a_b)))
    print(closure_set)
    clean_closure()
    print(closure_set)
    print("all parsed")

    #for1.f.__format__.__qualname__ == 'PLTLfAtomic.__format__' maybe the way of figuring the format of the atom?

    """ todoes 
    Figure out how I traveres the object. looking into its different elements. 
    I need to be able to recofnize at first H and O, in order to translate it to:
    H(a) = false T a
    O(a) = true S a

"""

def clean_closure():
    global closure_set
    closure_list = list(closure_set)
    closure_set.clear
    closure_temp =[]
    for element in closure_list:
        element_temp = element.strip()
        if len(element_temp) == 3 and '(' in element_temp and ')' in element_temp:
            element_temp = element_temp.replace('(', '').replace(')', '')
        elif element_temp.startswith('(') and element_temp.endswith(')'):
            i = 0
            can_delete_parantesses =  True
            for j in range(len(element_temp)):
                if element_temp[j] == '(':
                    i+=1
                if (i<1 & (j+1) != len(element_temp)):
                    can_delete_parantesses = False
                    break
                elif element_temp[j] == ')':
                    i+=-1
            if can_delete_parantesses: element_temp = element_temp[1:-1].strip()
        closure_temp.append(element_temp)
    closure_set = set(closure_temp)

def main() -> None: 
    run()

if __name__ == '__main__': 
    main()


'''
    a=[]
    for a1 in a: 
        print(a1)
        for1 = parser(a1)
        if not (special_instance(for1)):
            break
        special = modify(for1)
        print(special)
        p1 = parser(special)
        if not ((p1==for1)):
            if not (p1.operator_symbol == for1.operator_symbol):
                print("need work on:")
                print(for1, end=" =?=  ")
                print(p1)
                print(a1, end=" =?=  ")
                print(special)
        for2 = parser(a1)    
        print(for1)
'''