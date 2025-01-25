import os.path
import time
import tkinter
import tkinter.filedialog
import typing as tp
from pathlib import Path

import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(
        self, life: GameOfLife, rows: int = 10, cols: int = 10, cell_size: int = 35, speed: int = 10
    ) -> None:
        super().__init__(life)

        self.width = cols * cell_size
        self.height = rows * cell_size
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Скорость протекания игры
        self.speed = speed

    def get_cell(self, coordinates: tp.Tuple[int, int]) -> tp.Tuple[int, int]:
        return (coordinates[1]) // self.cell_size, (coordinates[0]) // self.cell_size

    def check_coords(self, coordinates: tp.Tuple[int, int]) -> bool:
        return not 0 <= coordinates[0] < self.life.rows or not 0 <= coordinates[1] < self.life.cols

    def draw_lines(self) -> None:
        """
        Отрисовать пустую сетку.
        """
        for x in range(self.life.cols + 1):
            pygame.draw.line(
                self.screen,
                pygame.Color("white"),
                (x * self.cell_size, 0),
                (x * self.cell_size, self.height),
                1,
            )
        for y in range(self.life.rows + 1):
            pygame.draw.line(
                self.screen,
                pygame.Color("white"),
                (0, y * self.cell_size),
                (self.width, y * self.cell_size),
                1,
            )

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                cell = self.life.curr_generation[i, j]
                if cell == 1:
                    pygame.draw.rect(
                        self.screen,
                        "green",
                        (
                            j * self.cell_size + 3,
                            i * self.cell_size + 3,
                            self.cell_size - 4,
                            self.cell_size - 4,
                        ),
                    )
                if cell == 0:
                    # print(i, j, 0)
                    pygame.draw.rect(
                        self.screen,
                        "black",
                        (
                            j * self.cell_size + 3,
                            i * self.cell_size + 3,
                            self.cell_size - 4,
                            self.cell_size - 4,
                        ),
                    )

    @staticmethod
    def choose_file() -> str:
        """Create a Tk file dialog and cleanup when finished"""
        top = tkinter.Tk()
        top.withdraw()  # hide window
        file_name = tkinter.filedialog.askopenfilename(parent=top)
        top.destroy()
        return file_name

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("black"))

        # Создание списка клеток произошла во время инициализации класса игры

        on_pause = False
        go_next = False
        skip_step = False
        filling = False
        filling_mode = True

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        # pause game
                        on_pause ^= True
                        go_next = False
                        skip_step = False
                        filling = False
                    elif event.key == K_q:  # quit
                        # quit the game
                        running = False

                    if not on_pause:
                        pass
                    elif event.key == K_s:  # save
                        # available only on pause
                        # save grid to file, only const path
                        filename = Path(self.choose_file())
                        print(filename)
                        if not os.path.isfile(filename):
                            continue
                        self.life.save_to_file(filename=filename)
                    elif event.key == K_l:  # load
                        # available only on pause
                        # load grid from file, only const path
                        filename = Path(self.choose_file())
                        print(filename)
                        if not os.path.isfile(filename):
                            continue
                        self.life = self.life.load_from_file(filename=filename)
                        self.__init__(
                            self.life, self.life.rows, self.life.cols, self.cell_size, self.speed
                        )
                        go_next = True
                        skip_step = True
                    elif event.key == K_r:  # random | reset
                        # available only on pause
                        # destroy grid and create new by random
                        self.life.generations = 0
                        self.life.prev_generation = self.life.create_grid()
                        self.life.curr_generation = self.life.create_grid(randomize=True)
                        self.life.step()
                        go_next = True
                    elif event.key == K_c:  # clear
                        # available only on pause
                        self.life.generations = 0
                        self.life.prev_generation = self.life.create_grid(randomize=True)
                        self.life.curr_generation = self.life.create_grid()
                        go_next = True
                    elif event.key == K_f:  # fill
                        # available only on pause
                        # fill cells with one value by mouse moving
                        filling ^= True
                    elif event.key == K_m:  # mode
                        # available only on pause
                        # change type of value what will be filling in f-mode
                        filling_mode ^= True
                    elif event.key == K_n or event.key == K_RIGHT:  # next
                        # available only on pause
                        # move to the next step being on pause
                        go_next = True
                    elif event.key == K_p or event.key == K_LEFT:  # previous
                        # available only on pause
                        # move to the previous step being on pause
                        self.life.curr_generation, self.life.prev_generation = (
                            self.life.prev_generation,
                            self.life.curr_generation,
                        )
                        go_next = True
                        skip_step = True
                    elif event.key == K_UP:  # increase speed
                        # available only on pause
                        # increase the speed of game
                        self.speed = min(99, max(1, self.speed + 2))
                    elif event.key == K_DOWN:  # decrease speed
                        # available only on pause
                        # decrease the speed of game
                        self.speed = min(99, max(1, self.speed - 2))
                elif event.type == MOUSEBUTTONDOWN:
                    # available only on pause
                    # change cell state
                    indexes = self.get_cell(event.pos)
                    if self.check_coords(indexes):
                        continue
                    if event.button == 1:
                        self.life.curr_generation[indexes[0], indexes[1]].swap()
                    go_next = True
                    skip_step = True

            if filling:
                indexes = self.get_cell(pygame.mouse.get_pos())
                if self.check_coords(indexes):
                    continue
                self.life.curr_generation[indexes[0], indexes[1]].state = filling_mode
                go_next = True
                skip_step = True

            if on_pause and not go_next:
                continue
            go_next = False

            print(f"Generation: {self.life.generations:4d}, speed: {self.speed:2d}, {time.ctime()}")

            # Логика игры
            # Выполнение одного шага игры (обновление состояния ячеек)
            if not skip_step:
                self.life.step()
            else:
                skip_step = False

            # GUI
            # Рисуем пустую сетку
            self.draw_lines()
            # Рисуем список клеток
            self.draw_grid()

            # Отрисовка на экране
            pygame.display.flip()
            clock.tick(self.speed)

            # Проверяем кол-во итераций и изменения
            if self.life.is_max_generations_exceeded or (
                (not self.life.is_changing) and self.life.generations != 1
            ):
                on_pause = True

        pygame.quit()
