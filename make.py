#!/usr/bin/env python3


def main():
    with open("src/game.html", "r", encoding="utf8") as f:
        game = f.read()

    with open("index.html", "w", encoding="utf8") as f:
        f.write(game)


if __name__ == "__main__":
    main()