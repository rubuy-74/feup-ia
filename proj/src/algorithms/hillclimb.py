from models.map import Map
from algorithms.functions import mutation_func
import copy

def hillclimb(m: Map, remaining_budget: int, it: int):
  temp = copy.deepcopy(m)
  for _ in range(it):
    new_map, new_budget, action = mutation_func(m, remaining_budget)
    
    new_map_value = new_map.evaluate(remaining_budget)
    old_map_value = temp.evaluate(remaining_budget) 

    if(new_map_value > old_map_value):
      temp = new_map
      remaining_budget = new_budget
      print(action)

  return temp, remaining_budget