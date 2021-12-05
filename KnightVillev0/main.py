from gameControl import StateControl
'''
main.py - main file to run the game.

last updated: 27 Oct 2021
'''

# Init game
gameState = StateControl()

# Start game
if __name__ == "__main__":
    
    # Start music at first time 
    gameState.currentMusic.load(gameState.musicList[0])
    gameState.currentMusic.play(-1)

    while gameState.running:
        gameState.currentState.displayScreen()