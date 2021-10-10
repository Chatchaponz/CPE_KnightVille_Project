from button import Button 
from screen import GameScreen

class MainMenu(GameScreen):
    
    def __init__(self, state):
        super(MainMenu, self).__init__(state)

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
            self.changePageByButton(self.buttonOption, self.state.option)

            self.buttonHost.draw(self.display)
            self.changePageByButton(self.buttonHost, self.state.host)

            self.buttonJoin.draw(self.display)
            self.changePageByButton(self.buttonJoin, self.state.join)

            self.drawText('Main Menu', 20 , 100, 100)
            self.biltScreen()