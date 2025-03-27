from models.solution import Solution
from models.map import Map
from models.router import Router
from algorithms.bfs import bfs_to_backbone_cell
import random
from models.cell import Cell


def add(s: Solution, m: Map):
    if m.get_cost(s) + m.rtPrice > m.budget:
       print("cant add due to budget")
       return s

    new_cell, path = find_best_router_cell(s, m)

    if not new_cell:
       return s
    
    if m.get_cost(s) + (m.bbPrice * len(path)) > m.budget:
       return s
    
    new_router = Router(new_cell, m.rRange, m.rtPrice, m.computeRouterTargets(new_cell))

    new_routers = s.routers.copy()
    new_routers.add(new_router)

    new_bb_connections = m.backbone.connections
    new_bb_connections[new_cell] = path

    return Solution(new_bb_connections, new_routers)

def find_best_router_cell(s: Solution, m: Map):
    covered_cells = s.computeCoverage()
    non_covered_cells = m.targets.difference(covered_cells)

    checked_cells = set()
    if non_covered_cells:
      c = random.choice(list(non_covered_cells - checked_cells))
      if router_is_valid(c, m, s):
        path = bfs_to_backbone_cell(m, c)
        return c, path
      
      checked_cells.add(c)
        
    print("returning maxer")
    c, path = maximizing_coverage(s, m)
    if c:
       return c, path
    
    print("returning random")
    return totally_random(s, m)

def router_is_valid(c: Cell, m: Map, s: Solution):
   return not m.isWall(c) and not m.isVoid(c) and not m.isBackbone(c) and c not in s.routers

def maximizing_coverage(s: Solution, m: Map):
   best_pos, best_path, best_cov = None, [], 0

   for _ in range(50):
    x = random.randint(0, m.columns - 1)
    y = random.randint(0, m.rows - 1)

    new_possible_cell = Cell(x, y)

    if router_is_valid(new_possible_cell, m, s):
       path_to_bb = bfs_to_backbone_cell(m, new_possible_cell)

       if path_to_bb:
          new_coverage = m.computeRouterTargets(new_possible_cell)
          if new_coverage > best_cov:
             best_cov = new_coverage
             best_path = path_to_bb
             best_pos = new_possible_cell
    
    return best_pos, best_path

def totally_random(s: Solution, m: Map):
   for _ in range(50):
    x = random.randint(0, m.columns - 1)
    y = random.randint(0, m.rows - 1)

    new_possible_cell = Cell(x, y)

    if router_is_valid(new_possible_cell, m, s):
       path_to_bb = bfs_to_backbone_cell(m, new_possible_cell)

       if path_to_bb:
          return new_possible_cell, path_to_bb
    
    print("returning none!")
    return None, []

       