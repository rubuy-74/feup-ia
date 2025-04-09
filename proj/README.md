# IART 2025 - ROUTER PLACEMENT

## How to Run

Due to the implementation of configuration files, running any map with any algorithm is simpler.

In a configuration file, you can: 
- Set which map and algorithm you want to run.
- Set the probabilites of each operator of the mutation function.
- Set a budget constraint to the naive solution.
- Set the map size inside the GUI.

```yaml
algorithm: <name of the algorithm>
map: <name of the map>
size: 1
seed: <random integer>
probabilities:
  remove: <desired percentage (decimal)>
  add: <desired percentage (decimal)>
  nothing: <desired percentage (decimal)>
constraints:
  budget: <desired percentage (decimal)>
```
Any custom configuration file must be placed inside the <code>configs</code> folder.

It is important to state that the sum of the three probabilities (add, remove and nothing) must add to 1.

To start the program, run on the <code>src</code> directory:

<code>python3 main.py \<config name> </code>

After the command above, a new window will open with the choosen map and the algorithm will start running **indefinetly** (excl. simulated annealing).

To stop the execution, open the map window and press <code>Space</code>. The execution will stop and the last computed solution will be drawn and dumped into a file in the <code>output</code> folder, as well as a plot.



## The Approach
### Heuristics

Heuristics are employed to guide the search for better solutions. Some heuristics that we used to base off our solution are:
+ Coverage Maximization: Prioritize placing routers in positions which maximize the coverage.
+ Minimize Cost: Try to keep routers closer to the backbone to spend less on backbone cells.
+ Avoid walls: Ensure that the router placement algorithm do not position routers within walls, to maintain feasibility.

### Evaluation Function

The evaluation function is used to score potential solutions based on their effectiveness and cost. The function is defined by:

```math
\text{score} = 1000 \cdot t + \left( B - \left( N \cdot P_b + M \cdot P_r \right) \right)
```

t  - number of targeted cells \
B  - budget \
N  - Number of cells connected to backbone \
Pb - price of connecting one cell to the backbone \
M  -  Number of routers connected to backbone \
Pr - price of connecting a router to the backbone 

This function prioritizes the coverage over the price of the final solution. The contribution of the solution cost penalizes excessive resources.

### Operators:

+ **Mutation**: Randomly adjust the placement to explore new solutions.
  + Add: Add a router in a random position if the budget allows
  + Remove: Removes a random router and its associated path until an interception of connections.
+ **Crossover**: Combine two solutions to generate a new one.
  + Chooses a random square in one of the parents and copies all the routers inside of it from that parent to the other. All routers from the second are previously deleted, as their paths.
  + This approach allows the merge of the solutions with a limited amount of calculations for new paths, which simplifies the calculations. 

## Implemented Algorithms 

### BFS - Breadth-First Search

The *Breadth-First Search (BFS)* algorithm is used to find the shortest path from a router to the backbone in the grid. It ensures that routers are connected to the backbone while respecting the constraints of the problem.

#### Algorithm Flow:
1. *Initialization*:
   - Start from the given router's position (begin).
   - Initialize a queue to store cells to be visited and a visited matrix to track explored cells.
   - Use a parent matrix to keep track of the path from the router to the backbone.

2. *Exploration*:
   - While there are cells in the queue:
     - Dequeue the current cell and check if it is connected to the backbone, a cable, or another router.
     - If a connection is found, backtrack using the parent matrix to construct the path.

3. *Path Construction*:
   - If a valid path is found, return the path from the router to the backbone, excluding the router itself.
   - If no path is found, return None.

4. *Output*:
   - Return the shortest path from the router to the backbone or None if no valid path exists.

#### Key Features:
- *Shortest Path*: Ensures that the path from the router to the backbone is the shortest possible.
- *Constraint Handling*: Only explores valid cells (e.g., not walls or void cells).
- *Backtracking*: Uses the parent matrix to reconstruct the path once a connection is found.

---

### Greedy Solution (Naive Solution)

The *Naive Solution* is a greedy algorithm that places routers iteratively to maximize coverage while respecting the budget constraints. It uses a medial axis transformation to prioritize router placement in areas that maximize coverage with minimal cost.

#### Algorithm Flow:
1. *Initialization*:
   - Start with an empty grid and the full budget.
   - Identify all target cells that require coverage.
   - Compute the maximum number of routers that can be placed based on the budget and the price of a router.

2. *Medial Axis Transformation*:
   - Use the medial axis transformation to identify the most central points in the grid that maximize coverage.
   - Generate a list of potential router placement positions based on the transformation.

3. *Router Placement*:
   - Shuffle the list of potential positions to introduce randomness.
   - For each position:
     - Place a router at the position.
     - Attempt to connect the router to the backbone using a breadth-first search (BFS) algorithm.
     - If the connection is successful and within budget:
       - Update the grid to reflect the router and its connection.
       - Deduct the cost of the router and its connection from the remaining budget.
       - Update the coverage set with the cells covered by the router.
     - If the connection is not successful or exceeds the budget, revert the placement.

4. *Stopping Condition*:
   - Stop when the budget falls below a predefined threshold or all target cells are covered.

5. *Output*:
   - Return the final grid configuration, the remaining budget, and the total coverage achieved.

#### Key Features:
- *Greedy Placement*: Places routers in positions that maximize coverage based on the medial axis transformation.
- *Budget-Constrained*: Ensures that the total cost of routers and connections does not exceed the budget.
- *Breadth-First Search (BFS)*: Finds the shortest path to connect a router to the backbone.
- *Coverage Update*: Dynamically updates the set of covered cells after each router placement.

---

### HillClimb

The *HillClimb* algorithm is a local search heuristic that iteratively improves a solution by applying random mutations and greedily accepting only better solutions. It is designed to explore the solution space efficiently while maintaining simplicity.

#### Algorithm Flow:
1. *Initialization*:
   - Start with an initial map (m) and a given budget.
   - Create a deep copy of the map (temp) to track the best solution found so far.
   - Initialize an empty list to store accepted solutions for post-analysis.

2. *Mutation*:
   - Apply a random mutation to the map using weighted probabilities:
     - *Add* a router.
     - *Remove* a router.
     - *Do nothing*.
   - The mutation is performed using the mutation_func, which ensures that the changes respect the problem's constraints.

3. *Evaluation*:
   - Evaluate the mutated map (new_map) and compare its score with the current best map (temp).
   - If the mutated map has a better score, accept it as the new best solution and update temp.

4. *Exploration*:
   - Continue the search from the mutated map, even if it is worse than the current best. This allows the algorithm to explore the solution space more broadly.

5. *Stopping Condition*:
   - The algorithm runs indefinitely until an external stop condition is met (e.g., pressing the space key).

6. *Output*:
   - Return the best solution found (temp), the remaining budget, the list of accepted solutions, the number of iterations, and the total runtime.

#### Key Features:
- *Greedy Acceptance*: Only accepts solutions that improve the current best score.
- *Randomness*: Introduces randomness through mutations to explore the solution space.
- *Post-Analysis*: Records all accepted solutions for further analysis and debugging.
- *Flexible Stopping*: Allows external conditions to terminate the search, making it adaptable to different use cases.

---

### Simulated Annealing

The *Simulated Annealing* algorithm is a probabilistic optimization technique inspired by the annealing process in metallurgy. It explores the solution space by applying random mutations and accepts solutions based on a probability that decreases over time, allowing it to escape local optima and converge to a near-optimal solution.

#### Algorithm Flow:
1. *Initialization*:
   - Start with an initial map (current_map) and a given budget.
   - Set the initial temperature (temp) and define the cooling rate (cooling_rate).
   - Initialize the best solution (best_map) as a copy of the initial map and evaluate its score.

2. *Mutation*:
   - Apply a random mutation to the map using weighted probabilities:
     - *Add* a router.
     - *Remove* a router.
     - *Do nothing*.
   - The mutation is performed using the mutation_func, ensuring that the changes respect the problem's constraints.

3. *Evaluation*:
   - Evaluate the mutated map (new_map) and compare its score with the current map (current_map).
   - If the mutated map has a better score, accept it as the new current map.
   - If the mutated map is worse, accept it with a probability proportional to the temperature (exp(delta / temp)), where delta is the difference in scores.

4. *Update Best Solution*:
   - If the current map is better than the best solution found so far, update the best solution (best_map).

5. *Cooling*:
   - Decrease the temperature after each iteration using the cooling rate (temp *= cooling_rate).

6. *Stopping Condition*:
   - Stop when the temperature falls below a predefined threshold (stopping_temp), the maximum number of iterations without improvement is reached, or an external stop condition is triggered (e.g., pressing the space key).

7. *Output*:
   - Return the best solution found (best_map), its score, the list of solutions over iterations, the number of iterations, and the total runtime.

#### Key Features:
- *Probabilistic Acceptance*: Can accept worse solutions, enabling escape from local optima.
- *Cooling Schedule*: Gradually reduces the probability of accepting worse solutions as the algorithm progresses.
- *Exploration and Exploitation*: Balances exploration of the solution space and exploitation of promising areas.
- *Flexible Stopping*: Allows external conditions to terminate the search, making it adaptable to different use cases.

---

### Genetic Algorithm

The *Genetic Algorithm* is an evolutionary optimization technique inspired by natural selection. It evolves a population of solutions over generations by applying selection, crossover, and mutation operators. This approach balances exploration and exploitation to converge toward an optimal or near-optimal solution.

#### Algorithm Flow:
1. *Initialization*:
   - Generate an initial population of maps (population) using the naive algorithm, ensuring each solution respects the budget constraint.
   - Evaluate the fitness of each individual in the population using the evaluate method of the Map class.

2. *Selection*:
   - Select parents based on their fitness using a tournament selection strategy.
   - Ensure diversity by avoiding duplicate parents in the selection process.

3. *Crossover*:
   - Combine features of two parent solutions to create a child solution.
   - Use a defined crossover region (e.g., a square) to determine which routers and paths are inherited from each parent.
   - The crossover ensures that the child respects the problem's constraints and budget.

4. *Mutation*:
   - Apply random mutations to the child solution using the mutation_func function.
   - Mutations include adding, removing, or doing nothing to routers, ensuring the changes respect the budget and constraints.

5. *Evaluation*:
   - Evaluate the fitness of the new individuals (children) and select the best solutions to form the next generation.

6. *Stopping Condition*:
   - Stop when an external stop condition is triggered (e.g., pressing the space key).

7. *Output*:
   - Return the best solution found, its fitness score, the list of fitness values over generations, the number of iterations, and the total runtime.

#### Key Features:
- *Crossover and Mutation*: Introduce diversity to the population, enabling exploration of the solution space.
- *Selection*: Ensures that better solutions are more likely to be passed on to the next generation.
- *Fitness Tracking*: Continuously tracks and preserves the best solution found so far.
- *Population Evolution*: The population evolves over generations toward an optimal map configuration within budget constraints.
- *Flexible Stopping*: Can be stopped based on a custom condition.

## Parameterizations

The comparison between all the algorithms was made with two different parameterizations, both present in the already created configuration files:

```yaml
add: 0.6
remove: 0.2
nothing: 0.2
time: ~60s
```

and

```yaml
add: 0.5
remove: 0.3
nothing: 0.2
time: ~60s
```

Although not very different from one another, each parameterization changed significantly the behaviour of the algorithms, as stated in the plots.

Different budget constraints were also used, varying from map to map and algorithm to algorithm, but always between [0, 0.5, 0.7].

## Specification of the Problem

Typically, buildings are connected to the Internet using a fiber backbone. In order to provide wireless Internet access, wireless routers are placed around the building and connected using fiber cables to the backbone.

Given a building plan, the objective is to decide where to put wireless routers and how to connect them to the fiber backbone to maximize coverage and minimize cost (not surpassing the budget).

### Constraints

The problem is represented as a grid, where each cell can be either a wall cell, a target cell or a void cell. Target cells are cells in which we need to have wireless coverage and the void cells don't need to be covered.

Routers have a limited range and cannot be placed in wall cells. Backbones in the other hand can be placed anywhere on the grid.

### Solution Representation

+ A matrix representing the map. Each entry has a type, possibly being <code>[BACKBONE, VOID, WALL, TARGET, WIRED, ROUTER, CONNECTED_ROUTER, CABLE]</code>.
+ Score of the solution, computed using the formula above
+ Time spent on the algorithm execution
  + In the execution of the algorithms that need a initial solution, its computation time was not taking into account.
+ Number of iterations

### Data Structures

+ Matrix <code>[ndarray from numpy]</code>
+ Cell

## Related Work

These are related research and solutions to the problem at hand:

+ Principled Modeling of the Google Hash Code Problems for Meta-Heuristics
  + https://estudogeral.uc.pt/retrieve/265403/tese_final_pedro_rodrigues.pdf
+ Genetic algorithms and greedy-randomized adaptive search procedure for router placement problem in wireless networks
  + https://journals.sagepub.com/doi/full/10.3233/JHS-190616
+ Teams Gyrating Flibbittygibbitts solution
  + https://github.com/sbrodehl/HashCode
