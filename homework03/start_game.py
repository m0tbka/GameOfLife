from life import GameOfLife
from life_gui import GUI


def start_game(width=10, height=18, cell_size=65, speed=10):
    life = GameOfLife((width, height), randomize=True)
    gui = GUI(life, life.rows, life.cols, speed=speed, cell_size=cell_size)
    gui.run()


if __name__ == "__main__":
    start_game()
    # life = GameOfLife((90, 180), randomize=True)
    # life = GameOfLife((60, 120), randomize=True)
    # ! life = GameOfLife((15, 20), randomize=True)
    # gui = GUI(life, life.rows, life.cols, speed=1000, cell_size=10)
    # gui = GUI(life, life.rows, life.cols, speed=10, cell_size=15)
    # ! gui = GUI(life, life.rows, life.cols, speed=60, cell_size=65)
    # ! gui.run()
