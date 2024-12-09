import pathlib
import typing as tp


class Cell:

    def __init__(self, row=0, col=0, state=False):
        self.row = row
        self.col = col
        self.state = state  # 1 - alive, 0 - dead

    def is_alive(self) -> bool:
        # 1 - alive, 0 - dead
        return self.state

    def swap(self):
        self.state = not self.state

    def __eq__(self, other) -> bool:
        if isinstance(other, Cell):
            return self.state == other.state
        if isinstance(other, int):
            return self.state == other
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f"Cell({self.row=}, {self.col=}, {self.state=})"


ALIVE_CELL = Cell(state=True)
DEAD_CELL = Cell(state=False)

Cells = tp.List[Cell]


class Grid:

    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.cells = [[Cell(j, i) for i in range(self.n_cols)] for j in range(self.n_rows)]

    def size(self) -> tp.Tuple[int, int]:
        return self.n_rows, self.n_cols

    def update(self, cells: Cells):
        for cell in cells:
            self[cell.row, cell.col] = cell

    def get_neighbours(self, cell: Cell) -> Cells:
        return [
            self.cells[cell.row + i][cell.col + j]
            for j in range(-1, 2)
            for i in range(-1, 2)
            if not i == j == 0
            and 0 <= cell.row + i < self.n_rows
            and 0 <= cell.col + j < self.n_cols
        ]

    @classmethod
    def load_from_file(cls, filename: pathlib.Path) -> "Grid":
        with open(filename, "r") as f:
            n_rows, n_cols = map(int, f.readline().strip().split())
            instance = cls(n_rows, n_cols)
            for i, line in enumerate(f.readlines()):
                # line = '110100110101'
                for j, cell in enumerate(" ".join(line.strip()).split()):
                    try:
                        instance[i, j] = Cell(i, j, bool(int(cell)))
                    except ValueError as err:
                        raise ValueError(
                            f"Value of cell {i=}, {j=} must only be 0 or 1, not {cell}"
                        ) from err
        return instance

    def save_to_file(self, filename: pathlib.Path):
        with open(filename, "w") as f:
            f.write(str(self.n_rows) + " " + str(self.n_cols) + "\n")
            for raw in self.cells:
                f.write("".join(map(lambda cell: str(int(cell.state)), raw)))
                f.write("\n")

    def print(self, debug=False):
        for e in self.cells:
            if debug:
                print(*e)
            else:
                print(*list(map(lambda x: int(x.state), e)))

    def __len__(self) -> int:
        return self.n_rows * self.n_cols

    def __iter__(self):
        for row in self.cells:
            for cell in row:
                yield cell

    def __getitem__(self, index) -> Cell:
        if len(index) != 2:
            raise IndexError(f"Index must be 2, got {len(index)}, {index=}")
        row, col = index
        try:
            return self.cells[row][col]
        except IndexError as err:
            raise IndexError(
                f"Indexes must be in diapason: 0 <= row < {self.n_rows} and"
                f" 0 <= col < {self.n_cols}. Got {row=} and {col=}"
            ) from err

    def __setitem__(self, key, value):
        if len(key) != 2:
            raise IndexError(f"Index must be 2, got {len(key)}, {key=}")
        row, col = key
        if isinstance(value, Cell):
            try:
                self.cells[row][col] = value
            except IndexError as err:
                raise IndexError(
                    f"Indexes must be in diapason: 0 <= row < {self.n_rows} and"
                    f" 0 <= col < {self.n_cols}. Got {row=} and {col=}"
                ) from err

    def __eq__(self, other) -> bool:
        if isinstance(other, Grid):
            return (
                self.n_rows == other.n_rows
                and self.n_cols == other.n_cols
                and self.cells == other.cells
            )
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f"Grid({self.n_rows=}, {self.n_cols=})"
