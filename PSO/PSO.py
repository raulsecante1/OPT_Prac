# Implementation of algoritm PSO
# supposing that the function is given like f(x1,x2,...) = y

import random
import numpy
import json
import math

inicial_a = []  # corresponde inicio parameters for the function

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


def func_a():
    '''
    The function to optimize
    Args:
          x
    Returns:
          y
    '''
    pass

inicial = [0, 0]  # corresponde inicio parameters for the function
def func(x1, x2):
    return 20 + (x1**2 - 10 * math.cos(2 * math.pi * x1)) + (x2 ** 2 - 10 * math.cos(2 * math.pi * x2))

def main_PSO():
    '''
    The main part of the PSO optimization
    '''

    with open('parameters.json', 'r') as file:
       raw_data = json.load(file)["parameter_sets"]["config_2_40_1"]
       data = raw_data["pso_params"]


    #iteration = iterations["Academic_Toy_Problems"]  # how many iterations for one PSO run

    r_p = random.uniform(0,1)
    r_g = random.uniform(0,1)

    #S, omiga, phi_p, phi_g, iteration
    swarm_size = data["swarm_size"]
    inertia_omega = data["omega"]
    cognitive_component_phip = data["phi_p"]
    social_component_phig = data["phi_g"]
    iteration = data["fitness_evaluations"]/swarm_size
    
    best_loc_self = [inicial for _ in range(swarm_size)]
    best_loc_social = inicial

    k = random.uniform(0.1, 0.2)
    upper_bound = 1
    lower_bound = -1
    velocity =  [random.uniform(-k * (upper_bound - lower_bound), + k * (upper_bound - lower_bound)) for _ in range(swarm_size)]
    currently_position = [inicial for _ in range(swarm_size)]

    for _ in range(iteration):
        for ind in range(swarm_size):
            velocity[ind] = velocity[ind] * inertia_omega + cognitive_component_phip * r_p * (best_loc_self[ind] - currently_position[ind]) + social_component_phig * r_g * (best_loc_social - currently_position[ind])
            currently_position[ind] = numpy.array(currently_position[ind]) + numpy.array(velocity[ind])
            if func(*currently_position[ind]) < func(*best_loc_self[ind]):
                best_loc_self[ind] = currently_position[ind]
            if func(*currently_position[ind]) < func(*best_loc_social):
                best_loc_social = currently_position[ind]

    return (best_loc_social, func(*best_loc_social))
        

