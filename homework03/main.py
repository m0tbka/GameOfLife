import argparse

from start_game import start_game

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("width", help="Количество клеток по ширине", type=int)
    parser.add_argument("height", help="Количество клеток по высоте", type=int)
    parser.add_argument(
        "-cs", dest="cell_size", help="Размер одной клетки", type=int, default=65, required=False
    )
    parser.add_argument(
        "-s", dest="speed", help="Скорость игры", type=int, default=10, required=False
    )
    args = parser.parse_args()
    start_game(args.width, args.height, args.cell_size, args.speed)
