import models.map as mapClass
import models.solution as solution
import models.router as router
import models.cell as cell
import algorithms.bfs as bfs
import random

import utils as utils

def placeRouter(map : mapClass.Map ) -> router.Router:
  while (True): 
    x = random.randint(0,map.columns)
    y = random.randint(0,map.rows)
    routerCell = cell.Cell(x,y)

    if checkValidRouter(map=map,cell=routerCell):
      return router.Router(routerCell,map.rRange,map.rtPrice,map)

def checkValidRouter(map: mapClass.Map, cell:cell.Cell) -> bool:
  return map.isTarget(cell=cell)

def getPath(map: mapClass.Map, router : router.Router) -> list[cell.Cell]:
  result = bfs.bfs(map=map,start=map.backbone.cell,target=router.cell)
  return result[1:-1]

def randomSolution(map : mapClass.Map, seed) -> solution.Solution:
  random.seed(seed)
  value = 0
  routers = []
  paths = dict()

  # Budget must be less than price of a new router
  while (value + map.rtPrice) < map.budget:
    router = placeRouter(map)
    if router not in routers:
      paths[router.cell] = getPath(map=map,router=router)
      routers.append(router)
      value += map.rtPrice
  return solution.Solution(routers=routers,paths=paths)
