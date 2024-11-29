from room import Room
from space import Space

class Mansion:
    def __init__(self):
        self.rooms = {}
        self.spaces = {}
        self.grid = []
        self._initialize_mansion()
    
    def _initialize_mansion(self):
        room_names = ["Kitchen", "Dining Room", "Lounge", "Ballroom", "Hall", "Conservatory", "Billiard Room", "Library", "Study", "Start Space"]

        for name in room_names:
            self.rooms[name] = Room(name)
        
        rows, cols = 10, 12
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

        room_positions = [
            (0, 0), (0, 7), (0, 11), (4, 0), (8, 0), (9, 5), (9, 11), (0, 3), (6, 11), (9, 2), (9, 9)]

        for pos, name in zip(room_positions, room_names[:-1]):
            r, c = pos
            self.grid[r][c] = self.rooms[name]

        middle_row, middle_col = rows // 2, cols // 2
        self.grid[middle_row][middle_col] = self.rooms["Start Space"]

        for r in range(rows):
            for c in range(cols):
                if self.grid[r][c] is None:
                    space_name = f"Space_{r}_{c}"
                    self.spaces[space_name] = Space(space_name)
                    self.grid[r][c] = self.spaces[space_name]

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

        self.rooms["Study"].set_secret_passage(self.rooms["Kitchen"])
        self.rooms["Kitchen"].set_secret_passage(self.rooms["Study"])
        self.rooms["Conservatory"].set_secret_passage(self.rooms["Lounge"])
        self.rooms["Lounge"].set_secret_passage(self.rooms["Conservatory"])

    def get_room(self, name):
        return self.rooms.get(name, None)

    def get_space(self, name):
        return self.spaces.get(name, None)

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