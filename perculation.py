import random as rn


def generate_graph():
  G = {}
  n = 100
  for i in range(-n,n+1,2):
    for j in range(-n+1,n,2):
      if EXIST_EDGE:
        G[f'{i},{j}'] = f'{i+1},{j}'
        G[f'{i+1},{j}'] = f'{i},{j}'
      if EXIST_EDGE:
        G[f'{i},{j}'] = f'{i-1},{j}'
        G[f'{i-1},{j}'] = f'{i},{j}'
      if EXIST_EDGE:
        G[f'{i},{j}'] = f'{i},{j+1}'
        G[f'{i},{j+1}'] = f'{i},{j}'
      if EXIST_EDGE:
        G[f'{i},{j}'] = f'{i},{j-1}'
        G[f'{i},{j-1}'] = f'{i},{j}'
  return G
        
def EXIST_EDGE():
  p = 0.5
  rn.random() > p

G = generate_graph()
print(G)
print(G["1,1"])
