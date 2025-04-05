import heapq
from time import process_time
import models.map as mapClass
import models.router as router
import models.solution as solution
import models.cell as cell
import utils as utils
import collections
import random
import algorithms.greedySolution as greedySolution
import menu.draw as draw

def a_star_router_search(m: mapClass.Map, routers: set[cell.Cell], start_cell: cell.Cell) -> tuple:
    def heuristic(cell1: cell.Cell, cell2: cell.Cell) -> float:
        return abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)

    priority_queue = [(0, start_cell, [])]
    visited = {start_cell}

    while priority_queue:
        priority, current_cell, path = heapq.heappop(priority_queue)

        if not m.isWall(current_cell) and not m.isBackbone(current_cell) and not m.isWired(current_cell) and not m.isVoid(current_cell) and current_cell not in routers:
            return current_cell, path

        for adj in current_cell.adjacents():
            if 0 <= adj.x < m.columns and 0 <= adj.y < m.rows and adj not in visited:
                visited.add(adj)
                new_path = path + [adj]
                priority = len(new_path) + heuristic(adj, start_cell)
                heapq.heappush(priority_queue, (priority, adj, new_path))

    return None, []

def initialize_solution(m: mapClass.Map) -> solution.Solution:
    """ Initialize a solution. """

    return greedySolution.greedySolution(m)

def tabu_search_solution(size, screen, m: mapClass.Map, max_iterations: int = 100, tabu_tenure: int = 10, initial_solution: solution.Solution = None, seed: int = None) -> solution.Solution:

    if seed is not None:
        random.seed(seed)

    if initial_solution is None:
        # Alter the solution to random or premade solution or other
        current_solution = initialize_solution(m)
        draw.draw_solution(screen, m, current_solution, size)

    else:
        current_solution = initial_solution

    best_solution = current_solution
    best_value = m.evaluate(current_solution)
    tabu_list = collections.deque(maxlen=tabu_tenure)

    time_start = process_time()

    # Start iteration
    for iteration in range(max_iterations):
        print(f"Iteration {iteration + 1}/{max_iterations}")  # Print iteration count
        new_solution = modify_solution(m, current_solution, tabu_list)
        new_value = m.evaluate(new_solution)

        if new_value > best_value:
            best_value = new_value
            best_solution = new_solution

        tabu_list.append(current_solution)
        current_solution = new_solution

        ## Brute forced values for testing purposes for now
        draw.draw_solution_shift(screen, m, best_solution, size)  # Update the visualization at each iteration

    time_end = process_time()
    print("TIME:", time_end - time_start)

    return best_solution

def modify_solution(m: mapClass.Map, current_solution: solution.Solution, tabu_list) -> solution.Solution:
    """ Modify the current solution by ensuring routers are placed in different cells while ensuring feasibility. """

    new_solution = solution.Solution(
        backbone_cells=current_solution.backbone_cells.copy(),
        routers=current_solution.routers.copy()
    )

    if new_solution.routers:
        # Randomly pick one router to move
        removed_router = random.choice(list(new_solution.routers))

        # Ensure we pick a valid new router position (not in tabu list, not the same position, and not a restricted area)
        new_router_cell, path = None, None
        for _ in range(10):  # Try up to 10 times to find a valid new position
            router_cells = set()
            for r in new_solution.routers:
                router_cells.add(r.cell)
            new_router_cell, path = a_star_router_search(m, router_cells, removed_router.cell)

            if new_router_cell and new_router_cell != removed_router and \
               new_router_cell not in tabu_list and \
               not m.isWall(new_router_cell) and \
               not m.isBackbone(new_router_cell) and \
               not m.isWired(new_router_cell) and \
               not m.isVoid(new_router_cell):
                break

        # If we found a valid new position, update the solution
        if new_router_cell:
            new_solution.routers.remove(removed_router)
            new_solution.routers.add(router.Router(new_router_cell, m.rRange, m.rtPrice, m.computeRouterTargets(new_router_cell)))
            new_solution.backbone_cells[new_router_cell] = path

    return new_solution
