from models.map import Map
from models.cell import Cell
from algorithms.naive import connect_to_backbone
from utils import computeAdjacents
import random
import numpy as np
from collections import deque

def add(m: Map, current_budget: int):
   if current_budget + m.rtPrice > m.budget:
      
      return m, current_budget, "add"
   
   for _ in range(50):
      x = random.randint(0, m.rows - 1)
      y = random.randint(0, m.columns - 1)
      
      if isValid(m, (x, y)):
         type_of_cell_before = m.matrix[x, y]
         m.matrix[x, y] = Cell.ROUTER
         
         temp, passed_budget, cost = connect_to_backbone(m, (x, y), current_budget)
      
         if not passed_budget:
            m.matrix[x, y] = type_of_cell_before
            temp.matrix[x, y] = type_of_cell_before
            continue
         
         router_targets = temp.computeRouterTargets((x,y))
         temp.coverage.update(router_targets)
         
         return temp, current_budget - cost, "add"
   
   return m, current_budget, "add"
      

def isValid(m: Map, coords: tuple):
   return not m.isBackBone(coords) and not m.isRouter(coords) and not m.isWall(coords) and not m.isVoid(coords) and not m.isCable(coords)

def remove(m: Map, current_budget: int):
   routers = np.argwhere(m.matrix == Cell.CONNECTED_ROUTER)
   
   if routers.size == 0:
      return m, current_budget, "remove"
   
   x, y = random.choice(routers)
   
   adjs = computeAdjacents((x, y))
   connected_adjs = list(filter(lambda x: m.isCable(x) or m.isBackBone(x) or m.isRouter(x), adjs))
   
   if len(connected_adjs) >= 2:
      m.matrix[x, y] = Cell.CABLE
      current_budget += m.rtPrice - m.bbPrice
   else:
      current_budget += m.rtPrice
      path_until_interception = bfs_until_interception(m, (x, y))
      
      for cell in path_until_interception[:-1]:
         if m.original[cell] != Cell.WALL:
            if m.matrix[cell] == Cell.CONNECTED_ROUTER:
               current_budget += m.rtPrice
            elif m.matrix[cell] == Cell.CABLE:
               current_budget += m.bbPrice
            
            m.matrix[cell] = Cell.TARGET
         else:
            m.matrix[cell] = Cell.WALL
      
   new_coverage = set()
      
   for router in routers:
      new_coverage.update(m.computeRouterTargets(router))

   m.coverage = new_coverage

   return m, current_budget, "remove"

def bfs_until_interception(m: Map, begin: tuple):
  visited = set()
  queue = deque()
  queue.append((begin, [begin]))
  
  while queue:
   current_cell, path = queue.popleft()
    
   if current_cell in visited:
      continue
   
   visited.add(current_cell)
   
   if current_cell != begin:
      adjs = computeAdjacents(current_cell)
      connected_adjs = list(filter(lambda x: m.isCable(x) or m.isBackBone(x) or m.isRouter(x), adjs))
    
      if len(connected_adjs) >= 3:
         return path
    
   for adj in computeAdjacents(current_cell):
      x, y = adj
      if (0 <= x < m.rows and 0 <= y < m.columns and adj not in visited and (m.isCable(adj) or m.isBackBone(adj) or m.isRouter(adj))):
         new_path = path + [adj]
         queue.append((adj, new_path))
  
  return None