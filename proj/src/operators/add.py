from models.solution import Solution
from models.map import Map
from models.router import Router
from algorithms.bfs import bfs_to_backbone_cell
import random

from models.cell import Cell

def add_router(s: Solution, m: Map) -> Solution:
  next_router_cell = None
  router_cells = [router.cell for router in m.routers]

  while True:
    x = random.randint(0, m.columns)
    y = random.randint(0, m.rows)

    possible_cell = Cell(x, y)

    if possible_cell not in (m.wired and m.walls and m.voids and router_cells) and not m.isBackbone(possible_cell):
      next_router_cell = possible_cell
      break

  if next_router_cell == None:
    while True:
      x = random.randint(0, m.columns)
      y = random.randint(0, m.rows)

      possible_cell = Cell(x, y)

      if possible_cell not in (m.walls and m.voids and router_cells) and not m.isBackbone(possible_cell):
        next_router_cell = possible_cell
        break

  s.routers.add(Router(possible_cell, m.rRange, m.rtPrice, m.computeRouterTargets(possible_cell)))
  
  s.backbone_cells.update(bfs_to_backbone_cell(m, possible_cell))

  return s
  


def remove_router(s: Solution, m: Map):
  print("to implement")