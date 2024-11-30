from mansion import Mansion
from player import Player
from card_setup import create_card_deck, distribute_cards
from solution import Solution
from room import Room
from space import Space
import random
import matplotlib.pyplot as plt
import numpy as np

class GameManager:
    def __init__(self):
        self.players = []
        self.mansion = None
        self.card_deck = []
        self.solution = None

    def setup_game(self, player_names):
        self.players = [Player(name, None) for name in player_names]
        self.card_deck = create_card_deck()
        room_cards = [card for card in self.card_deck if card.card_type == 'room']
        self.mansion = Mansion(room_cards)

        non_room_cards = [card for card in self.card_deck if card.card_type != 'room']
        distribute_cards(self.players, non_room_cards)

        start_space = self.mansion.get_room("Start Space")
        for player in self.players:
            if start_space:
                player.move(start_space)

        solution_room = random.choice(room_cards)
        solution_character = random.choice([card for card in self.card_deck if card.card_type == 'character'])
        solution_weapon = random.choice([card for card in self.card_deck if card.card_type == 'weapon'])
        self.solution = Solution(solution_room.name, solution_character.name, solution_weapon.name)

        self.visualize_mansion()

    def visualize_mansion(self):
        rows = len(self.mansion.grid)
        cols = len(self.mansion.grid[0])
        fig, ax = plt.subplots(figsize=(12, 10))

        secret_passage_pairs = [
            ('Study', 'Kitchen', '★'),
            ('Conservatory', 'Lounge', '✦')
        ]

        for room1_name, room2_name, symbol in secret_passage_pairs:
            if room1_name in self.mansion.rooms and room2_name in self.mansion.rooms:
                self.mansion.rooms[room1_name].name += f" {symbol}"
                self.mansion.rooms[room2_name].name += f" {symbol}"

        grid = np.full((rows, cols), "Space", dtype=object)

        for r in range(rows):
            for c in range(cols):
                tile = self.mansion.grid[r][c]
                if isinstance(tile, Room):
                    grid[r][c] = tile.name
                elif isinstance(tile, Space):
                    grid[r][c] = "Space"

        for player in self.players:
            position = player.current_position
            if position:
                for r in range(rows):
                    for c in range(cols):
                        if self.mansion.grid[r][c] == position:
                            grid[r][c] += f" ({player.name})"

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

    def roll_dice(self):
        return random.randint(1, 6) + random.randint(1, 6)

    def start_game(self):
        print("The game has started!")
        for player in self.players:
            print(f"{player.name}'s cards: {player.show_cards()}")

        game_over = False
        current_player_index = 0
        while not game_over:
            current_player = self.players[current_player_index]
            if current_player.is_active:
                print(f"{current_player.name}'s turn:")
                action = input("Enter 'move', 'suggest', or 'accuse': ").strip().lower()
                if action == 'move':
                    dice_roll = self.roll_dice()
                    print(f"You rolled a {dice_roll}.")
                    for _ in range(dice_roll):
                        destination = input("Enter the name of the room or space to move to: ").strip()
                        new_position = self.mansion.get_room(destination) or self.mansion.get_space(destination)
                        if new_position:
                            current_player.move(new_position)
                            print(f"{current_player.name} moved to {new_position.name}.")
                            self.visualize_mansion()
                        else:
                            print("Invalid destination. Try again.")
                            break
                elif action == 'suggest':
                    if not current_player.can_make_suggestion():
                        print("You must be in a room to make a suggestion.")
                    else:
                        character = input("Enter the character: ").strip()
                        weapon = input("Enter the weapon: ").strip()
                        suggestion = current_player.make_suggestion(current_player.current_position.name, character, weapon)
                        print(f"{current_player.name} suggests: {suggestion}")
                elif action == 'accuse':
                    room = input("Enter the room: ").strip()
                    character = input("Enter the character: ").strip()
                    weapon = input("Enter the weapon: ").strip()
                    accusation = current_player.make_accusation(room, character, weapon, self.solution)
                    if accusation[-1] == "correct":
                        print(f"{current_player.name} has won the game with the correct accusation!")
                        game_over = True
                    else:
                        print(f"{current_player.name}'s accusation was incorrect. They are eliminated from the game.")
                else:
                    print("Invalid action. Please enter 'move', 'suggest', or 'accuse'.")
            current_player_index = (current_player_index + 1) % len(self.players)

if __name__ == "__main__":
    game = GameManager()
    game.setup_game(["Player 1", "Player 2", "Player 3"])
    game.start_game()