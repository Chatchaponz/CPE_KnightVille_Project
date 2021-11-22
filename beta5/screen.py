import pygame, sys

class GameScreen():

    def __init__(self, control):
        self.control = control

        self.display = pygame.Surface((self.control.displayWidth, self.control.displayHeight))
        self.screenWidth = control.displayWidth
        self.screenHeight = control.displayHeight
        
        # clock (frame rate)
        self.clock = pygame.time.Clock()

        # Font
        self.font = 'font\Taviraj-Black.TTF'
        self.font1 = 'font/Black-Chancery.TTF'
        self.font2 = 'font/Dragon Fire.TTF'
        
    def blitScreen(self):
        self.control.screen.blit(self.display, (0, 0))
        pygame.display.update()
    
    def changePageByButton(self, button, page = None):
        buttonClick = button.isButtonClick()
        self.changePageByInput(buttonClick, page)
    
    def changePageByInput(self, input, state = None):
        previousStateLength = len(self.control.previousState)
        if input:
            if state == None and previousStateLength > 0:
                # if state == None just go back
                self.control.changeState(self.control.goBack())
            elif (previousStateLength > 0 and 
                self.control.previousState[-1] == state):
                # if next state equal previous state
                self.control.changeState(self.control.goBack())
            else:
                self.control.saveState()
                self.control.changeState(state)
            self.displayRunning = False

    def drawText(self, text, size, x, y, font, color):
        font = pygame.font.Font(font, size)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.center = (x, y)
        self.display.blit(textSurface, textRect)

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
                self.control.currentState.displayRunning = False
                pygame.quit()
                sys.exit()