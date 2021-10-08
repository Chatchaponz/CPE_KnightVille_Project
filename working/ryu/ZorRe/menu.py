from button import Button 
from screen import GameScreen

class MainMenu(GameScreen):
    
    def __init__(self, state):
        super(MainMenu, self).__init__(state)

        # Image / Button goes here
        self.buttonOption = Button(500, 500, 300, 100)
        self.buttonOption.addText('Option', self.font, 20, (255,255,255), 1, (50,50,50))

    
    def displayScreen(self):

        self.displayRunning = True
        
        while self.displayRunning:

            self.checkEvent()
            self.display.fill((0, 0, 0))

            self.buttonOption.draw(self.display)
            self.changePageByButton(self.buttonOption, self.state.option)

            self.drawText('Main Menu', 20 , 100, 100)
            self.biltScreen()