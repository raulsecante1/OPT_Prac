/*Inicializacion de la poblacion
 *Evaluacion
 *Condicion de termino
 *  Seleccion
 *  Recombinación o cruzamiento
 *  Mutacion
 *  Reemplazo
 */

#include "iostream"

#include "string"
#include "fstream"
#include "sstream"

#include "vector"   // optimized random generating chronosome
#include "random"   //

#include "numeric"  // optimized calculating the V_in_solution

#include "omp.h"  //  OpenMp

std::string path = "D:/Project1/1.gr";

bool read_file = true;

static std::mt19937 rng(std::random_device{}());

struct BipartiteGraph {
    int num_fix, num_fre, num_edge;
    std::vector<std::pair<int, int>> edges;
};


BipartiteGraph read_bipartite_graph(const std::string& filename) {
    std::ifstream fin(filename);

    std::string line;

    while (std::getline(fin, line)) {
        if (!line.empty() && line[0] == 'p') break;
    }

    std::string tmp, ocr;
    int nfix, nfre, med;
    std::istringstream header(line);
    header >> tmp >> ocr >> nfix >> nfre >> med;

    BipartiteGraph g;
    g.num_fix = nfix;
    g.num_fre = nfre;
    g.num_edge = med;
    g.edges.reserve(med);

    int u, v;
    while (fin >> u >> v) {
        g.edges.emplace_back(u, v);
    }

    return g;
}


std::vector<int> random_binary_vector(int k) {
    /*
     * the function that generate a k length random chronosome like {1,1,0,1,0,1,...}
     * Args:
     *      k(int): the length of chronosome
     * Returns:
     *      v(vector): the chronosome
     */

    static std::uniform_int_distribution<int> dist(0, 1);

    std::vector<int> v(k);
    for (int i = 0; i < k; ++i)
        v[i] = dist(rng);

    return v;
}


int fitness_function(const BipartiteGraph graph, const std::vector<int>& solution) {
    /*
     * the fitness function f = C1 * V_in_solution + C2 * V_missing
     */
    int constant_C1 = 2;
    int constant_C2 = 1683;
    
    int v_in_solution = 0;
    int v_missing = 0;

    int V_in_solution = std::accumulate(solution.begin(), solution.end(), 0);

    for (const auto& edge : graph.edges) {
        int idx_u = edge.first - 1;
        int idx_v = edge.second - 1;
        if (solution[idx_u] == 0 && solution[idx_v] == 0) {
            v_missing++;
        }
    }

    int fitness = constant_C1 * v_in_solution + constant_C2 * v_missing;
    return fitness;
}


std::vector<std::vector<int>> dual_point_selection(const int population, const std::vector<std::vector<int>> parents) {
    /*
     * function that dose the 2 point selection till get enough population
     * Args:
     *      population(int): the desired population
     *      parents(std::vector<std::vector<int>>): the current generation that used to produce the next generation
     * Returns:
     *      particles(std::vector<std::vector<int>>): the next generation
     */

    int new_population = 0;
    int num_vertex = parents[0].size();

    std::vector<std::vector<int>> particles(
        population,
        std::vector<int>(num_vertex, 0)
    );

    while (new_population + 1 < population) {
        std::uniform_int_distribution<int> dist_parent(0, population - 1);

        int idx1 = dist_parent(rng);
        int idx2 = dist_parent(rng);

        std::uniform_int_distribution<int> dist_two_point(0, num_vertex - 1);
        int p1 = dist_two_point(rng);
        int p2 = dist_two_point(rng);
        if (p1 > p2) std::swap(p1, p2);

        std::vector<int> child1 = parents[idx1];
        std::vector<int> child2 = parents[idx2];

        #pragma omp parallel for
        for (int i = p1; i <= p2; ++i) {
            std::swap(child1[i], child2[i]);
        }

        particles[new_population] = std::move(child1);
        particles[new_population+1] = std::move(child2);

        new_population += 2;

    }

    if (new_population < population) {
        std::uniform_int_distribution<int> dist_parent(0, population - 1);
        particles[new_population] = parents[dist_parent(rng)];
    }

    return particles;
}


void mutuation(const float posibility, std::vector<std::vector<int>> particles) {
    /*
     * the function that dose mutuation at every particle with a certain chance
     * Args:
     *      posibility(float): the chance
     *      particles(std::vector<std::vector<int>>): the vector of the vectors of chronomose
     * Returns:
     *      s
     */

    size_t pop_size = particles.size();

    std::mt19937 muta_rng(rng());
    std::bernoulli_distribution ber_dist(posibility);

#pragma omp parallel for
    for (size_t i = 0; i < pop_size; ++i) {
        std::vector<int>& particle = particles[i];
        size_t len = particle.size();
        for (size_t j = 0; j < len; ++j) {
            if (ber_dist(muta_rng)) {
                particle[j] ^= 1;
            }
        }
    }
}



int main(){
    //supposing that the inputs are [a,b,c,...] vertexs. [(a,b),(a,c),...] edges

    int num_vertex;
    int population;
    int constant_torneo = 2;  //tourment
    int num_iteration = 40;

    BipartiteGraph graph;
    
    if (read_file) {
        graph = read_bipartite_graph(path);
        num_vertex = graph.num_fix + graph.num_fre;
        population = num_vertex * 5;
    }
    else {
        num_vertex = 50;
        population = 180;
    }

    std::vector<int> eva_list(population, 0);
    
    //the chronosomes are like {0,1,1,0,1,...} 0 stands not taken, and 1 taken

    std::vector<std::vector<int>> particles(                             // initialzing
        population,                                                      //
        std::vector<int>(num_vertex, 0)                                  //
    );                                                                   //
                                                                         //
    for (int ind_ini = 0;ind_ini < population; ind_ini++){               //
        particles[ind_ini] = random_binary_vector(num_vertex);           //
    }                                                                    //

    for (int ind_eva = 0;ind_eva < population; ind_eva++) {                    // evaluation
        eva_list[ind_eva] = fitness_function(graph, particles[ind_eva]);       //
    }                                                                          //

    for (int ind_iter = 0; ind_iter < num_iteration; ind_iter++) {       // condition phase
 
        particles = dual_point_selection(population, particles);                               // tourment selection and 2points crossover

        mutuation(0.01, particles);                                         // 1% mutuation
    }
    

}