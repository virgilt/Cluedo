from room import Room
from space import Space

class Mansion:
    def __init__(self, room_cards):
        # Initialize the mansion with rooms based on the provided room cards.
        self.rooms = {}  # Dictionary of room names to Room objects.
        self.spaces = {}  # Dictionary of space names to Space objects.
        self.grid = []  # 2D grid representing the mansion layout.
        self._initialize_mansion(room_cards)
    
    # Create Room objects for each card and populate the rooms dictionary.
    def _initialize_mansion(self, room_cards):
        for card in room_cards:
            self.rooms[card.name] = Room(card.name)
        
        # Define the mansion grid dimensions.
        rows, cols = 10, 12
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

        # Define positions for the rooms in the mansion grid.
        room_positions = [
            (0, 0), (0, 7), (0, 11), (4, 0), (8, 0), (9, 5), (9, 11), (0, 3), (6, 11), (9, 2), (9, 9)
        ]

        # Place Room objects in their grid positions.
        for pos, card in zip(room_positions, room_cards):
            r, c = pos
            self.grid[r][c] = self.rooms[card.name]

        # Add a starting space at the center of the grid.
        middle_row, middle_col = rows // 2, cols // 2
        self.grid[middle_row][middle_col] = self.rooms.get("Start Space", Room("Start Space"))

        # Fill the rest of the grid with Space objects.
        for r in range(rows):
            for c in range(cols):
                if self.grid[r][c] is None:
                    space_name = f"Space_{r}_{c}"
                    self.spaces[space_name] = Space(space_name)
                    self.grid[r][c] = self.spaces[space_name]

        # Establish connections between adjacent Space objects.
        for r in range(rows):
            for c in range(cols):
                current_tile = self.grid[r][c]
                if isinstance(current_tile, Space):
                    if r > 0 and isinstance(self.grid[r - 1][c], Space):
                        current_tile.add_connection(self.grid[r - 1][c])
                    if r < rows - 1 and isinstance(self.grid[r + 1][c], Space):
                        current_tile.add_connection(self.grid[r + 1][c])
                    if c > 0 and isinstance(self.grid[r][c - 1], Space):
                        current_tile.add_connection(self.grid[r][c - 1])
                    if c < cols - 1 and isinstance(self.grid[r][c + 1], Space):
                        current_tile.add_connection(self.grid[r][c + 1])

        # Add secret passages between specific rooms.
        if "Study" in self.rooms and "Kitchen" in self.rooms:
            self.rooms["Study"].set_secret_passage(self.rooms["Kitchen"])
            self.rooms["Kitchen"].set_secret_passage(self.rooms["Study"])
        if "Conservatory" in self.rooms and "Lounge" in self.rooms:
            self.rooms["Conservatory"].set_secret_passage(self.rooms["Lounge"])
            self.rooms["Lounge"].set_secret_passage(self.rooms["Conservatory"])

    # Get a Room object by its name.
    def get_room(self, name):
        return self.rooms.get(name, None)

    # Get a Space object by its name.
    def get_space(self, name):
        return self.spaces.get(name, None)

    # Get a representation of the mansion layout.
    def show_mansion_layout(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                tile = self.grid[r][c]
                if isinstance(tile, Room):
                    secret = f" (Secret passage to {tile.secret_passage.name})" if tile.secret_passage else ""
                    print(f"Room: {tile.name}{secret}")
                elif isinstance(tile, Space):
                    connections_list = tile.get_connections() if tile.get_connections() else []
                    connections = ", ".join([connected_space.name for connected_space in connections_list])
                    print(f"Space {tile.name}: Connected to -> {connections}")