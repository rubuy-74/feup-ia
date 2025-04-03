import pygame

from models.map import Map
from models.cell import Cell

def draw_pixel(screen, x, y, color, size):
    pygame.draw.rect(screen, color, (x * size, y * size, size, size))

def draw_map(screen, m: Map, size):
    colors = {
        Cell.VOID: (255, 255, 255),
        Cell.WALL: (128, 128, 128),
        Cell.TARGET: (255, 255, 0),
        Cell.BACKBONE: (255, 0, 0),
    }

    for y in range(m.rows):
        for x in range(m.columns):
            cell_type = m.matrix[y, x]
            if cell_type in colors:
                draw_pixel(screen, x, y, colors[cell_type], size)
    
    pygame.display.flip()

def draw_solution(screen, m: Map, size):
    colors = {
        Cell.VOID: (255, 255, 255),
        Cell.WALL: (128, 128, 128),
        Cell.TARGET: (255, 255, 0),
        Cell.BACKBONE: (0, 0, 0),
        Cell.CONNECTED_ROUTER: (0, 0, 255),
        Cell.CABLE: (157, 0, 255),
        Cell.WIRED: (0, 255, 0),
    }

    coverage = set()

    for y in range(m.rows):
        for x in range(m.columns):
            
            if (y, x) == m.backbone:
                draw_pixel(screen, x, y, colors[Cell.BACKBONE], size)
                continue
            
            cell_type = m.matrix[y, x]
            
            if cell_type in colors:
                draw_pixel(screen, x, y, colors[cell_type], size)
                

    for coords in m.coverage:
        x, y = coords
        if m.matrix[x, y] != Cell.CONNECTED_ROUTER and m.matrix[x, y] != Cell.CABLE and (x,y) != m.backbone:
            draw_pixel(screen, y, x, colors[Cell.WIRED], size)
    
    pygame.display.flip()
