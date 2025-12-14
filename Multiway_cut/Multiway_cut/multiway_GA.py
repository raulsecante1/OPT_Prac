import random
import numpy as np
import networkx as nx
import time

import multiway_cut

random.seed(75)

read_file = False


class MultiwayCutGA:
    def __init__(self, G, terminals, pop_size=50, mutation_rate=0.01):
        self.G = G
        self.terminals = terminals
        self.k = len(terminals)
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate

        self.node_list = list(G.nodes())
        self.n = len(self.node_list)

        self.node_index = {v: i for i, v in enumerate(self.node_list)}

        self.terminal_labels = {terminals[i]: i for i in range(self.k)}  # Pre-lock terminal labels taht made sure all terminals are seperated


    def initialize_population(self):
        '''
        function that initialize the first chronosomes
        '''
        pop = []
        for _ in range(self.pop_size):
            chrom = np.random.randint(0, self.k, self.n)

            for t, label in self.terminal_labels.items():  # fix terminal labels, to not get 000000 or 1111111
                chrom[self.node_index[t]] = label

            pop.append(chrom)
        return pop


    def fitness(self, chrom):
        '''
        fitness function
        Args:
             chrom(list):
        Returns:
             fitness(float/int)
             cost(float)
        '''
        cost = 0
        for u, v, w in self.G.edges(data='capacity', default=1):
            iu, iv = self.node_index[u], self.node_index[v]
            if chrom[iu] != chrom[iv]:
                cost += w
        return 1.0 / (1.0 + cost), cost


    def crossover(self, p1, p2):
        '''
        crossover
        Args:
             p1(list)
             p2(list)
        Returns:
             child(list)
        '''
        mask = np.random.randint(0, 2, self.n)
        child = np.where(mask == 0, p1, p2)

        for t, label in self.terminal_labels.items():  # fix terminal labels, to not get 000000 or 1111111
            child[self.node_index[t]] = label
        return child


    def mutate(self, chrom):
        '''
        mutation phase with probability 1% by default
        Args:
             chrom(list):  chromosome represented as a list
        '''
        for i in range(self.n):
            if self.node_list[i] in self.terminal_labels:  # terminals cannot mutate
                continue
            if random.random() < self.mutation_rate:
                chrom[i] = random.randint(0, self.k - 1)


    def select_parent(self, population, fitnesses):
        '''
        tournament selection
        Args:
             population(list): lists of chromosomes
             fitness(list):
        Returns:
             (list): chromosome represented as a list
        '''
        i, j = random.sample(range(self.pop_size), 2)
        return population[i] if fitnesses[i] > fitnesses[j] else population[j]


    def run(self, iteraations=200):
        pop = self.initialize_population()

        best_chrom = None
        best_cost = float("inf")

        for _ in range(iteraations):
            fitness_vals = []
            costs = []

            for chrom in pop:
                f, c = self.fitness(chrom)
                fitness_vals.append(f)
                costs.append(c)

            idx = np.argmin(costs)
            if costs[idx] < best_cost:
                best_cost = costs[idx]
                best_chrom = pop[idx].copy()

            new_pop = []
            for _ in range(self.pop_size):
                p1 = self.select_parent(pop, fitness_vals)
                p2 = self.select_parent(pop, fitness_vals)

                child = self.crossover(p1, p2)
                self.mutate(child)

                new_pop.append(child)

            pop = new_pop
        print("cost = ", best_cost)

        return best_chrom, best_cost


def main():

    if read_file:
        #logics for reading files to get the graph
        pass
    else:
        graph = multiway_cut.make_random_graph()
        terminals =  random.sample(list(graph.nodes), random.randint(2, len(graph.nodes)))

    GA_start = time.perf_counter()

    mcga = MultiwayCutGA(graph, terminals)
    mcga.run()

    GA_stop = time.perf_counter()

    print("Elapsed time for ga: ", GA_stop - GA_start)

    aux = [(x, y, "capacity " + str(graph[x][y]["capacity"])) for x, y in graph.edges]
        
    print(aux)
    print("\n")

    print(terminals)
    print("\n")

main()
