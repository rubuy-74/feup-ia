from models.map import Map
from algorithms.functions import mutation_func
import copy
from tqdm import tqdm

def hillclimb(m: Map, remaining_budget: int, it: int):
  temp = copy.deepcopy(m)
  solutions = []
  
  pbar = tqdm(range(it), desc="Running Hill Climb")
  
  for _ in range(it):
    new_map, new_budget, _ = mutation_func(m, remaining_budget)
    
    new_map_value = new_map.evaluate(new_budget)
    old_map_value = temp.evaluate(remaining_budget) 
    
    if(new_map_value > old_map_value):
      solutions.append(new_map_value)
      
      temp = copy.deepcopy(m)
      
      remaining_budget = new_budget
    
    m = new_map
    pbar.update()
    
  pbar.close()      

  return temp, remaining_budget,solutions
