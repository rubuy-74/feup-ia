from algorithms.naive import naive
from algorithms.functions import mutation_func
from models.map import Map
import math
import random
import copy

def simulated_annealing(m: Map, initial_temp=1000, cooling_rate=0.995, stopping_temp=1e-8, max_iterations=500):
  solutions = []

  current_map, remaining_budget = naive(m)
  print("finished naive")
  best_map = copy.deepcopy(current_map)
  best_map_value = current_map.evaluate(remaining_budget)

  temporary = best_map_value

  temp = initial_temp
  iteration = 0
  no_improvement_count = 0
  max_no_improvement = 2000

  while temp > stopping_temp and iteration < max_iterations:

    new_map, new_budget, _ = mutation_func(current_map, remaining_budget)
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
        
        print("ACCEPTING BEST SOLUTION:", best_map_value)
        
    else: # if worse, accept it with a probability
      delta = new_map_value - current_map_value
      probability = math.exp(delta / temp)

      if random.random() < probability:
        current_map = copy.deepcopy(new_map)
        current_map_value = new_map_value
        remaining_budget = new_budget

    solutions.append(current_map)
    
    temp *= cooling_rate * 0.8
    iteration += 1
    no_improvement_count += 1
    
    print("CURRENT SOLUTION:", current_map_value)
    
    if no_improvement_count >= max_no_improvement:
      break
    
    
  print("DIFFERENCE:", best_map_value - temporary)
  return best_map, best_map_value, solutions
