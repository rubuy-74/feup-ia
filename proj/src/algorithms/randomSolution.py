import models.map as mapClass
import models.solution as solution
import models.router as router
import models.cell as cell
import algorithms.bfs as bfs
import random

import utils as utils

def placeRouter(m: mapClass.Map ) -> router.Router:
  while (True): 
    x = random.randint(0,m.columns)
    y = random.randint(0,m.rows)
    routerCell = cell.Cell(x,y)

    if checkValidRouter(m=m,cell=routerCell):
      return router.Router(routerCell,m.rRange,m.rtPrice, m.computeRouterTargets(routerCell))

def checkValidRouter(m: mapClass.Map, cell:cell.Cell) -> bool:
  return m.isTarget(cell=cell)

def getPath(m: mapClass.Map, router : router.Router) -> list[cell.Cell]:
  result = bfs.bfs(map=m,start=m.backbone.cell,target=router.cell)
  return result[1:-1]

def randomSolution(m: mapClass.Map) -> solution.Solution:
  value = 0
  routers = []
  backbone_cells = set()

  # Budget must be less than price of a new router
  while (value + m.rtPrice) < m.budget:
    router = placeRouter(m)
    if router not in routers:
      backbone_cells.update(getPath(m=m,router=router))
      routers.append(router)
      value += m.rtPrice
  return solution.Solution(routers=routers,backbone_cells=backbone_cells)
