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

        self.sfx = volumeBar(self.screenWidth//2 - 225, 250, 450, 40, 15)
        self.music = volumeBar(self.sfx.rangeRect.x, self.sfx.rangeRect.y + self.sfx.rangeRect.height + 50, 
        450, self.sfx.rangeRect.height, self.sfx.controlRect.width)
        
        self.music.controlRect.x = self.music.rangeRect.x + self.music.rangeRect.width/2
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
            for volumeBar, dummyText in self.volumeList:
                volumeBar.handleEvent(event)

    def displayScreen(self):

        self.displayRunning = True

        while self.displayRunning:
            self.checkEvent()
            self.display.blit(self.control.hostBoard, (0, 0))

            for volumeBar, text in self.volumeList:
                volumeBar.draw(self.display, self.control.offFilter, text, None, 26)
            self.control.currentMusic.set_volume(self.music.value/100)
            self.control.soundEffectVol = self.sfx.value/100
            self.buttonMenu.draw(self.display)
            if self.buttonMenu.isButtonClick(self.backButtonOptionSound):
                self.changePageByInput(True, self.control.menu)
            
            self.drawText('Option Menu', 40, self.screenWidth//2, 100, self.font, self.control.black)
            self.biltScreen()
