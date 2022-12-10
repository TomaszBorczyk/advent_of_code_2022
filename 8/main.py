import sys
from typing import List


def read_grid(filename: str) -> List[str]:
    grid = []

    with open(filename) as f:
        line = f.readline().strip()

        while line != '':
            grid.append(line)
            line = f.readline().strip()

    return grid


def is_visible_diagonally(x: int, y: int, grid: List[str]) -> bool:
    tree_height = int(grid[y][x])

    visible_up = all(int(grid[h][x]) < tree_height for h in range(0, y))
    visible_down = all(int(grid[h][x]) < tree_height for h in range(y+1, len(grid)))

    return visible_up or visible_down
    

def is_visible_horizontally(x: int, y: int, grid: List[str]) -> bool:
    tree_height = int(grid[y][x])

    visible_left = all(int(grid[y][w]) < tree_height for w in range(0, x))
    visible_right = all(int(grid[y][w]) < tree_height for w in range(x+1, len(grid[0])))

    return visible_left or visible_right


def is_tree_visible(x: int, y: int, grid: List[str]) -> bool:
    visible_diagonally = is_visible_diagonally(x, y, grid)
    visible_horizontally = is_visible_horizontally(x, y, grid)

    return visible_diagonally or visible_horizontally


def count_visible_trees(grid: List[str]) -> int:
    visible_count = 0
    
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if i == 0 or i == (len(grid) - 1):
                visible_count += 1
            elif j == 0 or j == (len(row) - 1):
                visible_count += 1
            else:
                visible = is_tree_visible(j, i, grid)
                if visible:
                    visible_count += 1

    return visible_count


def visible_trees(x_range: List[int], y_range: List[int], grid: List[str], tree_height: int) -> int:
    visible_count = 0

    for x in x_range:
        for y in y_range:
            visible_count += 1

            if int(grid[y][x]) >= tree_height:
                return visible_count

    return visible_count
            

def calc_scenic_score(x: int, y: int, grid: List[str]) -> int:
    h = int(grid[y][x])

    scenic_up = visible_trees([x], list(reversed(range(0, y))), grid, h)
    scenic_down = visible_trees([x], list(range(y+1, len(grid))), grid, h)
    scenic_left = visible_trees(list(reversed(range(0, x))), [y], grid, h)
    scenic_right = visible_trees(list(range(x+1, len(grid[0]))), [y], grid, h)

    return scenic_up * scenic_down * scenic_left * scenic_right


def get_top_scenic_score(grid: List[str]) -> int:
    max_score = 0

    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            score = calc_scenic_score(j, i, grid)

            if score > max_score:
                max_score = score

    return max_score


if __name__ == '__main__':
    filename = sys.argv[1]
    grid = read_grid(filename)

    visible = count_visible_trees(grid)
    print('part1: ', visible)
            
    top_scenic = get_top_scenic_score(grid)
    print('part2: ', top_scenic)
