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

def test_neighbors():
    pos = (10.0, 10.0)
    for x, y in run.neighbors(pos):
        assert type(x) == np.int32
        assert type(y) == np.int32
        dist_sqr = ((pos[0] - x) ** 2 + (pos[1] - y) ** 2)
        assert (dist_sqr > 0.) and (dist_sqr < 2.1)

boards = []
board = set([(10, 10), (11, 10), (10, 11), (11, 11)])
eboard = board
boards.append((board, eboard))

board = set([(10, 10), (11, 10), (9, 10)])
eboard = set([(10, 10), (10, 11), (10, 9)])
boards.append((board, eboard))

@pytest.mark.parametrize('start, end', boards)
def test_update(start, end):
    start = run.update(start)
    assert start == end
