import sys
import pygame
from screen import GameScreen
from button import Button
from popup import Popup

class MainMenu(GameScreen):
    
    def __init__(self, control):
        super(MainMenu, self).__init__(control)
        self.network = control.network

        # Image / Button goes here
        self.knightCover = control.knightCover
        self.knightCoverRect = self.knightCover.get_rect()
        self.BGCover = control.BGCover
        self.skyCover = control.skyCover
        self.woodBoard = control.woodBoard
        self.woodBoardWidth = self.woodBoard.get_rect().width
        self.woodBoardHeight = self.woodBoard.get_rect().height
        self.choice = control.choice
        self.choiceWidth = self.choice.get_rect().width
        self.skyPosition = 0
        self.skyCoverWidth = self.skyCover.get_rect().width

        self.buttonHost = Button(self.screenWidth//4, 240, 100, 70)
        self.buttonHost.addText('Host', self.font1, 40, control.white, 1, (50,50,50))

        self.buttonJoin = Button(self.screenWidth//4, 340, 100, 70)
        self.buttonJoin.addText('Join', self.font1, 40, control.white, 1, (50,50,50))

        self.buttonOption = Button(self.screenWidth//4, 440, 100, 70)
        self.buttonOption.addText('Option', self.font1, 40, control.white, 1, (50,50,50))

        self.buttonQuit = Button(self.screenWidth//4, 540, 100, 70)
        self.buttonQuit.addText('Quit', self.font1, 40, control.white, 1, (50,50,50))

        self.popupJoin = Popup((self.display.get_width() - 500)//2, (self.display.get_height() - 100)//2, 500, 100, 'Enter host/> ip address', pygame.Color('white'), pygame.Color('red'), 2)
        self.popupJoin.modTextbox(text='IP Address here.')
        self.popupJoin.modButton(b1Color=pygame.Color('paleturquoise4'), b1Over=pygame.Color('paleturquoise3'))

        self.popupHost = Popup((self.display.get_width() - 500)//2, (self.display.get_height() - 100)//2, 500, 100, 'Enter your/> ip address', pygame.Color('white'), pygame.Color('red'), 2)
        self.popupHost.modTextbox(text='IP Address here.')
        self.popupHost.modButton()
        self.hostClose = True
        self.joinClose = True

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
                self.control.currentState.displayRunning = False
                pygame.quit()
                sys.exit()
            if not self.joinClose:
                self.popupJoin.t1.handleEvent(event)
            if not self.hostClose:
                self.popupHost.t1.handleEvent(event)
    
    def displayScreen(self):

        self.displayRunning = True

        while self.displayRunning:

            self.checkEvent()
            self.display.fill((0, 0, 0))

            self.display.blit(self.skyCover, (self.skyPosition,0))
            self.skyPosition -= 2.7
            if self.skyPosition < -(self.skyCoverWidth - 1280):
                self.display.blit(self.skyCover, (self.skyPosition + self.skyCoverWidth,0))
            if self.skyPosition < -self.skyCoverWidth:
                self.skyPosition = 0

            self.display.blit(self.BGCover, (0,0))
            self.display.blit(self.knightCover, self.knightCoverRect)
            self.display.blit(self.woodBoard, ((self.screenWidth/4) - (self.woodBoardWidth/2) + 50,20))

            # draw button
            self.buttonHost.draw(self.display)
            self.buttonJoin.draw(self.display)
            self.buttonOption.draw(self.display)
            self.buttonQuit.draw(self.display)

            if self.buttonOption.isMouseOver():
                self.display.blit(self.choice, ((self.screenWidth/4) - (self.choiceWidth/2) + 50, 430))
            self.changePageByButton(self.buttonOption, self.control.option)

            # NEED POPUP HERE
            if self.buttonHost.isMouseOver():
                self.display.blit(self.choice, ((self.screenWidth/4) - (self.choiceWidth/2) + 50, 230))
            if self.buttonHost.isButtonClick():
                self.hostClose = False
            if not self.hostClose:
                self.popupHost.draw(self.display, size = 36, textAlign='centerAlign', bgColor=pygame.Color('grey2'), 
                bdColor=pygame.Color('grey3'))
                if self.popupHost.b1.isButtonClick():
                    ipHost = self.popupHost.t1.getText()
                    self.hostClose = True
                    if self.network.tryConnectServer(ipHost, 5555):
                        self.changePageByInput(True, self.control.host)
                    else:
                        print("[GAME] Unable to connect server")
            
            if self.buttonJoin.isMouseOver():
                self.display.blit(self.choice, ((self.screenWidth/4) - (self.choiceWidth/2) + 50, 330))
            if self.buttonJoin.isButtonClick():
                self.joinClose = False
            if not self.joinClose:
                self.popupJoin.draw(self.display, size = 36, textAlign='centerAlign', bgColor=pygame.Color('grey2'), 
                bdColor=pygame.Color('grey3'))
                if self.popupJoin.b1.isButtonClick():
                    ipJoin = self.popupJoin.t1.getText()
                    self.joinClose = True
                    if self.network.tryConnectServer(ipJoin, 5555):
                        self.changePageByInput(True, self.control.createPlayer)
                    else:
                        print("[GAME] Unable to connect server")

            if self.buttonQuit.isMouseOver():
                self.display.blit(self.choice, ((self.screenWidth/4) - (self.choiceWidth/2) + 50, 530))
            if self.buttonQuit.isButtonClick():
                pygame.quit()
                sys.exit()

            self.drawText('KnightVIlle', 60 , (self.screenWidth/4) + 50, 180, self.font2, self.control.black)
            self.biltScreen()