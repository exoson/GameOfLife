import pygame
import sys
import numpy as np
from copy import deepcopy
import time

def range2d(size):
    for i in range(size[0]):
        for j in range(size[1]):
            yield i, j

def neighbors(point):
    x, y = point
    for i, j in range2d([3, 3]):
        if ((i-1) != 0) or ((j-1) != 0):
            yield int(x + i -1), int(y + j -1)
def inrange(point, ran):
    return (point[0] >= 0) and (point[1] >= 0) and (point[0] < ran[0]) and (point[1] < ran[1])

def update(board):
    old_board = deepcopy(board)
    shape = board.shape
    for x, y in range2d(shape):
        n_count = 0
        for nbor in neighbors((x,y)):
            if inrange(nbor, shape):
                n_count += old_board[nbor]
        is_lv = old_board[x, y]
        if is_lv:
            board[x, y] = not (n_count > 3 or n_count < 2)
        else:
            board[x, y] = n_count == 3

def main():
    pygame.init()

    size = np.array([200, 100])
    color = (0, 0, 0)
    scale = 10
    board = np.random.random_integers(0, 1, size=size)
    screen=pygame.display.set_mode(scale*size)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        update(board)

        mouse_pos = np.array(pygame.mouse.get_pos(), dtype=np.int32)
        if pygame.mouse.get_pressed()[0]:
            scaled_pos = mouse_pos // scale
            board[scaled_pos[0], scaled_pos[1]] = 1

        screen.fill(color)
        img = pygame.Surface(size)
        pygame.surfarray.blit_array(img, 255*board)
        img = pygame.transform.scale(img, scale * size)
        screen.blit(img, img.get_rect())
        pygame.display.flip()

if __name__ == '__main__':
    main()