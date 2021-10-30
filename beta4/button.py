'''
button.py - Create a button object with button property.
last updated: 09 oct 2021
'''
import pygame

'''
Button - Create a button object.
'''
class Button():
    '''
    __init__ - Constructor for create an object which will also use to set-up a property of an object.
    + x, y - the coordinate position of an object.
    + width, height - size of an object.
    + text - text on an object.
    + bgColor - background color(Color for button).
    + textColor - color for text.
    + image - image for button.
    + overImage - image for button when mouse is over an object.
    + outline - have outline for rectangle button(optional when there is no image for button) or not.
    + bgColorOver - background color(Color for button) when mouse is over an object.
    + textColorOver - color for text when mouse is over an object
    + rect - area of an object.
    + clicked - Mouse being clicked.
    '''
    def __init__(self, x, y, width, height):
        self.text = None
        self.bgColor = None
        self.textColor = (255, 255, 255)
        self.image = None
        self.overImage = None
        self.outline = 0
        self.bgColorOver = None
        self.textColorOver = (255, 255, 255)
        self.rect =  pygame.Rect(x, y, width, height)
        self.clicked = False

    '''
    addText - add text on an object and dertermine the property of text such as color etc.
    determine from what is being given and set-up property according to.
    + text - text on an object.
    + fontPath - locate font(ttf file) for text.
    + fontSize - text size.
    + outline - have outline for object(optional when there is no image for button) or not.
    + textColor - color for text.
    + textColorOver - color for text when mouse is over an object
    + bgColor - background color of an object.
    + bgColorOver - background color of an object when mouse is over an object.
    '''
    def addText(self, text, fontPath = None, fontSize = 20, textColor = pygame.Color('white'), outline = 0, 
    textColorOver = pygame.Color('white'), bgColor = None, bgColorOver = None):
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
    addImage - add image on an object and adjust image to fit with an object.
    + image - image for button.
    + overImage - image for button when mouse is over an object.
    + width, height - size of an object.
    '''
    def addImage(self, image, overImage = None):
        self.image = pygame.transform.scale(image, (self.rect.width, self.rect.height))
        if overImage != None:
            self.overImage = pygame.transform.scale(overImage, (self.rect.width, self.rect.height))
        else:
            self.overImage = pygame.transform.scale(image, (self.rect.width, self.rect.height))

    '''
    draw - draw an object on screen with set-up property of an object.
    + screen - screen object.
    + mouseOver - check whether mouse position is over an object or not.
    + image - image for button.
    + overImage - image for button when mouse is over an object.
    + bgColor - background color(Color for button).
    + bgColorOver - background color(Color for button) when mouse is over an object.
    + text - text on an object.
    + fontPath - locate font(ttf file) for text.
    + fontSize - text size.
    + x, y - the coordinate position of an object.
    + width, height - size of an object.
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
    isMouseOver - checked mouse position is over a button or not by using the collidepoint 
    which determine is mouse in object area or not.
    + rect - area of an object.
    + mpos - current mouse position.
    '''
    def isMouseOver(self):
        mpos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mpos):
            return True
        else:
            return False

    '''
    isButtonClick - checked mouseclick state on button object by checking
    is mouse is over an object and mouse is being clicked or not.
    + action - Button being clicked.
    + clicked - Mouse being clicked.
    return True or False.
        if MouseOver then mouse is being click for True.
        if not for False.
    '''
    def isButtonClick(self):
        action = False
        if self.isMouseOver():
            if pygame.mouse.get_pressed()[0] == True:
                self.clicked = True
            elif pygame.mouse.get_pressed()[0] == False and self.clicked == True:
                self.clicked = False
                action = True
        return action