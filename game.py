from game_manager import GameManager

if __name__ == "__main__":
    game = GameManager()
    
    game.setup_game(["P1", "P2", "P3"])
    
    game.start_game()