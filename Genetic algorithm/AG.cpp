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

#include "chrono"  //  H-R clock

std::string path = "D:/Project1/1.gr";

bool read_file = true;

bool debug = false;

static std::mt19937 rng(std::random_device{}());

struct BipartiteGraph {
    int num_fix, num_fre, num_edge;
    std::vector<std::pair<int, int>> edges;
};


void print_particle(const std::vector<int>& v) {
    for (int x : v) {
        std::cout << x << " ";
    }
    std::cout << "\n";
}


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


int fitness_function(const BipartiteGraph& graph, const std::vector<int>& solution) {
    /*
     * the fitness function f = C1 * V_in_solution + C2 * V_missing
     */
    int constant_C1 = 1;
    int constant_C2 = 1683;
    
    int v_in_solution = std::accumulate(solution.begin(), solution.end(), 0);
    int v_missing = 0;

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


std::vector<std::vector<int>> dual_point_selection(const std::vector<std::vector<int>>& parents) {
    /*
     * function that dose the 2 point crossover to get a double population
     * Args:
     *      parents(std::vector<std::vector<int>>): the current generation that used to produce the next generation
     * Returns:
     *      particles(std::vector<std::vector<int>>): the next generation
     */

    int num_population = parents.size();
    int num_vertex = parents[0].size();

    std::vector<std::vector<int>> particles(
        num_population,
        std::vector<int>(num_vertex, 0)
    );

    int dual_count = 0;

//#pragma omp parallel for
    for (int ind = 0; ind < num_population; ind+=2) {
        if (debug)std::cout << "    dual run " << dual_count << "\n";
        std::uniform_int_distribution<int> dist_two_point(0, num_vertex - 1);
        int p1 = dist_two_point(rng);
        int p2 = dist_two_point(rng);
        if (p1 > p2) std::swap(p1, p2);

        std::vector<int> child1 = parents[ind];
        std::vector<int> child2 = parents[ind+1];

        for (int i = p1; i <= p2; ++i) {
            std::swap(child1[i], child2[i]);
        }

        particles[ind] = std::move(child1);
        particles[ind + 1] = std::move(child2);

        dual_count++;
    }

    return particles;
/*
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
*/
}


std::vector<std::vector<int>> torneo_selection(const std::vector<std::vector<int>>& current_generation, const BipartiteGraph graph) {
    /*
     * the function that do the tourment selection to get the relatively better genes from last iteration to pass to the next iteration
     * Args:
     *      current_generation(std::vector<std::vector<int>>): the current parents and children set
     * Returns:
     *      s
     */

    int num_population = current_generation.size() / 2;
    int num_vertex = current_generation[0].size();
    int eva_1, eva_2;

    std::vector<std::vector<int>> particles(
        num_population,
        std::vector<int>(num_vertex, 0)
    );

    for (int ind = 0; ind < num_population; ind += 2) {
        eva_1 = fitness_function(graph, current_generation[ind]);
        eva_2 = fitness_function(graph, current_generation[ind + 1]);
        if (eva_1 < eva_2) {
            particles[ind/2] = current_generation[ind];
        }
        else {
            particles[ind/2] = current_generation[ind+1];
        }
    }

    return particles;
}


void mutuation(const float posibility, std::vector<std::vector<int>>& particles) {
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

    auto start = std::chrono::high_resolution_clock::now(); //game start

    int num_vertex;
    int population;
    int constant_torneo = 2;  //tourment
    int num_iteration = 40;
    long int iteration_count = 0;

    BipartiteGraph graph;
    
    if (read_file) {
        graph = read_bipartite_graph(path);
        num_vertex = graph.num_fix + graph.num_fre;
        population = num_vertex * 4;
    }
    else {
        num_vertex = 15;
        population = 50;
    }

    std::vector<int> eva_list(population, 0);
    
    //the chronosomes are like {0,1,1,0,1,...} 0 stands not taken, and 1 taken

    std::vector<std::vector<int>> child_particles(
        population,
        std::vector<int>(num_vertex, 0)
    );

    std::vector<std::vector<int>> combined_particles;
    combined_particles.reserve(population * 2);

    std::vector<std::vector<int>> parent_particles(                             // initialzing
        population,                                                             //
        std::vector<int>(num_vertex, 0)                                         //
    );                                                                          //
                                                                                //
    for (int ind_ini = 0;ind_ini < population; ind_ini++){                      //
        parent_particles[ind_ini] = random_binary_vector(num_vertex);           //
    }                                                                           //

    for (int ind_eva = 0;ind_eva < population; ind_eva++) {                           // evaluation
        eva_list[ind_eva] = fitness_function(graph, parent_particles[ind_eva]);       //
    }                                                                                 //

    for (int ind_iter = 0; ind_iter < num_iteration; ind_iter++) {                 // condition phase
 
        if (debug) std::cout << "iteration run " << iteration_count << "\n";

        child_particles = dual_point_selection(parent_particles);                               // 2 points crossover

        mutuation(0.01f, child_particles);                                         // 1% mutuation

        combined_particles.clear();                                                                               // 2 zones
        combined_particles.insert(combined_particles.end(), parent_particles.begin(), parent_particles.end());    //
        combined_particles.insert(combined_particles.end(), child_particles.begin(), child_particles.end());      //
        parent_particles = torneo_selection(combined_particles, graph);

        iteration_count++;
    }

    auto end = std::chrono::high_resolution_clock::now();  // das spiel ist aus
    std::chrono::duration<double> elapsed = end - start;

    print_particle(parent_particles[0]);

    std::cout << "Elapsed time: " << elapsed.count() << " seconds\n";

}