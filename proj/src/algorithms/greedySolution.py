import models.map as mapClass
import models.router as router
import models.solution as solution
import models.cell as cell
import algorithms.bfs as bfs
import utils as utils

import collections

def checkValidRouter(map: mapClass.Map, cell:cell.Cell) -> bool:
  return map.isTarget(cell=cell)

def getPath(map: mapClass.Map, r: router.Router) -> list[cell.Cell]:
  result = bfs.bfs(map=map,start=map.backbone.cell,target=r.cell)
  return result[1:-1]

def findRouterCell(map: mapClass.Map, routers: list[router.Router]) -> cell.Cell:
  queue = collections.deque([map.backbone.cell])
  visited = set()
  while queue:
    possible_cell = queue.popleft()

    if not map.isWall(possible_cell) and not map.isBackbone(possible_cell) and not map.isWired(possible_cell) and not map.isVoid(possible_cell) and router.Router(possible_cell, 0, 0, []) not in routers:
      return possible_cell
    
    for adj in possible_cell.adjacents():
      if 0 <= adj.x < map.rows and 0 <= adj.y < map.columns and adj not in visited:
        visited.add(adj)
        queue.append(adj)

def greedySolution(map : mapClass.Map) -> solution.Solution:
  value = 0
  routers = []
  paths = dict()

  while value < map.budget:
    routerCell = findRouterCell(map=map,routers=routers)
    
    if routerCell is None:
      break
    
    rWalls = utils.getWallRange(map.rRange,routerCell.x,routerCell.y,map.walls)

    r = router.Router(routerCell,map.rRange,map.rtPrice,rWalls)
    
    tempPath = getPath(map=map,r=r)
    
    value += map.rtPrice + len(tempPath) * map.bbPrice

    print("Value is: " + str(value))

    if value > map.budget:
      break
    
    routers.append(r)
    paths[r.cell] = tempPath
    

  return solution.Solution(paths=paths,routers=routers)