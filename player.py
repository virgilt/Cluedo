from solution import Solution
from room import Room
class Player:
    def __init__(self, name, start_position, start_coordinates=None):
        self.name = name
        self.current_position = start_position
        self.current_coordinates = start_coordinates
        self.cards = []
        self.is_active = True

    def move(self, new_position, coordinates):
        self.current_position = new_position
        self.current_coordinates = coordinates

    def add_card(self, card):
        self.cards.append(card)

    def can_make_suggestion(self):
        return isinstance(self.current_position, Room)

    def can_make_accusation(self):
        return self.is_active

    def make_suggestion(self, room, character, weapon):
        if not self.can_make_suggestion():
            raise ValueError("Player must be in a room to make a suggestion.")
        return (room, character, weapon, "suggestion")
    
    def make_accusation(self, room, character, weapon, solution: Solution):
        if not self.can_make_accusation():
            raise ValueError("Eliminated players cannot make an accusation.")
        if solution.room.lower() == room and solution.weapon.lower() == weapon and solution.character.lower() == character:
            return (room, character, weapon, "accusation", "correct")
        else:
            self.eliminate()
            return (room, character, weapon, "accusation", "incorrect")
    
    def eliminate(self):
        self.is_active = False

    def show_cards(self):
        return self.cards

    def __repr__(self):
        return f"Player({self.name}, Position: {self.current_position}, Active: {self.is_active})"