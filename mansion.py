from room import Room
from space import Space

class Mansion:
    def __init__(self):
        self.rooms = {}
        self.spaces= {}
        self._initialize_mansion()
    
    def _initialize_mansion(self):
        room_names = ["Kitchen", "Dining Room", "Lounge", "Ballroom", "Hall", "Conservatory", "Billiard Room", "Library", "Study"]

        for name in room_names:
            self.rooms[name] = Room(name)