import models.solution as solution
import models.router as router
import models.cell as cell
from algorithms.bfs import bfs_to_backbone_cell
from models.map import Map
from models.cell import Cell
import random

import utils as utils

def placeRouter(m: Map ) -> router.Router:
  tries = 100
  while (tries): 
    x = random.randint(0,m.columns)
    y = random.randint(0,m.rows)
    routerCell = cell.Cell(x,y)

    if checkValidRouter(m=m,cell=routerCell):
      targets = m.computeRouterTargets(routerCell)
      return router.Router(routerCell,m.rRange,m.rtPrice,targets)
    tries -= 1
  return router.Router(Cell(-1,-1),-1,-1,[])

def checkValidRouter(m: Map, cell:cell.Cell) -> bool:
  return m.isTarget(cell=cell) and cell not in m.wired

def randomSolution(m: Map) -> solution.Solution:
  value = 0

  # new_map : Map = Map(m.rows,m.columns,m.walls,m.voids,m.targets,m.backbone,m.budget,m.rtPrice,m.bbPrice,m.rRange,m.routers)
  new_map = m
  routers = []
  current_paths = [m.backbone.cell] # targets
  paths = {} # real paths
  # Budget must be less than price of a new router
  while (value + new_map.rtPrice) < new_map.budget:
    router = placeRouter(new_map)
    # failed to place new router
    if(router.cell == Cell(-1,-1)):
      return solution.Solution(routers=routers, backbone_cells=paths)

    if router not in routers:
      # m.backbone.connections[router.cell] = getPath(m=m,router=router)
      path = bfs_to_backbone_cell(new_map,router.cell,current_paths)
      current_paths = path + [router.cell]
      paths[router.cell] = path
      routers.append(router)
      value += new_map.rtPrice
  return solution.Solution(routers=routers, backbone_cells=paths)
