class Room:
    def _init_(self, name):
        self.name = name
        self.connected_spaces = []
        self.secret_passage = None
    
    def add_connection(self, space):
        if space not in self.connected_spaces:
            self.connected_spaces.append(space)
    
    def get_connections(self):
        return self.connected_spaces
    
    def _repr_(self):
        return f"Space({self.name})"