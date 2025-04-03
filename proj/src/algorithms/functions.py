import models.map as mapClass
import operators.add as add
import operators.remove as remove
from models.solution import Solution
import random

def mutation_func(m: mapClass.Map,
                  solution: Solution,
                  add_rate: float = 0.40,
                  remove_rate: float = 0.40,
                  nothing_rate: float = 0.20):
  
  action = random.choices(["add","remove","nothing"],weights=[add_rate*100,remove_rate*100,nothing_rate*100])[0]

  # do nothing
  if action == "nothing": 
    return solution

  # adds a new router and path to solution
  if action == "add":
    print("adding")
    return add.add(solution,m)

  # remove random path from the solution
  if action == "remove":
    print("remving")
    return remove.remove(solution)

  return solution


def crossover_func(m: mapClass.Map, first: Solution, second: Solution) -> Solution:
  current_value = 0
  routers = set()
  
  new_bb_cells = {}
  bb_cells = set()
  
  while current_value <= m.budget:
    which_parent_to_choose = random.randint(1, 2)
    
    if current_value + m.rtPrice > m.budget:
      break
    
    if which_parent_to_choose == 1 and len(first.routers) > 0:
      router = first.routers.pop()
      
      routers.add(router)
      
      new_bb_cells[router.cell] = first.backbone_cells[router.cell]
      bb_cells.update(first.backbone_cells[router.cell])
      
    else:
      if len(second.routers) < 1:
       break
     
      router = second.routers.pop()
     
      routers.add(router)
      new_bb_cells[router.cell] = second.backbone_cells[router.cell]
      bb_cells.update(second.backbone_cells[router.cell])
      
  
    current_value = len(bb_cells) * m.bbPrice + len(routers) * m.rtPrice
      
  return Solution(routers=routers, backbone_cells=new_bb_cells)
  