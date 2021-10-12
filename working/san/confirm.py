import pygame
from button import Button

class Confirm():
    def __init__(self, x, y):
        self.x, self.y = x, y

        self.surface1 = pygame.Surface([300,200])
        self.surface1.fill((255,250,250))
        self.accept = False
        self.reject = False 
        self.accpetButt = Button(self.x+10, self.y+140, 100, 50)
        self.rejectButt = Button(self.x+190, self.y+140, 100, 50)
        self.accpetButt.addText('Accept', pygame.font.get_default_font(), 20, (255,255,255),0, (50,50,50),(100,255,130),(50,160,80))
        self.rejectButt.addText('Reject', pygame.font.get_default_font(), 20, (255,255,255),0, (50,50,50),(255,100,130),(160,50,80))
        
    
    def draw(self, screen):
        
        # surface1.fill(255,250,250)
        screen.blit(self.surface1, (self.x, self.y))
        self.accpetButt.draw(screen)
        self.rejectButt.draw(screen)
        if self.rejectButt.isButtonClick():
            self.rejectButt.bgColor,self.rejectButt.bgColorOver = (160,160,160),(160,160,160)
            self.accpetButt.bgColor,self.accpetButt.bgColorOver = (100,255,130),(50,160,80)
            self.reject = True
            self.accept = False
        if self.accpetButt.isButtonClick():
            self.accpetButt.bgColor,self.accpetButt.bgColorOver = (160,160,160),(160,160,160)
            self.rejectButt.bgColor,self.rejectButt.bgColorOver = (255,100,130),(160,50,80)
            self.reject = False
            self.accept = True

