'''

'''
import pygame
pygame.init()

'''
TextBox - Create input text box object.
'''
ACTIVECOLOR = pygame.Color('black')
INACTIVECOLOR = pygame.Color('goldenrod1')
font = pygame.font.Font(None, 32)

class TextBox():
    def __init__(self, x, y, width, height, text = ''):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = INACTIVECOLOR
        self.textSurface = font.render(text, True, pygame.Color('black'))
        self.active = False
        # self.saved = False
        # self.textReset = False

    def cf_submit(self):
        # print("text: "+ self.text)
        return self.text

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            if self.active:
                self.color = ACTIVECOLOR
            else:
                self.color = INACTIVECOLOR
        if self.active:
            if event.type == pygame.KEYDOWN:
                # if self.textReset:
                #     self.text = ''    
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 15:
                    self.text += event.unicode
                self.textSurface = font.render(self.text, 1, pygame.Color('black'))
        
            

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('white'), self.rect, 0)

        screen.blit(self.textSurface, (self.rect.x + 5, self.rect.y + 5))

        pygame.draw.rect(screen, self.color, self.rect, 3)