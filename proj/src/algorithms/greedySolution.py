import heapq
from time import process_time
import models.map as mapClass
import models.router as router
import models.solution as solution
import models.cell as cell
import utils as utils
import models.cell as cell
import collections
import algorithms.randomSolution as randomSolution

def compute_mst(m: mapClass.Map, routers: set[cell.Cell]) -> dict:
    if not routers:
        return {}
    
    edges = []
    for r1 in routers:
        for r2 in routers:
            if r1 != r2:
                distance = abs(r1.x - r2.x) + abs(r1.y - r2.y)
                edges.append((distance, r1, r2))
    
    edges.sort()
    parent = {r: r for r in routers}
    
    def find(cell):
        if parent[cell] != cell:
            parent[cell] = find(parent[cell])
        return parent[cell]
    
    def union(cell1, cell2):
        root1, root2 = find(cell1), find(cell2)
        if root1 != root2:
            parent[root2] = root1
    
    mst = {}
    for distance, r1, r2 in edges:
        if find(r1) != find(r2):
            union(r1, r2)
            path = []
            if r1.x != r2.x:
                step = 1 if r1.x < r2.x else -1
                for x in range(r1.x, r2.x, step):
                    path.append(cell.Cell(x, r1.y))
            if r1.y != r2.y:
                step = 1 if r1.y < r2.y else -1
                for y in range(r1.y, r2.y, step):
                    path.append(cell.Cell(r2.x, y))
            mst[r2] = path
    
    return mst

def findRouterCell(m: mapClass.Map, routers: set[cell.Cell], start_cell: cell.Cell, wired: set[cell.Cell]) -> tuple:
    queue = collections.deque([(start_cell, [])])
    visited = set()
    while queue:
        possible_cell, path = queue.popleft()
        if not m.isWall(possible_cell) and not m.isBackbone(possible_cell) and possible_cell not in wired and not m.isVoid(possible_cell) and possible_cell not in routers:
            return possible_cell, path 
        for adj in possible_cell.adjacents():
            if 0 <= adj.x < m.columns and 0 <= adj.y < m.rows and adj not in visited:
                visited.add(adj)
                queue.append((adj, path + [adj]))
    return None, []

def greedySolution(m : mapClass.Map) -> solution.Solution:
    value = 0
    first_router = randomSolution.placeRouter(m, set())
    routers_cells = set()
    routers = set()
    wired = set()
    backbone_connections = {}
    start_cell = m.backbone.cell
    previous_path = []
    time_start = process_time()
    
    if first_router.cell != cell.Cell(-1,-1):
        routers_cells.add(first_router.cell)
        routers.add(first_router)
        wired.update(first_router.coverage)
        start_cell = first_router.cell
        value = m.rtPrice
    
    second_router = randomSolution.placeRouter(m, routers_cells)
    if second_router.cell != cell.Cell(-1, -1):
        routers_cells.add(second_router.cell)
        routers.add(second_router)
        wired.update(second_router.coverage)
        start_cell = second_router.cell
        value += m.rtPrice
    
    while value < m.budget:
        routerCell, _ = findRouterCell(m, routers_cells, start_cell, wired)
        if routerCell is None:
            break
        r = router.Router(routerCell, m.rRange, m.rtPrice, m.computeRouterTargets(routerCell))
        wired.update(r.coverage)
        start_cell = r.cell
        routers.add(r)
        routers_cells.add(r.cell)
        value += m.rtPrice
        
        if value > m.budget:
            break
    
    # Compute MST for backbone connections
    backbone_connections = compute_mst(m, routers_cells)
    
    time_end = process_time()
    print("TIME: " + str(time_end - time_start))
    return solution.Solution(backbone_cells=backbone_connections, routers=routers)
