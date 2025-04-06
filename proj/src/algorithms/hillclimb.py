from models.map import Map
from algorithms.functions import mutation_func
import copy
from tqdm import tqdm

def hillclimb(m: Map, remaining_budget: int, stop_condition=None):
  temp = copy.deepcopy(m)
  solutions = []
  
  #pbar = tqdm(range(it), desc="Running Hill Climb")
  
  while True:
    if stop_condition and stop_condition():
      print("Stopping due to external condition")
      break
    new_map, new_budget, _ = mutation_func(m, remaining_budget)
    
    new_map_value = new_map.evaluate(new_budget)
    old_map_value = temp.evaluate(remaining_budget) 
    
    print(old_map_value, new_map_value)
    
    if(new_map_value > old_map_value):
      print("ACCEPTING BEST")
      solutions.append(new_map_value)
      temp = copy.deepcopy(new_map)
      
    m = new_map
    remaining_budget = new_budget
    
    #pbar.update()
    
  #pbar.close()      

  return temp, remaining_budget,solutions
