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
        self.soundEffectVol = control.soundEffectVol
        self.clickChoiceSound = self.soundList[2]

        # Image / Button goes here vvvv
        self.rightArrow = control.rightArrow
        self.leftArrow = control.leftArrow
        self.arrowWidth = self.rightArrow.get_rect().width
        self.arrowHeight = self.rightArrow.get_rect().height
        
        self.buttonJoin = Button(100, 200, 100, 50)
        self.buttonJoin.addText('Join', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonLeft = Button(200, 300, self.arrowWidth, self.arrowHeight)
        #self.buttonLeft.addText('←', self.font, 20, (255,255,255), 1, (50,50,50))
        self.buttonLeft.addImage(self.leftArrow)

        self.buttonRight = Button(900, 300, self.arrowWidth, self.arrowHeight)
        #self.buttonRight.addText('→', self.font, 20, (255,255,255), 1, (50,50,50))
        self.buttonRight.addImage(self.rightArrow)

        self.playerName = Textbox(self.screenWidth//2 - 125, 150, 250, 35, 
        pygame.Color('white'), pygame.Color('white'), 15, 'Your In-game name', size = 28)
        self.playerName.text = ''

        self.popupNoIGN = Popup(self.screenWidth//2 - 300, self.screenHeight//2 - 125, 600, 250, 'Please enter your/> In-game name', pygame.Color('white'), pygame.Color('red'))
        self.popupNoIGN.modComponents(self.popupNoIGN.b1, 'button', pygame.Color('darkseagreen4'), pygame.Color('darkslategray'), 'understand')

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

        skin = 0
        self.player.isPlaying = False
        
        while self.displayRunning:

            self.checkEvent()

            # page blackground
            self.display.fill((255, 150, 200))

            # Things in page vvv
            self.playerName.draw(self.display)

            self.display.blit(self.skins[skin], ((self.screenWidth//2) - 95, 300))
            self.buttonLeft.draw(self.display)
            if self.buttonLeft.isButtonClick(self.soundList[4],self.soundEffectVol):
                if skin == 0:
                    skin = self.amountSkins-1
                else:
                    skin -= 1

            self.buttonRight.draw(self.display)
            if self.buttonRight.isButtonClick(self.soundList[4],self.soundEffectVol):
                if skin == self.amountSkins-1:
                    skin = 0
                else:
                    skin += 1

                    
            self.buttonJoin.draw(self.display)
            if self.buttonJoin.isButtonClick(self.clickChoiceSound,self.soundEffectVol):
                playerName = self.playerName.getText()
                if playerName:
                    self.changePageByInput(True, self.control.lobby)    
                    self.player.setAttribute(50, 700, skin, playerName)
                else:
                    self.triggerNoIGN = True
            if self.triggerNoIGN:
                self.popupNoIGN.draw(self.display, self.font, size = 28, textAlign = 'centerAlign', bgColor = pygame.Color('darkgrey'))
                if self.popupNoIGN.b1.isButtonClick(self.clickChoiceSound,self.soundEffectVol):
                    self.triggerNoIGN = False

            self.drawText('Create Player[Under construction]', 20 , 100, 100, self.font, self.control.white)
            self.drawText('Your test character already created', 20 , 100, 150, self.font, self.control.white)
            self.biltScreen() # update screen