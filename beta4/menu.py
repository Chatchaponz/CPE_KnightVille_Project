import sys
import pygame
from screen import GameScreen
from button import Button
from popup import Popup

class MainMenu(GameScreen):
    
    def __init__(self, control):
        super(MainMenu, self).__init__(control)
        self.network = control.network

        # Music goes here
        self.currentMusic = control.currentMusic
        self.musicList = control.musicList

        # Sounds go here
        self.soundList = control.soundList

        # Image
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
        self.popupBackground = control.popupBackground

        # Button
        self.buttonHost = Button(self.screenWidth//4, 240, 100, 70)
        self.buttonHost.addText('Host', self.font1, 40, control.white, 1, (50,50,50))

        self.buttonJoin = Button(self.screenWidth//4, 340, 100, 70)
        self.buttonJoin.addText('Join', self.font1, 40, control.white, 1, (50,50,50))

        self.buttonOption = Button(self.screenWidth//4, 440, 100, 70)
        self.buttonOption.addText('Option', self.font1, 40, control.white, 1, (50,50,50))

        self.buttonQuit = Button(self.screenWidth//4, 540, 100, 70)
        self.buttonQuit.addText('Quit', self.font1, 40, control.white, 1, (50,50,50))

        # Popup set-up
        self.popupHost = Popup((self.display.get_width() - 700)//2, (self.display.get_height() - 250)//2, 700, 250, 
        'YOUR/> SERVER IP', pygame.Color('white'), pygame.Color('greenyellow'), type = 2)
        self.popupHost.adjustComponents(200, 80, fontPath = None, t1text = 'IP ADDRESS', t2text = 'PORT')
        self.popupHost.modComponents(self.popupHost.t1, 'textbox', pygame.Color('white'), font = self.font1, limit = 15)
        self.popupHost.modComponents(self.popupHost.t2, 'textbox', pygame.Color('white'), text = '5555', font = self.font1, 
        limit = 5)

        self.popupJoin = Popup((self.display.get_width() - 700)//2, (self.display.get_height() - 250)//2, 700, 250, 
        'HOST/> SERVER IP', pygame.Color('white'), pygame.Color('red'), type = 2)
        self.popupJoin.adjustComponents(200, 80, fontPath = None, t1text = 'IP ADDRESS', t2text = 'PORT')
        self.popupJoin.modComponents(self.popupJoin.t1, 'textbox', pygame.Color('white'), font = self.font1, limit = 15)
        self.popupJoin.modComponents(self.popupJoin.t2, 'textbox', pygame.Color('white'), text = '5555', font = self.font1, 
        limit = 5)

        self.popupFailCon = Popup((self.display.get_width() - 500)//2, (self.display.get_height() - 200)//2, 500, 200, 
        'UNABLE/> TO CONNECT HOST SERVER', pygame.Color('white'), pygame.Color('aquamarine2'), type = 0)
        self.popupFailCon.adjustComponents(bWidth=70, fontPath=None)


        # Popup state
        self.hostClose = True
        self.joinClose = True
        self.connect = True

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
                self.control.currentState.displayRunning = False
                pygame.quit()
                sys.exit()
            if not self.joinClose:
                self.popupJoin.t1.handleEvent(event)
                self.popupJoin.t2.handleEvent(event, False)
            if not self.hostClose:
                self.popupHost.t1.handleEvent(event)
                self.popupHost.t2.handleEvent(event, False)
    
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
            self.display.blit(self.knightCover, self.knightCoverRect)
            self.display.blit(self.woodBoard, ((self.screenWidth/4) - (self.woodBoardWidth/2) + 50,20))

            # draw button
            self.buttonHost.draw(self.display)
            self.buttonJoin.draw(self.display)
            self.buttonOption.draw(self.display)
            self.buttonQuit.draw(self.display)

            # Menu button sounds
            self.buttonHost.triggerSound(self.soundList[3])
            self.buttonJoin.triggerSound(self.soundList[3])
            self.buttonOption.triggerSound(self.soundList[3])
            self.buttonQuit.triggerSound(self.soundList[3])

            if self.buttonOption.isMouseOver():
                self.display.blit(self.choice, ((self.screenWidth/4) - (self.choiceWidth/2) + 50, 430))
            self.changePageByButton(self.buttonOption, self.control.option)

            # NEED POPUP HERE
            if self.buttonHost.isMouseOver():
                self.display.blit(self.choice, ((self.screenWidth/4) - (self.choiceWidth/2) + 50, 230))
            if self.buttonHost.isButtonClick():
                self.hostClose = False # OPEN HOST POPUP
            if not self.hostClose:
                self.popupHost.draw(self.display, self.font1, 52, textAlign = 'centerAlign', bgColor = None,
                image = self.popupBackground)
                # self.popupHost.b4.draw(self.display)
                # self.display.blit(self.popupBackground, ((self.screenWidth//4) - self.popupBackground))
                if self.popupHost.b1.isButtonClick():
                    ipHost = self.popupHost.t1.getText()
                    portHost = self.popupHost.t2.getText()
                    self.hostClose = True
                    if self.network.tryConnectServer(str(ipHost), int(portHost)):
                        self.changePageByInput(True, self.control.host)
                        self.connect = True
                    else:
                        print("[GAME] Unable to connect server")
                        self.connect = False
                # elif self.popupHost.b3.isButtonClick():
                #     self.hostClose = True
                # elif self.popupHost.b4.isButtonClick():
                #     print('???')
                #     self.hostClose = True
                
            
            if self.buttonJoin.isMouseOver():
                self.display.blit(self.choice, ((self.screenWidth/4) - (self.choiceWidth/2) + 50, 330))
            if self.buttonJoin.isButtonClick():
                self.joinClose = False # OPEN JOIN POPUP
            if not self.joinClose:
                self.popupJoin.draw(self.display, self.font1, 52, textAlign = 'centerAlign', bgColor = None, 
                image = self.popupBackground)
                # self.popupJoin.b4.draw(self.display) # OPTIONAL TO DRAWN GUIDE BUTTON ON POPUP
                if self.popupJoin.b1.isButtonClick():
                    ipJoin = self.popupJoin.t1.getText()
                    portJoin = self.popupJoin.t2.getText()
                    self.joinClose = True
                    if self.network.tryConnectServer(ipJoin, portJoin):
                        self.changePageByInput(True, self.control.createPlayer)
                        self.connect = True
                    else:
                        print("[GAME] Unable to connect server")
                        self.connect = False
                # elif self.popupJoin.b3.isButtonClick(): # POPUP CLOSE BUTTON
                #     self.joinClose = True
                # elif self.popupJoin.b4.isButtonClick(): # POPUP GUIDE BUTTON
                #     print('???')
                #     self.joinClose = True
            if not self.connect:
                self.popupFailCon.draw(self.display, self.font1, 30, textAlign= 'centerAlign',  bgColor = None, 
                image = self.popupBackground)
                if self.popupFailCon.b1.isButtonClick():
                    self.connect = True

            if self.buttonQuit.isMouseOver():
                self.display.blit(self.choice, ((self.screenWidth/4) - (self.choiceWidth/2) + 50, 530))
            if self.buttonQuit.isButtonClick():
                pygame.quit()
                sys.exit()

            self.drawText('KnightVIlle', 60 , (self.screenWidth/4) + 50, 180, self.font2, self.control.black)
            self.biltScreen()