import pathlib
import typing as tp
from random import randint

from tools import batched

T = tp.TypeVar("T")
POSSIBLE_NUMBERS = set(map(str, range(1, 10)))


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return list(batched(values, n))


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [e[pos[1]] for e in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block = []
    for i in range((pos[0] // 3) * 3, (pos[0] // 3) * 3 + 3):
        for j in range((pos[1] // 3) * 3, (pos[1] // 3) * 3 + 3):
            block.append(grid[i][j])
    return block


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """

    for i, row in enumerate(grid):
        for j, element in enumerate(row):
            if element == ".":
                return i, j
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """

    return (
        {"."}
        ^ POSSIBLE_NUMBERS
        ^ (set(get_row(grid, pos)) | set(get_col(grid, pos)) | set(get_block(grid, pos)))
    )


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    for row in range(9):
        for col in range(9):
            if grid[row][col] == ".":
                for num_str in find_possible_values(grid, (row, col)):
                    grid[row][col] = num_str
                    if solve(grid):
                        return grid
                    # Если данное число не подходит, отменяем его
                    grid[row][col] = "."
                return None
    return grid


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    # TODO: Add doctests with bad puzzles

    # Проверяем строки
    for row in range(9):
        if not is_list_valid(get_row(solution, (row, row))):
            return False

    # Проверяем столбцы
    for col in range(9):
        if not is_list_valid(get_col(solution, (col, col))):
            return False

    # Проверяем блоки
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            if not is_list_valid(get_block(solution, (row, col))):
                return False

    return True


def is_list_valid(grid: tp.List[str]) -> bool:
    return set(grid) == POSSIBLE_NUMBERS


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """

    # базовая сетка
    grid = [[str((i * 3 + i // 3 + j) % 9 + 1) for j in range(9)] for i in range(9)]

    func = {
        1: transpose,
        2: swap_rows_small,
        3: swap_columns_small,
        4: swap_rows_area,
        5: swap_columns_area,
    }

    for i in range(randint(10, 100)):
        id_func = randint(1, 5)
        func[id_func](grid)

    # удаляем 81 - N клеток
    N = 81 - min(N, 81) + 1
    while N := N - 1:
        i = randint(0, 8)
        j = randint(0, 8)
        while grid[i][j] == ".":
            i = randint(0, 8)
            j = randint(0, 8)
        grid[i][j] = "."

    return grid


def transpose(grid: tp.List[tp.List[str]]) -> tp.List[tp.List[str]]:
    return list(map(list, zip(*grid)))


def swap_rows_small(grid: tp.List[tp.List[str]]) -> tp.List[tp.List[str]]:
    area = randint(0, 2)  # получение случайного района и случайной строки

    line1 = randint(0, 2)
    i = area * 3 + line1  # номер 1 строки для обмена
    line2 = randint(0, 2)
    while line1 == line2:
        line2 = randint(0, 2)
    j = area * 3 + line2  # номер 2 строки для обмена

    grid[i], grid[j] = grid[i], grid[j]
    return grid


def swap_columns_small(grid: tp.List[tp.List[str]]) -> tp.List[tp.List[str]]:
    return transpose(swap_rows_small(transpose(grid)))


def swap_rows_area(grid: tp.List[tp.List[str]]) -> tp.List[tp.List[str]]:
    area1 = randint(0, 2)  # получение случайного района

    area2 = randint(0, 2)
    while area1 == area2:
        area2 = randint(0, 2)

    for i in range(0, 3):
        i, j = area1 * 3 + i, area2 * 3 + i
        grid[i], grid[j] = grid[j], grid[i]

    return grid


def swap_columns_area(grid: tp.List[tp.List[str]]) -> tp.List[tp.List[str]]:
    return transpose(swap_rows_area(transpose(grid)))


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
