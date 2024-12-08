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
        # Initialize the game manager's state, including players, mansion, card deck, and visualization components.
        self.players = []  # List of Player objects participating in the game.
        self.mansion = None  # Represents the game board/mansion structure.
        self.card_deck = []  # Full deck of Cluedo cards (characters, weapons, rooms).
        self.available_choices = None  # Cards available for suggestions or accusations.
        self.solution = None  # The actual solution to the murder mystery.
        self.fig = None  # Matplotlib figure for visualizing the board.
        self.ax = None  # Matplotlib axes for board visualization.
        self.secret_passage_symbols_added = False  # Tracks if secret passage symbols are added to the rooms.
        self.num_players_elim = 0  # Counter for eliminated players.

    def setup_game(self, player_names):
        # Initializes the game state based on the provided player names.
        self.players = [Player(name, None) for name in player_names]
        
        # Create and shuffle the card deck.
        self.card_deck = create_card_deck()

        # Copy the shuffled deck for player choices.
        self.available_choices = self.card_deck.copy()

        # Randomly select cards to form the murder mystery solution.
        solution_room = random.choice([card for card in self.card_deck if card.card_type == 'room'])
        solution_character = random.choice([card for card in self.card_deck if card.card_type == 'character'])
        solution_weapon = random.choice([card for card in self.card_deck if card.card_type == 'weapon'])
        self.solution = Solution(solution_room.name, solution_character.name, solution_weapon.name)
        # print(f"Solution: {self.solution}")

        # Initialize the mansion with the remaining room cards.
        room_cards = [card for card in self.card_deck if card.card_type == 'room']
        
        self.mansion = Mansion(room_cards)

        # Remove the solution cards from the deck
        self.card_deck.remove(solution_room)
        self.card_deck.remove(solution_character)
        self.card_deck.remove(solution_weapon)

        self.card_deck = [card for card in self.card_deck if card not in (solution_room, solution_character, solution_weapon)]

        # Distribute the remaining cards among the players.
        distribute_cards(self.players, self.card_deck)

        # Place all players in the starting space.
        start_space = self.mansion.get_room("Start Space")
        for player in self.players:
            if start_space:
                player.move(start_space)

        # Initialize the game board visualization.
        self.initialize_visualization()

    # Set up Matplotlib visualization for the game board.
    def initialize_visualization(self):
        rows = len(self.mansion.grid)
        cols = len(self.mansion.grid[0])
        self.fig, self.ax = plt.subplots(figsize=(12, 10))

        self.ax.set_xticks(np.arange(0, cols, 1))
        self.ax.set_yticks(np.arange(0, rows, 1))
        self.ax.set_xticklabels(range(cols))
        self.ax.set_yticklabels(range(rows))
        self.ax.set_xticks(np.arange(-.5, cols, 1), minor=True)
        self.ax.set_yticks(np.arange(-.5, rows, 1), minor=True)
        self.ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
        self.ax.tick_params(which="minor", size=0)
        self.ax.invert_yaxis()

        # Enable interactive mode for real-time updates.
        plt.ion()
        self.update_visualization()

    # Update the visualization to reflect the current game state.
    def update_visualization(self):
        rows = len(self.mansion.grid)
        cols = len(self.mansion.grid[0])
        grid = np.full((rows, cols), "", dtype=object)
        self.ax.clear()

        # Add secret passage symbols to the board (if not already added).
        secret_passage_pairs = [
            ('Study', 'Kitchen', '★'),
            ('Conservatory', 'Lounge', '✦')
        ]

        if not self.secret_passage_symbols_added:
            for room1_name, room2_name, symbol in secret_passage_pairs:
                if room1_name in self.mansion.rooms and room2_name in self.mansion.rooms:
                    self.mansion.rooms[room1_name].name += f" {symbol}"
                    self.mansion.rooms[room2_name].name += f" {symbol}"
            self.secret_passage_symbols_added = True

        # Populate the grid with room and space names.
        for r in range(rows):
            for c in range(cols):
                tile = self.mansion.grid[r][c]
                if isinstance(tile, Room):
                    grid[r][c] = tile.name
                elif isinstance(tile, Space):
                    grid[r][c] = ""

        # Mark player positions on the grid.
        for player in self.players:
            position = player.current_position
            if position:
                r, c = self.get_coordinates(position)
                grid[r][c] += f" ({player.name})"

        # Render grid values on the visualization.
        for (r, c), value in np.ndenumerate(grid):
            if value:
                self.ax.text(c, r, value, va='center', ha='center', color="black", fontsize=8)

        self.ax.set_xticks(np.arange(0, cols, 1))
        self.ax.set_yticks(np.arange(0, rows, 1))
        self.ax.set_xticklabels(range(cols))
        self.ax.set_yticklabels(range(rows))
        self.ax.set_xticks(np.arange(-.5, cols, 1), minor=True)
        self.ax.set_yticks(np.arange(-.5, rows, 1), minor=True)
        self.ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
        self.ax.tick_params(which="minor", size=0)
        self.ax.invert_yaxis()

        self.fig.canvas.draw()
        plt.pause(0.1)

    # Simulate rolling two six-sided dice and return the total.
    def roll_dice(self):
        return random.randint(1, 6) + random.randint(1, 6)

    # Get user input with the provided prompt, allowing 'quit' to exit the game.
    def get_input(self, prompt):
        user_input = input(prompt).strip().lower()
        if user_input == 'quit':
            print("The game has been quit.")
            exit()
        return user_input

    # Main game loop for player turns and actions.
    def start_game(self):
        print("The game has started!")
        for player in self.players:
            print(f"{player.name}'s cards: {player.show_cards()}")

        # Place all players at the starting position.
        start_space = (5, 6)
        start_position = self.mansion.grid[start_space[0]][start_space[1]]
        for player in self.players:
            if start_position:
                player.move(start_position, start_space)
                player.current_position = start_position

        self.update_visualization()
        game_over = False
        current_player_index = 0

        # Loop until the game ends.
        while not game_over:
            current_player = self.players[current_player_index]
            if current_player.is_active:
                print(f"{current_player.name}'s turn:")
                action = self.get_input("Enter 'move', 'suggest', 'accuse', 'secret', or 'quit': ")
                # Process the player's chosen action.
                if action == 'move':
                    print("To move, enter the grid coordinates in the format (row, column). Example: '1, 1'.")
                    # Player chooses to move on the board.
                    dice_roll = self.roll_dice()
                    print(f"You rolled a {dice_roll}.")
                    current_position = current_player.current_position
                    valid_move = False
                    while not valid_move:
                        try:
                            # Get input from user for move
                            destination = self.get_input("Enter the coordinates of the next space to move to (e.g., '1, 1'): ")
                            # print(f"Debug: Raw input received for destination: {destination}")
                            destination = tuple(map(int, destination.split(',')))
                            # print(f"Debug: Parsed destination coordinates: {destination}")
                            r, c = destination
                            if 0 <= r < len(self.mansion.grid) and 0 <= c < len(self.mansion.grid[0]):
                                new_position = self.mansion.grid[r][c]
                                # print(f"Debug: New position object at ({r}, {c}): {new_position}")
                                if new_position and isinstance(new_position, (Room, Space)):
                                    current_r, current_c = self.get_coordinates(current_position)
                                    movement_distance = abs(current_r - r) + abs(current_c - c)

                                    # Catch errors for illegal move
                                    if movement_distance <= dice_roll:

                                        current_player.move(new_position, (r, c))
                                        print(f"{current_player.name} moved to {new_position.name}.")
                                        self.update_visualization()
                                        valid_move = True
                                    else:
                                        print(f"Invalid move. You can only move up to {dice_roll} spaces, but your intended move is {movement_distance} spaces.")
                                else:
                                    print("Invalid destination. Try again.")
                            else:
                                print("Coordinates out of range. Try again.")
                        except (ValueError, IndexError):
                            print("Invalid format. Please enter the coordinates as 'row, column'. Example: '1, 1'.")

                        if not valid_move:
                            continue

                elif action == 'suggest':
                    # Player chooses to suggest on the board.
                    print("To suggest, enter the name of the character and weapon. Example: 'Professor Plum', 'Candlestick'.")
                    if not current_player.can_make_suggestion():
                        print("You must be in a room to make a suggestion.")
                        continue
                    else:
                        # Automatically gather room
                        print(f"Room: {player.current_position.name}")
                        available_characters = [card.name for card in self.available_choices if card.card_type == 'character' and card not in current_player.cards]
                        available_weapons = [card.name for card in self.available_choices if card.card_type == 'weapon' and card not in current_player.cards]
                        print(f"Available characters: {', '.join(available_characters)}")
                        print(f"Available weapons: {', '.join(available_weapons)}")

                        lowercase_characters = [character.lower() for character in available_characters]
                        lowercase_weapons = [weapons.lower() for weapons in available_weapons]
                        
                        # Get user input for suggestion
                        character = None
                        while character not in lowercase_characters:
                            character = self.get_input("Enter the character: ")
                            if character not in lowercase_characters:
                                print(f"You must enter a character that is available: {', '.join(available_characters)}")

                        weapon = None
                        while weapon not in lowercase_weapons:
                            weapon = self.get_input("Enter the weapon: ")
                            if weapon not in lowercase_weapons:
                                print(f"You must enter a weapon that is available: {', '.join(available_weapons)}")

                        suggestion = current_player.make_suggestion(current_player.current_position.name.lower(), character, weapon)
                        print(f"{current_player.name} suggests: {suggestion}")

                        # Disprove player suggestion
                        disproved = False
                        for other_player in self.players:
                            if other_player != current_player:
                                for card in other_player.cards:
                                    if card.name.lower() in [character, weapon, current_player.current_position.name.lower()]:
                                        print(f"{other_player.name} can disprove the suggestion with the card: {card.name}")
                                        disproved = True
                                        # Add the disproved card to player information
                                        current_player.add_card(card)
                                        print(f"{current_player.name} now has the card: {card.name}")
                                        break
                                if disproved:
                                    break

                        if not disproved:
                            print("No one can disprove the suggestion.")

                elif action == 'accuse':
                    # Player chooses to accuse on the board.
                    print("To accuse, enter the name of the room, character, and weapon. Example: 'Kitchen', 'Professor Plum', 'Candlestick'.")

                    accuse_rooms = [card.name for card in self.available_choices if card.card_type == 'room']
                    accuse_characters = [card.name for card in self.available_choices if card.card_type == 'character']
                    accuse_weapons = [card.name for card in self.available_choices if card.card_type == 'weapon']
                    
                    # Provide availabe choices
                    print(f"Available rooms: {', '.join(accuse_rooms)}")
                    print(f"Available characters: {', '.join(accuse_characters)}")
                    print(f"Available weapons: {', '.join(accuse_weapons)}")
                    
                    lowercase_accuse_characters = [character.lower() for character in accuse_characters]
                    lowercase_accuse_weapons = [weapons.lower() for weapons in accuse_weapons]
                    lowercase_accuse_rooms = [weapons.lower() for weapons in accuse_rooms]

                    # Get use inputs for accusation
                    room = None
                    while room not in lowercase_accuse_rooms:
                        room = self.get_input("Enter the room: ")
                        if room not in lowercase_accuse_rooms:
                            print(f"You must enter a room that is available: {', '.join(accuse_rooms)}")

                    character = None
                    while character not in lowercase_accuse_characters:
                        character = self.get_input("Enter the character: ")
                        if character not in lowercase_accuse_characters:
                            print(f"You must enter a character that is available: {', '.join(accuse_characters)}")

                    weapon = None
                    while weapon not in lowercase_accuse_weapons:
                        weapon = self.get_input("Enter the weapon: ")
                        if weapon not in lowercase_accuse_weapons:
                            print(f"You must enter a weapon that is available: {', '.join(accuse_weapons)}")

                    accusation = current_player.make_accusation(room, character, weapon, self.solution)
                    if accusation[-1] == "correct":
                        # Player wins the game
                        print(f"{current_player.name} has won the game with the correct accusation!")
                        print("""
                                                                                                              
  ██╗   ██╗ ██████╗ ██╗   ██╗    ██╗    ██╗██╗███╗   ██╗ ██╗██╗
  ╚██╗ ██╔╝██╔═══██╗██║   ██║    ██║    ██║██║████╗  ██║ ██║██║
   ╚████╔╝ ██║   ██║██║   ██║    ██║ █╗ ██║██║██╔██╗ ██║ ██║██║
    ╚██╔╝  ██║   ██║██║   ██║    ██║███╗██║██║██║╚██╗██║ ╚═╝╚═╝
     ██║   ╚██████╔╝╚██████╔╝    ╚███╔███╔╝██║██║ ╚████║ ██║██║
     ╚═╝    ╚═════╝  ╚═════╝      ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝ ╚═╝╚═╝

                              """)
                        game_over = True
                    else:
                        # Player is eliminated from the game
                        print(f"{current_player.name}'s accusation was incorrect. They are eliminated from the game.")
                        current_player.move(None, None)
                        self.num_players_elim += 1
                        self.update_visualization()
                        valid_move = True

                elif action == 'secret':
                    # Player chooses to use secret passage on the board.
                    print("To use a secret passage, you must be in a room with a secret passage and roll an even number.")
                    current_room = current_player.current_position
                    if isinstance(current_room, Room):
                        secret_passages = {
                            'Study': 'Kitchen',
                            'Kitchen': 'Study',
                            'Conservatory': 'Lounge',
                            'Lounge': 'Conservatory'
                        }
                        # Player rolls dice to see if they can use the secret passage
                        if current_room.name.split()[0] in secret_passages:
                            print(f"There is a secret passage to the {secret_passages[current_room.name.split()[0]]}.")
                            dice_roll = self.roll_dice()
                            print(f"You rolled a {dice_roll}.")
                            if dice_roll % 2 == 0:
                                new_room_name = secret_passages[current_room.name.split()[0]]
                                new_room = self.mansion.get_room(new_room_name)
                                current_player.move(new_room, self.get_coordinates(new_room))
                                print(f"{current_player.name} used the secret passage to move to {new_room.name}.")
                                self.update_visualization()
                            else:
                                print("You rolled an odd number. You cannot use the secret passage this turn.")
                        else:
                            print("There is no secret passage in this room.")
                            continue
                    else:
                        print("You must be in a room to use a secret passage.")
                        continue

                else:
                    # Error catch for incorrect input
                    print("Invalid action. Please enter 'move', 'suggest', 'accuse', 'secret', or 'quit'.")
                    continue
            if len(self.players) == self.num_players_elim:
                # Game ends if all players are eliminated
                print(f"No players remain, the game is over.")
                print(f"The solution was Room: {self.solution.room}, Character: {self.solution.character}, Weapon: {self.solution.weapon}")
                print(f"Thanks for playing, better luck next time!")
                exit()
            else:
                # Advance to the next player.
                current_player_index = (current_player_index + 1) % len(self.players)

    def get_coordinates(self, position):
        # Get the grid
        if position is None:
            raise ValueError("The provided position is None. Please ensure the player is properly initialized and moved.")
        for r in range(len(self.mansion.grid)):
            for c in range(len(self.mansion.grid[0])):
                if self.mansion.grid[r][c] == position:
                    return r, c
        raise ValueError(f"The position '{position}' was not found in the mansion grid. Please ensure the grid and player positions are properly tracked.")

if __name__ == "__main__":
    game = GameManager()
    game.setup_game(["Player 1", "Player 2", "Player 3"])
    game.start_game()