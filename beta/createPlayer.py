from button import Button 
from screen import GameScreen
from player import Player

class CreatePlayer(GameScreen):
    
    def __init__(self, control):
        super(CreatePlayer, self).__init__(control)
        self.network = control.network
        self.player = control.player
        # Image / Button goes here vvvv
        
        self.buttonJoin = Button(100, 200, 100, 50)
        self.buttonJoin.addText('Join', self.font, 20, (255,255,255), 1, (50,50,50))

    
    def displayScreen(self):

        self.displayRunning = True

        
        self.player.setAttribute(50, 700, 0, "Test player")

        
        while self.displayRunning:

            self.checkEvent()

            # page blackground
            self.display.fill((0, 0, 0))

            # Things in page vvv
            self.buttonJoin.draw(self.display)
            if self.buttonJoin.isButtonClick():
                if self.network.joinGame():
                    if self.player.host == True:
                        self.player.id = 0
                    self.changePageByInput(True, self.control.lobby)
                else:
                    print("[GAME] Cannot join game") # pop up here

            self.drawText('Create Player[Under construction]', 20 , 100, 100)
            self.drawText('Your test character already created', 20 , 100, 150)
            self.biltScreen() # update screen