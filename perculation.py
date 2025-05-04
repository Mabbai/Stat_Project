import random as rn

import networkx as nx
import matplotlib.pyplot as plt


GRAPH_SIZE = 1000
EDGE_PROB = 0.501

        
def EXIST_EDGE(p):
  return rn.random() < p

def generate_graph():
  G = {}
  n = GRAPH_SIZE
  for i in range(0,n+1):
    for j in range(0,n+1):
      G[f'{i},{j}'] = []
  for i in range(0,n+1):
    for j in range(0,n+1,2):
      if i & 1: # i modulo 2 = 1
        j += 1
      if j == n+1:
        continue
      Domestic_Edges = []

      if EXIST_EDGE(EDGE_PROB) and j+1 <= n:
        Domestic_Edges.append(f'{i},{j+1}')
        
        G[f'{i},{j+1}'].append(f'{i},{j}')

      if EXIST_EDGE(EDGE_PROB) and i+1 <= n:
        Domestic_Edges.append(f'{i+1},{j}')
        
        G[f'{i+1},{j}'].append(f'{i},{j}') 
      if EXIST_EDGE(EDGE_PROB) and i-1 >= 0:
        Domestic_Edges.append(f'{i-1},{j}')
        
        G[f'{i-1},{j}'].append(f'{i},{j}')
      
      if EXIST_EDGE(EDGE_PROB) and j-1 >= 0:
        Domestic_Edges.append(f'{i},{j-1}')
        
        G[f'{i},{j-1}'].append(f'{i},{j}')

      G[f'{i},{j}'] = Domestic_Edges
  return G


G = generate_graph()
#print(f'{G} \n')

def draw_graph_from_dict(grid) -> None:
  G = nx.Graph()
  for node, neighbors in grid.items():
    G.add_node(node)
    for neighbor in neighbors:
      G.add_edge(node, neighbor)

  pos = {node: tuple(map(int,node.split(','))) for node in G.nodes}
  nx.draw(G, pos, with_labels=True, node_size=100,
          node_color='lightgreen', font_size=4)
  plt.gca().invert_yaxis()
  plt.show()


searched_starts = set()

def iterate_frontier(start):
  old_frontier = set()
  frontier = {start}
  while frontier:
    leafs = set()
    for node in frontier:
      acc = grow_leafs(node, frontier | old_frontier)
      if acc == 'W':
        print('W')
        return 'W'
      leafs = leafs | acc
      
    print(leafs)
    old_frontier = frontier
    frontier = leafs
    
        
def grow_leafs(node, past_nodes):
  leafs = set()
  for n in G[node]:
    if not n in past_nodes | leafs:
      x_val = int(n.split(',')[0])
      if x_val == GRAPH_SIZE:
        return 'W'
      
      if x_val == 0:
        searched_starts.add(n)
      leafs.add(n)

  return leafs

i=0
RESULT = 'L'
while i <= GRAPH_SIZE and RESULT != 'W':
  node = f'0,{i}'
  if not node in searched_starts:
    RESULT = iterate_frontier(node)
  i += 1

#draw_graph_from_dict(G) //don't run it for large graphs 15<

