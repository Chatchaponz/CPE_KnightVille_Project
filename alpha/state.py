import pygame
from menu import MainMenu
from option import OptionMenu
from host import Host
from join import Join

class StateControl():

    def __init__(self):
        pygame.init()

        self.Running = True

        # add state here
        self.menu = MainMenu(self)
        self.option = OptionMenu(self)
        #temp
        self.host = Host(self)
        self.join = Join(self)

        self.currentState = self.menu
        self.previousState = self.menu
    

    def saveState(self):
        self.previousState = self.currentState
