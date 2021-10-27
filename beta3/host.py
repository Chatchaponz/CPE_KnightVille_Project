from button import Button 
from screen import GameScreen

class HostMenu(GameScreen):
    
    def __init__(self, control):
        super(HostMenu, self).__init__(control)
        self.network = control.network
        self.player = control.player
        
        # Image / Button goes here vvvv
        self.buttonBack = Button(100, 100, 100, 50)
        self.buttonBack.addText('Back', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonCreateLobby = Button(100, 150, 100, 50)
        self.buttonCreateLobby.addText('Create Lobby', self.font, 20, (255,255,255), 1, (50,50,50))
        

    
    def displayScreen(self):

        self.displayRunning = True
        
        while self.displayRunning:

            self.checkEvent()

            # page blackground
            self.display.fill((0, 0, 0))

            self.buttonBack.draw(self.display)
            if self.buttonBack.isButtonClick():
                if self.network.connectStatus == True:
                    self.network.disconnectFromServer()
                self.changePageByInput(True)

            self.buttonCreateLobby.draw(self.display)
            if self.buttonCreateLobby.isButtonClick():
                if self.network.createLobby(5, [True, False, True, False, True, False, True, False], 0, 0):
                    self.player.host = True
                    self.changePageByInput(True, self.control.createPlayer)
                else:
                    print("[GAME] Cannot create lobby") # pop up error
            
            self.drawText('Host Menu', 20 , 100, 100, self.font, self.control.white)
            self.biltScreen() # update screen