from button import Button 
from screen import GameScreen

class PageName(GameScreen):
    
    def __init__(self, state):
        super(PageName, self).__init__(state)

        # Image / Button goes here vvvv
        

    
    def displayScreen(self):

        self.displayRunning = True
        
        while self.displayRunning:

            self.checkEvent()

            # page blackground
            self.display.fill((0, 0, 0))

            # Things in page vvv
            

            self.blitScreen() # update screen