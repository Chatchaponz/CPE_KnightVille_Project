import pygame, sys
from button import Button
from popup import Popup 
from screen import GameScreen
from textbox import Textbox


class CreatePlayer(GameScreen):
    
    def __init__(self, control):
        super(CreatePlayer, self).__init__(control)
        self.network = control.network
        self.player = control.player

        # Sound goes here

        self.soundList = control.soundList
        self.clickChoiceSound = self.soundList[2]

        # Image / Button goes here vvvv
        self.rightArrow = control.rightArrow
        self.leftArrow = control.leftArrow
        self.arrowWidth = self.rightArrow.get_rect().width
        self.arrowHeight = self.rightArrow.get_rect().height
        self.dressingCab = control.dressingCab
        self.dressingCabWidth = self.dressingCab.get_rect().width
        self.dressingRoom = control.dressingRoom
        
        self.buttonJoin = Button(self.screenWidth//2 - 40, self.dressingCab.get_height(), 80, 35)
        self.buttonJoin.addText('JOIN', self.font2, 20, (255, 255, 255), 1, (144, 109, 99), (120, 90, 82))

        self.buttonLeft = Button((self.screenWidth//2) - (self.arrowWidth) - 80, 360, self.arrowWidth, self.arrowHeight)
        self.buttonLeft.addImage(self.leftArrow)

        self.buttonRight = Button((self.screenWidth//2) + 80, 360, self.arrowWidth, self.arrowHeight)
        self.buttonRight.addImage(self.rightArrow)

        self.playerName = Textbox(self.screenWidth//2 - 125, 150, 250, 35, 
        pygame.Color('white'), pygame.Color('white'), 15, 'Your In-game name',self.font, 28)
        self.playerName.text = ''

        self.popupNoIGN = Popup(self.screenWidth//2 - 250, self.screenHeight//2 - 90, 500, 180, 
        'Please enter your/> In-game name with no spacebar', pygame.Color('white'), pygame.Color('darkblue'))
        self.popupNoIGN.modComponents(self.popupNoIGN.b1, 'button', (97, 63, 45), (130,83,50), 'OK', self.font2)

        self.triggerNoIGN = False

        #load skins
        self.skins = self.control.skins

        self.amountSkins = len(self.skins)
    
    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
                self.control.currentState.displayRunning = False
                pygame.quit()
                sys.exit()
            self.playerName.handleEvent(event)
             
    def displayScreen(self):

        self.displayRunning = True

        skinRect = []
        self.player.isPlaying = False
        for i in range(self.amountSkins):
            skinRect.append(self.skins[i].get_rect())
        
        skin = 0
        
        while self.displayRunning:

            self.checkEvent()

            # page blackground
            self.display.fill((255, 150, 200))
            self.display.blit(self.dressingRoom, (0,0))
            self.display.blit(self.dressingCab, ((self.screenWidth//2) - (self.dressingCabWidth//2),80))

            # Things in page vvv
            self.playerName.draw(self.display)

            self.display.blit(self.skins[skin], ((self.screenWidth//2) - 95, 550 - skinRect[skin].bottom))
            self.buttonLeft.draw(self.display)
            if self.buttonLeft.isButtonClick(self.soundList[4],self.control.getSoundEffectVol()):
                if skin == 0:
                    skin = self.amountSkins-1
                else:
                    skin -= 1

            self.buttonRight.draw(self.display)
            if self.buttonRight.isButtonClick(self.soundList[4],self.control.getSoundEffectVol()):
                if skin == self.amountSkins-1:
                    skin = 0
                else:
                    skin += 1

                    
            self.buttonJoin.draw(self.display)
            if self.buttonJoin.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()):
                playerName = self.playerName.getText()
                if len(playerName) > 1:
                    if playerName[-1] == ' ':
                        playerName = playerName[:-1]
                if playerName and not ' ' in playerName:
                    self.changePageByInput(True, self.control.lobby)    
                    self.player.setAttribute(50, 700, skin, playerName)
                else:
                    self.triggerNoIGN = True
            if self.triggerNoIGN:
                self.popupNoIGN.draw(self.display, self.font2, size = 28, textAlign = 'centerAlign', image = self.control.popupBackground)
                if self.popupNoIGN.b1.isButtonClick(self.clickChoiceSound, self.control.getSoundEffectVol()):
                    self.triggerNoIGN = False

            self.biltScreen() # update screen