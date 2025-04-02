from time import process_time
import models.map as mapClass
import models.router as router
import models.solution as solution
import models.cell as cell
import utils as utils
import models.cell as cell
import collections

def findRouterCell(m: mapClass.Map, routers: set[cell.Cell], start_cell: cell.Cell) -> tuple:
  queue = collections.deque([(start_cell, [])])
  visited = set()
  while queue:
    possible_cell, path  = queue.popleft()

    if not m.isWall(possible_cell) and not m.isBackbone(possible_cell) and not m.isWired(possible_cell) and not m.isVoid(possible_cell) and possible_cell not in routers:
      return possible_cell, path 
  

    for adj in possible_cell.adjacents():
      if 0 <= adj.x < m.columns and 0 <= adj.y < m.rows and adj not in visited:
        visited.add(adj)
        queue.append((adj, path + [adj]))

  return None, []

def greedySolution(m : mapClass.Map) -> solution.Solution:
  value = 0
  routers_cells = set()

  start_cell = m.backbone.cell
  
  previous_path = []

  time_start = process_time()

  while value < m.budget:
    routerCell, path = findRouterCell(m=m,routers=routers_cells, start_cell=start_cell)

    if routerCell is None:
      break

    value += m.rtPrice + len(path) * m.bbPrice

    if value > m.budget:
      break

    r = router.Router(routerCell,m.rRange,m.rtPrice, m.computeRouterTargets(routerCell))
    
    start_cell = r.cell
    
    m.routers.add(r)
    routers_cells.add(r.cell)
    
    m.backbone.connections[r.cell] = path + previous_path
    previous_path = m.backbone.connections[r.cell]
    
  time_end = process_time()

  print("TIME: " + str(time_end - time_start))

  return solution.Solution(backbone_cells=m.backbone.connections, routers=m.routers)