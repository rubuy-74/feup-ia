from algorithms.naive import naive
from algorithms.functions import mutation_func
from models.map import Map
import math
import random
import copy
import time

def simulated_annealing(current_map: Map, remaining_budget : int, probabilities: object, initial_temp=1000, cooling_rate=0.995, stopping_temp=1e-8, stop_condition=None):
  print("Running...")
  
  solutions = []
  it = 0

  best_map = copy.deepcopy(current_map)
  best_map_value = current_map.evaluate(remaining_budget)

  temp = initial_temp
  no_improvement_count = 0
  max_no_improvement = 2000

  start = time.time()
  while temp > stopping_temp:
    it += 1
    if stop_condition and stop_condition():
      print("Stopping")
      break

    new_map, new_budget, _ = mutation_func(current_map, remaining_budget, probabilities['add'], probabilities['remove'], probabilities['nothing'])
    current_map_value = current_map.evaluate(remaining_budget)
    new_map_value = new_map.evaluate(new_budget)

    if new_map_value > current_map_value:
      current_map = copy.deepcopy(new_map)
      current_map_value = new_map_value
      remaining_budget = new_budget

      if current_map_value > best_map_value:
        best_map = copy.deepcopy(new_map)
        best_map_value = current_map_value
        no_improvement_count = 0
        
    else:
      delta = new_map_value - current_map_value
      probability = math.exp(delta / temp)

      if random.random() < probability:
        current_map = copy.deepcopy(new_map)
        current_map_value = new_map_value
        remaining_budget = new_budget

    solutions.append(current_map_value)
    
    temp *= cooling_rate
    no_improvement_count += 1
    
    if no_improvement_count >= max_no_improvement:
      break
    
  return best_map, best_map_value, solutions, it, (time.time() - start)
