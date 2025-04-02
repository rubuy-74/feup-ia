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

def bfs_following_only_bb_cells(m: classMap.Map, start: cell.Cell, target: cell.Cell, bb_cells: list[cell.Cell]) -> list[cell.Cell]:
  queue = collections.deque([(start, [start])])
  visited = set()
  visited.add(start)
  
  while queue:
    current_cell, path = queue.popleft()
    if current_cell == target:
      return path
    
    for adj in current_cell.adjacents():
      if 0 <= adj.x < m.columns and 0 <= adj.y < m.rows and adj not in visited and adj in bb_cells:
        visited.add(adj)
        queue.append((adj, path + [adj]))      

  return []
    

def bfs_to_backbone_cell(m: classMap.Map, start: cell.Cell, targets: set[cell.Cell]) -> list[cell.Cell]:
  queue = collections.deque([(start, [start])])
  visited = set()
  visited.add(start)
  
  while queue:
    current_cell, path = queue.popleft()
    if current_cell in targets and current_cell != start:
      
      remaining_path_to_backbone = []
      
      if not m.isBackbone(current_cell):
        remaining_path_to_backbone = bfs_following_only_bb_cells(m, current_cell, m.backbone.cell, targets)
      
        if remaining_path_to_backbone == []:
          remaining_path_to_backbone = bfs(m, current_cell, m.backbone.cell)
      
      return path + remaining_path_to_backbone
    
    for adj in current_cell.adjacents():
      if 0 <= adj.x < m.columns and 0 <= adj.y < m.rows and adj not in visited:
        visited.add(adj)
        queue.append((adj, path + [adj]))      
  
  return []