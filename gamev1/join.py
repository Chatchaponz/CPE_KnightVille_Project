import pygame, sys
from button import Button
from client import Client
from player import Player
from screen import GameScreen
from role import Role

class Join(GameScreen):
    
    def __init__(self, state):
        super(Join, self).__init__(state)

        # Image / Button goes here vvvv
        self.buttonBack = Button(100, 100, 100, 50)
        self.buttonBack.addText('Back', self.font, 20, (255,255,255), 1, (50,50,50))
        

    
    def displayScreen(self):
        if self.state.previousState != self.state.host:
            GameScreen.b = Client('25.66.152.97')
            GameScreen.b.connect()
            GameScreen.b.join()

        bConnect = True
        self.displayRunning = True

        player = Player(20, 200, 0, "Test Player")
        player.setRole(Role(0))

        blackground = pygame.image.load('images/kai.jpeg').convert_alpha()
        blackground = pygame.transform.scale(blackground, (1280,720))
        
        clock = pygame.time.Clock()
        while self.displayRunning:
            playersData = []

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        if playersData != []:
                            player.revealRole(playersData)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_z:
                        if playersData != []:
                            player.unrevealRole(playersData)
                player.playerMovement(event)

            # page blackground
            self.display.fill((0, 0, 0))
            self.display.blit(blackground,(0,0))

            # Things in page vvv
            if bConnect:
                othersPlayerInfo =  GameScreen.b.send([player.x,player.y,player.skin, player.name, player.getRole()])
                if othersPlayerInfo != None:
                    if len(playersData) > len(othersPlayerInfo):
                        playersData.pop(len(playersData) - 1)
                    for count, thisInfo in enumerate(othersPlayerInfo):
                        if count >= len(playersData) and thisInfo[1] != '':
                            tempPlayer = Player(thisInfo[1][0], thisInfo[1][1],thisInfo[1][2],thisInfo[1][3])
                            tempPlayer.setRole(thisInfo[1][4])
                            playersData.append(tempPlayer)
                        if len(playersData) > 0:
                            playersData[count].updatePosition(thisInfo[1][0], thisInfo[1][1])
                            playersData[count].draw(self.display)
                    
            player.draw(self.display)

            player.update()

            self.buttonBack.draw(self.display)
            if self.buttonBack.isButtonClick():
                GameScreen.b.disconnect()
                bConnect = False
                self.changePageByInput(True, self.state.previousState)
            

            self.biltScreen() # update screen
            clock.tick(60) # run at 60 fps