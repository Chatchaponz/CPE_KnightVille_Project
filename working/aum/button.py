'''
button.py - Create an button object with button ability
last updated: 07 oct 2021
'''
import pygame
from pygame.constants import MOUSEBUTTONDOWN

'''
Button - Create a button object.
'''
class Button():
    '''
    __init__ - Constructor for create an object
    + x, y - the coordinate position of button on screen.
    + width, height - size of button.
    + text - text for button.
    + bgColor - background color(Color for button).
    + textColor - color for text.
    + image - image for button.
    + overImage - image for button when mouse is over an object.
    + outline - have outline for rectangle button(optional when there is no image for button) or not.
    + bgColorOver - background color(Color for button) when mouse is over an object.
    + textColorOver - color for text when mouse is over an object
    '''
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text = None
        self.bgColor = None
        self.textColor = (255, 255, 255)
        self.image = None
        self.overImage = None
        self.outline = 0
        self.bgColorOver = None
        self.textColorOver = (255, 255, 255)

    '''
    addText - add text on button.
    + fontPath - locate font(ttf file) for text.
    + fontSize - text size.
    + outline - have outline for rectangle button(optional when there is no image for button) or not.
    + textColorOver - color for text when mouse is over an object
    + bgColor - background color(Color for button).
    + bgColorOver - background color(Color for button) when mouse is over an object.
    '''
    def addText(self, text, fontPath, fontSize, textColor = (255, 255, 255), outline = 0, textColorOver = (255, 255, 255), bgColor = None, bgColorOver = None):
        self.text = text
        if bgColor != None:
            self.bgColor = bgColor
        if bgColorOver != None:
            self.bgColorOver = bgColorOver
        else:
            self.bgColorOver = bgColor
        self.textColor = textColor
        if textColorOver != None:
            self.textColorOver = textColorOver
        else:
            self.textColorOver = textColor

        if outline != 0:
            self.outline = outline
        self.fontPath = fontPath
        self.fontSize = fontSize

    '''
    addImage - add image as a button.
    + image - image for button.
    + overImage - image for button when mouse is over an object.
    '''
    def addImage(self, image, overImage = None):
        self.image = pygame.transform.scale(image, (self.width, self.height))
        if overImage != None:
            self.overImage = pygame.transform.scale(overImage, (self.width, self.height))
        else:
            self.overImage = pygame.transform.scale(image, (self.width, self.height))

    '''
    draw - draw object on screen.
    + screen - screen object.
    '''
    def draw(self, screen):
        mouseOver = self.isMouseOver()
        
        if self.image != None:
            if mouseOver == False:
                screen.blit(self.image, (self.x, self.y))
            elif mouseOver == True:
                screen.blit(self.overImage, (self.x, self.y))
        else:
            if self.bgColor != None and mouseOver == False:
                pygame.draw.rect(screen, self.bgColor, (self.x, self.y, self.width, self.height),self.outline)
            elif self.bgColorOver != None and mouseOver == True:
                pygame.draw.rect(screen, self.bgColorOver, (self.x, self.y, self.width, self.height),self.outline)

        if self.text != None:
            font = pygame.font.Font(self.fontPath,self.fontSize)
            if mouseOver == False:
                text = font.render(self.text, 1, self.textColor)
            elif self.textColorOver != None and mouseOver == True:
                text = font.render(self.text, 1, self.textColorOver)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/3)))

    '''
    isMouseOver - checked mouse position is over a button or not.
    + mpos - current mouse position.
    '''
    def isMouseOver(self):
        mpos = pygame.mouse.get_pos()

        if mpos[0] > self.x and mpos[0] < self.x + self.width:
            if mpos[1] > self.y and mpos[1] < self.y + self.height:
                return True
        return False

    '''
    isButtonClick - checked mouseclick state on button object.
    + timeRes - time to wait for response in millisec
    return True or False.
        if MouseOver then mouse is being click for True.
        if not for False.
    '''
    def isButtonClick(self, timeRes):
        action = False
        event = pygame.event.wait(timeRes)
        if self.isMouseOver():
            if event.type == pygame.MOUSEBUTTONUP:
                action = True

        return action