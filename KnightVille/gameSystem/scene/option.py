import pygame, sys
from gameSystem.scene.screen import GameScreen
from gameSystem.scene.button import Button 
from gameSystem.scene.volume import volumeBar

'''
option.py - Manage the option page

[Class] + OptionMenu

last updated: 27 Oct 2021
'''

class OptionMenu(GameScreen):
    '''
    Option - Class to manage the option page
    '''
    def __init__(self, control):
        '''
        __init__ - Constructor of OptionMenu class.
       
        + control - gameControl variable
        '''
        super(OptionMenu, self).__init__(control)

        # Button goes here
        self.buttonMenu = Button(80, 80, 80, 35)
        self.buttonMenu.addText('BACK', self.font2, 20, (255,255,255), 1, (50,50,50))

        self.sfx = volumeBar(self.screenWidth//2 - 225, 250, 450, 40, 15)
        self.music = volumeBar(self.sfx.rangeRect.x, self.sfx.rangeRect.y + self.sfx.rangeRect.height + 50, 
        450, self.sfx.rangeRect.height, self.sfx.controlRect.width)
        
        self.music.controlRect.x = self.music.rangeRect.x + self.music.rangeRect.width/4
        self.sfx.controlRect.x = self.sfx.rangeRect.x + self.sfx.rangeRect.width/2
        self.volumeList = [[self.sfx, 'SFX'], [self.music, 'MUSIC']]
        

    def checkEvent(self):
        '''
        <<overide>>
        checkEvent - method to check event and input from volume bar
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
                self.control.currentState.displayRunning = False
                pygame.quit()
                sys.exit()
            for volumeBar, dummyText in self.volumeList:
                volumeBar.handleEvent(event)

    def displayScreen(self):
        '''
        displayScreen - loop to display the option screen
        '''
        self.displayRunning = True

        while self.displayRunning:
            self.checkEvent()
            self.display.blit(self.control.hostBoard, (0, 0))

            # Set background music / sound effect volumn
            for volumeBar, text in self.volumeList:
                volumeBar.draw(self.display, self.control.offFilter, text, None, 26)
            self.control.currentMusic.set_volume(self.music.value/100)
            self.control.soundEffectVol = self.sfx.value/100
            self.buttonMenu.draw(self.display)
            if self.buttonMenu.isButtonClick(self.clickChoiceSound, self.control.getSoundEffectVol()):
                self.changePageByInput(True, self.control.menu)
            
            self.drawText('Option Menu', 70, self.screenWidth//2, 120, self.font1, self.control.black)
            self.blitScreen()
