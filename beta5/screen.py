import pygame, sys, random
from button import Button

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

        # sound
        #self.clickChoiceSound = self.control.soundList[2]

        # Image
        self.buttonBG = self.control.buttonBG

        self.fullHowToPlay = self.control.howToPlay
        self.amountOfFullHowToPlayPage = len(self.fullHowToPlay)

        self.howToPlay = []
        self.amountOfHowToPlayPage = len(self.howToPlay)

        self.tapeRightArrow = self.control.tapeRightArrow
        self.tapeLeftArrow = self.control.tapeLeftArrow
        self.tapeArrowWidth = self.tapeLeftArrow.get_rect().width
        self.tapeArrowHeight = self.tapeLeftArrow.get_rect().height
        self.tapeClose = self.control.tapeClose
        self.tapeCloseWidth = self.tapeClose.get_rect().width
        self.tapeCloseHeight = self.tapeClose.get_rect().height

        self.currentPage = 0
        self.howToPlayStatus = False

        self.buttonTapeRight = Button(self.screenWidth - self.tapeArrowWidth - 80, self.screenHeight//2 - 20, self.tapeArrowWidth, self.tapeArrowHeight)
        self.buttonTapeRight.addImage(self.tapeRightArrow)

        self.buttonTapeLeft = Button(80, self.screenHeight//2 - 20, self.tapeArrowWidth, self.tapeArrowHeight)
        self.buttonTapeLeft.addImage(self.tapeLeftArrow)

        self.buttonClose = Button(self.screenWidth - self.tapeCloseWidth - 120, 20, self.tapeCloseWidth, self.tapeCloseHeight)
        self.buttonClose.addImage(self.tapeClose)

        self.buttonHowToPlay = None

        self.buttonHowToPlayList = (self.buttonClose, self.buttonTapeLeft, self.buttonTapeRight)

        
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

    def howToPlaySetup(self, x, y, text, pageList = [1,1,1,1,1,1,1,1,1,1]):
        self.buttonHowToPlay = Button(x, y, 170, 60)
        self.buttonHowToPlay.addText( text, self.font1, 30, self.control.white, (50,50,50))
        self.buttonHowToPlay.addImage(self.buttonBG)

        self.howToPlay = []
        n = 0
        for i in pageList:
            if i == 1:
                self.howToPlay.append( self.fullHowToPlay[n])
            n += 1
        self.amountOfHowToPlayPage = len(self.howToPlay)
    # create all buttons needed and 

    def howToPlayDraw(self, paperSound, backSound, available):
        self.buttonHowToPlay.draw(self.display, available)
        if available:
            if self.buttonHowToPlay.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()):
                self.howToPlayStatus = True

        if self.howToPlayStatus:
                self.display.blit(self.howToPlay[self.currentPage], (0, 0))
                for button in self.buttonHowToPlayList:
                    button.draw(self.display, available)
                if self.buttonTapeLeft.isButtonClick(random.choice(paperSound),self.control.getSoundEffectVol()):
                    if self.currentPage == 0:
                            self.currentPage = self.amountOfHowToPlayPage-1
                    else:
                        self.currentPage -= 1
                if self.buttonTapeRight.isButtonClick(random.choice(paperSound),self.control.getSoundEffectVol()):
                    if self.currentPage == self.amountOfHowToPlayPage-1:
                        self.currentPage = 0
                    else:
                        self.currentPage += 1
                if self.buttonClose.isButtonClick(backSound,self.control.getSoundEffectVol()):
                    self.howToPlayStatus = False
                    return False
                else:
                    return True
        else:
            self.currentPage = 0
            return False
    