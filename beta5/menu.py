import sys
import threading
import pygame
import random
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
        self.paperSoundList = control.paperSoundList
        self.clickChoiceSound = self.soundList[2]
        self.isMouseOverSound = self.soundList[0]
        self.backButtonSound = self.soundList[3]

        # Image
        self.logo = self.control.logo
        self.knightCover = control.knightCover 
        self.knightCoverRect = self.knightCover.get_rect()
        self.BGCover = control.BGCover
        self.BGCoverWidth = self.BGCover.get_rect().width
        self.BGCoverPosition = -2500
        self.skyCover = self.control.skyCover
        self.woodBoard = self.control.woodBoard
        self.woodBoardWidth = self.woodBoard.get_rect().width
        self.woodBoardHeight = self.woodBoard.get_rect().height
        self.choice = self.control.choice
        self.choiceWidth = self.choice.get_rect().width
        self.skyPosition = 0
        self.skyCoverWidth = self.skyCover.get_rect().width
        self.popupBackground = self.control.popupBackground

        self.howToPlay = self.control.howToPlay
        self.amountOfHowToPlayPage = len(self.howToPlay)

        self.tapeRightArrow = self.control.tapeRightArrow
        self.tapeLeftArrow = self.control.tapeLeftArrow
        self.tapeArrowWidth = self.tapeLeftArrow.get_rect().width
        self.tapeArrowHeight = self.tapeLeftArrow.get_rect().height
        self.tapeClose = self.control.tapeClose
        self.tapeCloseWidth = self.tapeClose.get_rect().width
        self.tapeCloseHeight = self.tapeClose.get_rect().height

        # Button
        self.buttonHost = Button(self.screenWidth//4, 270, 100, 70)
        self.buttonHost.addText('Host', self.font1, 40, control.white, (50,50,50))

        self.buttonJoin = Button(self.screenWidth//4, 360, 100, 70)
        self.buttonJoin.addText('Join', self.font1, 40, control.white, (50,50,50))

        self.buttonOption = Button(self.screenWidth//4, 450, 100, 70)
        self.buttonOption.addText('Option', self.font1, 40, control.white, (50,50,50))

        self.buttonQuit = Button(self.screenWidth//4, 540, 100, 70)
        self.buttonQuit.addText('Quit', self.font1, 40, control.white, (50,50,50))

        self.buttonHowToPlay = Button(self.screenWidth - 170, 20, 150, 50)
        self.buttonHowToPlay.addText('How to play', self.font1, 30, control.white, (50,50,50), pygame.Color("brown"))

        self.buttonRight = Button(self.screenWidth - self.tapeArrowWidth - 80, self.screenHeight//2 - 20, self.tapeArrowWidth, self.tapeArrowHeight)
        self.buttonRight.addImage(self.tapeRightArrow)

        self.buttonLeft = Button(80, self.screenHeight//2 - 20, self.tapeArrowWidth, self.tapeArrowHeight)
        self.buttonLeft.addImage(self.tapeLeftArrow)

        self.buttonClose = Button(self.screenWidth - self.tapeCloseWidth - 120, 20, self.tapeCloseWidth, self.tapeCloseHeight)
        self.buttonClose.addImage(self.tapeClose)

        # Popup
        self.popupHost = Popup((self.display.get_width() - 700)//2, (self.display.get_height() - 250)//2, 700, 250, 
        'YOUR/> SERVER IP', pygame.Color('white'), pygame.Color('darkblue'), type = 2)
        self.popupHost.adjustComponents(200, 80, fontPath = self.font2, t1text = 'IP ADDRESS', t2text = 'PORT')
        self.popupHost.modComponents(self.popupHost.t1, 'textbox', pygame.Color('white'), font = self.font, limit = 15)
        self.popupHost.modComponents(self.popupHost.t2, 'textbox', pygame.Color('white'), text = '5555', font = self.font, 
        limit = 5)

        self.popupJoin = Popup((self.display.get_width() - 700)//2, (self.display.get_height() - 250)//2, 700, 250, 
        'HOST/> SERVER IP', pygame.Color('white'), pygame.Color('darkblue'), type = 2)
        self.popupJoin.adjustComponents(200, 80, fontPath = self.font2, t1text = 'IP ADDRESS', t2text = 'PORT')
        self.popupJoin.modComponents(self.popupJoin.t1, 'textbox', pygame.Color('white'), font = self.font, limit = 15)
        self.popupJoin.modComponents(self.popupJoin.t2, 'textbox', pygame.Color('white'), text = '5555', font = self.font,
        limit = 5)

        for popupObj in [self.popupHost, self.popupJoin]:
            popupObj.modComponents(popupObj.b1, 'button', (97, 63, 45), (130,83,50), 'Connect', self.font2)
            popupObj.modComponents(popupObj.b2, 'button', (97, 63, 45), (130,83,50), 'Cancel', self.font2)

        self.popupFail = Popup((self.display.get_width() - 500)//2, (self.display.get_height() - 200)//2, 500, 200, 
        'UNABLE TO CONNECT HOST SERVER', pygame.Color('white'), pygame.Color('cyan3'), type = 0)
        self.popupFail.adjustComponents(bWidth=70, fontPath = self.font2)
        self.popupFail.modComponents(self.popupFail.b1, 'button', (97, 63, 45), (130,83,50), 'Close', 
        self.font2, 22)


        # Popup state
        self.available = True
        self.successConnect = True
        self.hosting = False
        self.joining = False

        # Thread
        self.hostClicked = False
        self.joinClicked = False
        self.connecting = False
        self.finishConnection = False
        self.connectResult = False
        self.errorMessage = ""

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
                self.control.currentState.displayRunning = False
                pygame.quit()
                sys.exit()
            if self.joining and not self.connecting:
                self.popupJoin.t1.handleEvent(event)
                self.popupJoin.t2.handleEvent(event, False)
            if self.hosting and not self.connecting:
                self.popupHost.t1.handleEvent(event)
                self.popupHost.t2.handleEvent(event, False)
    
    def makeConnection(self, ip, port):
        self.connecting = True
        self.connectResult, self.errorMessage = self.network.tryConnectServer(str(ip), int(port))
        self.connecting = False
        self.finishConnection = True


    def doConnection(self, ip, port):
        if not self.connecting:
            connectionThread = threading.Thread(target= self.makeConnection, args=(ip, port,))
            connectionThread.daemon = True
            connectionThread.start()
    
    def displayScreen(self):

        self.displayRunning = True
        
        buttonList = [self.buttonHost, self.buttonJoin, self.buttonOption, self.buttonQuit]
        buttonHowToPlayList = (self.buttonClose, self.buttonLeft, self.buttonRight)
        currentPage = 0
        howToPlayStatus = False

        while self.displayRunning:
            
            # print(f"{threading.activeCount()}") # print number of current thread
            
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
            for buttonSurface in buttonList:
                buttonSurface.draw(self.display, self.available)
            self.buttonHowToPlay.draw(self.display, self.available)
            self.display.blit(self.logo, (self.screenWidth//4 - self.logo.get_width()//2 + 50, 100))

            # Menu available to click
            if self.available:
            # Mouse over button sound
                for buttonSurface in buttonList:
                    buttonSurface.triggerSound(self.soundList[1],self.control.getSoundEffectVol())
                    if buttonSurface.isMouseOver():
                        self.display.blit(self.choice, ((self.screenWidth/4) - (self.choiceWidth/2) + 50, buttonSurface.rect.y))
                    
            # MENU LIST
                if self.buttonOption.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()):
                    self.changePageByInput(True, self.control.option)
                if self.buttonHost.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()):
                    self.hosting = True # OPEN HOST POPUP
                    self.available = False
                if self.buttonJoin.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()):
                    self.joining = True # OPEN JOIN POPUP
                    self.available = False
                if self.buttonQuit.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()):
                    pygame.quit()
                    sys.exit()
                if self.buttonHowToPlay.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()):
                    howToPlayStatus = True

            if howToPlayStatus:
                self.available = False
                self.display.blit(self.howToPlay[currentPage], (0, 0))
                for button in buttonHowToPlayList:
                    button.draw(self.display, self.available)
                if self.buttonLeft.isButtonClick(random.choice(self.paperSoundList),self.control.getSoundEffectVol()):
                    if currentPage == 0:
                            currentPage = self.amountOfHowToPlayPage-1
                    else:
                        currentPage -= 1
                if self.buttonRight.isButtonClick(random.choice(self.paperSoundList),self.control.getSoundEffectVol()):
                    if currentPage == self.amountOfHowToPlayPage-1:
                        currentPage = 0
                    else:
                        currentPage += 1
                if self.buttonClose.isButtonClick(self.backButtonSound,self.control.getSoundEffectVol()):
                    self.available = True
                    howToPlayStatus = False
            else:
                currentPage = 0
            
            # POPUP
            if self.hosting:  # HOSTING
                self.popupHost.draw(self.display, self.font2, 52, textAlign = 'centerAlign', bgColor = None,
                image = self.popupBackground)
                self.available = False
                # self.popupHost.b4.draw(self.display)
                # self.display.blit(self.popupBackground, ((self.screenWidth//4) - self.popupBackground))
                if not self.connecting:

                    if( self.popupHost.b1.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()) and 
                        self.network.connectStatus != True):
                        ipHost = self.popupHost.t1.getText()
                        portHost = self.popupHost.t2.getText()
                        self.doConnection(str(ipHost), int(portHost))
                        self.hostClicked = True
                        self.popupHost.activeButton = False
                    
                    if self.popupHost.b2.isButtonClick(self.backButtonSound,self.control.getSoundEffectVol()):
                        self.available = True
                        self.hosting = False

                if self.hostClicked:

                    if self.finishConnection:
                        
                        # reset
                        self.hosting = False
                        self.hostClicked = False
                        self.finishConnection = False
                        self.popupHost.activeButton = True

                        if self.connectResult:
                            self.changePageByInput(True, self.control.host)
                            self.successConnect = True
                        else:
                            self.popupFail.text = self.errorMessage.upper()
                            self.successConnect = False
                        
                        self.available = True

                    else:
                        self.drawText("Connecting . . .", 30, 640, 350, self.font1, self.control.white)



                # elif self.popupHost.b4.isButtonClick():
                #     print('???')
                #     self.hosting = True

            if self.joining: #JOINING
                self.popupJoin.draw(self.display, self.font2, 52, textAlign = 'centerAlign', bgColor = None, 
                image = self.popupBackground)
                # self.popupJoin.b4.draw(self.display) # OPTIONAL TO DRAWN GUIDE BUTTON ON POPUP
                if not self.connecting:

                    if (self.popupJoin.b1.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()) and 
                        self.network.connectStatus != True):
                        ipJoin = self.popupJoin.t1.getText()
                        portJoin = self.popupJoin.t2.getText()
                        self.doConnection(str(ipJoin), int(portJoin))
                        self.joinClicked = True
                        self.popupJoin.activeButton = False
                    
                    if self.popupJoin.b2.isButtonClick(self.backButtonSound,self.control.getSoundEffectVol()): # POPUP CLOSE BUTTON
                        self.available = True
                        self.joining = False
                
                if self.joinClicked:

                    if self.finishConnection:

                        # reset
                        self.joining = False
                        self.joinClicked = False
                        self.finishConnection = False
                        self.popupJoin.activeButton = True

                        if not self.connectResult:
                            self.popupFail.text = self.errorMessage.upper()
                            self.successConnect = False

                    else:
                        self.drawText("Connecting . . .", 30, 640, 350, self.font1, self.control.white)
                
                    if self.network.connectStatus == True:
                        joinResult, joinError = self.network.joinGame()
                        if joinResult:
                            self.changePageByInput(True, self.control.createPlayer)
                            self.successConnect = True
                        else:
                            self.popupFail.text = joinError.upper()
                            self.network.disconnectFromServer()
                            self.successConnect = False

                        self.available = True

                # elif self.popupJoin.b4.isButtonClick(): # POPUP GUIDE BUTTON
                #     print('???')
                #     self.joining = True
            if not self.successConnect: # FAILED TO CONNECT
                self.popupFail.draw(self.display, self.font2, 30, textAlign= 'centerAlign',  bgColor = None, 
                image = self.popupBackground)
                self.available = False
                if self.popupFail.b1.isButtonClick(self.backButtonSound,self.control.getSoundEffectVol()):
                    self.successConnect = True
                    self.available = True
                
            self.biltScreen()
