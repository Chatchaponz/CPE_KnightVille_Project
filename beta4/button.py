'''
button.py - Create a button object with button property.
last updated: 09 oct 2021
'''
import pygame

'''
Button - Create a button object.
'''
class Button():
    
    def __init__(self, x, y, width, height):
        self.text = None # text that will display on object.
        self.bgColor = None # background color.
        self.textColor = (255, 255, 255) # color of text.
        self.image = None # background image.
        self.overImage = None # background image when mouse is on object.
        self.outline = 0 # outline thick
        self.bgColorOver = None # background color when mouse is on object.
        self.textColorOver = (255, 255, 255) # color of text when mouse is on button.
        self.rect =  pygame.Rect(x, y, width, height) # area of an object.
        self.clicked = False # state to check is mouse being click.
        self.playedSound = True # trigger sound.
    '''
    __init__ - Constructor for create an object which will also use to set-up a property of an object.
    + x, y - the coordinate position of an object.
    + width, height - size of an object.
    '''
    
    def addText(self, text, fontPath = None, fontSize = 20, textColor = pygame.Color('white'), outline = 0, 
    textColorOver = pygame.Color('white'), bgColor = None, bgColorOver = None):
        self.text = text # text that will display on object.
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
        self.fontPath = fontPath # font location.
        self.fontSize = fontSize # scale/size of font.
    '''
    addText - config text on object.
    + text - text on an object.
    + fontPath - locate font(ttf file) for text.
    + fontSize - text size.
    + outline - have outline for object(optional when there is no image for button) or not.
    + textColor - color for text.
    + textColorOver - color for text when mouse is over an object
    + bgColor - background color of an object.
    + bgColorOver - background color of an object when mouse is over an object.
    '''

    def addImage(self, image, overImage = None):
        self.image = pygame.transform.scale(image, (self.rect.width, self.rect.height))
        if overImage != None:
            self.overImage = pygame.transform.scale(overImage, (self.rect.width, self.rect.height))
        else:
            self.overImage = pygame.transform.scale(image, (self.rect.width, self.rect.height))
    '''
    addImage - config image of an object.
    + image - background image of an object.
    + overImage - background image of an object when mouse is on an object.
    '''

    def draw(self, screen):
        mouseOver = self.isMouseOver()
        if self.image != None:
            if mouseOver == False:
                screen.blit(self.image, (self.rect.x, self.rect.y))
            elif mouseOver == True:
                screen.blit(self.overImage, (self.rect.x, self.rect.y))
        else:
            if self.bgColor != None and mouseOver == False:
                pygame.draw.rect(screen, self.bgColor, (self.rect.x, self.rect.y, self.rect.width, self.rect.height),self.outline)
            elif self.bgColorOver != None and mouseOver == True:
                pygame.draw.rect(screen, self.bgColorOver, (self.rect.x, self.rect.y, self.rect.width, self.rect.height),self.outline)

        if self.text != None:
            font = pygame.font.Font(self.fontPath,self.fontSize)
            if mouseOver == False:
                textSurface = font.render(self.text, True, self.textColor)
            elif self.textColorOver != None and mouseOver == True:
                textSurface = font.render(self.text, True, self.textColorOver)
            screen.blit(textSurface, (self.rect.x + (self.rect.width/2 - textSurface.get_width()/2), self.rect.y + (self.rect.height/2 - textSurface.get_height()/2)))
    '''
    draw - draw an object on screen.
    + screen - screen object.
    '''

    def isMouseOver(self):
        '''
        isMouseOver - checked mouse position is over a button or not by using the collidepoint 
        which determine is mouse in object area or not.
        
        + return.
            if mouse position is collide with area of a button then True.
            else then False.
        '''
        mpos = pygame.mouse.get_pos() # get and assign mouse position as mpos
        if self.rect.collidepoint(mpos):
            return True
        else:
            return False
    

    def isButtonClick(self):
        action = False
        if self.isMouseOver():
            if pygame.mouse.get_pressed()[0] == True:
                self.clicked = True
            elif pygame.mouse.get_pressed()[0] == False and self.clicked == True:
                self.clicked = False
                action = True
        return action
    '''
    isButtonClick - checked mouseclick state on button object by checking
    is mouse is over an object and mouse is being clicked or not.
    return True or False.
        if MouseOver then mouse is being click for True.
        if not for False.
    '''

    def triggerSound(self, soundPath):
        if self.isMouseOver() and self.playedSound:
            sound = pygame.mixer.Sound(soundPath)
            sound.play() # play sound
            self.playedSound = False
        if not self.isMouseOver():
            self.playedSound = True