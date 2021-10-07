import pygame
from page import Page

pro = Page()

while pro.programRunning:
    pro.currentState.display()
    pro.loop()
    pro.checkEvent()

pygame.quit()

        

#    state.currentState.displayMenu()
