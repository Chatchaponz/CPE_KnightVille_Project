import pygame  
from button import Button

class MainMenu():
    def __init__(self, page):
        self.page = page
        #self.bottonOption = Button(500, 500, 300, 100)
        #self.bottonOption.addText('Click me', self.page.fontName, 20, (0,0,0), 1, (50,50,50))
        self.simsim = pygame.image.load(r'C:\Zor/TestPygame/Simson.png')
        self.MerlinG = pygame.image.load(r'C:\Zor/TestPygame/MerlinF.png')
        self.simsim_1 = pygame.transform.scale(self.simsim, (300,300))
        self.MerlinG_1 = pygame.transform.scale(self.MerlinG, (300,300))
        self.simsim_1F = pygame.transform.flip(self.simsim_1, True, False)

        #self.menuRunning = True
    
    def biltScrene(self):
        self.page.screne.blit(self.page.display, (0, 0))
        pygame.display.update()
        self.page.resetKeys()
        

    def display(self):
        self.displayRunning = True
        while self.displayRunning:
            self.page.checkEvent()
            self.page.display.fill(self.page.blue)
            #self.bottonOption.draw(self.page.display)
            #for i in range (2):
            #    if self.bottonOption.isButtonClick(pygame.event.wait()):
            #        self.checkInput(True, self.page.option)
            self.page.drawText(self.page.getCurrentState(), 20, 100, 100)
            #self.page.display.blit(self.simsim_1F, (200, 200))
            #self.page.display.blit(self.MerlinG_1, (600, 200))
            self.biltScrene()

    def checkInput(self, botton, state):
        if botton: 
            self.page.updateState()
            self.page.currentState = state
            self.displayRunning = False
        self.page.resetKeys()