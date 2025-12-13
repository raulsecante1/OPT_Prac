'''
V: list of node IDs (strings)

E: dictionary:
    key: (u, v)
    value: weight

T = {t1, t2, ..., tk}

'''

import networkx as nx
import random
import time

read_file = False

# how graph looks like
vertexs = ["vertex1", "vertex2"]
edgess = {("vertex1", "vertex2"): 2}
terminals = {"vertex1"}

random.seed(75)


def make_random_graph(n = 150, p = 0.2, w_min=1, w_max=30):
    '''
    function used to generate the random graph
    Args:
         n(int): number of vertexs
         p(float): posiblity of generate an edge
         w_min(int): weight minimum
         w_max(int): weight maximum
    Returns:
         G(NetworkX graph): undirected NetworkX graph with 'capacity' on each edge.
    '''
    G = nx.gnp_random_graph(n, p)
    for u, v in G.edges():
        G[u][v]["capacity"] = random.randint(w_min, w_max)
    return G


def isolating_cut(G, terminals, s_i, debug = False):
    """
    the function that compute the minimum isolating cut for terminal s_i using the max-flow / min-cut method required in Algorithm 4.3. 
    Args:
         G(NetworkX graph): undirected NetworkX graph with 'capacity' on each edge.
         terminals(set): set of terminals.
         s_i(str): the terminal for which isolation is computed.
    Returns:
         cut_edges(list): list of the C_i
    """

    H = G.copy()

    T = "_SUPER_SINK_"
    H.add_node(T)

    C_max = sum(data['capacity'] for u, v, data in G.edges(data=True))
    for t in terminals:
        if t != s_i:
            H.add_edge(t, T, capacity = C_max)

    cut_value, (reachable, non_reachable) = nx.minimum_cut(H, s_i, T)

    if debug: print(reachable, non_reachable) 

    cut_edges = []
    for u in reachable:
        for v in G.neighbors(u):
            if v in non_reachable:
                cut_edges.append((u, v))

    return cut_edges


def cut_weight(G, cut_edges):
    '''
    the function that calculates the maximum weight, i.e thw sume of all capacities
    Args:
         G(NetworkX graph): undirected NetworkX graph with 'weight' on each edge.
         cut_edges(list): list of the C_i
    Returns:
         sum
    '''
    return sum(G[u][v]['capacity'] for u, v in cut_edges)


def multiway_cut_2minus2k_apro(graph, terminals):
    '''
    the main function to perform the multiway cut logic
    Args:
         graph(NetworkX graph): undirected NetworkX graph with 'capacity' on each edge.
         terminals(set): set of terminals.
    Returns:
         C_i(list): list of C_i but excluding the most weighted one
    '''
    C_i = []
    for segment in terminals:
        C_i.append(isolating_cut(graph, terminals, segment))
    max_ind = 0
    max_val = 0
    for ind_c in range(len(C_i)):
        aux_max = cut_weight(graph, C_i[ind_c])
        if aux_max > max_val:
            max_val = aux_max
            max_ind = ind_c
    C_i.pop(max_ind)
    return C_i


def main():
    
    if read_file:
        #logics for reading files to get the graph
        pass
    else:
        graph = make_random_graph()
        terminals =  random.sample(list(graph.nodes), random.randint(2, len(graph.nodes)))

    aux = [(x, y, "capacity " + str(graph[x][y]["capacity"])) for x, y in graph.edges]

    print(aux)
    print("\n")

    print(terminals)
    print("\n")

    mc_start = time.perf_counter()
    res_list = multiway_cut_2minus2k_apro(graph, terminals)
    mc_stop = time.perf_counter()
    print (res_list, "\n")

    print(f"Elapsed time for mc: ", mc_stop - mc_start)
    
    print("\n")
    cost = 0
    for elem in res_list:
        cost += cut_weight(graph, elem)
    print(cost)

main()