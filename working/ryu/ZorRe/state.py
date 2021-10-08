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
        self.previousState = self.menu
    

    def saveState(self):
        self.previousState = self.currentState
