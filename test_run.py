import pytest
import run
import numpy as np

def xfail(*params):
    return pytest.param(params, marks=pytest.mark.xfail(strict=True))

@pytest.mark.parametrize('size', [(2, 2), (2, 3), (3, 2)])
def test_range2d(size):
    x_values = range(size[0])
    y_values = range(size[1])
    generator = run.range2d(size)
    for x in x_values:
        for y in y_values:
            gen_val = next(generator)
            assert gen_val == (x, y)

@pytest.mark.parametrize('point',
                         [xfail((-1, 0)), 
                         xfail((0, -1)),
                         xfail((10, 0)),
                         xfail((0, 10)),
                         (9, 9),
                         (0, 0)])
def test_irange(point):
    ran = (10, 10)
    assert run.inrange(point, ran)

def test_neighbors():
    pos = (10.0, 10.0)
    for x, y in run.neighbors(pos):
        assert type(x) == int
        assert type(y) == int
        dist_sqr = ((pos[0] - x) ** 2 + (pos[1] - y) ** 2)
        assert (dist_sqr > 0.) and (dist_sqr < 2.1)

boards = []
size = (10, 10)
eboard = np.zeros(size)
eboard[-1, -1] = 1
eboard[0, -1] = 1
eboard[-1, 0] = 1
eboard[0, 0] = 1
boards.append((np.ones(size), eboard))

board = np.zeros(size)
board[5, 5] = 1
board[5, 6] = 1
board[5, 4] = 1
eboard = np.zeros(size)
eboard[5, 5] = 1
eboard[6, 5] = 1
eboard[4, 5] = 1

boards.append((board, eboard))

@pytest.mark.parametrize('start, end', boards)
def test_update(start, end):
    run.update(start)
    assert (start == end).all()
