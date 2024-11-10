import pygame, os
from timeit import default_timer as timer
from queue import PriorityQueue


pygame.display.set_caption("Problem Solving by State Space Search")
WIDTH = 700
win = pygame.display.set_mode((WIDTH, WIDTH))
clock = pygame.time.Clock()

COLOUR_EMPTY_NODE = (176, 192, 238)
COLOUR_BORDERS = (0, 0, 0)
BORDER_THICKNESS = 2
COLOUR_START_NODE = (156, 216, 142)
COLOUR_END_NODE = (66, 149, 47)
COLOUR_BOUNDARY = (255, 0, 0)
COLOUR_VISITED_PATH = (255, 218, 149)
COLOUR_EXPLORED_PATH = (194, 147, 3)
COLOUR_SOLUTION_PATH = (7, 162, 219)


class Node:
    def __init__(self, row, col, width, height, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * height
        self.colour = COLOUR_EMPTY_NODE
        self.neighbours = []
        self.width = width
        self.height = height
        self.total_rows = total_rows
        self.total_cols = total_cols

    def get_pos(self):
        return self.row, self.col

    def reset(self):
        self.colour = COLOUR_EMPTY_NODE

    def make_close(self):
        self.colour = COLOUR_EXPLORED_PATH

    def make_open(self):
        self.colour = COLOUR_VISITED_PATH

    def make_wall(self):
        self.colour = COLOUR_BOUNDARY

    def make_start(self):
        self.colour = COLOUR_START_NODE

    def make_end(self):
        self.colour = COLOUR_END_NODE

    def make_path(self):
        self.colour = COLOUR_SOLUTION_PATH

    def is_closed(self):
        return self.colour == COLOUR_EXPLORED_PATH

    def is_opened(self):
        return self.colour == COLOUR_VISITED_PATH

    def is_wall(self):
        return self.colour == COLOUR_BOUNDARY

    def is_start(self):
        return self.colour == COLOUR_START_NODE

    def is_end(self):
        return self.colour == COLOUR_END_NODE

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

    def update_neighbours(self, grid):
        self.neighbours = []
        # checks for neighbours in -y axis
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbours.append(grid[self.row + 1][self.col])

        # checks for neighbours in y axis
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbours.append(grid[self.row - 1][self.col])

        # checks for neighbours in -x axis
        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbours.append(grid[self.row][self.col + 1])

        # checks for neighbours in x axis
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbours.append(grid[self.row][self.col - 1])


def __lt__(self, other):
    return False


def h(p1, p2):
    x1, y1 = p1  # spliting values from a tuple
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(node_path, current, draw, counter_start):
    pygame.display.set_caption("Maze Solver ( Constructing Path... )")
    path_count = 0

    while current in node_path:
        current = node_path[current]
        current.make_path()
        path_count += 1
        draw()
    counter_end = timer()
    time_elapsed = counter_end - counter_start
    pygame.display.set_caption(
        f'Time Elapsed: {format(time_elapsed, ".2f")}s | Cells Visted: {len(node_path) + 1} | Shortest Path: {path_count + 1} Cells')


def algorithm(draw, grid, start, end, counter_start):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    node_path = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    while not open_set.empty():
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(node_path, end, draw, counter_start)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                node_path[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        pygame.display.update()

        pygame.time.delay(300)  # Delay in milliseconds (10 ms)

        if current != start:
            current.make_close()

    pygame.display.set_caption("Maze Solver ( Unable To Find The Target Node ! )")
    return False


def make_grid(rows, cols, width):
    grid = []
    gapR = width // rows
    gapC = width // cols
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            spot = Node(i, j, gapR, gapC, rows, cols)
            grid[i].append(spot)

    return grid


# def draw_grid(win, rows, cols, width):
#     gap = width // rows
#     for i in range(rows):
#         pygame.draw.line(win, GRID, (0, i * gap), (width, i * gap))
#         for j in range(cols):
#             pygame.draw.line(win, GRID, (i * gap, 0), (i * gap, width))

def draw_grid(win, rows, cols, width):
    row_gap = width // rows  # Height of each cell based on total rows
    col_gap = width // cols  # Width of each cell based on total columns

    # Draw horizontal lines (row separators)
    for i in range(rows + 1):
        pygame.draw.line(win, COLOUR_BORDERS, (0, i * col_gap), (width, i * col_gap), width = BORDER_THICKNESS)

    # Draw vertical lines (column separators)
    for j in range(cols + 1):
        pygame.draw.line(win, COLOUR_BORDERS, (j * row_gap, 0), (j * row_gap, width), width = BORDER_THICKNESS)


def draw_grid_wall(rows, grid):
    for i in range(rows):
        for j in range(rows):
            if i == 0 or i == rows - 1 or j == 0 or j == rows - 1:
                spot = grid[i][j]
                spot.make_wall()


def draw(win, grid, rows, cols, width):
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, cols, width)
    # draw_grid_wall(rows, grid)
    pygame.display.update()


def get_mouse_pos(pos, rows, cols, width):
    gapR = width // rows
    gapC = width // cols
    y, x = pos

    row = y // gapR
    col = x // gapC

    return row, col


def main(win, width):
    ROWS = 6
    COLS = 5
    grid = make_grid(ROWS, COLS, width)

    Start = None
    End = None
    Run = True

    while Run:
        draw(win, grid, ROWS, COLS, width)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                Run = False

            start_node = grid[0][0]
            end_node = grid[-1][-1]

            start_node.make_start()
            end_node.make_end()

            boundary_1 = grid[1][0]
            boundary_1.make_wall()
            boundary_2 = grid[1][2]
            boundary_2.make_wall()
            boundary_3 = grid[3][2]
            boundary_3.make_wall()
            boundary_4 = grid[1][3]
            boundary_4.make_wall()
            boundary_5 = grid[4][3]
            boundary_5.make_wall()
            boundary_6 = grid[4][4]
            boundary_6.make_wall()

            # if pygame.mouse.get_pressed()[0]:  # [0] left mouse btn
            #     pos = pygame.mouse.get_pos()
            #     row, col = get_mouse_pos(pos, ROWS, COLS, width)
            #     spot = grid[row][col]
            #     spot.make_wall()
            #
            # if pygame.mouse.get_pressed()[2]:  # [2] Right mouse btn
            #     pos = pygame.mouse.get_pos()
            #     row, col = get_mouse_pos(pos, ROWS, COLS, width)
            #     spot = grid[row][col]
            #     spot.reset()

                # if spot == Start:
                #     Start = None
                # if spot == End:
                #     End = None

            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_SPACE:

                    counter_start = timer()
                    pygame.display.set_caption("Maze Solver ( Searching... )")
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    algorithm(lambda: draw(win, grid, ROWS, COLS, width), grid, start_node, end_node, counter_start)

                if e.key == pygame.K_c:
                    Start = None
                    End = None
                    pygame.display.set_caption("Maze Solver ( Using A* Algorithm )")
                    grid = make_grid(ROWS, COLS, width)
    pygame.quit()


main(win, WIDTH)


# def main(win, width):
#     ROWS = 6
#     COLS = 5
#     grid = make_grid(ROWS, COLS, width)
#
#     Start = None
#     End = None
#     Run = True
#
#     while Run:
#         draw(win, grid, ROWS, COLS, width)
#         for e in pygame.event.get():
#             if e.type == pygame.QUIT:
#                 Run = False
#
#             if pygame.mouse.get_pressed()[0]:  # [0] left mouse btn
#                 pos = pygame.mouse.get_pos()
#                 row, col = get_mouse_pos(pos, ROWS, COLS, width)
#                 spot = grid[row][col]
#                 if not Start and spot != End:
#                     Start = spot
#                     Start.make_start()
#
#                 elif not End and spot != Start:
#                     End = spot
#                     End.make_end()
#
#                 elif spot != Start and spot != End:
#                     spot.make_wall()
#
#             if pygame.mouse.get_pressed()[2]:  # [2] Right mouse btn
#                 pos = pygame.mouse.get_pos()
#                 row, col = get_mouse_pos(pos, ROWS, COLS, width)
#                 spot = grid[row][col]
#                 spot.reset()
#                 if spot == Start:
#                     Start = None
#                 if spot == End:
#                     End = None
#
#             if e.type == pygame.KEYDOWN:
#
#                 if not Start and not End:
#                     pygame.display.set_caption("Maze Solver ( Set Start & End Nodes ! )")
#
#                 if e.key == pygame.K_SPACE and Start and End:
#
#                     counter_start = timer()
#                     pygame.display.set_caption("Maze Solver ( Searching... )")
#                     for row in grid:
#                         for spot in row:
#                             spot.update_neighbours(grid)
#
#                     algorithm(lambda: draw(win, grid, ROWS, COLS, width), grid, Start, End, counter_start)
#
#                 if e.key == pygame.K_c:
#                     Start = None
#                     End = None
#                     pygame.display.set_caption("Maze Solver ( Using A* Algorithm )")
#                     grid = make_grid(ROWS, COLS, width)
#     pygame.quit()
#
#
# main(win, WIDTH)