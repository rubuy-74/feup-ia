from time import process_time
import models.map as mapClass
import models.router as router
import models.solution as solution
import models.cell as cell
import utils as utils
import models.cell as cell
import collections

def findRouterCell(map: mapClass.Map, routers: set[cell.Cell], start_cell: cell.Cell) -> tuple:
  queue = collections.deque([(start_cell, [])])
  visited = set()
  while queue:
    possible_cell, path  = queue.popleft()

    if not map.isWall(possible_cell) and not map.isBackbone(possible_cell) and not map.isWired(possible_cell) and not map.isVoid(possible_cell) and possible_cell not in routers:
      return possible_cell, path
  

    for adj in possible_cell.adjacents():
      if 0 <= adj.x < map.columns and 0 <= adj.y < map.rows and adj not in visited:
        visited.add(adj)
        queue.append((adj, path + [adj]))

  return None, []

def greedySolution(m : mapClass.Map) -> solution.Solution:
  value = 0
  routers = set()
  backbone_cells = set()
  routers_cells = set()

  start_cell = m.backbone.cell

  time_start = process_time()

  while value < m.budget:
    routerCell, path = findRouterCell(map=m,routers=routers_cells, start_cell=start_cell)

    if routerCell is None:
      break

    r = router.Router(routerCell,m.rRange,m.rtPrice,m)
    
    start_cell = r.cell

    value += m.rtPrice + len(path) * m.bbPrice

    print("Value is: " + str(value))

    if value > m.budget:
      break
    
    routers.add(r)
    routers_cells.add(r.cell)
    
    backbone_cells.update(path)   
    
  time_end = process_time()

  print("TIME: " + str(time_end - time_start))

  return solution.Solution(backbone_cells=backbone_cells,routers=routers)