import matplotlib.pyplot as plt
import numpy as np
from mansion import Mansion
from room import Room
from space import Space

def visualize_mansion(mansion):
    rows = len(mansion.grid)
    cols = len(mansion.grid[0])
    fig, ax = plt.subplots(figsize=(12, 10))

    secret_passage_pairs = [
        ('Study', 'Kitchen', '★'),
        ('Conservatory', 'Lounge', '✦')
    ]

    for room1_name, room2_name, symbol in secret_passage_pairs:
        if room1_name in mansion.rooms and room2_name in mansion.rooms:
            mansion.rooms[room1_name].name += f" {symbol}"
            mansion.rooms[room2_name].name += f" {symbol}"

    grid = np.full((rows, cols), "Space", dtype=object)

    for r in range(rows):
        for c in range(cols):
            tile = mansion.grid[r][c]
            if isinstance(tile, Room):
                grid[r][c] = tile.name
            elif isinstance(tile, Space):
                grid[r][c] = "Space"

    for (r, c), value in np.ndenumerate(grid):
        if value == "Space":
            ax.text(c, r, "")
        else:
            ax.text(c, r, value, va='center', ha='center', color="black", fontsize=10)

    ax.set_xticks(np.arange(-.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-.5, rows, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
    ax.tick_params(which="minor", size=0)
    ax.invert_yaxis()

    plt.show()

if __name__ == "__main__":
    mansion = Mansion()
    visualize_mansion(mansion)