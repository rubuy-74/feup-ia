import sys
import pygame
import time
import yaml

import utils
import algorithms.randomSolution as randomSolution
import algorithms.greedySolution as greedySolution
import menu.draw as draw
import menu.ui as ui
import models.map as mapClass
import algorithms.tabuSearch as tabuSearch

# Game States
STATE_MENU = 'MENU'
STATE_ALG_CHOICE = 'ALGCHOICE'
STATE_ALGORITHM = 'ALGORITHM'
STATE_NOT_IMPLEMENTED = 'NOT_IMPLEMENTED'
STATE_FROZEN = 'FROZEN'
STATE_SEED = 'SEED'

class RouterPlacementGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1500, 900))
        pygame.display.set_caption('Router Placement')

        # Game configuration
        self.config = self.load_config('../configs/default.yaml')
        self.config['seed'] = int(time.time() * 1e9)
        self.config['seed'] = 1743888341484183296  # For testing purposes, set a fixed seed
        self.seed_input = ""

        # State variables
        self.state = STATE_MENU
        self.choice_map = 0
        self.choice_alg = 0
        self.font = pygame.font.SysFont(None, 55)

        # Define options
        self.texts = ['Simple Example', 'Charleston Road', 'Lets Go Higher', 'Opera', 'Rue De Londres']
        self.file_options = ['example.in', 'charleston_road.in', 'lets_go_higher.in', 'opera.in', 'rue_de_londres.in']
        self.algorithms = ['Random', 'Greedy', 'Hill Climbing', 'Simulated Annealing', 'Tabu Search', 'Genetic Algorithm']
        self.algorithms_config = ['random', 'greedy', 'hill_climbing', 'simulated_annealing', 'tabu_search', 'genetic_algorithm']

        # Load config if argument is provided
        if len(sys.argv) > 1:
            self.config = self.load_config(f"../configs/{sys.argv[1]}")
            self.state = STATE_ALGORITHM

    def load_config(self, config_file):
        with open(config_file) as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                self.handle_event(event)

            ui.display(self.screen, self.state, self.font.render('Choose Config', True, (255, 255, 255)), 
                       self.font, self.texts, self.choice_map, self.algorithms, self.choice_alg, self.seed_input)

    def handle_event(self, event):
        if self.state == STATE_MENU:
            self.handle_menu_event(event)
        elif self.state == STATE_ALG_CHOICE:
            self.handle_algorithm_choice_event(event)
        elif self.state == STATE_SEED:
            self.handle_seed_event(event)
        elif self.state == STATE_ALGORITHM:
            self.execute_algorithm()
        elif self.state == STATE_NOT_IMPLEMENTED:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = STATE_ALG_CHOICE

    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.choice_map = (self.choice_map + 1) % len(self.texts)
            elif event.key == pygame.K_UP:
                self.choice_map = (self.choice_map - 1) % len(self.texts)
            elif event.key == pygame.K_RETURN:
                pygame.display.set_caption(f'Router Placement - {self.texts[self.choice_map]}')
                self.config['size'] = 30 if self.choice_map == 0 else 2 if self.choice_map == 1 else 1
                self.config['map'] = f"{self.file_options[self.choice_map]}"
                self.state = STATE_ALG_CHOICE

    def handle_algorithm_choice_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.choice_alg = (self.choice_alg + 1) % len(self.algorithms)
            elif event.key == pygame.K_UP:
                self.choice_alg = (self.choice_alg - 1) % len(self.algorithms)
            elif event.key == pygame.K_RETURN:
                self.config['algorithm'] = self.algorithms_config[self.choice_alg]
                pygame.display.set_caption(f'Router Placement - {self.texts[self.choice_map]} - {self.algorithms[self.choice_alg]}')
                self.screen.fill((0, 0, 0))
                pygame.display.flip()
                self.state = STATE_SEED

    def handle_seed_event(self, event):
        if not hasattr(self, 'seed_input'):
            self.seed_input = ""

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.seed_input.isdigit():
                    self.config['seed'] = int(self.seed_input)
                self.state = STATE_ALGORITHM
            elif event.key == pygame.K_ESCAPE:
                self.state = STATE_ALG_CHOICE
            elif event.key == pygame.K_BACKSPACE:
                self.seed_input = self.seed_input[:-1]  # Remove the last digit
            elif event.unicode.isdigit():
                self.seed_input += event.unicode  # Add the pressed digit to the seed

    def execute_algorithm(self):
        m = utils.parse("../maps/" + self.config['map'])


        self.screen.fill((0, 0, 0))
        sol = None
        draw.draw_map(self.screen, m, self.config['size'])

        if self.config['algorithm'] == 'random':
            sol = randomSolution.randomSolution(m, self.config['seed'])
        elif self.config['algorithm'] == 'greedy':
            sol = greedySolution.greedySolution(m)
        elif self.config['algorithm'] == 'tabu_search':
            sol = tabuSearch.tabu_search_solution(self.config['size'], self.screen, m, max_iterations=100, tabu_tenure=10, seed=self.config['seed'])      
        else:
            self.state = STATE_NOT_IMPLEMENTED
            return

        if sol:
            if self.config['algorithm'] == 'tabu_search':
                draw.draw_solution_shift(self.screen, m, sol, self.config['size'])
            else:
                draw.draw_solution(self.screen, m, sol, self.config['size']) 

        print(f"Seed: {self.config['seed']}")
        self.state = STATE_FROZEN


if __name__ == "__main__":
    game = RouterPlacementGame()
    game.run()
