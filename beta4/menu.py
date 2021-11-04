import sys
import pygame
from screen import GameScreen
from button import Button
from popup import Popup

class MainMenu(GameScreen):
    
    def __init__(self, control):
        super(MainMenu, self).__init__(control)
        self.network = control.network

        # Music
        self.currentMusic = control.currentMusic
        self.musicList = control.musicList

        # Sound Effect
        self.soundList = control.soundList
        self.clickChoiceSound = self.soundList[5]

        # Image
        self.knightCover = control.knightCover
        self.knightCoverRect = self.knightCover.get_rect()
        self.BGCover = control.BGCover
        self.BGCoverWidth = self.BGCover.get_rect().width
        self.BGCoverPosition = -2500
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
        self.buttonHost.addText('Host', self.font1, 40, control.white, (50,50,50))

        self.buttonJoin = Button(self.screenWidth//4, 340, 100, 70)
        self.buttonJoin.addText('Join', self.font1, 40, control.white, (50,50,50))

        self.buttonOption = Button(self.screenWidth//4, 440, 100, 70)
        self.buttonOption.addText('Option', self.font1, 40, control.white, (50,50,50))

        self.buttonQuit = Button(self.screenWidth//4, 540, 100, 70)
        self.buttonQuit.addText('Quit', self.font1, 40, control.white, (50,50,50))

        # Popup
        self.popupHost = Popup((self.display.get_width() - 700)//2, (self.display.get_height() - 250)//2, 700, 250, 
        'YOUR/> SERVER IP', pygame.Color('white'), pygame.Color('cyan3'), type = 2)
        self.popupHost.adjustComponents(200, 80, fontPath = self.font1, t1text = 'IP ADDRESS', t2text = 'PORT')
        self.popupHost.modComponents(self.popupHost.t1, 'textbox', pygame.Color('white'), font = self.font1, limit = 15)
        self.popupHost.modComponents(self.popupHost.t2, 'textbox', pygame.Color('white'), text = '5555', font = self.font1, 
        limit = 5)
        # self.popupHost.modComponents(self.popupHost.b1, 'button', pygame.Color())

        self.popupJoin = Popup((self.display.get_width() - 700)//2, (self.display.get_height() - 250)//2, 700, 250, 
        'HOST/> SERVER IP', pygame.Color('white'), pygame.Color('cyan3'), type = 2)
        self.popupJoin.adjustComponents(200, 80, fontPath = self.font1, t1text = 'IP ADDRESS', t2text = 'PORT')
        self.popupJoin.modComponents(self.popupJoin.t1, 'textbox', pygame.Color('white'), font = self.font1, limit = 15)
        self.popupJoin.modComponents(self.popupJoin.t2, 'textbox', pygame.Color('white'), text = '5555', font = self.font1,
        limit = 5)

        self.popupFail = Popup((self.display.get_width() - 500)//2, (self.display.get_height() - 200)//2, 500, 200, 
        'UNABLE TO CONNECT HOST SERVER', pygame.Color('white'), pygame.Color('cyan3'), type = 0)
        self.popupFail.adjustComponents(bWidth=70, fontPath = self.font1)
        self.popupFail.modComponents(self.popupFail.b1, 'button', (132, 85, 47), (100, 64, 44), 'Close', 
        self.font1, 22)


        # Popup state
        self.available = True
        self.successConnect = True
        self.hosting = False
        self.joining = False

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
                self.control.currentState.displayRunning = False
                pygame.quit()
                sys.exit()
            if self.joining:
                self.popupJoin.t1.handleEvent(event)
                self.popupJoin.t2.handleEvent(event, False)
            if self.hosting:
                self.popupHost.t1.handleEvent(event)
                self.popupHost.t2.handleEvent(event, False)
    
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

            self.display.blit(self.BGCover, (self.BGCoverPosition,0))
            self.BGCoverPosition -= 1
            if self.BGCoverPosition < -(self.BGCoverWidth - 1280):
                self.display.blit(self.BGCover, (self.BGCoverPosition + self.BGCoverWidth,0))
            if self.BGCoverPosition < -self.BGCoverWidth:
                self.BGCoverPosition = 0

            self.display.blit(self.knightCover, self.knightCoverRect)
            self.display.blit(self.woodBoard, ((self.screenWidth/4) - (self.woodBoardWidth/2) + 50,20))

            # Draw button
            self.buttonHost.draw(self.display, self.available)
            self.buttonJoin.draw(self.display, self.available)
            self.buttonOption.draw(self.display, self.available)
            self.buttonQuit.draw(self.display, self.available)

            # Menu available to click
            if self.available:
            # Mouse over button sound
                self.buttonHost.triggerSound(self.soundList[4])
                self.buttonJoin.triggerSound(self.soundList[4])
                self.buttonOption.triggerSound(self.soundList[4])
                self.buttonQuit.triggerSound(self.soundList[4])
            # MENU LIST
                if self.buttonOption.isMouseOver(): # OPTION
                    self.display.blit(self.choice, ((self.screenWidth/4) - (self.choiceWidth/2) + 50, 430))
                if self.buttonOption.isButtonClick(self.clickChoiceSound,1):
                    self.changePageByInput(True, self.control.option)
                if self.buttonHost.isMouseOver(): # HOST
                    self.display.blit(self.choice, ((self.screenWidth/4) - (self.choiceWidth/2) + 50, 230))
                if self.buttonHost.isButtonClick(self.clickChoiceSound,1):
                    self.hosting = True # OPEN HOST POPUP
                    self.available = False
                if self.buttonJoin.isMouseOver(): # JOIN
                    self.display.blit(self.choice, ((self.screenWidth/4) - (self.choiceWidth/2) + 50, 330))
                if self.buttonJoin.isButtonClick(self.clickChoiceSound,1):
                    self.joining = True # OPEN JOIN POPUP
                    self.available = False
                if self.buttonQuit.isMouseOver(): # QUIT
                    self.display.blit(self.choice, ((self.screenWidth/4) - (self.choiceWidth/2) + 50, 530))
                if self.buttonQuit.isButtonClick(self.clickChoiceSound,1):
                    pygame.quit()
                    sys.exit()
            
            # POPUP
            if self.hosting:  # HOSTING
                self.popupHost.draw(self.display, self.font1, 52, textAlign = 'centerAlign', bgColor = None,
                image = self.popupBackground)
                self.available = False
                # self.popupHost.b4.draw(self.display)
                # self.display.blit(self.popupBackground, ((self.screenWidth//4) - self.popupBackground))
                if self.popupHost.b1.isButtonClick(self.clickChoiceSound,1):
                    ipHost = self.popupHost.t1.getText()
                    portHost = self.popupHost.t2.getText()
                    self.hosting = False
                    if self.network.tryConnectServer(str(ipHost), int(portHost)):
                        self.changePageByInput(True, self.control.host)
                        self.successConnect = True
                    else:
                        print("[GAME] Unable to connect server")
                        self.successConnect = False
                    self.available = True
                if self.popupHost.b2.isButtonClick(self.clickChoiceSound,1):
                    self.available = True
                    self.hosting = False
                # elif self.popupHost.b4.isButtonClick():
                #     print('???')
                #     self.hosting = True
            if self.joining: #JOINING
                self.popupJoin.draw(self.display, self.font1, 52, textAlign = 'centerAlign', bgColor = None, 
                image = self.popupBackground)
                # self.popupJoin.b4.draw(self.display) # OPTIONAL TO DRAWN GUIDE BUTTON ON POPUP
                if self.popupJoin.b1.isButtonClick(self.clickChoiceSound,1):
                    ipJoin = self.popupJoin.t1.getText()
                    portJoin = self.popupJoin.t2.getText()
                    self.joining = False
                    if self.network.tryConnectServer(str(ipJoin), int(portJoin)):
                        self.changePageByInput(True, self.control.createPlayer)
                        self.successConnect = True
                    else:
                        print("[GAME] Unable to connect server")
                        self.successConnect = False
                    self.available = True
                if self.popupJoin.b2.isButtonClick(self.clickChoiceSound,1): # POPUP CLOSE BUTTON
                    self.available = True
                    self.joining = False
                # elif self.popupJoin.b4.isButtonClick(): # POPUP GUIDE BUTTON
                #     print('???')
                #     self.joining = True
            if not self.successConnect: # FAILED TO CONNECT
                self.popupFail.draw(self.display, self.font1, 30, textAlign= 'centerAlign',  bgColor = None, 
                image = self.popupBackground)
                self.available = False
                if self.popupFail.b1.isButtonClick(self.clickChoiceSound,1):
                    self.successConnect = True
                    self.available = True
                

            self.drawText('KNiGHT VIlle', 60 , (self.screenWidth/4) + 50, 180, self.font1, pygame.Color('bisque3'))
            self.biltScreen()
