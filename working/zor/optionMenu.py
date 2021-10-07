import pygame

# class Option():
#     def __init__(self, page):
#         self.page = page
#         #self.ainMenu = True
    
#     def biltScrene(self):
#         self.page.screne.blit(self.page.display, (0, 0))
#         pygame.display.update()
#         self.page.resetKeys()
        

class OptionMenu():
    def __init__(self, page):
        self.page = page
        self.simsim = pygame.image.load(r'C:\Zor/TestPygame/Simson.png')
        self.simsim_1 = pygame.transform.scale(self.simsim, (300,300))

    def biltScrene(self):
        self.page.screne.blit(self.page.display, (0, 0))
        pygame.display.update()
        self.page.resetKeys()

    def display(self):
        self.displayRunning = True
        while self.displayRunning:
            self.page.checkEvent()
            self.checkInput()
            self.page.display.fill((0, 0, 0))
            self.page.drawText(self.page.getCurrentState(), 20, 100, 100)
            self.page.display.blit(self.simsim_1, (600, 200))
            self.biltScrene()

    def checkInput(self):
        if self.page.mKey:
            self.page.updateState()
            self.page.currentState = self.page.mainMenu
            #self.page.manuRunning = True
            self.displayRunning = False
        self.page.resetKeys()