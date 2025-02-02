import abc

from life import GameOfLife


class UI(abc.ABC):
    def __init__(self, life: GameOfLife) -> None:
        self.life: GameOfLife = life

    @abc.abstractmethod
    def run(self) -> None:
        pass
