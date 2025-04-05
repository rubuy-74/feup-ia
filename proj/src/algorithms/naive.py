from models.map import Map
from models.cell import Cell
import numpy as np
from skimage.morphology import medial_axis
from tqdm import tqdm
from random import shuffle
from collections import deque
from utils import computeAdjacents

def naive(m: Map, loaded=False):
  if(loaded):
    routers = np.where(m.matrix == Cell.CONNECTED_ROUTER)
    x_coords, y_coords = routers
    coords = list(zip(x_coords,y_coords))
    for router in coords:
      router_targets = m.computeRouterTargets(router)
      m.coverage.update(router_targets)
    
    num_backbones = len(np.where(m.matrix == Cell.CABLE)[0])
    num_routers = len(x_coords)

    remaining_budget = m.budget - (num_routers * m.rtPrice + num_backbones * m.bbPrice)

    return m, remaining_budget

  to_check = np.where(m.matrix == Cell.TARGET, 1, 0).astype(np.bool_)
  budget = m.budget
  
  max_num_routers = int(m.budget / m.rtPrice)
  pbar = tqdm(range(max_num_routers), desc="Placing Routers")
  
  while budget > 0:
    abstraction = medial_axis(to_check)
    coverage = np.argwhere(abstraction > 0).tolist()
    
    if not len(coverage):
      break
    
    shuffle(coverage)
  
    x, y = coverage[0]
    
    if m.matrix[x][y] == Cell.CABLE:
      continue
    
    m.matrix[x, y] = Cell.ROUTER
    
    temp, passed_budget, cost = connect_to_backbone(m, (x, y), budget)
    
    if not passed_budget:
      break
    
    m = temp
    
    budget -= cost
    
    router_targets = m.computeRouterTargets((x,y))
    
    m.coverage.update(router_targets)
    
    for target in router_targets:
      tx, ty = target
      to_check[tx, ty] = 0
          
    pbar.update()
    
  pbar.close()
  return m, budget
      
    
def connect_to_backbone(m: Map, router: Cell, budget: int):
  path = bfs(m, router)
  cost = m.get_path_cost(path)
  
  temp = m
  
  if cost <= budget:
    for cell in path:
      if temp.matrix[cell] == Cell.ROUTER:
        temp.matrix[cell] = Cell.CONNECTED_ROUTER
      else:
        temp.matrix[cell] = Cell.CABLE
      
    return temp, True, cost

  return temp, False, cost


def bfs(m: Map, begin: tuple):
  visited = np.zeros((m.rows, m.columns), dtype=np.bool_)
  parent = [[-1] * m.columns for _ in range(m.rows)]
  
  queue = deque()
  queue.append(begin)
  visited[begin[0]][begin[1]] = True
  
  while queue:
    current_cell = queue.popleft()
    
    if m.matrix[current_cell] == Cell.CONNECTED_ROUTER or m.matrix[current_cell] == Cell.CABLE or current_cell == m.backbone:
      path = []
      curr_backtrack = current_cell
      while curr_backtrack != begin:
        path.append(curr_backtrack)
        curr_backtrack = parent[curr_backtrack[0]][curr_backtrack[1]]
      path.append(curr_backtrack)
      
      return path[1:]
    
    for adj in computeAdjacents(current_cell):
      x, y = adj
      if 0 <= x < m.rows and 0 <= y < m.columns:
        if not visited[x][y]:
          queue.append(adj)
          visited[x][y] = True
          parent[x][y] = current_cell
  
  return None