import pygame
from mainMenu import MainMenu
from optionMenu import OptionMenu
from credit import CreditsMenu

class Page():
    def __init__(self):
        pygame.init()
        self.programRunning = True
        self.loopRunning = False
        self.displayWidth = 1280
        self.displayHeight = 720

        self.display = pygame.Surface((self.displayWidth, self.displayHeight))
        self.screne = pygame.display.set_mode((self.displayWidth, self.displayHeight))

        self.textPositionW = self.displayWidth/2
        self.textPositionH = self.displayHeight/2

        self.fontName = 'Taviraj-Black.TTF'

        self.mainMenu = MainMenu(self)
        self.option = OptionMenu(self)
        self.credits = CreditsMenu(self)
        #self.lobby = LobbyRoom()
        #self.changeAvatar = ChangeAvatar()
        #self.gameSetting = GameSetting()
        #self.mainGame = MainGame()

        self.enterKey = False
        self.backKey = False
        self.wKey = False
        self.aKey = False
        self.sKey = False
        self.dKey = False

        self.oKey = False #for option
        self.mKey = False #for MainMenu
        self.cKey = False #for credit

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.currentState = self.mainMenu

    def updateState(self):
        self.previousState = self.currentState

    def getCurrentState(self):
        if self.currentState == self.mainMenu:
            return 'main menu'
        elif self.currentState == self.option:
            return 'option'
        elif self.currentState == self.credits:
            return 'credits'
        #elif self.currentState == self.lobby:
        #    return 'lobby'
        #elif self.currentState == self.changeAvatar:
        #    return 'changeAvatar'
        #elif self.currentState == self.gameSetting:
        #    return 'gameSetting'
        #elif self.currentState == self.mainGame:
        #    return 'mainGame'
        else:
            return 'no state'
        #return self.currentState

    def loop(self):
        while self.loopRunning:
            self.checkEvent()
            if self.enterKey:
                self.loopRunning = False
            # for event in pygame.event.get():
            #    if event.type == pygame.KEYDOWN:
            #        if self.previousState == self.mainMenu:
            #            if self.currentState == self.option:
            #                self.currentState.displayOption()
            #        elif self.previousState == self.option:
            #            if self.currentState == self.mainMenu:
            #                self.currentState.displayMenu()
            self.display.fill(self.black)
            self.drawText('no state', 50, self.textPositionW, self.textPositionH)
            self.screne.blit(self.display, (0,0))
            pygame.display.update()
            self.resetKeys()
            

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.programRunning = False
                self.currentState.displayRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.enterKey = True
                if event.key == pygame.K_BACKSPACE:
                    self.backKey = True
                if event.key == pygame.K_w:
                    self.wKey = True
                if event.key == pygame.K_a:
                    self.aKey = True
                if event.key == pygame.K_s:
                    self.sKey = True
                if event.key == pygame.K_d:
                    self.dKey = True
                if event.key == pygame.K_o:
                    self.oKey = True
                if event.key == pygame.K_m:
                    self.mKey = True
                if event.key == pygame.K_c:
                    self.cKey = True
                if event.key == pygame.K_q:
                    pygame.quit()

    def resetKeys(self):
        self.enterKey = False
        self.backKey = False
        self.wKey = False
        self.aKey = False
        self.sKey = False
        self.dKey = False
        self.oKey = False
        self.mKey = False
        self.cKey = False

    def drawText(self, text, size, x, y):
        font = pygame.font.Font(self.fontName, size)
        textSurface = font.render(text, True, self.white)
        textRect = textSurface.get_rect()
        textRect.center = (x, y)
        self.display.blit(textSurface, textRect)