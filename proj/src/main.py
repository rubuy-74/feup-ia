import sys
import utils as utils
import algorithms.randomSolution as randomSolution
import algorithms.greedySolution as greedySolution

""" def find_nearest_available_cell_to_router(map: Map, routers: list):
  queue = collections.deque([map.backbone.cell])
  visited = set()
  visited.add(map.backbone.cell)
  while queue:
    possible_cell = queue.popleft()

    if not is_wall(possible_cell, map) and not is_backbone(possible_cell, map) and not is_wired(possible_cell, map) and not is_void(possible_cell, map) and possible_cell not in routers:
      return possible_cell
    
    for adj in adjacents(possible_cell):
      if 0 <= adj.x < map.rows and 0 <= adj.y < map.columns and adj not in visited:
        visited.add(adj)
        queue.append(adj)
  
  return None """

""" def compute_targets(map: Map, router: Router):
  targets = set()
  range_ = router.range_
  rx, ry = router.cell.x, router.cell.y

  for x in range(max(0, rx - range_), min(map.rows, rx + range_ + 1)):
    for y in range(max(0, ry - range_), min(map.columns, ry + range_ + 1)):
      if abs(rx - x) <= range_ and abs(ry - y) <= range_:
        if not any(is_wall(Cell(w, v), map) for w in range(min(rx, x), max(rx, x)) for v in range(min(ry, y), max(ry, y))):
          possible_target = Cell(x, y)
          
          if is_target(possible_target, map):
            targets.add(possible_target)

  return targets """

""" 
def greedy(map: Map, router_cost, router_range):
  solution = Solution([], 0, set())

  while True:
    # find the closest available cell of the backbone to place a router
    cell_to_router = find_nearest_available_cell_to_router(map, [router.cell for router in solution.routers])

    if(cell_to_router is None):
      break

    # create the router
    router = routerClass.Router(cell_to_router, router_cost, router_range)
    
    # find the shortest path between the router and the backbone
    path = bfs.bfs(map, map.backbone.cell, router.cell)

    # update cost
    new_cost = solution.cost + router_cost + map.backbone.cost * (len(path)-1)

    if new_cost <= map.budget:
      solution.cost = new_cost
      solution.routers.append(router)
      solution.fiber.update(path)

      # update targets based on the new router
      map.wired.update(compute_targets(map, router))

      # update the backbone connections
      map.backbone.connected_to.extend(path)
    else:
      break
   
  return solution
 """

import models.cell as cell
import models.map as mapClass
import models.router as router

def main():
  m: mapClass.Map = utils.parse(sys.argv[1])

  sol = greedySolution.greedySolution(m)
  print(sol)
  print(m.evaluate(sol))

  targets = sol.getTargets()
  routerCells = list(map(lambda router: router.cell,sol.routers))

  for i in range(0,m.rows):
    for j in range(0,m.columns):
      newCell = cell.Cell(j,i)
      if(newCell in routerCells):
        print("r",end="")
      elif newCell == m.backbone.cell:
        print("b",end="")
      elif newCell in targets:
        print("x",end="")
      elif m.isWall(newCell):
        print("w",end="")
      elif m.isVoid(newCell):
        print("-",end="")
      else:
        print(" ",end="")
    print()

if __name__ == "__main__":
  main()
