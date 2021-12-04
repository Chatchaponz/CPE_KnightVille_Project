from button import Button 
from screen import GameScreen
from client import Client

class Host(GameScreen):
    
    def __init__(self, state):
        super(Host, self).__init__(state)

        # Image / Button goes here vvvv
        self.buttonBack = Button(100, 100, 100, 50)
        self.buttonBack.addText('Back', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonCreate = Button(100, 150, 100, 50)
        self.buttonCreate.addText('Create Room', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonJoin = Button(100, 200, 100, 50)
        self.buttonJoin.addText('Join', self.font, 20, (255,255,255), 1, (50,50,50))
        

    
    def displayScreen(self):
        #Set up
        GameScreen.b = Client('25.66.152.97')
        GameScreen.b.connect()

        self.displayRunning = True
        
        while self.displayRunning:

            self.checkEvent()

            # page blackground
            self.display.fill((0, 0, 0))

            # Things in page vvv
            self.buttonBack.draw(self.display)
            self.changePageByButton(self.buttonBack, self.state.previousState)

            self.buttonCreate.draw(self.display)
            if self.buttonCreate.isButtonClick():
                GameScreen.b.createMatch()
            
            self.buttonJoin.draw(self.display)
            if self.buttonJoin.isButtonClick():
                GameScreen.b.join()
                self.changePageByInput(True, self.state.join)

            self.biltScreen() # update screen