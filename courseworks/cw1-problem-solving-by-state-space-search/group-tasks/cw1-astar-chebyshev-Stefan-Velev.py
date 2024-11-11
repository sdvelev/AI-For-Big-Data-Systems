import math
import pygame
from timeit import default_timer as timer
from queue import PriorityQueue


COLOUR_EMPTY_NODE = (176, 192, 238)
COLOUR_BORDERS = (0, 0, 0)
BORDER_THICKNESS = 2
COLOUR_START_NODE = (156, 216, 142)
COLOUR_END_NODE = (17, 111, 45)
COLOUR_OBSTACLE = (255, 0, 0)
COLOUR_VISITED_PATH = (255, 218, 149)
COLOUR_EXPANDED_PATH = (194, 147, 3)
COLOUR_SOLUTION_PATH = (59, 234, 19)

WIDTH = 700

ROWS = 5
COLS = 6

ANIMATION_TIME_MILLISECONDS = 600

pygame.display.set_caption("Problem Solving by State Space Search: A* (Chebyshev distance)")
win = pygame.display.set_mode((WIDTH, WIDTH))
clock = pygame.time.Clock()

class Node:
    def __init__(self, row, col, width, height, total_rows, total_cols):
        self.row = row
        self.col = col

        self.width = width
        self.height = height

        self.total_rows = total_rows
        self.total_cols = total_cols

        self.x = row * width
        self.y = col * height

        self.colour = COLOUR_EMPTY_NODE

        self.neighbours = []

    def get_pos_index(self):
        return self.row, self.col

    def expand(self):
        self.colour = COLOUR_EXPANDED_PATH

    def visit(self):
        self.colour = COLOUR_VISITED_PATH

    def make_obstacle(self):
        self.colour = COLOUR_OBSTACLE

    def make_start_node(self):
        self.colour = COLOUR_START_NODE

    def make_end_node(self):
        self.colour = COLOUR_END_NODE

    def make_solution_path(self):
        self.colour = COLOUR_SOLUTION_PATH

    def is_obstacle(self):
        return self.colour == COLOUR_OBSTACLE

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

    def update_neighbours(self, grid):
        self.neighbours = []

        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_obstacle():
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():
            self.neighbours.append(grid[self.row][self.col - 1])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle():
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():
            self.neighbours.append(grid[self.row - 1][self.col])

    def __lt__(self, other):
        return self.row < other.row

def chebyshev_distance(start, goal):
    x1, y1 = start
    x2, y2 = goal
    return max(abs(x2 - x1), abs(y2 - y1))

def reconstruct_path(parent_of, current, draw, start_time, max_frontier_size):
    path_count = 0

    while current in parent_of:
        current = parent_of[current]
        current.make_solution_path()
        path_count += 1
        draw()
    end_time = timer()
    working_time = end_time - start_time
    pygame.display.set_caption(f'Time of A* Algorithm (Chebyshev distance): {format(working_time, ".2f")}s | '
                               f'Solution: {path_count + 1} nodes | '
                               f'Max size of frontier: {max_frontier_size}')


def a_star(draw, grid, start_node, end_node, start_time):
    frontier = PriorityQueue()
    insertion_counter = 0
    frontier.put((0, insertion_counter, start_node))
    max_frontier_size = 1
    parent_of = {}
    g_score = {current_neighbour: float("inf") for row in grid for current_neighbour in row}
    g_score[start_node] = 0

    f_score = {current_neighbour: float("inf") for row in grid for current_neighbour in row}
    f_score[start_node] = chebyshev_distance(start_node.get_pos_index(), end_node.get_pos_index())


    frontier_set = {start_node}
    while not frontier.empty():
        current_node = frontier.get()[2]
        frontier_set.remove(current_node)

        if current_node != start_node:
            current_node.expand()

        if current_node == end_node:
            reconstruct_path(parent_of, end_node, draw, start_time, max_frontier_size)
            return True

        for neighbour in current_node.neighbours:
            current_g_score = g_score[current_node] + 1

            if current_g_score < g_score[neighbour]:
                parent_of[neighbour] = current_node
                g_score[neighbour] = current_g_score
                f_score[neighbour] = current_g_score + chebyshev_distance(neighbour.get_pos_index(),
                                                                          end_node.get_pos_index())
                if neighbour not in frontier_set:
                    insertion_counter += 1
                    frontier.put((f_score[neighbour], insertion_counter, neighbour))
                    frontier_set.add(neighbour)
                    max_frontier_size = max(max_frontier_size, frontier.qsize())
                    neighbour.visit()

        draw()
        pygame.display.update()
        pygame.time.delay(ANIMATION_TIME_MILLISECONDS)

    return False


def make_grid(rows, cols, total_width):
    grid = []
    height = total_width // rows
    width = total_width // cols
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            current_node = Node(i, j, height, width, rows, cols)
            grid[i].append(current_node)

    return grid

def draw_grid(win, rows, cols, total_width):
    row_height = total_width // rows
    col_width = total_width // cols

    for i in range(rows + 1):
        pygame.draw.line(win, COLOUR_BORDERS, (0, i * col_width), (total_width, i * col_width),
                         width = BORDER_THICKNESS)

    for j in range(cols + 1):
        pygame.draw.line(win, COLOUR_BORDERS, (j * row_height, 0), (j * row_height, total_width),
                         width = BORDER_THICKNESS)


def draw(win, grid, rows, cols, width):
    for row in grid:
        for current_node in row:
            current_node.draw(win)

    draw_grid(win, rows, cols, width)
    pygame.display.update()

def create_obstacles(grid):
    grid[1][0].make_obstacle()
    grid[1][2].make_obstacle()
    grid[3][2].make_obstacle()
    grid[1][3].make_obstacle()
    grid[4][3].make_obstacle()
    grid[4][4].make_obstacle()

def main(win, width):
    grid = make_grid(COLS, ROWS, width)

    algorithm_started = False
    is_running = True
    while is_running:
        draw(win, grid, COLS, ROWS, width)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                is_running = False

            start_node = grid[0][0]
            end_node = grid[-1][-1]

            start_node.make_start_node()
            end_node.make_end_node()

            create_obstacles(grid)

            if e.type == pygame.KEYDOWN and not algorithm_started:
                algorithm_started = True
                counter_start = timer()
                pygame.display.set_caption("Searching for a Solution with A* (Chebyshev distance) ...")
                for row in grid:
                    for current_node in row:
                        current_node.update_neighbours(grid)

                a_star(lambda: draw(win, grid, COLS, ROWS, width), grid, start_node, end_node, counter_start)

    pygame.quit()


main(win, WIDTH)