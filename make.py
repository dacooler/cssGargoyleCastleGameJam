#!/usr/bin/env python3


import math
import base64
import io

from PIL import Image


def raw_file(path):
    with open(path, "r", encoding="utf8") as f:
        result = f.read()
    return result


def cursor_styles():
    num_sizes = 20
    max_size = 128
    min_size = 10

    result = ""

    cursors = {}

    for name in ["alive", "gargoyle", "carpenter", "dead"]:
        cursors[name] = Image.open(f"assets/player_{name}.png")

    for i, exp in enumerate(range(num_sizes)):
        size = math.pow(max_size / min_size, exp / (num_sizes - 1)) * min_size

        styles = f"--cursor-x: {round(size / 2)}; "
        styles += f"--cursor-y: {round(size)}; "

        for name, img in cursors.items():
            scaled = img.resize((round(size), round(size)))

            scaled_png = io.BytesIO()
            scaled.save(scaled_png, format='PNG')
            scaled_png = scaled_png.getvalue()

            url = "data:image/png;base64," + base64.b64encode(scaled_png).decode("utf8")
            styles += f"--cursor-{name}: url('{url}'); "

        styles = f":root {{ {styles}}}"

        if i > 0:
            cursor_size_units = 10
            window_width_units = 160
            window_height_units = 90

            min_width = round(window_width_units / cursor_size_units * size)
            min_height = round(window_height_units / cursor_size_units * size)
            styles = f"@media only screen and (min-width: {min_width}px) and (min-height: {min_height}px) {{ {styles} }}"

        result += styles + "\n"

    return result


def maze_logic():
    with open("src/debugMaze.txt", "r", encoding="utf8") as f:
        maze_lines = f.read()

    result = ""
    for y, line in enumerate(maze_lines.split("\n")):
        for x, cell in enumerate(line.strip()):
            if cell in ".":
                result += f"<div class='cell' style='grid-area: {y+1}/{x+1}'></div>"
            if cell in "123":
                result += f"<div class='cell hole hole{cell}' style='grid-area: {y+1}/{x+1}'></div>"
                result += f"<div class='repair hole hole{cell}' style='grid-area: {y+1}/{x+1}'></div>"
                result += f"<div class='abyss hole hole{cell}' style='grid-area: {y+1}/{x+1}'></div>"
            if cell == "x":
                result += f"<div class='abyss' style='grid-area: {y+1}/{x+1}'></div>"

    with open("src/maze_logic.html", "r", encoding="utf8") as f:
        template = f.read()

    return template.replace("MAZE_CELLS", result)


def maze_graphics():
    with open("src/maze2.txt", "r", encoding="utf8") as f:
        maze_lines = f.read()

    result = ""

    has_permanent = set()
    has_trap = dict()

    for y, line in enumerate(maze_lines.split("\n")):
        for x, cell in enumerate(line.strip()):
            if cell in ".":
                result += f"<div class='cell' style='grid-area: {y+1}/{x+1}'></div>"
                has_permanent.add((x, y))
            if cell in "123":
                has_trap[(x, y)] = cell
            if cell == "x":
                pass

    for (x, y) in has_permanent:
        if (x, y + 1) not in has_permanent:
            result += f"<div class='scaffold horiz' style='grid-area: {y+1}/{x+1}'></div>"
        if (x + 1, y) not in has_permanent:
            result += f"<div class='scaffold vert' style='grid-area: {y+1}/{x+1}'></div>"
        if (x - 1, y) not in has_permanent:
            result += f"<div class='scaffold vert' style='grid-area: {y+1}/{x}'></div>"

    for (x, y), kind in has_trap.items():
        if (x, y - 1) not in has_trap and (x - 1, y) not in has_trap:
            result += f"<div class='bridge hole{kind}' style='grid-area: {y+1}/{x+1}/span 2/span 2'></div>"


    with open("src/maze_graphics.html", "r", encoding="utf8") as f:
        template = f.read()

    return template.replace("MAZE_CELLS", result)


def main():
    with open("src/game.html", "r", encoding="utf8") as f:
        game = f.read()

    game = game.replace("STATE_CTX", raw_file("src/state_ctx.css"))
    game = game.replace("TIMER_CTX", raw_file("src/timer_ctx.css"))
    game = game.replace("MAZE_CTX", raw_file("src/maze_ctx.css"))
    game = game.replace("MAZE_LOGIC", maze_logic())
    game = game.replace("STORAGE_LOGIC", raw_file("src/storage_logic.html"))
    game = game.replace("YARD_LOGIC", raw_file("src/yard_logic.html"))
    game = game.replace("GATEROOM_LOGIC", raw_file("src/gateroom_logic.html"))
    game = game.replace("MAZE_GRAPHICS", maze_graphics())
    game = game.replace("STORAGE_GRAPHICS", raw_file("src/storage_graphics.html"))
    game = game.replace("YARD_GRAPHICS", raw_file("src/yard_graphics.html"))
    game = game.replace("GATEROOM_GRAPHICS", raw_file("src/gateroom_graphics.html"))
    game = game.replace("WALL_GRAPHICS", raw_file("src/wall_graphics.html"))
    game = game.replace("CURSORS", cursor_styles())

    with open("index.html", "w", encoding="utf8") as f:
        f.write(game)


if __name__ == "__main__":
    main()
