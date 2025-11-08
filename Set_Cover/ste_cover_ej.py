import random

def generate_set_cover_instance(
    n_elements=50,        # number of elements in the universe
    n_subsets=30,         # number of subsets
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

    sett = [f"x{i}" for i in range(1, n_elements + 1)]
    
    coleccion = []
    

    min_size, max_size = max(int(n_elements/n_subsets) + 1, int(n_subsets/n_elements) + 1), max(int(n_elements/n_subsets*2) + 2, int(n_subsets/n_elements*2) + 2)
    total_slots = n_subsets * max_size
    if n_elements > total_slots:
        raise ValueError("Impossible to cover all elements with given subset sizes")

    sett = [f"x{i}" for i in range(1, n_elements + 1)]
    coleccion = [[] for _ in range(n_subsets)]

    # Step 1: Force every element into at least one subset
    all_slots = [(i, j) for i in range(n_subsets) for j in range(max_size)]
    random.shuffle(all_slots)
    for elem, slot in zip(sett, all_slots):
        subset_idx = slot[0]
        coleccion[subset_idx].append(elem)

    # Step 2: Fill remaining subset slots randomly to reach min_size
    for subset in coleccion:
        while len(subset) < min_size:
            candidate = random.choice(sett)
            if candidate not in subset:
                subset.append(candidate)
        # Step 3: Assign a cost
        cost = random.randint(*cost_range)
        subset.append(cost)

    return sett, coleccion