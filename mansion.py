from room import Room
from space import Space

class Mansion:
    def _init_(self):
        self.rooms = {}
        self.spaces= {}
        self._initialize_mansion()
    
    def _initialize_mansion(self):
        room_names = ["Kitchen", "Dining Room", "Lounge", "Ballroom", "Hall", "Conservatory", "Billiard Room", "Library", "Study"]

        for name in room_names:
            self.room[name] = Room(name)

        space_names = [f"Space {i}" for i in range(1, 49)]

        for name in space_names:
            self.spaces[name] = Space(name)