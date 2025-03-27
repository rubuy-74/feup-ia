from models.solution import Solution
from models.map import Map
from models.cell import Cell
from models.backbone import Backbone
from algorithms.bfs import bfs_to_backbone_cell
import random

def remove(s: Solution, m: Map):
  router_to_remove = random.choice(list(s.routers))

  new_routers = s.routers - {router_to_remove}
  m.routers = new_routers

  routers_possibly_affected = update_backbone_cells(router_to_remove.cell, m.backbone, {r.cell for r in m.routers})
  
  for r in routers_possibly_affected:
    if any(r.adjacents()) in m.backbone.connected_to:
      continue
    else:
      new_path = bfs_to_backbone_cell(m, r)
      m.backbone.connected_to.update(new_path)

  new_backbone_cells = m.backbone.connected_to
  
  return Solution(new_backbone_cells, new_routers)

def update_backbone_cells(removedCell: Cell, backbone: Backbone, router_cells: set[Cell]) -> set[Cell]:
  neighbours = filter(lambda c: c in backbone.connected_to or c in router_cells or c == backbone.cell, removedCell.adjacents())

  routers_affected = set()

  for n in neighbours:
    if n in router_cells or n == backbone.cell: # found affected router, add it to optimize its path
      routers_affected.add(n)
      break
    
    if n in backbone.connected_to:
      backbone.connected_to.remove(n)
      

    routers_affected.update(update_backbone_cells(n, backbone, router_cells))


  return routers_affected
    
    
