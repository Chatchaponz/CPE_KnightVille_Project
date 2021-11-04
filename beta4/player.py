from sys import path
import pygame
import os


class Player:
    def __init__(self, x = 0, y = 0, skin = 0, name = "Unknown"):
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

        # Name
        self.name = name
        self.fontColor = (255, 255, 255)
        self.font = pygame.font.Font('font/Taviraj-Black.ttf', 25)
        self.playerName = self.font.render(self.name, True, self.fontColor)

        # Role
        self.__role = None
        self.__roleReveal = False
        self.__identityReveal = False
        self.__unknownReveal = False

        # Player addr (id)
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
        if(self.__role != None):
        # Role reveal
            if(self.__roleReveal == True):
                roleName = self.font.render("<" + self.__role.getName() + ">", False, self.fontColor)
                roleNameRect = roleName.get_rect(center = (nameX, nameY))
                screen.blit(roleName, roleNameRect)
                nameY -= 25
        # Identity reveal
            if(self.__identityReveal == True):
                pygame.draw.rect(screen, (255,0,0), pygame.Rect(nameX, nameY - 25, 30, 30) )
        # Unknown reveal
            if(self.__unknownReveal == True):
                pygame.draw.rect(screen, (100,100,100), pygame.Rect(nameX, nameY - 25, 30, 30) )
        
        # Party leader
            if(self.partyLeader == True):
                pygame.draw.rect(screen, (0,255,0), pygame.Rect(nameX, nameY - 25, 30, 30) )
        
        # Party Member
            if(self.isSelected == True):
                pygame.draw.rect(screen, (0,0,255), pygame.Rect(nameX, nameY - 50, 30, 30) )
        
        # Target
            if(self.isTarget == True):
                pygame.draw.rect(screen, (255,0,255), pygame.Rect(nameX, nameY - 50, 30, 30) )
        
        # Killed
            if(self.isKilled == True):
                pygame.draw.rect(screen, (255,255,0), pygame.Rect(nameX, nameY - 50, 30, 30) )

        # Draw player's name
        playerNameRect = self.playerName.get_rect(center = (nameX, nameY))
        screen.blit(self.playerName, playerNameRect)
        # Draw player
        screen.blit(self.playerSkin, self.playerRect)
    
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
            self.__role.doSpecial(otherPlayers)
    
    def unrevealRole(self, otherPlayers):
        self.__roleReveal = False
        for player in otherPlayers:
            player.setRoleReveal(False)
            player.setIdentityReveal(False)
            player.setUnknownReveal(False)
    
    def updateByPosition(self, x, y):
        self.x = x
        self.y = y
        self.playerRect = self.playerSkin.get_rect(bottomleft = (int(self.x), int(self.y)))
    
    def setAttribute(self, x = 0, y = 0, skin = 0, name = "Unknown"):
        self.x = x
        self.y = y

        self.skin = skin
        self.playerSkin = pygame.image.load( self.imagePath + self.skinList[self.skin]).convert_alpha()
        self.playerRect = self.playerSkin.get_rect(bottomleft = (self.x, self.y))
        
        self.name = name
        self.playerName = self.font.render(self.name, True, self.fontColor)
    
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
            if event.key == pygame.K_LEFT:
                self.goLeft = True
            if event.key == pygame.K_RIGHT:
                self.goRight = True
            if event.key == pygame.K_UP:
                self.goUp = True
            if event.key == pygame.K_DOWN:
                self.goDown = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.goLeft = False
            if event.key == pygame.K_RIGHT:
                self.goRight = False
            if event.key == pygame.K_UP:
                self.goUp = False
            if event.key == pygame.K_DOWN:
                self.goDown = False