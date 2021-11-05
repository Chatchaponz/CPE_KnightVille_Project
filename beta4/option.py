import pygame
from button import Button 
from screen import GameScreen

class OptionMenu(GameScreen):

    def __init__(self, control):
        super(OptionMenu, self).__init__(control)

        # Button goes here
        self.buttonMenu = Button(100, 100, 100, 50)
        self.buttonMenu.addText('back', self.font, 25, control.white, 1, (50,50,50))

        # Sound goes here
        self.soundList = control.soundList
        self.backButtonOptionSound = self.soundList[2]
    
    def displayScreen(self):

        self.displayRunning = True

        while self.displayRunning:

            self.checkEvent()
            self.display.fill((0, 0, 0))

            self.buttonMenu.draw(self.display)
            if self.buttonMenu.isButtonClick(self.backButtonOptionSound):
                self.changePageByInput(True, self.control.menu)
            
            self.drawText('Option Menu', 40 , self.screenWidth//2, 80, self.font, self.control.white)
            self.biltScreen()
