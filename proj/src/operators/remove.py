from models.solution import Solution
from models.map import Map
from models.cell import Cell
from models.backbone import Backbone
from algorithms.bfs import bfs_to_backbone_cell
import random

def remove(s: Solution, m: Map):
  if not s.routers:
    return s
  
  router_to_remove = random.choice(list(s.routers))

  new_routers = s.routers.copy()
  new_routers.remove(router_to_remove)

  exclusive_cells = find_exclusive_cells(m, s, router_to_remove.cell)

  print("Connections:", m.backbone.connections)

  print("Exclusive cells:", exclusive_cells)

  new_bb_cells = s.backbone_cells.copy()
  print("Old bb:", new_bb_cells)
  new_bb_cells.difference_update(exclusive_cells)
  print("New bb:", new_bb_cells)

  return Solution({'':new_bb_cells}, new_routers)

def get_paths_from_other_routers(m: Map, r: Cell):
  other_paths = set()
  
  print(m.backbone.connections.items())

  for key, value in m.backbone.connections.items():
    print(key, value, r)
    if key != r:
      other_paths.update(value)

  return other_paths

def find_exclusive_cells(m: Map, s: Solution, r: Cell):
  exclusive_cells = set()
  router_path = m.backbone.connections[r]

  print("Path for R:", router_path)

  for c in router_path:
    if m.isBackbone(c):
      continue

    cell_is_shared = c in get_paths_from_other_routers(m, r)

    print(str(c) + " is shared: " + str(cell_is_shared))

    if not cell_is_shared:
      exclusive_cells.add(c)

  return exclusive_cells

  
