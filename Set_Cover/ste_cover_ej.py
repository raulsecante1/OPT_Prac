import random

def generate_set_cover_instance(
    n_elements=50,        # number of elements in the universe
    n_subsets=30,         # number of subsets
    subset_size_range=(5, 12),  # how many elements per subset
    cost_range=(5, 20),   # cost range for subsets
    seed=None
):
    """
    Generates a random Set Cover instance.
    
    Returns:
        sett: list of element labels
        coleccion: list of subsets, each as [elements..., cost]
    """
    if seed is not None:
        random.seed(seed)

    # Universe of elements
    sett = [f"x{i}" for i in range(1, n_elements + 1)]
    
    coleccion = []
    for _ in range(n_subsets):
        size = random.randint(*subset_size_range)
        subset = random.sample(sett, size)
        cost = random.randint(*cost_range)
        coleccion.append(subset + [cost])
    
    return sett, coleccion

'''
# Example usage:
if __name__ == "__main__":
    sett, coleccion = generate_set_cover_instance(
        n_elements=50,
        n_subsets=30,
        subset_size_range=(5, 15),
        cost_range=(5, 20),
        seed=42  # for reproducibility
    )

    print("sett =", sett)
    print("\ncoleccion = [")
    for c in coleccion:
        print("   ", c, ",")
    print("]")
'''