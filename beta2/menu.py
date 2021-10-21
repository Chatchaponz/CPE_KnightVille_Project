from button import Button 
from screen import GameScreen

class MainMenu(GameScreen):
    
    def __init__(self, control):
        super(MainMenu, self).__init__(control)
        self.network = control.network
        # Image / Button goes here
        self.buttonOption = Button(100, 100, 100, 50)
        self.buttonOption.addText('Option', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonHost = Button(100, 150, 100, 50)
        self.buttonHost.addText('Host', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonJoin = Button(100, 200, 100, 50)
        self.buttonJoin.addText('Join', self.font, 20, (255,255,255), 1, (50,50,50))


    
    def displayScreen(self):

        self.displayRunning = True
        
        while self.displayRunning:

            self.checkEvent()
            self.display.fill((0, 0, 0))

            self.buttonOption.draw(self.display)
            self.changePageByButton(self.buttonOption, self.control.option)

            # NEED POPUP HERE
            self.buttonHost.draw(self.display)
            if self.buttonHost.isButtonClick():
                if self.network.tryConnectServer("25.66.152.97", 5555):
                    self.changePageByInput(True, self.control.host)
                else:
                    print("[GAME] Unable to connect server")
            
            self.buttonJoin.draw(self.display)
            if self.buttonJoin.isButtonClick():
                if self.network.tryConnectServer("25.66.152.97", 5555):
                    self.changePageByInput(True, self.control.createPlayer)
                else:
                    print("[GAME] Unable to connect server")

            self.drawText('Main Menu', 20 , 100, 100)
            self.biltScreen()