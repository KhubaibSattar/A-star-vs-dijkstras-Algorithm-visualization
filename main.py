import pygame
from enum import IntEnum
import numpy as np
from dijkstra import dijkstra
from astar import a_star
from colors import *

# Initialize pygame
pygame.init()

GRID_SIZE = (10, 10)
BLOCK_SIZE = 30
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
GRID_START_X = 100
GRID_START_Y = 100

# Create a screen
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
grid = np.zeros(GRID_SIZE)


def create_rect(x, y, color):
    pygame.draw.rect(SCREEN, color, [x, y, BLOCK_SIZE, BLOCK_SIZE])


class GridBlock(IntEnum):
    EMPTY = 0
    START = 1
    END = 2
    OBSTACLE = 3
    VISITED_DIJKSTRA = 4
    VISITED_ASTAR = 5


def visualize_grid():
    y = GRID_START_Y
    for row in grid:
        x = GRID_START_X
        for item in row:
            if item == GridBlock.EMPTY:
                create_rect(x, y, WHITE)
            if item == GridBlock.START:
                create_rect(x, y, GREEN)
            if item == GridBlock.END:
                create_rect(x, y, GREEN)
            if item == GridBlock.OBSTACLE:
                create_rect(x, y, RED)
            if item == GridBlock.VISITED_DIJKSTRA:
                create_rect(x, y, PINK)
            if item == GridBlock.VISITED_ASTAR:
                create_rect(x, y, ORANGE)
            x += BLOCK_SIZE + 10
        y += BLOCK_SIZE + 10


selecting_start_cell = False
selecting_end_cell = False
selecting_obstacle_cells = False
started_to_find_path = False

start_cell = None
end_cell = None
obstacle_cells = []

running = True


class Rect:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.rect(SCREEN, self.color,
                         [self.x, self.y, self.width, self.height])

    def is_clicked(self, mouse_pos):
        return self.x <= mouse_pos[
            0] <= self.x + self.width and self.y <= mouse_pos[
                1] <= self.y + self.height


class Text:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        font = pygame.font.Font(pygame.font.get_default_font(), 15)
        text = font.render(self.text, True, self.color)
        textRect = text.get_rect()
        textRect.center = (self.x, self.y)
        SCREEN.blit(text, textRect)


reset_button = Rect(20, 20, 70, 30, WHITE)
start_cell_button = Rect(120, 20, 70, 30, GREEN)
end_cell_button = Rect(220, 20, 70, 30, GREEN)
obstacle_button = Rect(320, 20, 70, 30, RED)
dijkstra_button = Rect(420, 20, 70, 30, PINK)
astar_button = Rect(520, 20, 70, 30, ORANGE)

reset_text = Text('Reset', 55, 35, BLACK)
start_cell_text = Text('Start', 155, 35, BLACK)
end_cell_text = Text('End', 255, 35, BLACK)
obstacle_text = Text('Obstacle', 355, 35, BLACK)
dijkstra_text = Text('Dijkstra', 455, 35, BLACK)
astar_text = Text('A*', 555, 35, BLACK)

# Game loop
while running:

    # Change Obstacle button color
    obstacle_button.color = YELLOW if selecting_obstacle_cells else RED

    started_to_find_path = start_cell is not None and end_cell is not None and not selecting_start_cell and not selecting_end_cell and not selecting_obstacle_cells
    dijkstra_button.color = PINK if started_to_find_path else BLACK
    astar_button.color = ORANGE if started_to_find_path else BLACK

    # Draw Rects
    reset_button.draw()
    start_cell_button.draw()
    end_cell_button.draw()
    obstacle_button.draw()
    dijkstra_button.draw()
    astar_button.draw()

    # Draw texts
    reset_text.draw()
    start_cell_text.draw()
    end_cell_text.draw()
    obstacle_text.draw()
    dijkstra_text.draw()
    astar_text.draw()

    visualize_grid()

    # Loop through the events
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            y = GRID_START_Y
            row_num = 0
            for row in grid:
                col_num = 0
                x = GRID_START_X
                for item in row:
                    if x <= mouse_x <= x + BLOCK_SIZE and y <= mouse_y <= y + BLOCK_SIZE:
                        if selecting_start_cell:
                            start_cell = (row_num, col_num)
                            grid[row_num, col_num] = 1
                            selecting_start_cell = False
                        elif selecting_end_cell:
                            end_cell = (row_num, col_num)
                            grid[row_num, col_num] = 2
                            selecting_end_cell = False
                        elif selecting_obstacle_cells:
                            obstacle_cells.append((row_num, col_num))
                            grid[row_num, col_num] = 3
                    col_num += 1
                    x += BLOCK_SIZE + 10
                row_num += 1
                y += BLOCK_SIZE + 10

            # select reset cell
            if reset_button.is_clicked(event.pos):
                grid = np.zeros(GRID_SIZE)
                start_cell = None
                end_cell = None
                obstacle_cells = []

            # select start cell
            if start_cell_button.is_clicked(event.pos):
                selecting_start_cell = True
                selecting_end_cell = False
                selecting_obstacle_cells = False

            # select end cell
            if end_cell_button.is_clicked(event.pos):
                selecting_start_cell = False
                selecting_end_cell = True
                selecting_obstacle_cells = False

            # select obstacle cells
            if obstacle_button.is_clicked(event.pos):
                selecting_start_cell = False
                selecting_end_cell = False
                selecting_obstacle_cells = not selecting_obstacle_cells

            # run dijkstra
            if dijkstra_button.is_clicked(event.pos):
                if not selecting_start_cell and not selecting_obstacle_cells and not selecting_end_cell:
                    grid = np.zeros(GRID_SIZE)
                    grid[start_cell] = GridBlock.START
                    grid[end_cell] = GridBlock.END
                    for x, y in obstacle_cells:
                        grid[x][y] = GridBlock.OBSTACLE
                    path = dijkstra(grid, start_cell, end_cell, obstacle_cells)
                    for x, y in path:
                        grid[x][y] = GridBlock.VISITED_DIJKSTRA

            # run A*
            if astar_button.is_clicked(event.pos):
                if not selecting_start_cell and not selecting_obstacle_cells and not selecting_end_cell:
                    grid = np.zeros(GRID_SIZE)
                    grid[start_cell] = GridBlock.START
                    grid[end_cell] = GridBlock.END
                    for x, y in obstacle_cells:
                        grid[x][y] = GridBlock.OBSTACLE
                    path = a_star(grid, start_cell, end_cell, obstacle_cells)
                    for x, y in path:
                        grid[x][y] = GridBlock.VISITED_ASTAR

        # Check for QUIT event; if QUIT, set running to false
        if event.type == pygame.QUIT:
            running = False

        # Check for KEYDOWN event; KEYDOWN is a constant defined in pygame.locals, which we imported earlier
        if event.type == pygame.KEYDOWN:
            # If the Esc key has been pressed set running to false to exit the main loop
            if event.key == pygame.K_ESCAPE:
                running = False

    pygame.display.update()

# Done! Time to quit.
pygame.quit()