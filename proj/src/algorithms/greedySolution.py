import heapq
from time import process_time
import models.map as mapClass
import models.router as router
import models.solution as solution
import models.cell as cell
import utils as utils
import models.cell as cell
import collections

def a_star_router_search(m: mapClass.Map, routers: set[cell.Cell], start_cell: cell.Cell) -> tuple:
    def heuristic(cell1: cell.Cell, cell2: cell.Cell) -> float:
        return abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)

    priority_queue = [(0, start_cell, [])]
    visited = {start_cell}

    while priority_queue:
        priority, current_cell, path = heapq.heappop(priority_queue)

        if not m.isWall(current_cell) and not m.isBackbone(current_cell) and not m.isWired(current_cell) and not m.isVoid(current_cell) and current_cell not in routers:
            return current_cell, path

        for adj in current_cell.adjacents():
            if 0 <= adj.x < m.columns and 0 <= adj.y < m.rows and adj not in visited:
                visited.add(adj)
                new_path = path + [adj]
                priority = len(new_path) + heuristic(adj, start_cell)
                heapq.heappush(priority_queue, (priority, adj, new_path))

    return None, []

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
    routerCell, path = a_star_router_search(m=m,routers=routers_cells, start_cell=start_cell)

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
    
    print("VALUE:", value)
    
  time_end = process_time()

  print("TIME: " + str(time_end - time_start))

  return solution.Solution(backbone_cells=m.backbone.connections, routers=m.routers)