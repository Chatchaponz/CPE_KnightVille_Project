import pygame

'''
volume.py - Create a ocject that can adjust with mouse.

[Class] + volumeBar

last updated: 6 Nov 2021
'''
class volumeBar():
    '''
    volumeBar - Create a component object.
    '''
    def __init__(self, ranX, ranY, ranWidth, ranHeight, conWidth):
        '''
        __init__ - Contructor of volumeBar class.
        + ranX, ranY - the coordinate of an object.
        + ranWidth, ranHeight - size of an object.
        + conWidth - size of an object component that dragable.
        '''
        self.rangeRect = pygame.Rect(ranX, ranY, ranWidth + conWidth, ranHeight) # main object as body
        self.controlRect = pygame.Rect(self.rangeRect.right - conWidth, ranY, conWidth, ranHeight) # dragable object as controller
        
        self.value = 100 # Position of controller in body as percentage
        self.maxrange = self.rangeRect.width - conWidth # Max range that controller can drag in body
        self.draging = False # Draging state

    def handleEvent(self, event):
        '''
        handleEvent - collect the event and decision which action is using on object.
        + event - event object.
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouseX, mouseY = event.pos # Mouse position
                if self.controlRect.collidepoint(event.pos):
                    self.draging = True
                elif self.rangeRect.collidepoint(event.pos):
                    self.controlRect.centerx = self.mouseX
                    self.draging = True  
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.draging = False
        if event.type == pygame.MOUSEMOTION:
            if self.draging:
                self.mouseX, mouseY = event.pos
                self.controlRect.centerx = self.mouseX
            
    def __limit(self):
        '''
        __limit - validate the position of an object and value.
        '''
        self.value = int((self.controlRect.x - self.rangeRect.x)*100/self.maxrange)
        if self.controlRect.right > self.rangeRect.right:
            self.controlRect.right = self.rangeRect.right
            self.value = 100

        if self.controlRect.left < self.rangeRect.left:
            self.controlRect.x = self.rangeRect.x
            self.value = 0
                
    def draw(self, screen, rangeSkin, text = '', fontPath = None, fontSize = 20, fontColor = pygame.Color('white')):
        '''
        draw - draw an object on the screen.
        + screen - screen object.
        + rangeSkin - body of an object.
        + text - text display on an object.
        + fontPath - font of text on an object.
        + fontSize - size of font on an object.
        + fontColor - color of font on an object.
        '''
        self.__limit()
        textSurface = pygame.font.Font(fontPath, fontSize).render(text + ':' + str(self.value) + '%', 
        True, fontColor)

        rangeSkin = pygame.transform.scale(rangeSkin, (self.rangeRect.width, self.rangeRect.height))
        screen.blit(rangeSkin, (self.rangeRect.x, self.rangeRect.y)) # inner body

        pygame.draw.rect(screen, pygame.Color('black'), (self.controlRect.x - 2, self.controlRect.y - 2, 
        self.controlRect.width + 2, self.controlRect.height + 2), 2) # outline of controller
        pygame.draw.rect(screen, pygame.Color('grey48'), self.controlRect) # controller
        pygame.draw.rect(screen, pygame.Color('white'), (self.controlRect.x, self.controlRect.y, self.controlRect.width, 2)) # top shade of controller
        pygame.draw.rect(screen, pygame.Color('grey40'), (self.controlRect.x, self.controlRect.bottom - 6,  
        self.controlRect.width, 6)) # bottom shade of controller

        pygame.draw.rect(screen, pygame.Color('black'), (self.rangeRect.x - 2, self.rangeRect.y - 2, 
        self.rangeRect.width + 2, self.rangeRect.height + 2), 2) # outline of body

        screen.blit(textSurface, (self.rangeRect.centerx - textSurface.get_width()//2, self.rangeRect.centery - 
        textSurface.get_height()//2)) # text on body

