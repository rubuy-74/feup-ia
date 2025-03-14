import sys
import pygame
import ctypes
import utils as utils
import algorithms.randomSolution as randomSolution
import algorithms.greedySolution as greedySolution

""" def find_nearest_available_cell_to_router(map: Map, routers: list):
  queue = collections.deque([map.backbone.cell])
  visited = set()
  visited.add(map.backbone.cell)
  while queue:
    possible_cell = queue.popleft()

    if not is_wall(possible_cell, map) and not is_backbone(possible_cell, map) and not is_wired(possible_cell, map) and not is_void(possible_cell, map) and possible_cell not in routers:
      return possible_cell
    
    for adj in adjacents(possible_cell):
      if 0 <= adj.x < map.rows and 0 <= adj.y < map.columns and adj not in visited:
        visited.add(adj)
        queue.append(adj)
  
  return None """

""" def compute_targets(map: Map, router: Router):
  targets = set()
  range_ = router.range_
  rx, ry = router.cell.x, router.cell.y

  for x in range(max(0, rx - range_), min(map.rows, rx + range_ + 1)):
    for y in range(max(0, ry - range_), min(map.columns, ry + range_ + 1)):
      if abs(rx - x) <= range_ and abs(ry - y) <= range_:
        if not any(is_wall(Cell(w, v), map) for w in range(min(rx, x), max(rx, x)) for v in range(min(ry, y), max(ry, y))):
          possible_target = Cell(x, y)
          
          if is_target(possible_target, map):
            targets.add(possible_target)

  return targets """

""" 
def greedy(map: Map, router_cost, router_range):
  solution = Solution([], 0, set())

  while True:
    # find the closest available cell of the backbone to place a router
    cell_to_router = find_nearest_available_cell_to_router(map, [router.cell for router in solution.routers])

    if(cell_to_router is None):
      break

    # create the router
    router = routerClass.Router(cell_to_router, router_cost, router_range)
    
    # find the shortest path between the router and the backbone
    path = bfs.bfs(map, map.backbone.cell, router.cell)

    # update cost
    new_cost = solution.cost + router_cost + map.backbone.cost * (len(path)-1)

    if new_cost <= map.budget:
      solution.cost = new_cost
      solution.routers.append(router)
      solution.fiber.update(path)

      # update targets based on the new router
      map.wired.update(compute_targets(map, router))

      # update the backbone connections
      map.backbone.connected_to.extend(path)
    else:
      break
   
  return solution
 """

def main():
  pygame.init()

  map = None
  state = 'MENU'
  title_text = 'Hello, choose the file!'
  texts = ['Simple Example', 'Charleston Road', 'Lets Go Higher', 'Opera', 'Rue De Londres']
  file_options = ['example.in', 'charleston_road.in', 'lets_go_higher.in', 'opera.in', 'rue_de_londres.in']
  algorithms = ['Random', 'Greedy', 'Hill Climbing', 'Simulated Annealing', 'Tabu Search', 'Genetic Algorithm']


  choice_map = 0

  choice_alg = 0

  font = pygame.font.SysFont(None, 55)

  screen = pygame.display.set_mode((1000, 900))
  pygame.display.set_caption('Router Placement')

  hwnd = pygame.display.get_wm_info()['window']

  # Move the window to the top-left corner
  ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0)


  title = font.render(title_text, True, (255, 255, 255))

  running = True
  while running:
    for event in pygame.event.get():
      if state == 'MENU':
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False
          elif event.key == pygame.K_DOWN:
            choice_map = (choice_map + 1) % len(texts)
          elif event.key == pygame.K_UP:
            choice_map = (choice_map - 1) % len(texts)
          elif event.key == pygame.K_RETURN:
            path = "../maps/"+file_options[choice_map]
            map = utils.parse(path)
            state = 'ALGCHOICE'
      elif state == 'ALGCHOICE':
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            state = 'MENU'
          elif event.key == pygame.K_DOWN:
            choice_alg = (choice_alg + 1) % len(algorithms)
          elif event.key == pygame.K_UP:
            choice_alg = (choice_alg - 1) % len(algorithms)
          elif event.key == pygame.K_RETURN:
            state = 'ALGORITHM'
      elif state == 'ALGORITHM':
        if(choice_alg == 0):
          solRandom = randomSolution.randomSolution(map)
          print(map.evaluate(solRandom))
          running = False
        elif(choice_alg == 1):
          solGreedy = greedySolution.greedySolution(map)
          print(map.evaluate(solGreedy))
          running = False
        else:
          state = 'NOT_IMPLEMENTED'
      elif state == 'NOT_IMPLEMENTED':
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            state = 'ALGCHOICE'

    
    # print(solGreedy)
    if state == 'MENU':
        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the title on the screen
        screen.blit(title, (10, 50))

        # Draw the options on the screen
        y = 150
        for i, text in enumerate(texts):
            color = (255, 255, 255) if i != choice_map else (255, 0, 0)
            rendered_text = font.render(text, True, color)
            screen.blit(rendered_text, (10, y))
            y += 60  # Adjust the y position for the next text

        # Update the display
        pygame.display.flip()

    elif state == 'ALGCHOICE':
        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the title on the screen
        screen.blit(title, (10, 50))

        # Draw the options on the screen
        y = 150
        for i, text in enumerate(algorithms):
            color = (255, 255, 255) if i != choice_alg else (255, 0, 0)
            rendered_text = font.render(text, True, color)
            screen.blit(rendered_text, (10, y))
            y += 60  # Adjust the y position for the next text

        # Update the display
        pygame.display.flip()
    
    elif state == 'NOT_IMPLEMENTED':
      screen.fill((0, 0, 0))
      text = font.render('Not implemented yet', True, (255, 0, 0))
      screen.blit(text, (10, 50))
      pygame.display.flip()
        


if __name__ == "__main__":
  main()
