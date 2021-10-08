import pygame
from menu import MainMenu
from option import OptionMenu

class StateControl():

    def __init__(self):
        pygame.init()
        
        self.Running = True

        # add state here
        self.menu = MainMenu(self)
        self.option = OptionMenu(self)

        self.currentState = self.menu
    
    
    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.Running = False
                self.currentState.displayRunning = False

    def resetKeys(self):
        pass
