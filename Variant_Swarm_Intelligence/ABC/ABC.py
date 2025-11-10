# Implementation of algoritm PSO
# supposing that the function is given like f(x1,x2,...) = y

import numpy
import random

'''
inicial_template = [[x1_1, x1_2, x1_3,...],...,[xn_1, xn_2, xn_3,...]]   corresponde inicio parameters for the function
def func_template(x1, x2,...):
    
    The function to optimize
    Args:
          x
    Returns:
          y
    
    return func(x1, x2, ...)
'''

def ABC_main():
    '''
    The main part of the ABC optimization:
        
        Initialization Phase 

        REPEAT 

        Employed Bees Phase

        Onlooker Bees Phase

        Scout Bees Phase

        Memorize the best solution achieved so far

        UNTIL(Cycle=Maximum Cycle Number or a Maximum CPU time)

        
    '''
    dimension = n

