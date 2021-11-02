from button import Button
from popup import Popup 
from screen import GameScreen
import pygame

class HostMenu(GameScreen):
    
    def __init__(self, control):
        super(HostMenu, self).__init__(control)
        self.network = control.network
        self.player = control.player
        
        # Image / Button goes here vvvv
        self.buttonBack = Button(130, 130, 80, 35)
        self.buttonBack.addText('Back', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonCreateLobby = Button(900, 130, 250, 35)
        self.buttonCreateLobby.addText('Create Lobby', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonReduce = Button(130, 200, 55, 35)
        self.buttonReduce.addText('-', self.font, 20, pygame.Color('white'), pygame.Color('orange'), pygame.Color('darkgrey'))
        self.buttonAdd = Button(255, 200, 55, 35)
        self.buttonAdd.addText('+', self.font, 20, pygame.Color('white'), pygame.Color('darkgreen'), pygame.Color('darkgrey'))
        

        self.numPlayer = 5
        self.rectNumPlayer = pygame.Rect(self.buttonReduce.rect.right, self.buttonAdd.rect.y, 
        self.buttonAdd.rect.left - self.buttonReduce.rect.right, self.buttonAdd.rect.height)

        self.woodBoard = pygame.transform.scale(control.woodBoard2, (1080, 520))
        self.popupBackground = control.popupBackground

        self.numberWarnPopup = Popup((self.display.get_width() - 600)//2, (self.display.get_height() - 250)//2, 600, 250, 
        'PLAYER HAVE TO BE ATLEAST 5/> or NOT MORE THAN 10/>', pygame.Color('white'), pygame.Color('aquamarine2'))
        self.numberWarnPopup.adjustComponents(bWidth=70, fontPath=None)
        self.numberWarnPopup.modComponents(self.numberWarnPopup.b1, 'button', pygame.Color('lightsalmon3'), pygame.Color('lightsalmon4'), 
        'CLOSE', self.font1, 22)
        
        self.lobbyFailPopup = Popup((self.display.get_width() - 500)//2, (self.display.get_height() - 200)//2, 500, 200, 
        'Failed/> to create lobby/>', pygame.Color('white'), pygame.Color('aquamarine2'))
        self.lobbyFailPopup.adjustComponents(bWidth=70, fontPath=None)
        self.lobbyFailPopup.modComponents(self.lobbyFailPopup.b1, 'button', pygame.Color('lightsalmon3'), pygame.Color('lightsalmon4'), 
        'CLOSE', self.font1, 22)

        self.numberWarning = False
        self.lobbyFailed = False
        self.available = True
    
    def displayScreen(self):

        self.displayRunning = True
        
        while self.displayRunning:

            self.checkEvent()
            fontColor = pygame.Color('black')
            # page blackground
            self.display.fill((0, 0, 0))

            self.display.blit(self.woodBoard, (100, 100, 1080, 520))

            self.drawText('Host Menu', 20 , self.screenWidth/2, 100, self.font, self.control.white)

            numPlayerSurface = pygame.font.Font(self.font, 20).render(str(self.numPlayer), True, fontColor)
            pygame.draw.rect(self.display, pygame.Color('white'), self.rectNumPlayer)
            self.display.blit(numPlayerSurface, (self.rectNumPlayer.centerx - numPlayerSurface.get_width()//2, self.rectNumPlayer.centery - numPlayerSurface.get_height()//2))

            self.buttonAdd.draw(self.display)
            self.buttonReduce.draw(self.display)
            self.buttonBack.draw(self.display)
            self.buttonCreateLobby.draw(self.display)

            if self.available:
                if self.buttonReduce.isButtonClick():
                    self.numPlayer -= 1
                    if self.numPlayer < 5:
                        self.numPlayer = 5
                        self.numberWarning = True
                if self.buttonAdd.isButtonClick():
                    self.numPlayer += 1
                    if self.numPlayer > 10:
                        self.numPlayer = 10
                        self.numberWarning = True

                if self.buttonBack.isButtonClick():
                    if self.network.connectStatus == True:
                        self.network.disconnectFromServer()
                    self.changePageByInput(True)

                if self.buttonCreateLobby.isButtonClick():
                    if self.network.createLobby(self.numPlayer, [True, False, True, False, True, False, True, False], 0, 0):
                        self.player.host = True
                        self.changePageByInput(True, self.control.createPlayer)
                    else:
                        print("[GAME] Cannot create lobby") # pop up error
                        self.lobbyFailed = True

            if self.numberWarning:
                self.numberWarnPopup.draw(self.display, self.font1, 28, textAlign = 'centerAlign', bgColor = None,
                image = self.popupBackground)
                self.available = False
                if self.numberWarnPopup.b1.isButtonClick():
                    self.available = True
                    self.numberWarning = False
            if self.lobbyFailed:
                self.lobbyFailPopup.draw(self.display, self.font1, 52, textAlign = 'centerAlign', bgColor = None,
                image = self.popupBackground)
                self.available = False
                if self.lobbyFailPopup.b1.isButtonClick():
                    self.available = True
                    self.lobbyFailed = False

            self.biltScreen() # update screen