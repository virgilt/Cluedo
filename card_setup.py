import random

class Card:
    def __init__(self, name, card_type):
        # Initializes a card with a name and type (character, weapon, or room).
        self.name = name
        self.card_type = card_type

    def __repr__(self):
        # Provides a string representation of the card for debugging.
        return f"Card({self.name}, Type: {self.card_type})"

# Creates a deck of Cluedo cards categorized by characters, weapons, and rooms.
def create_card_deck():
    characters = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
    weapons = ["Knife", "Candlestick", "Revolver", "Rope", "Lead Pipe", "Wrench"]
    rooms = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Lounge", "Hall", "Study", "Library", "Billiard Room"]

    # Creating the card deck
    cards = [Card(name, 'character') for name in characters] + \
            [Card(name, 'weapon') for name in weapons] + \
            [Card(name, 'room') for name in rooms]

    # Shuffle the cards
    random.shuffle(cards)
    return cards

# Distribute cards among players
def distribute_cards(players, cards):
    """
    Distribute the cards evenly among players.
    :param players: List of Player objects
    :param cards: List of Card objects
    """
    num_players = len(players)
    for i, card in enumerate(cards):
        players[i % num_players].add_card(card)

if __name__ == "__main__":
    from player import Player

    # Create players
    players = [Player("Player 1", None), Player("Player 2", None), Player("Player 3", None)]

    # Create and shuffle the card deck
    card_deck = create_card_deck()

    # Distribute the cards among the players
    distribute_cards(players, card_deck)

    # Show each player's cards
    for player in players:
        print(f"{player.name}'s cards: {player.show_cards()}")