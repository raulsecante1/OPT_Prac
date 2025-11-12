# Implementation of algoritm PSO
# supposing that the function is given like f(x1,x2,...) = y

import numpy
import random
import copy

'''
def func_template(x1, x2, ...):
    
    The function to optimize
    Args:
          x
    Returns:
          y
    
    return func(x1, x2, ...)
'''

def func(x1, x2, ...):
    '''
    The function to optimize
    Args:
          x
    Returns:
          y
    '''
    return func(x1, x2, ...)

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
    iteration = n_it
    dimension = n_d
    n_bee = n_b
    domain_x = list_d_X #dominio de cada variable [[x_1_min, x_1_max],...]
    sol_swarm = [[0 for _ in range(dimension)] for _ in range(n_bee)]
    new_cand_sol_v = [[0 for _ in range(dimension)] for _ in range(n_bee)]
    fit = [0 for _ in range(n_bee)]
    selection_probability = [0 for _ in range(n_bee)]

    for i in range(n_bee):  #Initialization
        for j in range(dimension):
            sol_swarm[i][j] = domain_x[j][0] + random.uniform(0,1) * (domain_x[1] - domain_x[0])
    
    for _ in range(iteration):
        for i in range(n_bee):  #Employed Bees Phase
            for j in range(dimension):
                k = random.randint(1, n_d)
                new_cand_sol_v[i][j] = sol_swarm[i][j] + random.uniform(0,1) * (sol_swarm[i][j] - sol_swarm[k][j])
            if func(*new_cand_sol_v[i]) < func(*sol_swarm[i]):  #Update the bee or the solution
                sol_swarm[i] = copy.deepcopy(new_cand_sol_v[i])

        for i in range(n_bee):  #Onlooker Bees Phase
            fx = func(*sol_swarm)
            if fx >= 0:
                fit[i] = 1 / (1 + fx)
            else:
                fit[i] = 1 + numpy.abs(fx)
        
        fit_sum = sum(fit)
        for i in range(n_bee):
            selection_probability[i] = fit[i]/fit_sum

