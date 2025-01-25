import pathlib
import typing as tp
from copy import copy
from random import choices, randint

from grid import ALIVE_CELL, DEAD_CELL, Cell, Cells, Grid


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
        # history_size: tp.Optional[int] = 100,
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

        # Кол-во хранимых последних поколений
        # self.history_size = history_size
        # Состояния последних history_size поколений
        # self.history = list()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """

        grid = Grid(self.rows, self.cols)

        if not randomize:
            return grid

        alive_num = randint(0, self.rows * self.cols)
        alive_cells = choices([cell for cell in grid], k=alive_num)
        for cell in alive_cells:
            cell.swap()

        grid.update(alive_cells)

        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """

        return self.curr_generation.get_neighbours(cell)

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """

        next_generation = Grid(self.rows, self.cols)
        for cell in self.curr_generation:
            neighbours = self.get_neighbours(cell)
            alive_n = neighbours.count(ALIVE_CELL)

            next_generation[cell.row, cell.col] = copy(cell)
            if (cell.state and (alive_n != 2 and alive_n != 3)) or (
                (not cell.state) and alive_n == 3
            ):
                next_generation[cell.row, cell.col].swap()

        return next_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = copy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations > self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """

        return self.curr_generation != self.prev_generation

    @staticmethod
    def load_from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """

        grid = Grid.load_from_file(filename)
        instance = GameOfLife(grid.size())
        instance.curr_generation = grid

        return instance

    def save_to_file(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        self.curr_generation.save_to_file(filename)
