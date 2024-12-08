import random

class Solution:
    def __init__(self, rooms, characters, weapons):
        # Initialize the solution with the room, character, and weapon involved in the mystery.
        self.room = rooms  # The correct room.
        self.character = characters  # The correct character.
        self.weapon = weapons  # The correct weapon.

    # Define comparison for the solution.
    def __eq__(self, other):
        # Returns True if the room, character, and weapon match.
        return (self.room == other[0] and
                self.character == other[1] and
                self.weapon == other[2])

    # Representation of the solution for debugging purposes.
    def __repr__(self):
        return f"Solution(Room: {self.room}, Character: {self.character}, Weapon: {self.weapon})"