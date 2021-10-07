import pygame

'''
Button - Create button object.

'''
class Button():
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text = None
        self.bgColor = None
        self.textColor = (255, 255, 255)
        self.image = None
        self.clicked = False
        self.over = False
        self.outline = 0
        self.bgColorOver = None
        self.textColorOver = (255, 255, 255)




    def addText(self, text, fontName, fontSize, textColor = (255, 255, 255), outline = 0, textColorOver = (255, 255, 255), bgColor = None, bgColorOver = None):
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
        self.fontName = fontName
        self.fontSize = fontSize




    def addImage(self, image, overImage = None):
        self.image = pygame.transform.scale(image, (self.width, self.height))
        if overImage != None:
            self.overImage = pygame.transform.scale(overImage, (self.width, self.height))
        else:
            self.overImage = pygame.transform.scale(image, (self.width, self.height))



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
            font = pygame.font.SysFont(self.fontName,self.fontSize)
            if mouseOver == False:
                text = font.render(self.text, 1, self.textColor)
            elif self.textColorOver != None and mouseOver == True:
                text = font.render(self.text, 1, self.textColorOver)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    # isMouseOver - checked if mouse is over the button
    # return state if mouseover
    def isMouseOver(self):
        mpos = pygame.mouse.get_pos()

        if mpos[0] > self.x and mpos[0] < self.x + self.width:
            if mpos[1] > self.y and mpos[1] < self.y + self.height:
                return True
        return False

    '''
    isButtonClick - checked mouseclick state on button object
    event - event
    return True or False
        if MouseOver then mouse is being click for True
        if not for False
    '''
    def isButtonClick(self,event):
        action = False

        if self.isMouseOver():
            if event.type == pygame.MOUSEBUTTONUP:
                action = True   
        return action