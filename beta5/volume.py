import pygame

class volumeBar():
    def __init__(self, ranX, ranY, ranWidth, ranHeight, conWidth):
        self.rangeRect = pygame.Rect(ranX, ranY, ranWidth + conWidth, ranHeight)
        self.controlRect = pygame.Rect(self.rangeRect.right - conWidth, ranY, conWidth, ranHeight)
        
        self.value = 100
        self.x, self.offset = 0, 0
        self.maxrange = self.rangeRect.width - conWidth
        self.draging = False

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouseX, self.mouseY = event.pos
                self.offset = self.controlRect.x - self.mouseX
                if self.controlRect.collidepoint(event.pos):
                    self.draging = True
                elif self.rangeRect.collidepoint(event.pos):
                    self.controlRect.centerx = self.mouseX
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.draging = False
                self.__limit()
        if event.type == pygame.MOUSEMOTION:
            if self.draging:
                self.mouseX, self.mouseY = event.pos
                self.controlRect.x = self.mouseX + self.offset
                self.__limit()
            
    def __limit(self):
        self.value = int((self.controlRect.x - self.rangeRect.x)*100/self.maxrange)
        if self.value > 100:
            self.controlRect.x = self.rangeRect.right - self.controlRect.width
            self.value = 100
        if self.value < 0:
            self.controlRect.x = self.rangeRect.x
            self.value = 0
                
    def draw(self, screen, rangeSkin, text = '', fontPath = None, fontSize = 20, fontColor = pygame.Color('white')):
        textSurface = pygame.font.Font(fontPath, fontSize).render(text + ':' + str(self.value) + '%', 
        True, fontColor)
        rangeSkin = pygame.transform.scale(rangeSkin, (self.rangeRect.width, self.rangeRect.height))
        screen.blit(rangeSkin, (self.rangeRect.x, self.rangeRect.y))
        pygame.draw.rect(screen, pygame.Color('black'), (self.controlRect.x - 2, self.controlRect.y - 2, 
        self.controlRect.width + 2, self.controlRect.height + 2), 2)
        pygame.draw.rect(screen, pygame.Color('grey48'), self.controlRect)
        pygame.draw.rect(screen, pygame.Color('white'), (self.controlRect.x, self.controlRect.y, self.controlRect.width, 4))
        pygame.draw.rect(screen, pygame.Color('grey40'), (self.controlRect.x, self.controlRect.bottom - 4, 
        self.controlRect.width, 4))
        pygame.draw.rect(screen, pygame.Color('black'), (self.rangeRect.x - 2, self.rangeRect.y - 2, 
        self.rangeRect.width + 2, self.rangeRect.height + 2), 2)
        screen.blit(textSurface, (self.rangeRect.centerx - textSurface.get_width()//2, self.rangeRect.centery - 
        textSurface.get_height()//2))

