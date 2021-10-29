import sys
import pygame
from screen import GameScreen
from button import Button
from popup import Popup

class MainMenu(GameScreen):
    
    def __init__(self, control):
        super(MainMenu, self).__init__(control)
        self.network = control.network

        self.knightCover = control.knightCover
        self.BGCover = control.BGCover
        self.skyCover = control.skyCover
        self.woodBoard = control.woodBoard
        self.choice = control.choice
        self.skyPosition = 0
        self.skyCoverWidth = self.skyCover.get_rect().width
        #self.angle = 0

        # Music goes here
        self.currentMusic = control.currentMusic
        self.musicList = control.musicList

        # Image / Button goes here
        self.buttonHost = Button(300, 250, 100, 70)
        self.buttonHost.addText('Host', self.font1, 40, control.white, 1, (50,50,50))

        self.buttonJoin = Button(300, 350, 100, 70)
        self.buttonJoin.addText('Join', self.font1, 40, control.white, 1, (50,50,50))

        self.buttonOption = Button(300, 450, 100, 70)
        self.buttonOption.addText('Option', self.font1, 40, control.white, 1, (50,50,50))

        self.buttonQuit = Button(300, 550, 100, 70)
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

        # Main music is loaded here
        self.currentMusic.load(self.musicList[0])
        self.currentMusic.play(-1)
        
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
            self.display.blit(self.knightCover, (0,0))
            #self.display.blit(self.woodBoard, (145,30))
            self.display.blit(self.woodBoard, (135,20))

            self.buttonOption.draw(self.display)
            if self.buttonOption.isMouseOver():
                self.display.blit(self.choice, (182, 440))
            self.changePageByButton(self.buttonOption, self.control.option)

            # NEED POPUP HERE
            self.buttonHost.draw(self.display)
            if self.buttonHost.isMouseOver():
                self.display.blit(self.choice, (182, 240))
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
            
            self.buttonJoin.draw(self.display)
            if self.buttonJoin.isMouseOver():
                self.display.blit(self.choice, (182, 340))
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

            self.buttonQuit.draw(self.display)
            if self.buttonQuit.isMouseOver():
                self.display.blit(self.choice, (182, 540))
            if self.buttonQuit.isButtonClick():
                pygame.quit()
                sys.exit()

            self.drawText('KnightVIlle', 60 , 350, 175, self.font2, self.control.black)
            self.biltScreen()