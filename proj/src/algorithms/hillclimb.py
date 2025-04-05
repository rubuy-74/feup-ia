from models.map import Map
from algorithms.functions import mutation_func
import copy

def hillclimb(m: Map, remaining_budget: int, it: int):
  temp = copy.deepcopy(m)
  solutions = []
  
  for _ in range(it):
    new_map, new_budget, _ = mutation_func(m, remaining_budget)
    
    new_map_value = new_map.evaluate(new_budget)
    old_map_value = temp.evaluate(remaining_budget) 
    
    # print(f"old_value:{old_map_value} / new_value = {new_map_value}")
    
    if(new_map_value >= old_map_value):
      temp = new_map
      c = Map(temp.rows,temp.columns,temp.backbone,temp.budget,temp.rtPrice,temp.bbPrice,temp.rRange,temp.matrix)
      solutions.append(c.evaluate(new_budget))
      remaining_budget = new_budget
      

  return temp, remaining_budget,solutions