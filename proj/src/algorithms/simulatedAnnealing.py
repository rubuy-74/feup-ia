from algorithms.randomSolution import randomSolution
from algorithms.functions import mutation_func
from models.map import Map
from models.solution import Solution
import math
import random

def simulated_annealing(m: Map, initial_temp=1000, cooling_rate=0.995, stopping_temp=1e-8, max_iterations=10000):
  solutions = []

  # Create initial solution
  current_solution : Solution = randomSolution(m)
  best_solution = current_solution
  best_solution_value = m.evaluate(current_solution)

  # Auxiliary variables
  temp = initial_temp
  iteration = 0
  num_repetitions = 100

  while temp > stopping_temp and iteration < max_iterations:
    # Create mutated solution
    new_solution = mutation_func(m,current_solution)
    current_solution_value = m.evaluate(current_solution)
    new_solution_value = m.evaluate(new_solution)
    
    # if better accept it
    if(num_repetitions == 0): # TODO: Repeat if reaches a stop point
      return best_solution,best_solution_value,solutions
    if(current_solution == best_solution):
      num_repetitions -= 1

    if new_solution_value > current_solution_value:
      current_solution = new_solution
      current_solution_value = new_solution_value

      if current_solution_value > best_solution_value:
        best_solution = new_solution
        best_solution_value = current_solution_value
    else: # if worse, accept it with a probability
      delta = current_solution_value - new_solution_value
      probability = math.exp(-delta/temp)

      if random.random() < probability:
        current_solution = new_solution
        current_solution_value = new_solution_value

    solutions.append(current_solution)
    print(current_solution_value)
    temp *= cooling_rate
    iteration += 1
  return best_solution,best_solution_value,solutions
