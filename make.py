#!/usr/bin/env python3


def main():
    with open("src/maze.txt", "r", encoding="utf8") as f:
        maze_lines = f.read()

    maze_cells = ""
    for y, line in enumerate(maze_lines.split("\n")):
        for x, cell in enumerate(line.strip()):
            if cell == ".":
                maze_cells += f"<div class='cell' style='grid-area: {y+1}/{x+1}'></div>"

    with open("src/game.html", "r", encoding="utf8") as f:
        game = f.read()

    game = game.replace("MAZE", maze_cells)

    with open("index.html", "w", encoding="utf8") as f:
        f.write(game)


if __name__ == "__main__":
    main()