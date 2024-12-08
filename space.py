class Space:
    def __init__(self, name):
        # Initialize a space with a name and a list of connected spaces.
        self.name = name  # Name of the space.
        self.connected_spaces = []  # List of spaces connected to this one.

    # Add a connection to another space.
    def add_connection(self, space):
        if space not in self.connected_spaces:
            self.connected_spaces.append((space))
    
    # Get all spaces connected to this space.
    def get_connections(self):
        return self.connected_spaces
    
    # Representation of the space for debugging purposes.
    def __repr__(self):
        return f"Space({self.name})"