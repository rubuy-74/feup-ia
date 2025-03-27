from models.solution import Solution
from models.map import Map
from models.cell import Cell
import random

def remove(s: Solution, m: Map):
  if not s.routers:
    return s

  router_to_remove = random.choice(list(s.routers))

  new_routers = s.routers.copy()
  new_routers.remove(router_to_remove)

  new_bb_connections = m.backbone.connections.copy()
  del new_bb_connections[router_to_remove.cell]

  #exclusive_cells = find_exclusive_cells(m, s, router_to_remove.cell)

  #new_bb_cells = s.backbone_cells.copy()
  #new_bb_cells.difference_update(exclusive_cells)

  #new_solution = 

  return Solution(new_bb_connections, new_routers)

def get_paths_from_other_routers(m: Map, r: Cell):
  other_paths = set()

  for key, value in m.backbone.connections.items():
    if key != r:
      other_paths.update(value)

  return other_paths

def find_exclusive_cells(m: Map, s: Solution, r: Cell):
  exclusive_cells = set()
  router_path = m.backbone.connections[r]

  for c in router_path:
    if m.isBackbone(c):
      continue

    cell_is_shared = c in get_paths_from_other_routers(m, r)

    if not cell_is_shared:
      exclusive_cells.add(c)

  return exclusive_cells

  
