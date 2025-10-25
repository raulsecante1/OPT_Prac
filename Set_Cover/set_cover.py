# algoritmo para el set-cover
# la entrada tiene la forma Set: [a, b, c, d, e, f,...], y los subconjuntos: [[[a, b, c,...], c1], [[b, d,...], c2],...]
# se define el concepto de valor como len(x_s_i) con x_s_i={y|y in Set and y in s_i}
# y tiene el algoritmo de log-opt.



# debug mode is on !!



import math

sett = ["a", "b", "c", "d", "e", "f", "g"]
coleccion = [["a","b", 5],
             ["a", "c", "e", 9],
             ["f", "g", 4],
             ["a", "e", "f", 7],
             ["d", "g", 3],
             ["b", "d", "e", 12]]
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
    debug = True
    solucion = []
    total_cost = 0
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

        
