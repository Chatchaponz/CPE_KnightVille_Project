from button import Button
from popup import Popup 
from screen import GameScreen
import pygame

class HostMenu(GameScreen):
    
    def __init__(self, control):
        super(HostMenu, self).__init__(control)
        self.network = control.network
        self.player = control.player
        

        # Sound goes here 
        self.soundList = control.soundList
        # self.soundEffectVol = control.soundEffectVol
        self.clickChoiceSound = self.soundList[2]
        self.lockSoundOn = True
        self.alreadyPlay = False

        # Button
        self.buttonBack = Button(80, 80, 80, 35)
        self.buttonBack.addText('BACK', self.font2, 20, (255,255,255), 1, (50,50,50))

        self.buttonCreateLobby = Button(1000, 600, 200, 35)
        self.buttonCreateLobby.addText('CREATE LOBBY', self.font2, 20, (255,255,255), 1, (50,50,50))

        self.prefixNumPlayer = pygame.font.Font(self.font1, 20).render('Number of players', True, self.control.black)
        
        self.buttonLeft = Button(self.screenWidth//2 - (self.prefixNumPlayer.get_width() - 180)//2, 140, 55, 30)
        self.buttonLeft.addText('<', self.font1, 20, pygame.Color('white'), pygame.Color('orange'), pygame.Color('darkgrey'))
        
        self.buttonRight = Button(self.buttonLeft.rect.right + 70, self.buttonLeft.rect.y, 55, self.buttonLeft.rect.height)
        self.buttonRight.addText('>', self.font1, 20, pygame.Color('white'), pygame.Color('darkgreen'), pygame.Color('darkgrey'))
        
        # Player numbers
        self.numPlayer = 5
        self.rectNumPlayer = pygame.Rect(self.buttonLeft.rect.right, self.buttonRight.rect.y, 
        self.buttonRight.rect.left - self.buttonLeft.rect.right, self.buttonRight.rect.height)

        # Background
        self.hostBoard = pygame.transform.scale(control.hostBoard, (1280, 720))

        # Role Selection State
        self.role = [False, False, False, False, True] # Moudred, Oberon, Morgana, Percival, Minion of moudred

        # Special role image/button
        buttonWidth, buttonHeight = 120, 120

        self.buttonRole1 = Button(self.screenWidth//2 + 60, 250, buttonWidth, buttonHeight)
        self.buttonRole1.addImage(self.control.oberon)

        self.buttonRole2 = Button(self.buttonRole1.rect.right + 60, self.buttonRole1.rect.y, buttonWidth, buttonHeight)
        self.buttonRole2.addImage(self.control.mordred)

        self.buttonRole3 = Button((self.buttonRole1.rect.x + self.buttonRole2.rect.x)/2, self.buttonRole1.rect.bottom + 70, 
        buttonWidth, buttonHeight)
        self.buttonRole3.addImage(self.control.morganaPercival)

        # Standard role image
        self.minion = pygame.transform.scale(self.control.minion, (buttonWidth, buttonHeight))
        self.minionRect = pygame.Rect(self.screenWidth//2 - ((self.buttonRole1.rect.width) + 60), 
        self.buttonRole3.rect.y, buttonWidth, buttonHeight)

        self.assasin = pygame.transform.scale(self.control.assasin, (buttonWidth, buttonHeight))
        self.assasinRect = pygame.Rect(self.screenWidth//2 - ((self.buttonRole1.rect.width * 2) + 120), 
        self.buttonRole3.rect.y, buttonWidth, buttonHeight)

        self.servant = pygame.transform.scale(self.control.servant, (buttonWidth, buttonHeight))
        self.servantRect = pygame.Rect(self.screenWidth//2 - ((self.buttonRole1.rect.width) + 60), 
        self.buttonRole1.rect.y, buttonWidth, buttonHeight)

        self.merlin = pygame.transform.scale(self.control.merlin, (buttonWidth, buttonHeight))
        self.merlinRect = pygame.Rect(self.screenWidth//2 - ((self.buttonRole1.rect.width * 2) + 120), 
        self.buttonRole1.rect.y, buttonWidth, buttonHeight)

        # Decoration Layer
        self.offFilter = pygame.transform.scale(self.control.offFilter, (buttonWidth, buttonHeight))
        
        self.lock = pygame.transform.scale(self.control.lock, (int(buttonWidth*3/4), buttonHeight))

        self.roleFrame = pygame.transform.scale(self.control.roleFrame, (buttonWidth + 25, buttonHeight + 25))
        
        self.checked = pygame.transform.scale(self.control.checked, (buttonWidth - 75, buttonHeight - 75))

        # Role number
        self.count = 0

        # Popup
        dummy_string = 'Unknown Error' # DUMMY
        popWidth, popHeight = 500, 130
        self.hostFailed = Popup((self.screenWidth - popWidth)//2, (self.screenHeight - popHeight)//2, popWidth, popHeight, dummy_string,
        self.control.white, pygame.Color('darkblue'))
        self.hostFailed.adjustComponents(bWidth = 60)
        self.hostFailed.modComponents(self.hostFailed.b1, 'button', (97, 63, 45), (130,83,50), 'CLOSE', self.font2)

        # Tracking connect state
        self.hostSuccess = True

    def resetRole(self):
        # Reset Role
        self.role = [False, False, False, False, True] 
        self.count = 0
        
    def configRole(self, maxrole, buttonList):
        # Draw role selector button
        for button, name in buttonList:
            self.display.blit(self.roleFrame, (button.rect.centerx - self.roleFrame.get_width()//2, 
            button.rect.centery - self.roleFrame.get_height()//2))
            button.draw(self.display)
            self.drawText(name, 22 , button.rect.centerx, button.rect.bottom + 35, self.font2, self.control.black) 

        # Role Oberon
        if self.buttonRole1.isButtonClick():
            # Check Role Number can be available
            if not self.role[4] and self.count < maxrole:
                self.count += 1
                self.role[4] = True
            elif self.role[4]:
                self.count -= 1
                self.role[4] = False
        # Display role available
        if self.role[4]:
            self.display.blit(self.checked, (self.buttonRole1.rect.right - self.checked.get_width()//2, 
            self.buttonRole1.rect.top - self.checked.get_height()//2))
        
        # Role Mordred
        if self.buttonRole2.isButtonClick():
            # Check Role Number can be available
            if not self.role[1] and self.count < maxrole:
                self.count += 1
                self.role[1] = True
            elif self.role[1]:
                self.count -= 1
                self.role[1] = False
        # Display role available
        if self.role[1]:
            self.display.blit(self.checked, (self.buttonRole2.rect.right - self.checked.get_width()//2, 
            self.buttonRole2.rect.top - self.checked.get_height()//2))

        # Role Morgana and Percival
        if self.buttonRole3.isButtonClick():
            # Check Role Number can be available
            if not self.role[2] and self.count < maxrole:
                self.count += 1
                self.role[2] = True
                self.role[0] = True
            elif self.role[2] and self.role[0]:
                self.count -= 1
                self.role[2] = False
                self.role[0] = False
        # Display role available
        if self.role[2] and self.role[0]:
            self.display.blit(self.checked, (self.buttonRole3.rect.right - self.checked.get_width()//2, 
            self.buttonRole3.rect.top - self.checked.get_height()//2))
        
        # Verify Role Number due to the Player Number and Rules
        if self.numPlayer <= 6 and self.count > 1: # select role exceed the amount player format
            self.resetRole()
        if self.numPlayer > 6 and self.numPlayer < 10 and self.count > 2: # select role exceed the amount player format
            self.resetRole()

        # Display not available role
        if self.count == maxrole:
            self.role[3] = False
            if not self.role[4]:
                self.display.blit(self.offFilter, self.buttonRole1.rect)
                self.display.blit(self.lock, (self.buttonRole1.rect.centerx - self.lock.get_width()//2, self.buttonRole1.rect.y))
                self.lockSoundOn = True            
            if not self.role[1]:
                self.display.blit(self.offFilter, self.buttonRole2.rect)
                self.display.blit(self.lock, (self.buttonRole2.rect.centerx - self.lock.get_width()//2, self.buttonRole2.rect.y))
                self.lockSoundOn = True
            if not self.role[2] and not self.role[0]:
                self.display.blit(self.offFilter, self.buttonRole3.rect)
                self.display.blit(self.lock, (self.buttonRole3.rect.centerx - self.lock.get_width()//2, self.buttonRole3.rect.y))
                self.lockSoundOn = True
            if not self.role[3]:
                self.display.blit(self.offFilter, self.minionRect)
                self.display.blit(self.lock, (self.minionRect.centerx - self.lock.get_width()//2, self.minionRect.y))
                self.lockSoundOn = True
        elif self.count < maxrole:
            self.role[3] = True
            self.lockSoundOn = False
            self.alreadyPlay = False

        if self.lockSoundOn == True and self.alreadyPlay == False:
            self.control.playSoundWithVol(self.soundList[6],self.control.getSoundEffectVol())
            self.alreadyPlay = True
    
    def displayScreen(self):

        self.hostSuccess = True
        buttonList = [self.buttonBack, self.buttonCreateLobby, self.buttonLeft, self.buttonRight]
        specialRoleList = [[self.buttonRole1, 'Oberon'], [self.buttonRole2, 'Mordred'], [self.buttonRole3, 'Morgana and Percival']]
        standardRoleList = [[self.merlin, self.merlinRect, 'Merlin'], [self.servant, self.servantRect, 'Royal Servant'], 
        [self.assasin, self.assasinRect, 'Assasin'], [self.minion, self.minionRect, 'Minion of Mordred']]
        
        self.displayRunning = True
        
        while self.displayRunning:

            self.checkEvent()
            # page blackground
            self.display.blit(self.hostBoard, (0, 0))
            self.drawText('Host Setting', 45 , self.screenWidth/2, 100, self.font1, self.control.black)

            pygame.draw.rect(self.display, pygame.Color('black'), (self.screenWidth//2 - 2, self.buttonLeft.rect.y + 65, 4, 410))

            # Host Config UI
            self.display.blit(self.prefixNumPlayer, (self.buttonLeft.rect.left - self.prefixNumPlayer.get_width() - 15, 
            self.buttonLeft.rect.y + (35 -20)//2))
            numPlayerSurface = pygame.font.Font(self.font2, 28).render(str(self.numPlayer), True, self.control.black)
            pygame.draw.rect(self.display, pygame.Color('white'), self.rectNumPlayer)
            self.display.blit(numPlayerSurface, (self.rectNumPlayer.centerx - numPlayerSurface.get_width()//2, 
            self.rectNumPlayer.centery + 5 - numPlayerSurface.get_height()//2))

            self.drawText('Special Role (Optional)', 28, self.buttonRole3.rect.centerx, 200, self.font1, self.control.black)
            self.drawText('Standard Role', 28, (self.merlinRect.centerx + self.servantRect.centerx)/2, 200, self.font1, self.control.black)

            # UI Button
            for button in buttonList:
                button.draw(self.display)

            # Standard Roles
            for role, rect, name in standardRoleList:
                self.display.blit(self.roleFrame, (rect.centerx - self.roleFrame.get_width()//2, 
                rect.centery - self.roleFrame.get_height()//2))
                self.display.blit(role, rect)  
                if not rect is self.minionRect:
                    self.display.blit(self.checked, (rect.right - self.checked.get_width()//2, 
                    rect.top - self.checked.get_height()//2))
                elif rect is self.minionRect:
                    if self.role[3]:
                        self.display.blit(self.checked, (rect.right - self.checked.get_width()//2, 
                        rect.top - self.checked.get_height()//2))
                self.drawText(name, 22 , rect.centerx, rect.bottom + 35, self.font2, self.control.black)    

            # Player number config
            if self.buttonLeft.isButtonClick(self.soundList[4],self.control.getSoundEffectVol()):
                self.numPlayer -= 1
                if self.numPlayer < 5:
                    self.numPlayer = 10
            if self.buttonRight.isButtonClick(self.soundList[4],self.control.getSoundEffectVol()):
                self.numPlayer += 1
                if self.numPlayer > 10:
                    self.numPlayer = 5
                    
            # Role selector
            #       Number Player -> Evil Number -> Can choose role on certain number
            if self.numPlayer <= 6: # can select 1 evil role + assasin
                self.configRole(1, specialRoleList)
            if self.numPlayer > 6 and self.numPlayer < 10: # can select 2 evil role + assasin
                self.configRole(2, specialRoleList)
            if self.numPlayer > 9: # can select 3 evil role + assasin
                self.configRole(3, specialRoleList)
            
            # Back to menu
            if self.buttonBack.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()):
                self.resetRole()
                self.numPlayer = 5
                if self.network.connectStatus == True:
                    self.network.disconnectFromServer()
                self.changePageByInput(True)

            if self.buttonCreateLobby.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()):
                # if self.network.createLobby(self.numPlayer, [True, False, True, False, True, False, True, False], 0, 0):
                createResult, createError = self.network.createLobby(self.numPlayer, [True, self.role[0], True, self.role[1], 
                                         True, self.role[2], self.role[3], self.role[4]], 0, 0)
                if createResult:
                    self.hostSuccess = True
                    joinResult, joinError = self.network.joinGame()
                    if joinResult:
                        self.player.host = True
                        self.player.id = 0
                        self.changePageByInput(True, self.control.createPlayer)
                        self.hostSuccess = True
                    else:
                        self.hostFailed.text = joinError.upper()
                        self.hostSuccess = False
                else:
                    self.hostFailed.text = createError.upper()
                    self.hostSuccess = False

            # POPUP
            if not self.hostSuccess:
                self.hostFailed.draw(self.display, self.font2, 28, textAlign = 'centerAlign', image = self.control.popupBackground)
                if self.hostFailed.b1.isButtonClick():    
                    self.hostSuccess = True
                    self.resetRole()
                    self.numPlayer = 5
                    if self.network.connectStatus == True:
                        self.network.disconnectFromServer()
                    self.changePageByInput(True, self.control.menu)

            self.biltScreen() # update screen