from room import Room

class Mansion:
    def _init_(self):
        self.rooms = {}
        self.spaces= {}
        self._initialize_mansion()
    
    def _initialize_mansion(self):
        room_names = ["Kitche", "Dining Room", "Lounge", "Ballroom", "Hall", "Conservatory", "Billiard Room", "Library", "Study"]

        for name in room_names:
            self.room[name] = Room(name)