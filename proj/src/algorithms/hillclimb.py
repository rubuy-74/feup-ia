from models.map import Map
from algorithms.functions import mutation_func
import copy
import time

def hillclimb(m: Map, remaining_budget: int, probabilities: object, stop_condition=None):
  temp = copy.deepcopy(m)
  solutions = []
  it = 0
  
  start = time.time()
  while True:
    if stop_condition and stop_condition():
      print("Stopping due to external condition")
      break
    new_map, new_budget, _ = mutation_func(m, remaining_budget, probabilities['add'], probabilities['remove'], probabilities['nothing'])
    
    new_map_value = new_map.evaluate(new_budget)
    old_map_value = temp.evaluate(remaining_budget) 
    
    if(new_map_value > old_map_value):
      solutions.append(new_map_value)
      temp = copy.deepcopy(new_map)
      
    m = new_map
    remaining_budget = new_budget
    it += 1

  return temp, remaining_budget,solutions, it, (time.time()-start)
