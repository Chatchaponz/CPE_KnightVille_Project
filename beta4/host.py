from button import Button
from popup import Popup 
from screen import GameScreen
import pygame

class HostMenu(GameScreen):
    
    def __init__(self, control):
        super(HostMenu, self).__init__(control)
        self.network = control.network
        self.player = control.player
        
        # Button
        self.buttonBack = Button(130, 130, 80, 35)
        self.buttonBack.addText('Back', self.font1, 20, (255,255,255), 1, (50,50,50))

        self.buttonCreateLobby = Button(900, 130, 250, 35)
        self.buttonCreateLobby.addText('Create Lobby', self.font1, 20, (255,255,255), 1, (50,50,50))

        self.buttonLeft = Button(130, 200, 55, 35)
        self.buttonLeft.addText('←', self.font1, 20, pygame.Color('white'), pygame.Color('orange'), pygame.Color('darkgrey'))
        
        self.buttonRight = Button(255, 200, 55, 35)
        self.buttonRight.addText('→', self.font1, 20, pygame.Color('white'), pygame.Color('darkgreen'), pygame.Color('darkgrey'))
        
        # Player numbers
        self.numPlayer = 5
        self.rectNumPlayer = pygame.Rect(self.buttonLeft.rect.right, self.buttonRight.rect.y, 
        self.buttonRight.rect.left - self.buttonLeft.rect.right, self.buttonRight.rect.height)

        # Background
        self.woodBoard = pygame.transform.scale(control.woodBoard2, (1080, 520))
        self.popupBackground = control.popupBackground



        # Role optimize using image button
        # self.roleButton = Button()
    
    def displayScreen(self):

        self.displayRunning = True
        
        while self.displayRunning:

            self.checkEvent()
            fontColor = pygame.Color('black')
            # page blackground
            self.display.fill((0, 0, 0))

            self.display.blit(self.woodBoard, (100, 100, 1080, 520))

            self.drawText('Host Menu', 20 , self.screenWidth/2, 100, self.font1, self.control.white)

            numPlayerSurface = pygame.font.Font(self.font1, 20).render(str(self.numPlayer), True, fontColor)
            pygame.draw.rect(self.display, pygame.Color('white'), self.rectNumPlayer)
            self.display.blit(numPlayerSurface, (self.rectNumPlayer.centerx - numPlayerSurface.get_width()//2, self.rectNumPlayer.centery - numPlayerSurface.get_height()//2))

            self.buttonRight.draw(self.display)
            self.buttonLeft.draw(self.display)
            self.buttonBack.draw(self.display)
            self.buttonCreateLobby.draw(self.display)

            if self.buttonLeft.isButtonClick():
                self.numPlayer -= 1
                if self.numPlayer < 5:
                    self.numPlayer = 10
                    # self.numberWarning = True
            if self.buttonRight.isButtonClick():
                self.numPlayer += 1
                if self.numPlayer > 10:
                    self.numPlayer = 5
                    # self.numberWarning = True
            # Role unlock
            # Number Player -> Evil Number -> Can choose role on certain number
            # normal can select 2 evil role
            if self.numPlayer > 6: # can select 3 evil role
                pass
            if self.numPlayer > 9: # can select 4 evil role
                pass

            if self.buttonBack.isButtonClick():
                if self.network.connectStatus == True:
                    self.network.disconnectFromServer()
                self.changePageByInput(True)

            if self.buttonCreateLobby.isButtonClick():
                if self.network.createLobby(self.numPlayer, [True, False, True, False, True, False, True, False], 0, 0):
                    if self.network.joinGame():
                        self.player.host = True
                        self.player.id = 0
                        self.changePageByInput(True, self.control.createPlayer)
                    else:
                        print("[GAME] Cannot join game") # pop up here
                        self.lobbyFailed = True
                else:
                    print("[GAME] Cannot create lobby") # pop up error
                    self.lobbyFailed = True

            # if self.numberWarning:
            #     self.numberWarnPopup.draw(self.display, self.font1, 28, textAlign = 'centerAlign', bgColor = None,
            #     image = self.popupBackground)
            #     self.available = False
            #     if self.numberWarnPopup.b1.isButtonClick():
            #         self.available = True
            #         self.numberWarning = False
            # if self.lobbyFailed:
            #     self.lobbyFailPopup.draw(self.display, self.font1, 52, textAlign = 'centerAlign', bgColor = None,
            #     image = self.popupBackground)
            #     self.available = False
            #     if self.lobbyFailPopup.b1.isButtonClick():
            #         self.available = True
            #         self.lobbyFailed = False

            self.biltScreen() # update screen