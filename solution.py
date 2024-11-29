import random

class Solution:
    def __init__(self, rooms, characters, weapons):
        self.room = random.choice(rooms)
        self.character = random.choice(characters)
        self.weapon = random.choice(weapons)

    def __eq__(self, other):
        return (self.room == other[0] and
                self.character == other[1] and
                self.weapon == other[2])

    def __repr__(self):
        return f"Solution(Room: {self.room}, Character: {self.character}, Weapon: {self.weapon})"