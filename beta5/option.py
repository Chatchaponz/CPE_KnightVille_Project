import pygame, sys
from button import Button 
from screen import GameScreen
from volume import volumeBar

class OptionMenu(GameScreen):

    def __init__(self, control):
        super(OptionMenu, self).__init__(control)

        # Button goes here
        self.buttonMenu = Button(100, 100, 100, 50)
        self.buttonMenu.addText('back', self.font, 25, control.white, 1, (50,50,50))

        self.sfx = volumeBar(150, 250, 400, 40, 15)
        self.music = volumeBar(self.sfx.rangeRect.x, self.sfx.rangeRect.y + self.sfx.rangeRect.height + 50, 
        400, self.sfx.rangeRect.height, self.sfx.controlRect.width)
        
        self.volumeList = [[self.sfx, 'SFX'], [self.music, 'MUSIC']]
        # Sound goes here
        self.soundList = control.soundList
        self.backButtonOptionSound = self.soundList[2]

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
                self.control.currentState.displayRunning = False
                pygame.quit()
                sys.exit()
            for volumeBar, text in self.volumeList:
                volumeBar.handleEvent(event)

    def displayScreen(self):

        self.displayRunning = True

        while self.displayRunning:
            self.checkEvent()
            self.display.fill((255, 255, 255))

            for volumeBar, text in self.volumeList:
                volumeBar.draw(self.display, self.control.offFilter, text, None, 26)
            self.buttonMenu.draw(self.display)
            if self.buttonMenu.isButtonClick(self.backButtonOptionSound):
                self.changePageByInput(True, self.control.menu)
            
            self.drawText('Option Menu', 40, self.screenWidth//2, 80, self.font, self.control.black)
            self.biltScreen()
