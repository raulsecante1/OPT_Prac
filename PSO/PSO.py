# Implementation of algoritm PSO
# supposing that the function is given like f(x1,x2,...) = y

import random
import numpy
import json

iterations = {"Academic_Toy_Problems": random.randint(50,200),
              "Engineering_Design_Problems": random.randint(200,1000),
              "Hyperparameter_Tuning_for_Machine_Learning": random.randint(100, 500),
              "Neural_Network_Weight_Training": random.randint(1000, 2500)
             }  #use table to get iteration instead

#Problem Dimensions, Fitness Evaluations, S, omiga, phi_p, phi_g
table = [[2, 40, 25, 0.3925, 2.5586, 1.3358],
         [2, 40, 29, -0.434, -0.6504, 2.2073],
         [2, 4000, 156, 0.4091, 2.1304, 1.0575],
         [2, 4000, 237, -0.2887, 0.4862, 2.5067],
         [5, 1000, 63, -0.3595, -0.7238, 2.0289],
         [5, 1000, 47, -0.1832, 0.5287, 3.1913],
         [5, 10000, 223, -0.3669, -0.1027, 3.3657],
         [5, 10000, 203, 0.5069, 2.5524, 1.0056],
         [10, 2000, 63, 0.6571, 1.6319, 0.6239],
         [10, 2000, 204, -0.2134, -0.3344, 2.3259],
         [10, 20000, 53, -0.3488, -0.2476, 4.8976],
         [20, 40000, 69, -0.4438, -0.2699, 3.3950],
         [20, 400000, 149, -0.3236, -0.1136, 3.9789]]

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
    
inicial_upper_simple = 5.24  # for estimating those initial values of x
inicial_lowwer_simple = -5.24
def func_simple(x1, x2):
    '''
    primero calculando su gradiente igualando a 0 => 2x+20πsin(2πx) == 0
                                                     2y+20πsin(2πy) == 0
    luego tenemos un punto critico (0, 0), y 2 otro mas.
    y pasandolos a la matriz hessiano, tiene que (0, 0) es el minimo global
    '''
    return (20 + x1**2 + x2**2 - 10*(numpy.cos(2*numpy.pi*x1) + numpy.cos(2*numpy.pi*x2)))

inicial_upper_ackley = 32.768  # for estimating those initial values of x
inicial_lowwer_ackley = -32.768

def func(*args):
    '''
    The Ackley Function function to optimize
    Args:
          args: the tuple of the (x1, x2, ...), which in this case should be dynamically depends on the PSO_main for testing convenience
    Returns:
          y
    '''
    x = numpy.array(args)
    n = len(x)
    sum_sq = numpy.sum(x**2)
    sum_cos = numpy.sum(numpy.cos(2 * numpy.pi * x))
    term1 = -20 * numpy.exp(-0.2 * numpy.sqrt(sum_sq / n))
    term2 = -numpy.exp(sum_cos / n)
    return term1 + term2 + 20 + numpy.exp(1)

def main_PSO():
    '''
    The main part of the PSO optimization
    '''

    with open('PSO_config.json', 'r') as file:
       raw_data = json.load(file)["parameter_sets"]["config_10_20000_1"]
       data = raw_data["pso_params"]


    #iteration = iterations["Academic_Toy_Problems"]  # how many iterations for one PSO run

    #S, omiga, phi_p, phi_g, iteration
    swarm_size = data["swarm_size"]
    inertia_omega = data["omega"]
    cognitive_component_phip = data["phi_p"]
    social_component_phig = data["phi_g"]
    problem_dimension = data["problem_dimension"]
    iteration = int(data["fitness_evaluations"]/swarm_size)

    inicial_upper = inicial_upper_ackley
    inicial_lowwer = inicial_lowwer_ackley

    inicial = [[random.uniform(inicial_lowwer, inicial_upper) for _ in range(problem_dimension)] for _ in range(swarm_size)]

    best_loc_self = [inicial.copy()[i] for i in range(swarm_size)]
    best_loc_social = min(inicial, key=lambda x: func(*x))


    k = random.uniform(0.1, 0.2)
    upper_bound = 1
    lower_bound = -1
    velocity =  [[random.uniform(-k * (upper_bound - lower_bound), + k * (upper_bound - lower_bound)) for _ in range(problem_dimension)] for _ in range(swarm_size)]

    currently_position = [inicial.copy()[i] for i in range(swarm_size)]

    for _ in range(iteration):
        for ind in range(swarm_size):
            r_p = random.uniform(0,1)
            r_g = random.uniform(0,1)

            velocity[ind] = numpy.array(velocity[ind]) * inertia_omega + cognitive_component_phip * r_p * (numpy.array(best_loc_self[ind]) - numpy.array(currently_position[ind])) + social_component_phig * r_g * (numpy.array(best_loc_social) - numpy.array(currently_position[ind]))
            
            currently_position[ind] = numpy.array(currently_position[ind]) + numpy.array(velocity[ind])
            currently_position[ind] = numpy.clip(currently_position[ind], inicial_lowwer, inicial_upper)  #limits the value to not get the particle fly freely

            if func(*currently_position[ind]) < func(*best_loc_self[ind]):
                best_loc_self[ind] = currently_position[ind]
            if func(*currently_position[ind]) < func(*best_loc_social):
                best_loc_social = currently_position[ind]

    print(best_loc_social, func(*best_loc_social))
    #return (best_loc_social, func(*best_loc_social))
        
main_PSO()