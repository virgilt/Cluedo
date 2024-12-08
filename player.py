from solution import Solution
from room import Room
class Player:
    def __init__(self, name, start_position, start_coordinates=None):
        # Initialize a player with a name, starting position, and optional coordinates.
        self.name = name  # Name of the player.
        self.current_position = start_position  # The player's current position on the board.
        self.current_coordinates = start_coordinates  # Coordinates on the grid.
        self.cards = []  # Cards held by the player.
        self.is_active = True  # Indicates if the player is still in the game.

    # Update the player's position and coordinates.
    def move(self, new_position, coordinates):
        self.current_position = new_position
        self.current_coordinates = coordinates

    # Add a card to the player's hand.
    def add_card(self, card):
        self.cards.append(card)

    # Check if the player can make a suggestion (must be in a room).
    def can_make_suggestion(self):
        return isinstance(self.current_position, Room)

    # Check if the player can make an accusation (must be active in the game).
    def can_make_accusation(self):
        return self.is_active

    # Make a suggestion for the murder details.
    def make_suggestion(self, room, character, weapon):
        if not self.can_make_suggestion():
            raise ValueError("Player must be in a room to make a suggestion.")
        return (room, character, weapon, "suggestion")
    
    # Make an accusation and check if it matches the solution.
    def make_accusation(self, room, character, weapon, solution: Solution):
        if not self.can_make_accusation():
            raise ValueError("Eliminated players cannot make an accusation.")
        if solution.room.lower() == room and solution.weapon.lower() == weapon and solution.character.lower() == character:
            return (room, character, weapon, "accusation", "correct")
        else:
            self.eliminate()
            return (room, character, weapon, "accusation", "incorrect")
    
    # Eliminate the player from the game.
    def eliminate(self):
        self.is_active = False

    # Display the cards held by the player.
    def show_cards(self):
        return self.cards

    # Representation of the player for debugging.
    def __repr__(self):
        return f"Player({self.name}, Position: {self.current_position}, Active: {self.is_active})"