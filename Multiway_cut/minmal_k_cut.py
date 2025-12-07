'''
1. Compute a Gomory-Hu tree T for G.

2. Output the union of the lightest k-1 cuts of the n-1 cuts associated with edges of T in G; let C be this union.
'''

import networkx as nx
import random

# how graph looks like
vertexs = ["vertex1", "vertex2"]
edgess = {("vertex1", "vertex2"): 2}
terminals = {"vertex1"}

random.seed(42)


def make_random_graph(n = 50, p = 0.1, w_min=1, w_max=10):
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


def min_k_cut_2minus2dk(graph, k):
    '''
    the function that calculates the 2-2/k_opt cut
    Args:
         graph(NetworkX graph): undirected NetworkX graph with 'capacity' on each edge.
         k(int): how many components we are going to need
    Returns:
         s
    '''
    
    if k > len(graph.nodes):
        return "issued components are more than vertexs it has"
    
    G_H_tree = nx.gomory_hu_tree(graph, capacity='capacity')
    raw_edges_to_cut = sorted(G_H_tree.edges(data=True), key=lambda x: x[2]['weight'])[:k-1]
    edges_to_cut = [(x, y) for x, y, z in raw_edges_to_cut]

    cuts = []
    for ver1, ver2 in edges_to_cut:
        cut_value, (reachable, non_reachable) = nx.minimum_cut(graph, ver1, ver2, capacity = 'capacity')
        aux_cuts = [(u, v) for u in reachable for v in graph.neighbors(u) if v in non_reachable]
        cuts.append(aux_cuts)
    return cuts

def main():
    graph = make_random_graph()
    result = min_k_cut_2minus2dk(graph, 4)

    print (result)

main()