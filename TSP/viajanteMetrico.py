# -*- coding: utf-8 -*-

import math
from collections import defaultdict, deque

def coste(a, b):
    pass

def arm(nodos, grafos, debug = False):
    '''
    Calcular el MST mediante algoritmo de Prim
    Args: 
          nodos (list): una lista de vertices
          grafos (list): una lista de tupla de (arista, coste)
    Returns:
          arbol(list): una lista que contiene el coste minimo, y el vertice asociado a cada vertice
    '''

    '''
    nodo_aux = list(nodos)
    start = "a"
    nodo_aux.remove(start)
    arista = list(grafos)
    while nodo_aux != []:
        for i in arista:
            if i[0] == start:
                ARM.append(i)
                start = i[1]
                nodo_aux.remove(start)
                arista.remove(i)
                break
            elif i[1] == start:
                ARM.append(i)
                start = i[0]
                nodo_aux.remove(start)
                arista.remove(i)
                break
    '''
    #mediante el algoritmo de prim
    Coste = [math.inf for i in range(len(nodos))]
    Arista = [None for i in range(len(nodos))]
    nodo_aux = list(nodos)
    arbol_aux = [list(t) for t in zip(Coste, Arista, nodo_aux)]
    arbol = []
    arbol_aux[0][0] = 0
    arbol_aux[0][1] = arbol_aux[0][2]
    while len(arbol_aux) > 0:
        costa = math.inf
        for i in arbol_aux:
            if i[0] < costa:
                if(debug):  print("take this cause " + str(i[0]) + " is smaller than " + str(costa))
                elem = i
                costa = i[0]
        if(debug):  print("choose " + elem[2])
        arbol.append(elem)
        arbol_aux.remove(elem)
        for i in grafos:
            elemP = i[0].split(" to ")
            if elemP[0] == elem[2]:
                for j in range(len(arbol_aux)):
                    if arbol_aux[j][2] == elemP[1] and arbol_aux[j][0] > i[1]:
                        if(debug):  print("we are at " + elem[2] + " and we go " + arbol_aux[j][2] + " as " + str(arbol_aux[j][0]) + " is bigger than " + str(i[1]))
                        arbol_aux[j][0] = i[1]
                        arbol_aux[j][1] = elemP[0]
                    elif arbol_aux[j][2] == elemP[1] and arbol_aux[j][0] <= i[1]:
                        if(debug):  print("we are at " + elem[2] + " but we don´t go " + arbol_aux[j][2] + " as " + str(arbol_aux[j][0]) + " is smaller than " + str(i[1]))
                        pass
            elif elemP[1] == elem[2]:
                for j in range(len(arbol_aux)):
                    if arbol_aux[j][2] == elemP[0] and arbol_aux[j][0] > i[1]:
                        if(debug):  print("we are at " + elem[2] + " and we go " + arbol_aux[j][2] + " as " + str(arbol_aux[j][0]) + " is bigger than " + str(i[1]))                        
                        arbol_aux[j][0] = i[1]
                        arbol_aux[j][1] = elemP[1]
                    elif arbol_aux[j][2] == elemP[0] and arbol_aux[j][0] > i[1]:
                        if(debug):  print("we are at " + elem[2] + " but we don´t go " + arbol_aux[j][2] + " as " + str(arbol_aux[j][0]) + " is smaller than " + str(i[1]))
                        pass
    return arbol

def duplicar(ARM):
    '''
    Duplicar las aristas
    '''
    ARM_aux = list(ARM)
    for i in ARM:
        elem = i.split(" to ")
        ARM_aux.append(elem[1] + " to " + elem[0])
    return ARM_aux

def ce(ARM, marco, CE = "", debug = False):
    '''
    Usando el algoritmo de Von Hierholzer para encontrar el circulo euleriano
    Args: 
          ARM(list): lista TSM pero doblada
          CE(str): string de un circulito euleriano, "" por defecto
          marco(str): Inicio del circulo
    Returns:
          CE(str): string de un circulito euleriano completo
    '''

    '''
    start = marco
    requiremente = ""
    requirement_set_tag = False
    CE += marco
    ARRM = duplicar(ARM)
    while ARRM != []:
        for i in ARRM:
            elem = i.split(" to ")
            if elem[0] == start:
                if not requirement_set_tag:
                    requiremente = elem[1]
                    requirement_set_tag = True
                elif requiremente == elem[0] and elem[1] == marco:
                    continue
                CE = CE + " to " + elem[1]
                start = elem[1]
                if ARRM != []:
                    ARRM.remove(i)
                    #print(CE + "\n")
                    break
            elif elem[1] == start:
                if not requirement_set_tag:
                    requiremente = elem[0]
                    requirement_set_tag = True
                elif requiremente == elem[1] and elem[0] == marco:
                    continue
                CE = CE + " to " + elem[0]
                start = elem[0]
                if ARRM != []:
                    ARRM.remove(i)
                    #print(CE + "\n")
                    break
        if len(ARRM) == 1:
            CE = CE + " to " + ARRM[0].split(" to ")[1]
            break
    return CE
    '''

    CE += marco
    fila = [marco]
    ARRM = duplicar(ARM)
    aux_grafo = {}
    for elem in ARRM:
        u, v = elem.split(" to ")
        if u not in aux_grafo:
            aux_grafo[u] = []
        if v not in aux_grafo:
            aux_grafo[v] = []
        aux_grafo[u].append(v)
        aux_grafo[v].append(u)
    if(debug):
        for i in aux_grafo:
            print(i + " is connected with " + ", ".join(aux_grafo[i])) 
        print("current step is " + fila[-1])
    while fila:
        current = fila[-1]
        if(debug):  print("checked " + current)
        if aux_grafo[current]:
            next_node = aux_grafo[current].pop()
            fila.append(next_node)
        else:
            if(debug):  print("next step is " + fila[-1])
            CE = CE + " to " + fila.pop()
    
    return CE


def elirep(CE):
    '''
    Eliminar los vertices repetidos
    '''
    #seen = set()
    #return ''.join(c for c in CE if not (c in seen or seen.add(c)))
    list = CE.split(" to ")
    unique_list = []
    for item in list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list

def cost(CE, grafos):
    '''
    Calcular el coste
    '''
    coste = 0
    ce_list = list(CE)
    aux_grafos = list(grafos)
    for index in range(len(ce_list)-1):
        for i in aux_grafos:
            elem = i[0].split(" to ")
            if elem[0] == ce_list[index] and elem[1] == ce_list[index+1]:
                coste += i[1]
                break
            elif elem[1] == ce_list[index] and elem[0] == ce_list[index+1]:
                coste += i[1]
                break
    return coste

def notmain():
    nodos = ["a", "b", "c", "d", "e", "f"]
    grafos = [["a to c", 2], ["a to f", 5], ["b to c", 3], ["b to d", 3], ["c to d", 5], ["c to e", 4], ["e to f", 7]]
    #ARM = ["ac", "af", "bc", "bd", "cd", "ce", "ef"]
    #ARM = ["ab", "bc", "cd"]
    ARM_aux = arm(nodos, grafos)
    ARM = [i[1] + " to " + i[2] for i in ARM_aux]
    print(ARM_aux)
    print(ARM)
    CE = ce(ARM, nodos[0], "")
    print(elirep(CE))

#notmain()