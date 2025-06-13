import random as rn
import networkx as nx
import matplotlib.pyplot as plt
import copy
import matplotlib.colors as mcolors

# Parameters
GRAPH_SIZE = 10  # Only for even-sized graphs
EDGE_PROB = 0.5  # Probability of edge existence
UP_DIAG = False  # Toggle for up-diagonals (↘)
DOWN_DIAG = False  # Toggle for down-diagonals (↙)
SHOW_GRAPH = True  # Enable graph drawing if size is reasonable

GRAPH = {}

def add_edge(a, b):
    """Adds an undirected edge between nodes a and b in the GRAPH."""
    a_key = f"{a[0]},{a[1]}"
    b_key = f"{b[0]},{b[1]}"
    GRAPH.setdefault(a_key, []).append(b_key)
    GRAPH.setdefault(b_key, []).append(a_key)

def add_edge_rn(a, b):
    """Adds an edge based on EDGE_PROB."""
    if rn.random() < EDGE_PROB:
        add_edge(a, b)

def generate_graph(size, edge_prob, up_diag, down_diag):
    """Generates a probabilistic grid graph with optional diagonals."""
    global GRAPH
    GRAPH = {}

    # Pre-populate all nodes if SHOW_GRAPH is on
    if SHOW_GRAPH:
        for i in range(size + 1):
            for j in range(size + 1):
                GRAPH[f"{i},{j}"] = []

    # Frame edges
    for i in range(size):
        add_edge_rn((0, i), (0, i + 1))
        add_edge_rn((size, i), (size, i + 1))
        add_edge_rn((i, 0), (i + 1, 0))
        add_edge_rn((i, size), (i + 1, size))

    # Entry edges
    for i in range(2, size, 2):
        add_edge_rn((0, i), (1, i))
        add_edge_rn((size, i), (size - 1, i))
        add_edge_rn((i, 0), (i, 1))
        add_edge_rn((i, size), (i, size - 1))

    # Inner box edges (odd grid points)
    for i in range(1, size, 2):
        for j in range(1, size, 2):
            add_edge_rn((i, j), (i + 1, j))
            add_edge_rn((i, j), (i - 1, j))
            add_edge_rn((i, j), (i, j + 1))
            add_edge_rn((i, j), (i, j - 1))

    # Even grid connections
    for i in range(2, size, 2):
        for j in range(2, size, 2):
            add_edge_rn((i, j), (i + 1, j))
            add_edge_rn((i, j), (i - 1, j))
            add_edge_rn((i, j), (i, j + 1))
            add_edge_rn((i, j), (i, j - 1))

    # Diagonals ↘
    if up_diag:
        for i in range(size):
            for j in range(size):
                add_edge_rn((i, j), (i + 1, j + 1))

    # Diagonals ↙
    if down_diag:
        for i in range(size):
            for j in range(1, size + 1):
                add_edge_rn((i, j), (i + 1, j - 1))


# Search and Visualization
PATH_FOUND = False
TOTAL_TREE = []
BACKUP_GRAPH = {}

def grow_tree_canopy(sapling):
    """Expands search tree from a given sapling."""
    global TOTAL_TREE, PATH_FOUND
    tree_canopy = {sapling}
    while not PATH_FOUND and tree_canopy:
        tree_canopy = {
            new_leaf
            for leaf in tree_canopy
            for new_leaf in grow_leaf(leaf)
            if new_leaf not in tree_canopy
        }
        if tree_canopy:
            TOTAL_TREE.append(tree_canopy)
        else:
            TOTAL_TREE = []

def grow_leaf(leaf):
    """Expands from a leaf node and checks for path to bottom."""
    global PATH_FOUND
    x_val = int(leaf.split(',')[0])
    if x_val == GRAPH_SIZE:
        PATH_FOUND = True
        return []
    return GRAPH.pop(leaf, [])

def run_search():
    """Runs the tree search from top row."""
    for i in range(GRAPH_SIZE + 1):
        node = f"0,{i}"
        if GRAPH.get(node):
            grow_tree_canopy(node)
            if PATH_FOUND:
                print("Path Found!")
                return
    print("No Path Found")

def draw_graph_from_dict(grid):
    """Visualizes the graph and the path search tree."""
    G = nx.Graph()
    for node, neighbors in grid.items():
        G.add_node(node)
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Color nodes by group index
    norm = mcolors.Normalize(vmin=0, vmax=len(TOTAL_TREE))
    cmap = mcolors.LinearSegmentedColormap.from_list('cold_to_warm', ['#ff3300', '#008000'], N=256)
    node_to_group = {
        node: i for i, group in enumerate(TOTAL_TREE) for node in group
    }
    node_colors = [
        cmap(norm(node_to_group.get(node))) if node in node_to_group else (0.3, 0.3, 0.3)
        for node in G.nodes
    ]

    pos = {node: tuple(map(int, node.split(','))) for node in G.nodes}
    nx.draw(G, pos, with_labels=True, node_size=100, node_color=node_colors, font_size=4)
    plt.show()


# Main routine
generate_graph(GRAPH_SIZE, EDGE_PROB, UP_DIAG, DOWN_DIAG)
if SHOW_GRAPH:
    BACKUP_GRAPH = copy.deepcopy(GRAPH)
run_search()
if SHOW_GRAPH:
    draw_graph_from_dict(BACKUP_GRAPH)
