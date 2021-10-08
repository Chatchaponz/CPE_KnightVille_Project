import pygame


class GameScreen():

    def __init__(self, state):
        self.state = state

        # Display size
        self.displayWidth = 1280
        self.displayHeight = 720

        self.display = pygame.Surface((self.displayWidth, self.displayHeight))
        self.screen = pygame.display.set_mode((self.displayWidth, self.displayHeight))

        # Font
        self.font = 'Taviraj-Black.TTF'

        # Default color
        self.white = (255, 255, 255)

    
    def biltScreen(self):
        self.screen.blit(self.display, (0, 0))
        pygame.display.update()
        # self.state.resetKeys()
    
    def changePageByButton(self, button, page):
        buttonClick = button.isButtonClick(50) # wait 50 ms
        self.changePageByInput(buttonClick, page)
    
    def changePageByInput(self, input, state):
        if input: 
            self.state.currentState = state
            self.displayRunning = False
        # self.state.resetKeys()
    
    def drawText(self, text, size, x, y):
        font = pygame.font.Font(self.font, size)
        textSurface = font.render(text, True, self.white)
        textRect = textSurface.get_rect()
        textRect.center = (x, y)
        self.display.blit(textSurface, textRect)