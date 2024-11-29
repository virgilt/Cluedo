class Player:
    def __init__(self, name, start_position):
        self.name = name
        self.current_position = start_position
        self.cards = []
        self.is_active = True

    def move(self, new_position):
        self.current_position = new_position

    def add_card(self, card):
        self.cards.append(card)

    def make_suggestion(self, room, character, weapon):
        return (room, character, weapon)
    
    def make_accusation(self, room, character, weapon):
        return (room, character, weapon)
    
    def eliminate(self):
        self.is_active = False

    def __repr__(self):
        return f"Player({self.name}, Position: {self.current_position}, Active: {self.is_active})"