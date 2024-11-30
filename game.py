from game_manager import GameManager

if __name__ == "__main__":
    game = GameManager()
    
    game.setup_game(["Player 1", "Player 2", "Player 3"])
    
    game.start_game()