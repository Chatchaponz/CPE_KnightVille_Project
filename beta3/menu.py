import pygame
from button import Button 
from screen import GameScreen

class MainMenu(GameScreen):
    
    def __init__(self, control):
        super(MainMenu, self).__init__(control)
        self.network = control.network

        self.knightCover = control.knightCover
        self.BGCover = control.BGCover
        self.skyCover = control.skyCover
        self.woodBoard = control.woodBoard
        self.angle = 0

        # Image / Button goes here
        self.buttonHost = Button(300, 250, 100, 70)
        self.buttonHost.addText('Host', self.font1, 40, control.white, 1, (50,50,50))

        self.buttonJoin = Button(300, 350, 100, 70)
        self.buttonJoin.addText('Join', self.font1, 40, control.white, 1, (50,50,50))

        self.buttonOption = Button(300, 450, 100, 70)
        self.buttonOption.addText('Option', self.font1, 40, control.white, 1, (50,50,50))

        self.buttonQuit = Button(300, 550, 100, 70)
        self.buttonQuit.addText('Quit', self.font1, 40, control.white, 1, (50,50,50))


    
    def displayScreen(self):

        self.displayRunning = True
        
        while self.displayRunning:

            self.checkEvent()
            self.display.fill((0, 0, 0))

            if self.angle >= 360:
                self.angle = 0

            self.skyRotated = pygame.transform.rotate(self.skyCover, self.angle)
            self.skyRotateRect = self.skyRotated.get_rect(center = (670,670))
            self.display.blit(self.skyRotated, self.skyRotateRect)
            self.angle += 0.1

            self.display.blit(self.BGCover, (0,0))
            self.display.blit(self.knightCover, (0,0))
            self.display.blit(self.woodBoard, (145,30))

            self.buttonOption.draw(self.display)
            self.changePageByButton(self.buttonOption, self.control.option)

            # NEED POPUP HERE
            self.buttonHost.draw(self.display)
            if self.buttonHost.isButtonClick():
                if self.network.tryConnectServer("192.168.1.5", 5555):
                    self.changePageByInput(True, self.control.host)
                else:
                    print("[GAME] Unable to connect server")
            
            self.buttonJoin.draw(self.display)
            if self.buttonJoin.isButtonClick():
                if self.network.tryConnectServer("192.168.1.5", 5555):
                    self.changePageByInput(True, self.control.createPlayer)
                else:
                    print("[GAME] Unable to connect server")

            self.buttonQuit.draw(self.display)

            self.drawText('KnightVIlle', 60 , 350, 175)
            self.biltScreen()