import pygame

class CreditsMenu():
    def __init__(self, page):
        self.page = page

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
            self.biltScrene()

    def checkInput(self):
        if self.page.mKey:
            self.page.updateState()
            self.page.currentState = self.page.mainMenu
            self.displayRunning = False
        self.page.resetKeys()