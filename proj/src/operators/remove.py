from models.solution import Solution
from models.map import Map
from algorithms import bfs
from models.cell import Cell
import random

def remove(s: Solution):
  if not s.routers:
    return s

  router_to_remove = random.choice(list(s.routers))

  new_routers = s.routers.copy()
  new_routers.remove(router_to_remove)

  new_bb_connections = s.backbone_cells.copy()
  
  del new_bb_connections[router_to_remove.cell]

  return Solution(new_bb_connections, new_routers)