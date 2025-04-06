from algorithms.naive import naive, connect_to_backbone
from algorithms.functions import mutation_func
from models.map import Map
from models.cell import Cell
from random import sample, choice
from operators.add import bfs_until_interception
import numpy as np
from tqdm import tqdm
import copy
from utils import computeAdjacents
import time

def genetic(m: Map, population_size = 10, mutation_rate = 0.01, crossover_square = 15, stop_condition=None):
  population = create_population(m, population_size)
  solutions = []
  it = 0

  start = time.time() 
  while True:
    if stop_condition and stop_condition():
      print("Stopping due to external condition")
      break
    it += 1
    fitnesses = [pop.evaluate(rem_budget) for (pop, rem_budget) in population]
    
    best_fitness = max(fitnesses)
    best_individual = population[fitnesses.index(best_fitness)]
    solutions.append(best_fitness)

    parents = selection(population, fitnesses)
    next_generation = []
    
    while len(next_generation) < population_size:
      father = choice(parents)
      mother = choice(parents)
      
      if father != mother:
        bob = crossover(father, mother, crossover_square)
        new_map, new_budget, _ = mutation_func(bob[0], bob[1])
        next_generation.extend([(new_map, new_budget)])
        
        if len(next_generation) > population_size:
          next_generation = next_generation[:population_size]
        
    population = next_generation
  
  best_fitness = max(fitnesses)
  best_individual = population[fitnesses.index(best_fitness)]
  solutions.append(best_fitness)
  
  rts = np.argwhere(best_individual[0].matrix == Cell.CONNECTED_ROUTER)
  
  pbar2 = tqdm(range(len(rts)), desc="Updating coverage")
  
  new_coverage = set()
  
  for rt in rts:
    new_coverage.update(best_individual[0].computeRouterTargets(rt))
    pbar2.update()
  
  pbar2.close()
  
  best_individual[0].coverage = new_coverage
  
  return best_individual,solutions, it, time.time() - start
  
  
def create_population(m: Map, size: int):
  (base_solution, remaining_budget) = naive(copy.deepcopy(m),True)
  population = [(base_solution,remaining_budget)]
  for i in range(size-1):
    rb = remaining_budget
    mutated = copy.deepcopy(base_solution)
    for j in range(100):
      (mutated, rb,_) = mutation_func(mutated,rb)
      print(str(j)+": " + str(mutated.evaluate(rb)))
    population.append((mutated,rb))
    print(str(i)+": " + str(list(map(lambda x: x[0].evaluate(x[1]),population))))

  return population

def selection(population: list, fitnesses: list):
  parents = []
  selected_parents = set()
  
  while len(parents) < 3:
    candidates_pool = 3
    candidates = sample(list(zip(population, fitnesses)), candidates_pool)
    best_candidate = max(candidates, key = lambda item: item[1])[0]
    
    if best_candidate not in selected_parents:
      parents.append(best_candidate)
      selected_parents.add(best_candidate)
    
  return parents

def crossover(father: tuple, mother: tuple, crossover_square: int):
  x, y = choice(np.argwhere(father[0].matrix == Cell.CONNECTED_ROUTER))
  
  x_start, x_end = x, min(x + crossover_square, father[0].rows - 1)
  y_start, y_end = y, min(y + crossover_square, father[0].columns - 1)
  
  routers_in_square = set()
  
  # (map, budget)
  child = copy.deepcopy(mother)
  new_budget = child[1]
    
  for i in range(x_start, x_end):
    for j in range(y_start, y_end):
      modified_cell = child[0].matrix[i, j]
      if modified_cell == Cell.CONNECTED_ROUTER:
        adjs = computeAdjacents((i,j))
        connected_adjs = list(filter(lambda x: child[0].isCable(x) or child[0].isBackBone(x) or child[0].isRouter(x), adjs))
        
        if len(connected_adjs) >= 2:
          child[0].matrix[i, j] = Cell.CABLE
          new_budget += child[0].rtPrice - child[0].bbPrice
        else:
          new_budget += child[0].rtPrice
          path_until_interception = bfs_until_interception(child[0], (i, j))
          
          for cell in path_until_interception[:-1]:
            if child[0].original[cell] != Cell.WALL:
              if child[0].matrix[cell] == Cell.ROUTER:
                new_budget += child[0].rtPrice
              elif child[0].matrix[cell] == Cell.CABLE:
                new_budget += child[0].bbPrice
              child[0].matrix[cell] = Cell.TARGET
            else:
              new_budget += child[0].bbPrice
              child[0].matrix[cell] = Cell.WALL
  
  additional_routers = 0
  
  for i in range(x_start, x_end):
    for j in range(y_start, y_end):
      if father[0].matrix[i, j] == Cell.CONNECTED_ROUTER:
        if new_budget - child[0].rtPrice * (additional_routers + 1) >= 0:
          routers_in_square.add(((i, j), child[0].matrix[i, j]))
          child[0].matrix[i, j] = Cell.ROUTER
          additional_routers += 1
        else:
          child[0].matrix[i, j] = Cell.TARGET
      
  child = (child[0], new_budget)
  
  for router, old_cell in routers_in_square:
    updated_map, passed_budget, cost = connect_to_backbone(child[0], router, child[1])
    
    if not passed_budget:
      child[0].matrix[router] = old_cell
      child = (child[0], child[1] + child[0].rtPrice)
      continue
      
    child = (updated_map, child[1] - cost)
    
  print(child[1])
      
  return child