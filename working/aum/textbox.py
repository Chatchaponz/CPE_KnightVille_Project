import pygame

pygame.init()
pygame.key.set_repeat(500, 80)

'''
textbox.py - Create a textbox object which can get input text on an object.
last updated: 29 oct 2021
'''

class Textbox():
    '''
    Textbox - Create a textbox object.
    '''
    def __init__(self, x, y, width, height, inactiveColor, activeColor = pygame.Color('black'), limit = None, text = '', fontPath = None, size = 32):
        '''
        __init__ - Constructor of textbox class.
        + x, y - the coordinate position of an object.
        + width, height - size of an object.
        + text - input text in object.
        + inactiveColor - border color for inactive textbox object.
        + activeColor - border color for active textbox object.
        + limit - limit input character of an object.
        '''
        self.rect = pygame.Rect(x, y, width, height) # area of an object.
        self.text = text # text on object.
        self.prevText = text # previous text on object.
        self.initText = text # text on object when object being initialize.
        self.inactiveColor = inactiveColor # color of object when inactive.
        self.activeColor = activeColor # color of object when active.
        self.color = self.inactiveColor # color of object in current state.
        self.fontSurface = pygame.font.Font(fontPath, size) # font configs.
        self.textSurface = self.fontSurface.render(text, True, pygame.Color('grey')) # text with font configs.
        self.active = False # state of object.
        if limit != None:
            self.limit = limit # limit of character in object.
        else:
            self.limit = None

    def getText(self):
        '''
        getText - get text that being type in object.

        + return text
        '''
        self.prevText = self.text
        return self.text 

    def handleEvent(self, event, initReset = True):
        '''
        handleEvent - collect the event and decision which action is using on object.
        + event - event object.
        + initReset - reset text in object when it is initial text. 
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            if self.active:
                self.color = self.activeColor
                if self.text == self.initText and initReset:
                    self.text = ''
            else:
                self.color = self.inactiveColor
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif self.limit != None and len(self.text) < self.limit or self.limit == None:
                    self.text += event.unicode
            self.textSurface = self.fontSurface.render(self.text + '|', True, pygame.Color('black'))
        else:
            if self.prevText != self.initText and self.text == '':
                self.textSurface = self.fontSurface.render(self.text, True, pygame.Color('grey'))
            elif self.text != '':
                self.textSurface = self.fontSurface.render(self.text, True, pygame.Color('grey'))
            elif self.text == '' and self.prevText == self.initText:
                self.textSurface = self.fontSurface.render(self.initText, True, pygame.Color('grey'))
    
    def resetText(self):
        '''
        resetText - empty text in object.
        '''
        self.text = ''

    def update(self):
        '''
        update - update width of object due to text lenght.
        '''
        width = max(200, self.textSurface.get_width() + 10)
        self.rect.width = width

    def draw(self, screen):
        '''
        draw - draw an object on the screen.
        + screen - screen object.
        '''
        pygame.draw.rect(screen, pygame.Color('white'), self.rect, 0)
        screen.blit(self.textSurface, (self.rect.x + 5, self.rect.y + (self.rect.height/2 - self.textSurface.get_height()/2)))
        if self.color != None:
            pygame.draw.rect(screen, self.color, self.rect, 3)