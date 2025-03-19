import collections
import models.map as classMap
import models.cell as cell

def bfs(map: classMap.Map, start: cell.Cell, target: cell.Cell) -> list[cell.Cell]:
  queue = collections.deque([(start, [start])])
  visited = set()
  visited.add(start)

  while queue:
    current_cell, path = queue.popleft()
    if current_cell == target:
      return path
    
    for adj in current_cell.adjacents():
      if 0 <= adj.x < map.columns and 0 <= adj.y < map.rows and adj not in visited:
        visited.add(adj)
        queue.append((adj, path + [adj]))      

  return []