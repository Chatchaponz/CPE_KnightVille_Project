'''
textbox.py - Create a textbox object which can get input text on an object.
last updated: 16 oct 2021
'''
import pygame

pygame.init()
pygame.key.set_repeat(500, 80)
font = pygame.font.Font(None, 32)

'''
Textbox - Create a textbox object.
'''
class Textbox():
    '''
    __init__ - Constructor for create an object which will use to set-up an object.
    + x, y - the coordinate position of an object.
    + width, height - size of an object.
    + rect - area of an object. #เรียกว่าอะไรนะ
    + text - input text in object.
    + prevText - text from previous event.
    + initText - text when initial object.
    + inactiveColor - border color for inactive textbox object.
    + activeColor - border color for active textbox object.
    + color - border color of an object to update.
    + textSurface - render a text with set-up properties.
    + active - status of an object.
    + limit - limit input character of an object.
    '''
    def __init__(self, x, y, width, height, inactiveColor, activeColor = pygame.Color('black'), limit = None, text = 'Input text here'):
        self.rect = pygame.Rect(x, y, width, height)
        self.width = width
        self.text = text
        self.prevText = text
        self.initText = text
        self.inactiveColor = inactiveColor
        self.activeColor = activeColor
        self.color = self.inactiveColor
        self.textSurface = font.render(text, True, pygame.Color('grey'))
        self.active = False
        if limit != None:
            self.limit = limit
        else:
            self.limit = None

    '''
    getText - get input text from an object.
    + text - input text in object.
    + prevText - input text in previous event.
    '''
    def getText(self):
        self.prevText = self.text
        return self.text 

    '''
    handle_event - handle event which occur on an object such as is object being activate? and to
    activate an object by click on an object, is object is being type in? by check object state and
    keyboard being type etc.
    + event - event object.
    + rect - area of an object.
    + inactiveColor - border color for inactive textbox object.
    + activeColor - border color for active textbox object.
    + color - border color of an object to update.
    + textSurface - render a text with set-up properties.
    + active - status of an object. 
    + limit - limit input character of an object..
    + text - input text in object.
    + prevText - text from previous event.
    + initText - text when initial object.
    '''
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            if self.active:
                self.color = self.activeColor
                if self.text == self.initText:
                    self.text = ''
            else:
                self.color = self.inactiveColor
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif self.limit != None and len(self.text) < self.limit or self.limit == None:
                    self.text += event.unicode
            self.textSurface = font.render(self.text + '|', True, pygame.Color('black'))
        else:
            if self.prevText != self.initText and self.text == '':
                self.textSurface = font.render(self.prevText, True, pygame.Color('grey'))
            elif self.text != '':
                self.textSurface = font.render(self.text, True, pygame.Color('grey'))
            elif self.text == '' and self.prevText == self.initText:
                self.textSurface = font.render(self.initText, True, pygame.Color('grey'))
                

    '''
    resetText - reset text in an object.
    + text - input text in object.
    + reset - do reset or not.
    ''' 
    def resetText(self, reset = False):
        if reset:
            self.text = ''

    '''
    update - update width size of width according to how many character being type in.
    + width - width size of an object.
    + rect - area of an object.
    '''
    def update(self):
        width = max(200, self.textSurface.get_width() + 10)
        self.rect.width = width

    '''
    draw - draw an object on the screen.
    + textSurface - render a text with set-up properties.
    + rect - area of an object.
    + color - border color of an object.
    + x, y - coordinate position of an object.
    + screen - screen object.
    '''
    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('white'), self.rect, 0)
        screen.blit(self.textSurface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 3)