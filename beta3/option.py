from button import Button 
from screen import GameScreen

class OptionMenu(GameScreen):

    def __init__(self, control):
        super(OptionMenu, self).__init__(control)

        # Button goes here
        self.buttonMenu = Button(100, 100, 100, 50)
        self.buttonMenu.addText('Menu', self.font, 20, (255,255,255), 1, (50,50,50))
    
    
    def displayScreen(self):

        self.displayRunning = True

        while self.displayRunning:

            self.checkEvent()
            self.display.fill((0, 0, 0))

            self.buttonMenu.draw(self.display)
            self.changePageByButton(self.buttonMenu, self.control.menu)
            
            self.drawText('Option Menu', 20 , 100, 100, self.font, self.control.white)
            self.biltScreen()
