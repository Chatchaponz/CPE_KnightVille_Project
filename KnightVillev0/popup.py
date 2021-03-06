import pygame
from button import Button
from textbox import Textbox

'''
popup.py - Create a popup object contain word textbox and button.
           1. Popup that let user know the information.
           2. Popup that ask user on a certian information.
           3. Popup that ask user permision.
           
last updated: 10 Nov 2021
'''
class Popup:
    '''
    Popup - Create a popup object.
    '''
    def __init__(self, x, y, width, height, textline, textColor, textHighlight = None, type = 0):
        '''
        __init__ - Contructor of popup class.
        + x, y - the coordinate position of an object.
        + width, height - size of an object.
        + textline - text on object.
        + textColor - color of text.
        + textHightlight - color of text which is being highlight.
        + type - type of popup.
        '''
        self.rect =  pygame.Rect(x, y, width, height) # area of an object.
        self.text = textline # text on object.
        self.textColor = textColor # color of text.
        self.t1preText = pygame.font.Font(None, 20).render('', True, self.textColor) # text in front of textbox.
        self.t2preText = '' # text in front of textbox.
        self.textRect = self.rect.inflate(-150, -80) # area of text object.

        self.activeButton = True # state of button

        if textHighlight: 
            self.textHighlight = textHighlight
        else:
            self.textHighlight = None
        self.type = type
        if self.type == 1: # type 1, ask user to agree or not.
            self.b1 = Button(self.rect.centerx - 55, self.rect.bottom - 60, 60, 30) # button left.
            self.b1.addText('Yes', bgColor = pygame.Color('green2'), bgColorOver = pygame.Color('green3'))
            self.b2 = Button(self.rect.centerx + 30, self.rect.bottom - 60, 60, 30) # button right.
            self.b2.addText('No', bgColor = pygame.Color('red2'), bgColorOver = pygame.Color('red3'))
        elif self.type == 2: # type 2, ask user to fill information.
            self.t1 = Textbox(self.rect.centerx - 200//2, self.rect.bottom - 100,
            200, 30, pygame.Color('gainsboro')) # textbox left.
            self.t2 = Textbox(self.t1.rect.right + 15, self.rect.bottom - 100,
            0, 30, pygame.Color('gainsboro')) # textbox right.
            self.b1 = Button(self.rect.centerx - 80, self.rect.bottom - 60, 60, 30)
            self.b1.addText('DONE', bgColor = pygame.Color('black'), bgColorOver = pygame.Color('grey'))
            self.b2 = Button(self.rect.centerx + 20, self.rect.bottom - 60, 60, 30)
            self.b2.addText('CANCEL', bgColor = pygame.Color('black'), bgColorOver = pygame.Color('grey'))
        else: # type 0 , it is popup let user known some information.
            self.b1 = Button(self.rect.centerx - 45, self.rect.bottom - 60, 90, 30) # button.
            self.b1.addText('Understand', bgColor = pygame.Color('black'), bgColorOver = pygame.Color('grey'))
        
    def fitText(self, screen, font, newlineSpacing = 5, textAlign = 'leftAlign'):
        '''
        fitText - fit a textline in popup object.
        + screen - surface object.
        + font - font for text.
        + newlineSpacing - Space between line.
        + textAlign - Alignment of text on popup.
        '''
        spaceWidth = font.size(" ")[0]
        fontHeight = font.size("Ab")[1]

        wordsList = self.text.split(" ")
        line = []
        for word in wordsList:
            if self.textHighlight and '/>' in word:
                word = word[:-2]
                line.append(font.render(word, True, self.textHighlight))
            else:
                line.append(font.render(word, True, self.textColor))    
        
        maxLen = self.textRect[2]
        lineLenList = [0]
        lineList = [[]]
        for lineFit in line:
            width = lineFit.get_width()
            lineLen = lineLenList[-1] + len(lineList[-1]) * spaceWidth + width
            if len(lineList[-1]) == 0 or lineLen <= maxLen:
                lineLenList[-1] += width
                lineList[-1].append(lineFit)
            else:
                lineLenList.append(width)
                lineList.append([lineFit])
        
        lineBottom = self.textRect[1]
        lastLineList = []
        lastLine = 0
        for lineLen, lineSurface in zip(lineLenList, lineList):
            lineLeft = self.textRect[0]
            if textAlign == 'rightAlign':
                lineLeft += + self.textRect[2] - lineLen - spaceWidth * (len(lineSurface) - 1)
            elif textAlign == 'centerAlign':
                lineLeft += (self.textRect[2] - lineLen - spaceWidth * (len(lineSurface) - 1))//2
            elif textAlign == 'blockAlign' and len(lineSurface) > 1:
                lineLeft += (self.textRect[2] - lineLen) // (len(lineSurface) - 1)
            lastLine += 1

            lastLineList.append(lastLine)

            if fontHeight * max(lastLineList) > self.rect.height - 120:
                self.rect.height = self.rect.height + (max(lastLineList) * (fontHeight + newlineSpacing))
                self.rect.y = screen.get_height()//2 - self.rect.height//2
                self.textRect = self.rect.inflate(-round(self.rect.height*1/6), -round(self.rect.height*3/5))
                self.b1.rect.y = self.rect.bottom - round(self.rect.height*2/7)
                if self.type in [1, 2]:
                    self.b2.rect.y = self.rect.bottom - round(self.rect.height*2/7)
                    if self.type == 2:
                        self.t1.rect.y = self.rect.bottom - round(self.rect.height*2/5)
                        self.t2.rect.y = self.rect.bottom - round(self.rect.height*2/5)
              
            for i, lineFit in enumerate(lineSurface):
                x, y = lineLeft + i * spaceWidth, lineBottom
                screen.blit(lineFit, (round(x), y))
                lineLeft += lineFit.get_width()
            lineBottom += fontHeight + newlineSpacing
        if lastLine < len(lineList):
            drawLine = sum([len(lineList[i]) for i in range(lastLine)])
            remainingText = ""
            for text in wordsList[drawLine:]:
                remainingText += text + " "
            return remainingText
        return ""

    def adjustComponents(self, t1Width = 200, t2Width = 100, tHeight = 30, bWidth = 90, bHeight = 30, fontPath = None, t1text = '', t2text = ''):
        '''
        adjustComponents - Adjust the component such as textbox and button.
        + t1Width - textbox left width.
        + t2Width - textbox right width.
        + tHeight - textbox height.
        + bWidth - button width.
        + bHeight - button height.
        + fontPath - font for text in textbpx.
        + t1text - text on textbox left.
        + t2text - text on textbox right.
        '''
        y = self.rect.bottom - tHeight//2 - 40
        if self.type == 1:
            bX1 = self.rect.centerx - 20 - bWidth
            bX2 = self.rect.centerx + 20
            self.__adjustComponents(self.b2, bX2, y, bWidth, bHeight)
        if self.type == 2:
            font = pygame.font.Font(fontPath, tHeight)
            self.t1preText = font.render(t1text, True, self.textColor)
            self.t2preText = font.render(t2text, True, self.textColor)
            if t2text != '':
                t1X = self.rect.centerx - (t1Width + t2Width + 15 + self.t1preText.get_width() + 
                self.t2preText.get_width())//2 + self.t1preText.get_width()
                t2X = t1X + t1Width + 15 + self.t2preText.get_width()
                self.__adjustComponents(self.t1, t1X, y - 45, t1Width, tHeight)
                self.__adjustComponents(self.t2, t2X, y - 45, t2Width, tHeight)
            else:
                self.t2preText = ''
                t1X = self.rect.centerx - (t1Width + 15 + self.t1preText.get_width())//2 + self.t1preText.get_width()
                self.__adjustComponents(self.t1, t1X, y - 45, t1Width, tHeight)
            bX1 = self.rect.centerx - bWidth - 20
            self.__adjustComponents(self.b1, bX1, y, bWidth, bHeight)
            bX2 = self.rect.centerx + 20
            self.__adjustComponents(self.b2, bX2, y, bWidth, bHeight)
        else:
            bX1 = self.rect.centerx - bWidth//2
            self.__adjustComponents(self.b1, bX1, y, bWidth, bHeight)

    def __adjustComponents(self, object, x, y, width, height):
        '''
        __adjustComponents - reshape the area of an object.
        + object - object
        + x, y - the coordinate of an object.
        + width, height - size of an object.
        '''
        object.rect = pygame.Rect(x, y, width, height)

    def modComponents(self, obj, cls, inactive, active = None, text = '', font = None, fontSize = 20, outline = 0, limit = None):
        '''
        modComponents - modify the component object.
        + obj - object
        + cls - class of an object.
        + inactive - color or surface of object's inactive state.
        + active - color or surface of object's active state.
        + text - text on an object.
        + font - font of text on an object.
        + fontSize - size of text.
        + outline - outline color of an object.
        + limit - limit number of character can input to an object.
        '''
        if cls == 'button':
            if type(inactive) == type((0,0,0)):
                obj.bgColor = inactive
                if active != None:
                    obj.bgColorOver = active
            if type(inactive) == type(pygame.Surface):
                obj.image = inactive
                if active != None:
                    obj.overImage = active
            obj.text = text
            obj.font = font
            obj.fontSize = fontSize
            obj.outline = outline
        elif cls == 'textbox':
            obj.prevText, obj.initText, obj.text = text, text, text
            obj.fontSurface = pygame.font.Font(font, fontSize)
            obj.limit = limit
            obj.inactiveColor = inactive
            if active != None:
                obj.activeColor = active
            else:
                obj.activeColor = inactive

    def draw(self, screen, font, size, newlineSpacing = 5, textAlign = 'leftAlign', bgColor = pygame.Color('white'), 
    bdColor = None, bdSize = 1, image = None):
        '''
        draw - draw an object on the screen.
        + screen - surface object.
        + font - font of text on object.
        + size - size of text.
        + newlineSpacing - Space between line.
        + textAlign - Alignment of text on popup.
        + bgColor - background color of an object.
        + bdColor - border color of an object.
        + bdSize - border size of an object.
        + image - background image of an object.
        '''
        if image != None:
            imageSurface = pygame.transform.scale(image, (self.rect.width, self.rect.height))
            screen.blit(imageSurface, (self.rect.centerx - self.rect.width//2, self.rect.y))
        elif bgColor != None:
            pygame.draw.rect(screen, bgColor, self.rect, 0)
        if bdColor != None:
            pygame.draw.rect(screen, bdColor, self.rect, bdSize)
        self.fitText(screen, pygame.font.Font(font, size), newlineSpacing, textAlign)
        if self.type == 1:
            self.b1.draw(screen, self.activeButton)
            self.b2.draw(screen, self.activeButton)
        elif self.type == 2:
            self.t1.draw(screen)
            self.b1.draw(screen, self.activeButton)
            self.b2.draw(screen, self.activeButton)
            screen.blit(self.t1preText, (self.t1.rect.x - self.t1preText.get_width() - 5, self.t1.rect.centery - self.t1preText.get_height()//2))
            if self.t2preText != '':        
                self.t2.draw(screen)
                screen.blit(self.t2preText, (self.t2.rect.x - self.t2preText.get_width() - 5, self.t2.rect.centery - self.t2preText.get_height()//2))
        else:
            self.b1.draw(screen, self.activeButton)