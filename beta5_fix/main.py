from gameControl import StateControl

gameState = StateControl()

# Start music at first time 
gameState.currentMusic.load(gameState.musicList[0])
gameState.currentMusic.play(-1)

while gameState.running:
    gameState.currentState.displayScreen()