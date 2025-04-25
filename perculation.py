import random as rn
from collections import defaultdict

import networkx as nx
import matplotlib.pyplot as plt

graph_size = 30
def generate_graph():
  G = {}
  n = graph_size
  p = 0.50
  for i in range(0,n+1):
    for j in range(0,n+1):
      G[f'{i},{j}'] = []
  for i in range(0,n+1):
    for j in range(0,n+1,2):
      if i & 1: # if i modulo 4 is 1
        j += 1
      if j == n+1:
        continue
      Domestic_Edges = []

      if EXIST_EDGE(p) and j+1 <= n:
        Domestic_Edges.append(f'{i},{j+1}')
        
        G[f'{i},{j+1}'].append(f'{i},{j}')

      if EXIST_EDGE(p) and i+1 <= n:
        Domestic_Edges.append(f'{i+1},{j}')
        
        G[f'{i+1},{j}'].append(f'{i},{j}') 
      if EXIST_EDGE(p) and i-1 >= 0:
        Domestic_Edges.append(f'{i-1},{j}')
        
        G[f'{i-1},{j}'].append(f'{i},{j}')
      
      if EXIST_EDGE(p) and j-1 >= 0:
        Domestic_Edges.append(f'{i},{j-1}')
        
        G[f'{i},{j-1}'].append(f'{i},{j}')
      G[f'{i},{j}'] = Domestic_Edges
  
  return G
        
def EXIST_EDGE(p):
  return rn.random() < p

G = generate_graph()
print(f'{G}+\n')

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

total_nodes_checked = []

def graph_explorer(node, path_trekked):
  #print(node)
  if int(node.split(',')[0]) == graph_size:
    print(f'WIN! {path_trekked}')
    return 'WIN'
  for n in G[node]:
    if n in path_trekked:
      continue
    if n in total_nodes_checked:
      continue
    
    total_nodes_checked.append(n)
    if graph_explorer(n, path_trekked + [n]) == 'WIN':
      return 'WIN'

for i in range(0,graph_size+1):
  node = f'0,{i}'
  if node in total_nodes_checked:
    continue
  total_nodes_checked.append(node)
  graph_explorer(node, [node])
    

draw_graph_from_dict(G)
