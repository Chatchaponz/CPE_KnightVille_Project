import pygame

# class Menu():
#     def __init__(self, page):
#         self.page = page
#         #self.menuRunning = True
    
#     def biltScrene(self):
#         self.page.screne.blit(self.page.display, (0, 0))
#         pygame.display.update()
#         self.page.resetKeys()
        

# class MainMenu(Menu):
#     def __init__(self, page):
#         Menu.__init__(self, page)
#         #self.state = "Start"

#     def displayMenu(self):
#         #self.page.menuRunning = True
#         while self.page.menuRunning:
#             self.page.checkEvent()
#             self.checkInput()
#             self.page.display.fill(self.page.black)
#             #self.page.drawText('Main Menu', 20, 100, 100)
#             self.page.drawText(self.page.getCurrentState(), 20, 100, 100)
#             self.biltScrene()

#     def checkInput(self):
#         if self.page.oKey:
#             self.page.updateState()
#             self.page.currentState = self.page.option
#             self.page.optionRunning = True
#             self.page.menuRunning = False
#         self.page.resetKeys()
        

class MainMenu():
    def __init__(self, page):
        self.page = page
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
            self.checkInput()
            self.page.display.fill(self.page.black)
            self.page.drawText(self.page.getCurrentState(), 20, 100, 100)
            self.page.display.blit(self.simsim_1F, (200, 200))
            self.page.display.blit(self.MerlinG_1, (600, 200))
            self.biltScrene()

    def checkInput(self):
        if self.page.oKey:
            self.page.updateState()
            self.page.currentState = self.page.option
            #self.page.optionRunning = True
            self.displayRunning = False
        elif self.page.cKey:
            self.page.updateState()
            self.page.currentState = self.page.credits
            self.displayRunning = False
        self.page.resetKeys()