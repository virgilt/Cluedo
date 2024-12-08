class Room:
    def __init__(self, name):
        # Initialize a room with a name and optional connections or secret passages.
        self.name = name  # Name of the room.
        self.connected_spaces = []  # List of spaces directly connected to this room.
        self.secret_passage = None  # Room connected by a secret passage, if any.
    
    # Add a connecting space to the room.
    def add_connection(self, space):
        if space not in self.connected_spaces:
            self.connected_spaces.append(space)

    # Set a secret passage to another room.
    def set_secret_passage(self, room):
        self.secret_passage = room
    
    # Get all connected spaces for this room.
    def get_connections(self):
        return self.connected_spaces
    
    # Representation of the room for debugging purposes.
    def __repr__(self):
        return f"Space({self.name})"