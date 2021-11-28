from sys import path
import pygame
import os


class Player:
    def __init__(self, x = 0, y = 0, skin = 0, name = "Unknown", icons = None):
        # Position
        self.x = int(x)
        self.y = int(y)
        self.speed = 7
        self.velX = 0
        self.velY = 0

        # Direction
        self.goLeft = False
        self.goRight = False
        self.goUp = False
        self.goDown = False
        self.collided = []

        # Skin
        self.skin = skin
        self.imagePath = "images/skins/"
        self.skinList = os.listdir(self.imagePath)
        self.playerSkin = pygame.image.load( self.imagePath + self.skinList[self.skin]).convert_alpha()
        self.playerRect = self.playerSkin.get_rect(bottomleft = (self.x, self.y))

        # Role icon
        self.iconListAvailable = [False,False,False,False,False,False]
        self.iconList = []
        if type(icons) is list:
            self.iconList = icons

        # Name
        self.name = name
        self.fontColor = (255, 255, 255)
        self.font = pygame.font.Font('font/Taviraj-Black.ttf', 22)
        self.playerName = self.font.render(self.name, True, self.fontColor)

        # Role
        self.__role = None
        self.__roleReveal = False
        self.__identityReveal = False
        self.__unknownReveal = False

        # Player addr
        self.address = None

        self.id = None

        self.host = False

        self.isPlaying = False

        self.choose = 0

        self.syncSignal = 0

        self.isSelected = False

        self.partyLeader = False

        self.isTarget = False

        self.isKilled = False

    def draw(self, screen):
        
        nameX, nameY = self.playerRect.midtop
        iconX = 0
        aimY = nameY + 50
        numIcon = 0
        widthIcon = 0

        # Draw Host
        if self.host == True:
            self.iconListAvailable[0] = True
            numIcon += 1
            #screen.blit(self.hostIcon, (iconX, nameY - 50))
            #iconX += 40

        # Draw player
        screen.blit(self.playerSkin, self.playerRect)

        if(self.__role != None):
        # Role reveal
            if(self.__roleReveal == True):
                roleName = self.font.render("<" + self.__role.getName() + ">", False, self.fontColor)
                roleNameRect = roleName.get_rect(center = (nameX, nameY))
                screen.blit(roleName, roleNameRect)
                nameY -= 25
        # Identity reveal
            if(self.__identityReveal == True):
                self.iconListAvailable[1] = True
                numIcon += 1
                #screen.blit(self.evil, (iconX, nameY - 50))
                #iconX += 40

        # Unknown reveal
            if(self.__unknownReveal == True):
                self.iconListAvailable[2] = True
                numIcon += 1
                #screen.blit(self.merlin, (iconX, nameY - 50))
                #iconX += 40
        
        # Party leader
            if(self.partyLeader == True):
                self.iconListAvailable[3] = True
                numIcon += 1
                #screen.blit(self.leader, (iconX, nameY - 50))
                #iconX += 40
        
        # Party Member
            if(self.isSelected == True):
                self.iconListAvailable[4] = True
                numIcon += 1
                #screen.blit(self.member, (iconX, nameY - 50))
                #iconX += 40
        
        # Target
            if(self.isTarget == True):
                #self.iconListAvailable[5] = True
                screen.blit(self.aim, (nameX - 60, aimY))
        
        # Killed
            if(self.isKilled == True):
                self.iconListAvailable[5] = True
                numIcon += 1
                #screen.blit(self.death, (nameX - 20, nameY - 50))

        widthIcon = 40 * numIcon
        iconX = nameX - (widthIcon//2)

        for i in range(len(self.iconList)):
            if (len(self.iconListAvailable) == len(self.iconList) and
                self.iconListAvailable[i] == True):
                
                screen.blit(self.iconList[i], (iconX, nameY - 50))
                iconX += 40
                self.iconListAvailable[i] = False

        # Draw player's name
        playerNameRect = self.playerName.get_rect(center = (nameX, nameY))
        # Name's background
        bgPlayerName = pygame.Surface((playerNameRect.width + 8, playerNameRect.height - 8))
        bgPlayerNameRect = bgPlayerName.get_rect(center = playerNameRect.center)
        bgPlayerName.set_alpha(100)
        bgPlayerName.fill((0, 0, 0))
        screen.blit(bgPlayerName, bgPlayerNameRect)
        screen.blit(self.playerName, playerNameRect)
    
    def update(self):
        self.velX = 0
        self.velY = 0

        if self.goLeft and not self.goRight:
            self.velX = -self.speed
        if self.goRight and not self.goLeft:
            self.velX = self.speed
        if self.goUp and not self.goDown:
            self.velY = -self.speed
        if self.goDown and not self.goUp:
            self.velY = self.speed
        
        if self.collided != [] and len(self.collided) > 1:
            if (self.x + self.velX > self.collided[0][0] and 
                self.x + self.velX < (self.collided[0][1] - self.playerRect.width)):
                self.x += self.velX
            if (self.y + self.velY > self.collided[1][0] and 
                self.y + self.velY < self.collided[1][1]):
                self.y += self.velY
        else:
            self.x += self.velX
            self.y += self.velY

        self.playerRect = self.playerSkin.get_rect(bottomleft = (int(self.x), int(self.y)))
    
    def setRole(self, role):
        self.__role = role

    def getRole(self):
        return self.__role
    
    def setRoleReveal(self, boolean = False):
        self.__roleReveal = boolean
    
    def setIdentityReveal(self, boolean = False):
        self.__identityReveal = boolean
    
    def setUnknownReveal(self, boolean = False):
        self.__unknownReveal = boolean
    
    def revealRole(self, otherPlayers):
        self.__roleReveal = True
        if self.__role != None:
            if self.__role.getName() == "Oberon":
                self.__identityReveal = True
            self.__role.doSpecial(otherPlayers)
    
    def unrevealRole(self, otherPlayers):
        self.__roleReveal = False
        self.__identityReveal = False
        for player in otherPlayers:
            player.setRoleReveal(False)
            player.setIdentityReveal(False)
            player.setUnknownReveal(False)
    
    def updateByPosition(self, x, y):
        self.x = x
        self.y = y
        self.playerRect = self.playerSkin.get_rect(bottomleft = (int(self.x), int(self.y)))
    
    def resetMovement(self):
        self.goLeft = False
        self.goRight = False
        self.goUp = False
        self.goDown = False
    
    def setAttribute(self, x = 0, y = 0, skin = 0, name = "Unknown"):
        self.x = x
        self.y = y

        self.skin = skin
        self.playerSkin = pygame.image.load( self.imagePath + self.skinList[self.skin]).convert_alpha()
        self.playerRect = self.playerSkin.get_rect(bottomleft = (self.x, self.y))
        
        self.name = name
        self.playerName = self.font.render(self.name, True, self.fontColor)

        self.resetMovement()
    
    def updateSkin(self, skin = 0):
        self.skin = skin
        self.playerSkin = pygame.image.load( self.imagePath + self.skinList[self.skin]).convert_alpha()
        self.playerRect = self.playerSkin.get_rect(bottomleft = (self.x, self.y))

    def updateName(self, name = "Unknown"):
        self.name = name
        self.playerName = self.font.render(self.name, True, self.fontColor)

    # 'event' should be event in pygame.event.get()
    def playerMovement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_LEFT, pygame.K_a]:
                self.goLeft = True
            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                self.goRight = True
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.goUp = True
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                self.goDown = True
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_a]:
                self.goLeft = False
            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                self.goRight = False
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.goUp = False
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                self.goDown = False