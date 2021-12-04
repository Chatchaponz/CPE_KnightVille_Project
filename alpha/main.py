from state import StateControl

gameState = StateControl()

while gameState.Running:
    gameState.currentState.displayScreen()