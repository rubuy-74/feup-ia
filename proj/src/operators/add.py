from models.solution import Solution
from models.map import Map
from models.router import Router
from algorithms.bfs import bfs_to_backbone_cell
import random

from models.cell import Cell

def add(s: Solution, m: Map) -> Solution:
  next_router_cell = None
  router_cells = [router.cell for router in m.routers]

  remaining_target_cells = list(m.wired.difference(m.targets))

  if len(remaining_target_cells) == 0:
    while True:
      possible_cell = random.choice(list(m.targets))

      if possible_cell not in (m.walls and m.voids and router_cells) and not m.isBackbone(possible_cell) and possible_cell not in router_cells:
        next_router_cell = possible_cell
        break
  else:
    possible_cell = random.choice(remaining_target_cells)
    
    if possible_cell not in router_cells and not m.isBackbone(possible_cell):
      next_router_cell = possible_cell

  new_router = Router(next_router_cell, m.rRange, m.rtPrice, m.computeRouterTargets(next_router_cell))
  
  # change map routers and create new list for further solution
  m.routers.add(new_router)
  new_routers = s.routers.union({new_router})

  # change map backbone cells and create new list for further solution
  new_backbone_cells = s.backbone_cells.union(bfs_to_backbone_cell(m, next_router_cell))
  m.backbone.connected_to.update(bfs_to_backbone_cell(m, next_router_cell))


  return Solution(new_backbone_cells, new_routers)