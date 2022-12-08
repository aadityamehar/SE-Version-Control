import os
from queue import PriorityQueue
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

'''
Visualizing a Pathfinding Algorithm
Data Structures Mini Project

by Aaditya Mehar, Siddhant Meshram and Abhishek Pai

PEP8 Compliant
'''

pygame.display.set_caption("Pathfinder")

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DBLUE = (0, 50, 128)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
DARK = (50, 50, 50)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = DARK
        self.adList = []
        self.width = width
        self.total_rows = total_rows  # To avoid spaghetti code

    def position(self):
        return self.row, self.col

    def is_obstacle(self):
        return self.color == BLACK

    def reset(self):
        self.color = DARK

    def start(self):
        self.color = GREEN

    def visited(self):
        self.color = BLUE

    def open(self):
        self.color = DBLUE

    def obstacle(self):
        self.color = BLACK

    def end(self):
        self.color = RED

    def path(self):
        self.color = YELLOW

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def create_adList(self, grid):
        self.adList = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle():
            self.adList.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():
            self.adList.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_obstacle():
            self.adList.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():
            self.adList.append(grid[self.row][self.col - 1])
        


# UI helper functions
# Draws grid lines
def draw_grid(win, rows, width):
    bw = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * bw), (width, i * bw))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * bw, 0), (j * bw, width))


# Draws blocks in grid
def draw(win, grid, rows, width):
    win.fill(GREY)
    for row in grid:
        for node in row:
            node.draw(win)
    #draw_grid(win, rows, width)
    pygame.display.update()


def mouse_position(pos, rows, width):
    bw = width // rows
    y, x = pos
    row = y // bw
    col = x // bw
    return row, col


# Algorithm helper functions
# Calculates the "L" distance between two nodes
def manhattan_distance(n1, n2):
    x1, y1 = n1
    x2, y2 = n2
    return abs(x1 - x2) + abs(y1 - y2)


# Adds nodes to the graph matrix
def create_grid(rows, width):
    grid = []
    bw = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, bw, rows)
            grid[i].append(node)

    return grid


# Backtracks through the origin dictionary to get to the start point
def backtrack(origin, curr, draw):
    while curr in origin:
        curr = origin[curr]
        curr.path()
        draw()


# Main Algorithm Function
# Implements the A* Search Algorithm
def pathfinder(grid, start, end):
    count = 0
    visited = PriorityQueue()
    visited.put((0, count, start))
    origin = {}
    start_heuristic = {node: float("inf") for row in grid for node in row}

    start_heuristic[start] = 0

    visited_iter = {start}

    while not visited.empty():

        curr = visited.get()[2]
        visited_iter.remove(curr)

        if curr == end:
            backtrack(origin, end)
            end.end()
            return True

        for node in curr.adList:
            temp_start_heuristic = start_heuristic[curr] + 1
            if temp_start_heuristic < start_heuristic[node]:
                origin[node] = curr
                start_heuristic[node] = temp_start_heuristic

                if node not in visited_iter:
                    count += 1
                    visited.put((count, node))
                    visited_iter.add(node)
                    node.open()

        if curr != start:
            curr.visited()

    return False


# Main function with run loop and UI functionality
def main(win, width, rows):
    grid = create_grid(rows, width)

    start = end = None
    run = True
    # Run loop
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = mouse_position(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.start()

                elif not end and node != start:
                    end = node
                    end.end()

                elif node != end and node != start:
                    node.obstacle()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    start = end = None
                    grid = create_grid(rows, width)

                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.create_adList(grid)

                    pathfinder(lambda: draw(win, grid, rows, width), grid, start, end)

            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


# Driver Code
if __name__ == "__main__":
    WIDTH = int(input("Enter size of window: "))
    ROWS = int(input("Enter no. of blocks: "))
    WIN = pygame.display.set_mode((WIDTH, WIDTH))

    main(WIN, WIDTH, ROWS)
