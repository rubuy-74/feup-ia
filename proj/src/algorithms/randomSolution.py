# import models.cell as cell
# from algorithms.bfs import bfs
# from models.map import Map
# from models.cell import Cell
# import random

# import utils as utils

# def placeRouter(m: Map,wired: set[cell.Cell]) -> router.Router:
#   tries = 100
#   while (tries): 
#     x = random.randint(0,m.columns)
#     y = random.randint(0,m.rows)
#     routerCell = cell.Cell(x,y)

#     if checkValidRouter(m=m,cell=routerCell,wired=wired):
#       targets = m.computeRouterTargets(routerCell)
#       return router.Router(routerCell,m.rRange,m.rtPrice,targets)
#     tries -= 1
#   return router.Router(Cell(-1,-1),-1,-1, [])

# def checkValidRouter(m: Map, cell:cell.Cell, wired: set[cell.Cell]) -> bool:
#   return m.isTarget(cell=cell) and cell not in wired

# def randomSolution(m: Map, seed : int = -1) -> solution.Solution:
#   if(seed != -1):
#     random.seed(seed)
#   value = 0
  
#   wired = set()

#   # new_map : Map = Map(m.rows,m.columns,m.walls,m.voids,m.targets,m.backbone,m.budget,m.rtPrice,m.bbPrice,m.rRange,m.routers)
#   new_map = m
#   routers = []
#   paths = {} # real paths
  
#   last_path = []
#   last_cell = m.backbone.cell
#   # Budget must be less than price of a new router
#   while (value + new_map.rtPrice) < new_map.budget:
#     router = placeRouter(new_map, wired)
#     # failed to place new router
#     if(router.cell == Cell(-1,-1)):
#       return solution.Solution(routers=routers, backbone_cells=paths)
    

#     if router not in routers:
#       # m.backbone.connections[router.cell] = getPath(m=m,router=router)
#       path = bfs(new_map, router.cell, last_cell)
#       last_path += path
#       paths[router.cell] = last_path
#       last_cell = router.cell
      
      
#       routers.append(router)
#       value += new_map.rtPrice
#       wired.update(router.coverage)
      
#   return solution.Solution(routers=routers, backbone_cells=paths)
