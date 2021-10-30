import pygame
import os
from button import Button 
from screen import GameScreen


class CreatePlayer(GameScreen):
    
    def __init__(self, control):
        super(CreatePlayer, self).__init__(control)
        self.network = control.network
        self.player = control.player
        # Image / Button goes here vvvv
        
        self.buttonJoin = Button(100, 200, 100, 50)
        self.buttonJoin.addText('Join', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonLeft = Button(200, 300, 100, 50)
        self.buttonLeft.addText('←', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonRight = Button(900, 300, 100, 50)
        self.buttonRight.addText('→', self.font, 20, (255,255,255), 1, (50,50,50))

        #load skins
        self.skins = []
        imagePath = "images/skins/"
        skinList = os.listdir(imagePath)
        for nameSkin in skinList:
            self.skins.append(pygame.image.load( imagePath + nameSkin).convert_alpha())
        self.amountSkins = len(self.skins)
             
    def displayScreen(self):

        self.displayRunning = True

        skin = 0
        self.player.isPlaying = False
        
        while self.displayRunning:

            self.checkEvent()

            # page blackground
            self.display.fill((0, 0, 0))

            # Things in page vvv
            self.buttonJoin.draw(self.display)
            if self.buttonJoin.isButtonClick():
                if self.network.joinGame():
                    if self.player.host == True:
                        self.player.id = 0
                    self.changePageByInput(True, self.control.lobby)
                    self.player.setAttribute(50, 700, skin, "Test player")
                else:
                    print("[GAME] Cannot join game") # pop up here


            self.display.blit(self.skins[skin], ((self.screenWidth//2) - 95, 300))
            self.buttonLeft.draw(self.display)
            if self.buttonLeft.isButtonClick():
                if skin == 0:
                    skin = self.amountSkins-1
                else:
                    skin -= 1

            self.buttonRight.draw(self.display)
            if self.buttonRight.isButtonClick():
                if skin == self.amountSkins-1:
                    skin = 0
                else:
                    skin += 1

            self.drawText('Create Player[Under construction]', 20 , 100, 100, self.font, self.control.white)
            self.drawText('Your test character already created', 20 , 100, 150, self.font, self.control.white)
            self.biltScreen() # update screen