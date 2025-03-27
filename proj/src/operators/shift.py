from models.solution import Solution
from models.map import Map
from models.router import Router
import random

def shift(s: Solution, m: Map) -> Solution:
  router_to_remove : Router = random.choice(list(s.routers))

  backbone_cells = m.backbone.connected_to
  adj_cells = router_to_remove.cell.adjacents()
  adj_backbone_cells = set(filter(lambda x: x in backbone_cells,adj_cells))

  new_router_cell = random.choice(router_to_remove.cell.adjacents())
  while(new_router_cell in adj_backbone_cells or m.isWall(new_router_cell)):
    new_router_cell = random.choice(router_to_remove.cell.adjacents())

  # adjecent to the adjacent backbone cells
  adj_adj_backbone_cells = [x for xs in list(map(lambda x: x.adjacents(),adj_backbone_cells)) for x in xs]

  new_routers = s.routers
  new_bb_cells = s.backbone_cells

  if(new_router_cell in adj_adj_backbone_cells):
    new_routers = new_routers - {router_to_remove}
    new_routers = new_routers.union({Router(new_router_cell, m.rRange, m.rtPrice, m.computeRouterTargets(new_router_cell))})
  else:
    # check if possible
    if(m.get_cost(s) + m.bbPrice > m.budget):
      print("couldn't shift")
      return s
    new_routers = new_routers - {router_to_remove}

    new_adj_cells = new_router_cell.adjacents()
    for i in new_adj_cells:
      if(i in s.backbone_cells): new_bb_cells = s.backbone_cells - {i}
      if(i in m.backbone.connected_to): m.backbone.connected_to.remove(i)
    new_bb_cells = new_bb_cells.union({router_to_remove.cell})
    m.backbone.connected_to.add(router_to_remove.cell)

  new_routers = new_routers.union({Router(new_router_cell, m.rRange, m.rtPrice, m.computeRouterTargets(new_router_cell))})

  return Solution(new_bb_cells, new_routers)





