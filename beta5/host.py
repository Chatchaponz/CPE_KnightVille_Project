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
        self.buttonBack.addText('Back', self.font1, 20, (255,255,255), 1, (50,50,50))

        self.buttonCreateLobby = Button(970, 600, 230, 35)
        self.buttonCreateLobby.addText('Create Lobby', self.font1, 20, (255,255,255), 1, (50,50,50))

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
        self.roleMorgana = False
        self.rolePercival = False
        self.roleOberon = False
        self.roleMordred = False
        self.roleMinion = True

        # Role Selector
        buttonWidth, buttonHeight = 120, 120

        self.buttonRole1 = Button(self.screenWidth//2 + 60, 250, buttonWidth, buttonHeight)
        self.buttonRole1.addImage(self.control.oberon)

        self.buttonRole2 = Button(self.buttonRole1.rect.right + 60, self.buttonRole1.rect.y, buttonWidth, buttonHeight)
        self.buttonRole2.addImage(self.control.mordred)

        self.buttonRole3 = Button((self.buttonRole1.rect.x + self.buttonRole2.rect.x)/2, self.buttonRole1.rect.bottom + 70, 
        buttonWidth, buttonHeight)
        self.buttonRole3.addImage(self.control.morganaPercival)

        # Nonselectable role image
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
        # dummy
        dummy_string = 'Unknown Error'
        dummy_colorhighlight = pygame.Color('red')
        popWidth, popHeight = 300, 130
        self.createFailed = Popup((self.screenWidth - popWidth)//2, (self.screenHeight - popHeight)//2, popWidth, popHeight, dummy_string,
        self.control.white, dummy_colorhighlight)
        self.joinFailed = Popup((self.screenWidth - popWidth)//2, (self.screenHeight - popHeight)//2, popWidth, popHeight, dummy_string,
        self.control.white, dummy_colorhighlight)

        # Tracking connect state
        self.createSuccess = True
        self.joinSuccess = True

    def resetRole(self):
        self.roleMordred = False
        self.roleMorgana = False
        self.roleOberon = False
        self.rolePercival = False
        self.roleMinion = True
        self.count = 0
        
    def configRole(self, maxrole, buttonList):
        for button in buttonList:
            self.display.blit(self.roleFrame, (button.rect.centerx - self.roleFrame.get_width()//2, 
            button.rect.centery - self.roleFrame.get_height()//2))
            button.draw(self.display) 
        if self.buttonRole1.isButtonClick():
            if not self.roleOberon and self.count < maxrole:
                self.count += 1
                self.roleOberon = True
            elif self.roleOberon:
                self.count -= 1
                self.roleOberon = False
        if self.roleOberon:
            self.display.blit(self.checked, (self.buttonRole1.rect.right - self.checked.get_width()//2, 
            self.buttonRole1.rect.top - self.checked.get_height()//2))
        if self.buttonRole2.isButtonClick():
            if not self.roleMordred and self.count < maxrole:
                self.count += 1
                self.roleMordred = True
            elif self.roleMordred:
                self.count -= 1
                self.roleMordred = False
        if self.roleMordred:
            self.display.blit(self.checked, (self.buttonRole2.rect.right - self.checked.get_width()//2, 
            self.buttonRole2.rect.top - self.checked.get_height()//2))
        if self.buttonRole3.isButtonClick():
            if not self.roleMorgana and self.count < maxrole:
                self.count += 1
                self.roleMorgana = True
                self.rolePercival = True
            elif self.roleMorgana and self.rolePercival:
                self.count -= 1
                self.roleMorgana = False
                self.rolePercival = False
        if self.roleMorgana and self.rolePercival:
            self.display.blit(self.checked, (self.buttonRole3.rect.right - self.checked.get_width()//2, 
            self.buttonRole3.rect.top - self.checked.get_height()//2))
        
        if self.numPlayer <= 6 and self.count > 1: # select role exceed the amount player format
            self.resetRole()
        if self.numPlayer > 6 and self.numPlayer < 10 and self.count > 2: # select role exceed the amount player format
            self.resetRole()

        if self.count == maxrole:
            self.roleMinion = False
            if not self.roleOberon:
                self.display.blit(self.offFilter, self.buttonRole1.rect)
                self.display.blit(self.lock, (self.buttonRole1.rect.centerx - self.lock.get_width()//2, self.buttonRole1.rect.y))
                self.lockSoundOn = True            
            if not self.roleMordred:
                self.display.blit(self.offFilter, self.buttonRole2.rect)
                self.display.blit(self.lock, (self.buttonRole2.rect.centerx - self.lock.get_width()//2, self.buttonRole2.rect.y))
                self.lockSoundOn = True
            if not self.roleMorgana and not self.rolePercival:
                self.display.blit(self.offFilter, self.buttonRole3.rect)
                self.display.blit(self.lock, (self.buttonRole3.rect.centerx - self.lock.get_width()//2, self.buttonRole3.rect.y))
                self.lockSoundOn = True
            if not self.roleMinion:
                self.display.blit(self.offFilter, self.minionRect)
                self.display.blit(self.lock, (self.minionRect.centerx - self.lock.get_width()//2, self.minionRect.y))
                self.lockSoundOn = True
        elif self.count < maxrole:
            self.roleMinion = True
            self.lockSoundOn = False
            self.alreadyPlay = False

        if self.lockSoundOn == True and self.alreadyPlay == False:
            self.control.playSoundWithVol(self.soundList[6],self.control.getSoundEffectVol())
            self.alreadyPlay = True
    
    def displayScreen(self):

        buttonList = [self.buttonBack, self.buttonCreateLobby, self.buttonLeft, self.buttonRight]
        rolebuttonList = [self.buttonRole1, self.buttonRole2, self.buttonRole3]
        nonselectableRoles = [[self.merlin, self.merlinRect], [self.servant, self.servantRect], [self.assasin, self.assasinRect], 
        [self.minion, self.minionRect]]
        
        self.displayRunning = True
        
        while self.displayRunning:

            self.checkEvent()
            fontColor = pygame.Color('black')
            # page blackground
            self.display.blit(self.hostBoard, (0, 0))
            self.drawText('HOST SETTING', 45 , self.screenWidth/2, 100, self.font1, self.control.black)

            pygame.draw.rect(self.display, pygame.Color('black'), (self.screenWidth//2 - 2, self.buttonLeft.rect.y + 65, 4, 410))

            # Host Config UI
            self.display.blit(self.prefixNumPlayer, (self.buttonLeft.rect.left - self.prefixNumPlayer.get_width() - 15, 
            self.buttonLeft.rect.y + (35 -20)//2))
            numPlayerSurface = pygame.font.Font(self.font1, 28).render(str(self.numPlayer), True, fontColor)
            pygame.draw.rect(self.display, pygame.Color('white'), self.rectNumPlayer)
            self.display.blit(numPlayerSurface, (self.rectNumPlayer.centerx - numPlayerSurface.get_width()//2, 
            self.rectNumPlayer.centery + 5 - numPlayerSurface.get_height()//2))

            self.drawText('Special Role (Optional)', 28, self.buttonRole3.rect.centerx, 200, self.font1, self.control.black)
            self.drawText('Standard Role', 28, (self.merlinRect.centerx + self.servantRect.centerx)/2, 200, self.font1, self.control.black)

            for button in buttonList:
                button.draw(self.display)

            for role, rect in nonselectableRoles:
                self.display.blit(self.roleFrame, (rect.centerx - self.roleFrame.get_width()//2, 
                rect.centery - self.roleFrame.get_height()//2))
                self.display.blit(role, rect)  
                if not rect is self.minionRect:
                    self.display.blit(self.checked, (rect.right - self.checked.get_width()//2, 
                    rect.top - self.checked.get_height()//2))
                elif rect is self.minionRect:
                    if self.roleMinion:
                        self.display.blit(self.checked, (rect.right - self.checked.get_width()//2, 
                        rect.top - self.checked.get_height()//2))    

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
                self.configRole(1, rolebuttonList)
            if self.numPlayer > 6 and self.numPlayer < 10: # can select 2 evil role + assasin
                self.configRole(2, rolebuttonList)
            if self.numPlayer > 9: # can select 3 evil role + assasin
                self.configRole(3, rolebuttonList)
            
            # 
            if self.buttonBack.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()):
                self.resetRole()
                if self.network.connectStatus == True:
                    self.network.disconnectFromServer()
                self.changePageByInput(True)

            # Draw role name
            self.drawText('Merlin', 18 , self.merlinRect.centerx, self.merlinRect.bottom + 25, self.font1, self.control.black)
            self.drawText('Loyal Servant', 18 , self.servantRect.centerx, self.servantRect.bottom + 25, self.font1, self.control.black)
            self.drawText('of King Arthur', 18 , self.servantRect.centerx, self.servantRect.bottom + 45, self.font1, self.control.black)
            self.drawText('Oberon', 18 , self.buttonRole1.rect.centerx, self.buttonRole1.rect.bottom + 25, self.font1, self.control.black)
            self.drawText('Percival / Morgana', 18 , self.buttonRole3.rect.centerx, self.buttonRole3.rect.bottom + 25, self.font1, 
            self.control.black)
            self.drawText('Mordred', 18 , self.buttonRole2.rect.centerx, self.buttonRole2.rect.bottom + 25, self.font1, self.control.black)
            self.drawText('Assasin', 18 , self.assasinRect.centerx, self.assasinRect.bottom + 25, self.font1, self.control.black)
            self.drawText('Minion of', 18 , self.minionRect.centerx, self.minionRect.bottom + 25, self.font1, self.control.black)
            self.drawText('Mordred', 18 , self.minionRect.centerx, self.minionRect.bottom + 45, self.font1, self.control.black)

            if self.buttonCreateLobby.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()):
                # if self.network.createLobby(self.numPlayer, [True, False, True, False, True, False, True, False], 0, 0):
                createResult, createError = self.network.createLobby(self.numPlayer, [True, self.rolePercival, True, self.roleMordred, 
                                         True, self.roleMorgana, self.roleMinion, self.roleOberon], 0, 0)
                if createResult:
                    self.createSuccess = True
                    joinResult, joinError = self.network.joinGame()
                    if joinResult:
                        self.player.host = True
                        self.player.id = 0
                        self.changePageByInput(True, self.control.createPlayer)
                        self.joinSuccess = True
                    else:
                        self.joinFailed.text = joinError
                        self.joinSuccess = False

                else:
                    self.createFailed.text = createError
                    self.createSuccess = False
            # dummy
            if not self.joinSuccess:
                self.joinFailed.draw(self.display, None, 28, textAlign = 'leftAlign', bgColor = pygame.Color('lightgrey'))
                if self.joinFailed.b1.isButtonClick():
                    self.joinSuccess = True
            if not self.createSuccess:
                self.createFailed.draw(self.display, None, 28, textAlign = 'leftAlign', bgColor = pygame.Color('lightgrey'))
                if self.createFailed.b1.isButtonClick():
                    self.createSuccess = True

            self.biltScreen() # update screen