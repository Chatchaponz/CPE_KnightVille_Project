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

        # Skin
        self.skin = skin
        path = "images\skins\\"
        skins = os.listdir(path)
        self.playerSkin = pygame.image.load(path + skins[self.skin]).convert_alpha()
        self.playerRect = self.playerSkin.get_rect(bottomleft = (self.x, self.y))

        # Name
        self.name = name
        self.fontColor = (255, 255, 255)
        self.font = pygame.font.Font('font\Taviraj-Black.ttf', 25)
        self.playerName = self.font.render(self.name, False, self.fontColor)

        # Role
        self.__role = None
        self.__roleReveal = False
        self.__identityReveal = False
        self.__unknownReveal = False


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
        self.__role.doSpecial(otherPlayers)
    
    def unrevealRole(self, otherPlayers):
        self.__roleReveal = False
        for player in otherPlayers:
            player.setRoleReveal(False)
            player.setIdentityReveal(False)
            player.setUnknownReveal(False)

    def updatePosition(self, x, y):
        self.playerRect = self.playerSkin.get_rect(bottomleft = (int(x), int(y)))
    
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