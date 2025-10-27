# algoritmo para el set-cover
# la entrada tiene la forma Set: [a, b, c, d, e, f,...], y los subconjuntos: [[[a, b, c,...], c1], [[b, d,...], c2],...]
# se define el concepto de valor como len(x_s_i) con x_s_i={y|y in Set and y in s_i}
# y tiene el algoritmo de log-opt.



# debug mode is on !!



import math
import ste_cover_ej
import random


sett = [f"x{i}" for i in range(1, 51)]
coleccion = [
    ["x1","x2","x3","x4","x5","x10", 8],
    ["x6","x7","x8","x9","x10","x15","x20", 10],
    ["x11","x12","x13","x14","x15","x16","x17", 9],
    ["x18","x19","x20","x21","x22","x23", 7],
    ["x24","x25","x26","x27","x28","x29", 6],
    ["x30","x31","x32","x33","x34","x35","x36", 11],
    ["x37","x38","x39","x40","x41", 5],
    ["x42","x43","x44","x45","x46","x47","x48","x49","x50", 9],
    ["x1","x6","x11","x16","x21","x26","x31","x36","x41","x46", 14],
    ["x2","x7","x12","x17","x22","x27","x32","x37","x42","x47", 13],
    ["x3","x8","x13","x18","x23","x28","x33","x38","x43","x48", 12],
    ["x4","x9","x14","x19","x24","x29","x34","x39","x44","x49", 15],
    ["x5","x10","x15","x20","x25","x30","x35","x40","x45","x50", 16],
    ["x1","x5","x9","x13","x17","x21","x25","x29","x33","x37","x41","x45","x49", 18],
    ["x2","x6","x10","x14","x18","x22","x26","x30","x34","x38","x42","x46","x50", 17],
    ["x3","x7","x11","x15","x19","x23","x27","x31","x35","x39","x43","x47", 15],
    ["x4","x8","x12","x16","x20","x24","x28","x32","x36","x40","x44","x48", 14],
    ["x5","x15","x25","x35","x45", 8],
    ["x10","x20","x30","x40","x50", 7],
    ["x1","x11","x21","x31","x41", 6],
    ["x2","x12","x22","x32","x42", 6],
    ["x3","x13","x23","x33","x43", 6],
    ["x4","x14","x24","x34","x44", 6],
    ["x5","x25","x45","x15","x35", 7],
    ["x6","x26","x36","x46","x16", 8],
    ["x7","x27","x37","x47","x17", 9],
    ["x8","x28","x38","x48","x18", 9],
    ["x9","x29","x39","x49","x19", 9],
    ["x10","x30","x40","x50","x20", 9],
]

'''
sett = ["a", "b", "c", "d", "e", "f", "g"]
coleccion = [["a","b", 5],
             ["a", "c", "e", 9],
             ["f", "g", 4],
             ["a", "e", "f", 7],
             ["d", "g", 3],
             ["b", "d", "e", 12]]
'''

cubierta = []

def minus(lista, listb = sett, listc = cubierta):
    '''
    se calcula cuantos elementos de la listb estan en lista 
    Args: 
          lista(list): se refiere a elemento de coleccion
          listb(list): se refiere a sett
          listc(list): se refiere a cubierta
    Return:
          n(int): cantidad de elementos de la listb estan en lista 
    '''
    n = 0
    for elem in lista:
        if (elem in listb) and (elem not in listc):
            n += 1
    return n

if __name__ == "__main__":
    debug = False
    solucion = []
    total_cost = 0
    sett, coleccion = ste_cover_ej.generate_set_cover_instance(
        n_elements=1000,
        n_subsets=250,
        subset_size_range=(5, 15),
        cost_range=(5, 200),
        seed=42  # for reproducibility
    )
    while set(cubierta) != set(sett):
        if (debug): print("into a new loop with cubierta =", cubierta) 
        coste = [math.inf for _ in range(len(coleccion))]
        for indice in range(len(coleccion)):
            try:
                coste[indice] = (coleccion[indice][-1]/minus(coleccion[indice][:-1]))
            except ZeroDivisionError:
                coste[indice] = math.inf
            if (debug): print("now the coste for ", coleccion[indice][:-1], " is ", coste[indice])
        minimo = math.inf
        ind = -1
        for index in range(len(coste)):
            if minimo > coste[index]:
                minimo = coste[index]
                ind = index
        for elem in coleccion[ind][:-1]:
            if elem not in cubierta:
                cubierta.append(elem)
        if (debug): print("the cubierta is now: ", cubierta)
        solucion.append(coleccion[ind][:-1])
        total_cost += coleccion[ind][-1]
        coleccion.pop(ind)
    print("la solucion es ", solucion, "con el coste de ",total_cost)

        
