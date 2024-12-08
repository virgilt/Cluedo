from game_manager import GameManager

if __name__ == "__main__":
    # Initialize the game manager instance to manage the game state and flow.
    game = GameManager()
    
    # Set up the game with three players. Replace "P1", "P2", "P3" with actual player names if desired.
    game.setup_game(["P1", "P2", "P3"])
    
    # Start the game, initiating the game loop where players take turns.
    game.start_game()