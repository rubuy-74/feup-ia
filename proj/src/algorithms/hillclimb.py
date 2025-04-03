from models.map import Map
from algorithms.functions import mutation_func

#TODO: Change number of iterations to time
def hillclimb(m: Map, remaining_budget: int, it: int):
  for _ in range(it):
    new_map, new_budget = mutation_func(m, remaining_budget)
    
    #TODO: EVALUATE
    new_map_value = new_map.evaluate(remaining_budget)
    old_map_value = m.evaluate(remaining_budget) 

    if(new_map_value >= old_map_value):
      m = new_map_value
      remaining_budget = new_budget

  return m