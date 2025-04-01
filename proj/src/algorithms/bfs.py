import collections
import models.map as classMap
import models.cell as cell

def bfs(m: classMap.Map, start: cell.Cell, target: cell.Cell) -> list[cell.Cell]:
  queue = collections.deque([(start, [start])])
  visited = set()
  visited.add(start)

  while queue:
    current_cell, path = queue.popleft()
    if current_cell == target:
      return path
    
    for adj in current_cell.adjacents():
      if 0 <= adj.x < m.columns and 0 <= adj.y < m.rows and adj not in visited:
        visited.add(adj)
        queue.append((adj, path + [adj]))      

  return []

def bfs_to_backbone_cell(m: classMap.Map, start: cell.Cell, targets: set[cell.Cell]) -> list[cell.Cell]:
  print(targets)
  
  queue = collections.deque([(start, [start])])
  visited = set()
  visited.add(start)
  
  while queue:
    current_cell, path = queue.popleft()
    if current_cell in targets:
      return path + bfs(m, current_cell, m.backbone.cell)
    
    for adj in current_cell.adjacents():
      if 0 <= adj.x < m.columns and 0 <= adj.y < m.rows and adj not in visited:
        visited.add(adj)
        queue.append((adj, path + [adj]))      
  
  return []