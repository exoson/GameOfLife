import pygame
import sys
import numpy as np
from copy import deepcopy
import itertools
import time

SIZE = np.array([200, 100])

def range2d(size):
    for i in range(size[0]):
        for j in range(size[1]):
            yield i, j

def wrap_point(point):
    x, y = point
    x %= SIZE[0]
    y %= SIZE[1]
    return x, y

def neighbors(point):
    x, y = point
    for i, j in range2d([3, 3]):
        if ((i-1) != 0) or ((j-1) != 0):
            nx = int(x + i -1)
            ny = int(y + j -1)
            yield wrap_point((nx, ny))

def wrap_around(board):
    new_board = set()
    for point in board:
        x, y = wrap_point(point, SIZE)
        new_board.add((x, y))
    return new_board

def update(board):
    new_board = set()
    recalc = board | set(itertools.chain(*map(neighbors, board)))
    for point in recalc:
        count = sum((neigh in board)
                    for neigh in neighbors(point))
        if count == 3 or (count == 2 and point in board):
            new_board.add(point)
    return new_board

def set_to_arr(board):
    arr = np.zeros(SIZE)
    for x, y in board:
        arr[x, y] = 1
    return arr

def main():
    pygame.init()

    bg_color = (0, 0, 0)
    scale = 10
    board = set([(0,0), (1,0), (2,0), (0, 1), (1, 2)])
    screen=pygame.display.set_mode(scale*SIZE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        board = update(board)

        mouse_pos = np.array(pygame.mouse.get_pos(), dtype=np.int32)
        if pygame.mouse.get_pressed()[0]:
            scaled_pos = mouse_pos // scale
            board.add((scaled_pos[0], scaled_pos[1]))
        
        board_arr = set_to_arr(board)

        screen.fill(bg_color)
        img = pygame.Surface(SIZE)
        pygame.surfarray.blit_array(img, 255*board_arr)
        img = pygame.transform.scale(img, scale * SIZE)
        screen.blit(img, img.get_rect())
        pygame.display.flip()

if __name__ == '__main__':
    main()
