import viajanteMetrico
import math

'''
readFile("a280.tsp", 7)
readFile("ali535.tsp", 8)
readFile("att48.tsp", 7)
'''

def readFile(fie, n, debug= False):
    '''
    Leer los ejemplos de .tsp
    Args:
          fie(str): ruta al fichero
          n(int): datos desde n-ésima fila
    Returns:
          nodos(list): una lista de los nombres de cada vertices
          grafos(list): una lista de tupla de (arista, coste)
    '''
    nodes = []
    with open(fie,"r") as file:
        for _ in range(n-1):
            next(file)
        for line in file:
            line = line.strip()
            if line != "EOF":
                nodes.append([float(i) for i in line.split()])
            else:
                break
    nodes_aux = list(nodes)

    grafos = []
    nodos = []
    elem = nodes_aux[0]
    nodes_aux.pop(0)
    nodos.append(str(elem[0]))
    while nodes_aux != []:
        for i in nodes_aux:
            grafos.append([str(elem[0])+" to "+str(i[0]), math.sqrt((elem[1]-i[1])**2 + (elem[2]-i[2])**2)])
        elem = nodes_aux[0]
        nodes_aux.pop(0)
        nodos.append(str(elem[0]))
    if(debug):
        return nodes
    else:
        return nodos, grafos


def main():
    nodos, grafos = readFile("a280.tsp", 7)
    ARM_aux = viajanteMetrico.arm(nodos, grafos)
    ARM = [i[1] + " to " + i[2] for i in ARM_aux]
    CE = viajanteMetrico.ce(ARM, nodos[0], "")
    elirep_CE = viajanteMetrico.elirep(CE)
    final_cost = viajanteMetrico.cost(elirep_CE, grafos)
    print(final_cost)


main()
