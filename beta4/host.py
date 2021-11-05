from button import Button
from popup import Popup 
from screen import GameScreen
import pygame

class HostMenu(GameScreen):
    
    def __init__(self, control):
        super(HostMenu, self).__init__(control)
        self.network = control.network
        self.player = control.player
        
        # Button
        self.buttonBack = Button(130, 80, 80, 35)
        self.buttonBack.addText('Back', self.font1, 20, (255,255,255), 1, (50,50,50))

        self.buttonCreateLobby = Button(900, 80, 230, 35)
        self.buttonCreateLobby.addText('Create Lobby', self.font1, 20, (255,255,255), 1, (50,50,50))

        self.prefixNumPlayer = pygame.font.Font(self.font1, 20).render('Number of players', True, self.control.white)
        self.buttonLeft = Button(self.prefixNumPlayer.get_width() + 130 + 15, 200, 55, 35)
        self.buttonLeft.addText('←', self.font1, 20, pygame.Color('white'), pygame.Color('orange'), pygame.Color('darkgrey'))
        
        self.buttonRight = Button(450, 200, 55, 35)
        self.buttonRight.addText('→', self.font1, 20, pygame.Color('white'), pygame.Color('darkgreen'), pygame.Color('darkgrey'))
        
        # Player numbers
        self.numPlayer = 5
        self.rectNumPlayer = pygame.Rect(self.buttonLeft.rect.right, self.buttonRight.rect.y, 
        self.buttonRight.rect.left - self.buttonLeft.rect.right, self.buttonRight.rect.height)

        # Background
        self.hostBoard = pygame.transform.scale(control.hostBoard, (1180, 620))
        self.popupBackground = control.popupBackground


        # Role Selection
        self.roleMorgana = False
        self.rolePercival = False
        self.roleOberon = False
        self.roleMordred = False
        self.roleMinion = True

        # Role Selector
        buttonWidth, buttonHeight = 160, 160
        self.offFilter = pygame.transform.scale(self.control.offFilter, (buttonWidth, buttonHeight))
        self.lock = pygame.transform.scale(self.control.lock, (int(buttonWidth*3/4), buttonHeight))
        self.buttonRole1 = Button(self.display.get_width()//2 + 30, 140, buttonWidth, buttonHeight)
        self.buttonRole1.addText('Morgana and Percival', self.font1, 20)
        self.buttonRole1.addImage(self.control.morganaPercival)
        self.buttonRole2 = Button(self.buttonRole1.rect.right + 60, 140, buttonWidth, buttonHeight)
        self.buttonRole2.addText('Mordred', self.font1, 50)
        self.buttonRole2.addImage(self.control.mordred)
        self.buttonRole3 = Button(self.buttonRole1.rect.x, self.buttonRole1.rect.bottom + 60, buttonWidth, buttonHeight)
        self.buttonRole3.addText('Oberon', self.font1, 50)
        self.buttonRole3.addImage(self.control.oberon)

        self.roleFrame = pygame.transform.scale(self.control.roleFrame, (buttonWidth + 25, buttonHeight + 25))

        self.count = 0

        # Role optimize using image button
        # self.roleButton = Button()
    def configRole(self, maxrole, buttonList):
        for button in buttonList:
            self.display.blit(self.roleFrame, (button.rect.centerx - self.roleFrame.get_width()//2, 
            button.rect.centery - self.roleFrame.get_height()//2))
            button.draw(self.display) 
        if self.buttonRole1.isButtonClick():
            if not self.roleMorgana and self.count < maxrole:
                self.count += 1
                self.roleMorgana = True
                self.rolePercival = True
            elif self.roleMorgana and self.rolePercival:
                self.count -= 1
                self.roleMorgana = False
                self.rolePercival = False
        if not self.roleMorgana:
            self.display.blit(self.offFilter, self.buttonRole1.rect)
        if self.buttonRole2.isButtonClick():
            if not self.roleMordred and self.count < maxrole:
                self.count += 1
                self.roleMordred = True
            elif self.roleMordred:
                self.count -= 1
                self.roleMordred = False
        if not self.roleMordred:
            self.display.blit(self.offFilter, self.buttonRole2.rect)
        if self.buttonRole3.isButtonClick():
            if not self.roleOberon and self.count < maxrole:
                self.count += 1
                self.roleOberon = True
            elif self.roleOberon:
                self.count -= 1
                self.roleOberon = False
        if not self.roleOberon:
            self.display.blit(self.offFilter, self.buttonRole3.rect)
        
        if self.count == maxrole:
            self.roleMinion = False
            if not self.roleMorgana and not self.rolePercival:
                self.display.blit(self.lock, (self.buttonRole1.rect.centerx - self.lock.get_width()//2, self.buttonRole1.rect.y))
            if not self.roleMordred:
                self.display.blit(self.lock, (self.buttonRole2.rect.centerx - self.lock.get_width()//2, self.buttonRole2.rect.y))
            if not self.roleOberon:
                self.display.blit(self.lock, (self.buttonRole3.rect.centerx - self.lock.get_width()//2, self.buttonRole3.rect.y))
        elif self.count < maxrole:
            self.roleMinion = True
    
    def displayScreen(self):

        buttonList = [self.buttonBack, self.buttonCreateLobby, self.buttonLeft, self.buttonRight]
        rolebuttonList = [self.buttonRole1, self.buttonRole2, self.buttonRole3]
        self.displayRunning = True
        
        while self.displayRunning:

            self.checkEvent()
            fontColor = pygame.Color('black')
            # page blackground
            self.display.fill((0, 0, 0))

            self.display.blit(self.hostBoard, (50, 50))

            self.drawText('Host Menu', 20 , self.screenWidth/2, 100, self.font1, self.control.white)

            # Lobby Config UI
            self.display.blit(self.prefixNumPlayer, (self.buttonLeft.rect.left - self.prefixNumPlayer.get_width() - 15, 
            self.buttonLeft.rect.y + (35 -20)//2))
            numPlayerSurface = pygame.font.Font(self.font1, 20).render(str(self.numPlayer), True, fontColor)
            pygame.draw.rect(self.display, pygame.Color('white'), self.rectNumPlayer)
            self.display.blit(numPlayerSurface, (self.rectNumPlayer.centerx - numPlayerSurface.get_width()//2, 
            self.rectNumPlayer.centery - numPlayerSurface.get_height()//2))

            for button in buttonList:
                button.draw(self.display)

            if self.buttonLeft.isButtonClick():
                self.numPlayer -= 1
                if self.numPlayer < 5:
                    self.numPlayer = 10
            if self.buttonRight.isButtonClick():
                self.numPlayer += 1
                if self.numPlayer > 10:
                    self.numPlayer = 5
                    
            # Role selector
            # Number Player -> Evil Number -> Can choose role on certain number
            if self.numPlayer <= 6: # can select 1 evil role + assasin
                self.configRole(1, rolebuttonList)
            if self.numPlayer > 6 and self.numPlayer < 10: # can select 2 evil role + assasin
                self.configRole(2, rolebuttonList)
            if self.numPlayer > 9: # can select 3 evil role + assasin
                self.configRole(3, rolebuttonList)
            if self.buttonBack.isButtonClick():
                if self.roleMinion:
                    print('there is minion')
                if self.roleMordred:
                    print('there is mordred')
                if self.roleMorgana:
                    print('there is morgana')
                if self.roleOberon:
                    print('there is oberon')
                if self.rolePercival:
                    print('there is percival')
                self.roleMordred = False
                self.roleMorgana = False
                self.roleOberon = False
                self.rolePercival = False
                self.roleMinion = True
                self.count = 0
                if self.network.connectStatus == True:
                    self.network.disconnectFromServer()
                self.changePageByInput(True)

            if self.buttonCreateLobby.isButtonClick():
                # if self.network.createLobby(self.numPlayer, [True, False, True, False, True, False, True, False], 0, 0):
                if self.network.createLobby(self.numPlayer, [True, self.rolePercival, True, self.roleMordred, 
                True, self.roleMorgana, self.roleMinion, self.roleOberon], 0, 0):
                    if self.network.joinGame():
                        self.player.host = True
                        self.player.id = 0
                        self.changePageByInput(True, self.control.createPlayer)
                    else:
                        print("[GAME] Cannot join game") # pop up here
                        self.lobbyFailed = True
                else:
                    print("[GAME] Cannot create lobby") # pop up error
                    self.lobbyFailed = True

            self.biltScreen() # update screen