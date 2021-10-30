'''
popup.py -  Create a popup object which have 3 type.
            the first one is popup that let user know some information then have a b to close popup.
            the second one is popup that user have to take an action from two of choice that appear as a b that being show on popup.
            the last one is popup that ask the user to fill some information right at the popup which has a textbox so user can fill and
            click a b to submit the information.
last updated: 29 oct 2021
'''
import pygame
from button import Button
from textbox import Textbox

class Popup:
    def __init__(self, x, y, width, height, textline, textColor, textHighlight = None, type = 0, image = None):
        self.rect =  pygame.Rect(x, y, width, height)
        self.textRect = self.rect.inflate(-30, -50)
        self.image = image
        self.text = textline
        self.textColor = textColor
        self.t1preText = pygame.font.Font(None, 20).render('', True, self.textColor)
        self.t2preText = ''
        if textHighlight:
            self.textHighlight = textHighlight
        else:
            self.textHighlight = None
        self.type = type
        if self.type == 1:
            self.b1 = Button(self.rect.centerx - 55, self.rect.height + self.rect.y - 55, 60, 30)
            self.b1.addText('Yes', bgColor=pygame.Color('green2'), bgColorOver=pygame.Color('green3'))
            self.b2 = Button(self.rect.centerx + 30, self.rect.height + self.rect.y - 55, 60, 30)
            self.b2.addText('No', bgColor=pygame.Color('red2'), bgColorOver=pygame.Color('red3'))
        elif self.type == 2:
            self.t1 = Textbox(self.rect.centerx - (200 + 60 + 30)//2, self.rect.height + self.rect.y - 55, 200, 30, pygame.Color('gainsboro'))
            self.t2 = Textbox(self.t1.rect.x + self.t1.rect.width + 15, self.rect.height + self.rect.y - 55, 100, 30, pygame.Color('gainsboro'))
            self.b1 = Button(self.t2.rect.x + 15, self.rect.height + self.rect.y - 55, 60, 30)
            self.b1.addText('DONE', bgColor=pygame.Color('black'), bgColorOver=pygame.Color('grey'))
        else:
            self.b1 = Button(self.rect.centerx - 45, self.rect.height + self.rect.y - 55, 90, 30)
            self.b1.addText('Understand', bgColor=pygame.Color('black'), bgColorOver=pygame.Color('grey'))
        self.b3 = Button(self.rect.x + self.rect.width - 20, self.rect.y + 5, 15, 15)
        self.b3.addText('x', fontSize=24, bgColor=pygame.Color('red1'), bgColorOver=pygame.Color('red3'))
        self.b4 = Button(self.rect.x + self.rect.width - 45, self.rect.y + 5, 15, 15)
        self.b4.addText('?', fontSize=24, bgColor=pygame.Color('yellow3'), bgColorOver=pygame.Color('yellow4'))
        
    def fitText(self, screen, newlineSpacing = 5, fontPath = None, size = 20, textAlign = 'leftAlign'):
        font = pygame.font.Font(fontPath, size)
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
        lastLine = 0
        for lineLen, lineSurface in zip(lineLenList, lineList):
            lineLeft = self.textRect[0]
            if textAlign == 'rightAlign':
                lineLeft += + self.textRect[2] - lineLen - spaceWidth * (len(lineSurface) - 1)
            elif textAlign == 'centerAlign':
                lineLeft += (self.textRect[2] - lineLen - spaceWidth * (len(lineSurface) - 1)) // 2
            elif textAlign == 'blockAlign' and len(lineSurface) > 1:
                lineLeft += (self.textRect[2] - lineLen) // (len(lineSurface) - 1)
            if lineBottom + fontHeight > self.textRect[1] + self.textRect[3]:
                break
            lastLine += 1
            for i, lineFit in enumerate(lineSurface):
                x, y = lineLeft + i * spaceWidth, lineBottom
                screen.blit(lineFit, (round(x), y))
                lineLeft += lineFit.get_width()
            lineBottom += fontHeight + newlineSpacing
        if lastLine < len(lineList):
            for i in range(lastLine):
                drawLine = sum(len(lineList[i]))
            remainingText = ""
            for text in wordsList[drawLine:]:
                remainingText += text + " "
            return remainingText
        return ""

    def adjustComponents(self,t1Width = 200, t2Width = 100, tHeight = 30, bWidth = 90, bHeight = 30, fontPath = None, t1text = '', t2text = ''):
        y = self.rect.height + self.rect.y - tHeight//2 - 40
        if self.type == 1:
            bX1 = self.rect.centerx - 30 - bWidth//2
            bX2 = self.rect.centerx + 30
            self.__adjustComponents(self.b2, bX2, y, bWidth, bHeight)
        if self.type == 2:
            font = pygame.font.Font(fontPath, tHeight)
            self.t1preText = font.render(t1text, True, self.textColor)
            self.t2preText = font.render(t2text, True, self.textColor)
            if t2text != '':
                t1X = self.rect.centerx - (t1Width + t2Width + 15 + self.t1preText.get_width() + self.t2preText.get_width())//2 + self.t1preText.get_width()
                t2X = t1X + t1Width + 15 + self.t2preText.get_width()
                bX1 = self.rect.centerx - bWidth//2
                self.__adjustComponents(self.t1, t1X, y - 45, t1Width, tHeight)
                self.__adjustComponents(self.t2, t2X, y - 45, t2Width, tHeight)
            else:
                self.t2preText = ''
                t1X = self.rect.centerx - (t1Width + 15 + self.t1preText.get_width())//2 + self.t1preText.get_width()
                bX1 = self.rect.centerx - bWidth//2
                self.__adjustComponents(self.t1, t1X, y, t1Width, tHeight)
        else:
            bX1 = self.rect.centerx - bWidth//2
        self.__adjustComponents(self.b1, bX1, y, bWidth, bHeight)

    def __adjustComponents(self, object, x, y, width, height):
        object.rect = pygame.Rect(x, y, width, height)

    def modComponents(self, obj, cls, inactive, active = None, text = '', fontPath = None, fontSize = 20, outline = 0, limit = None):
        if cls == 'button':
            if type(active) == type('imagePath'):
                obj.image = inactive
                if active == None:
                    obj.overImage = active
            else:
                obj.bgColor = inactive
                if active == None:
                    obj.bgColorOver = active
            obj.text = text
            obj.fontPath = fontPath
            obj.fontSize = fontSize
            obj.outline = outline
        elif cls == 'textbox':
            obj.prevText, obj.initText, obj.text = text, text, text
            obj.font = pygame.font.Font(fontPath, fontSize)
            obj.limit = limit
            obj.inactiveColor = inactive
            if active == None:
                obj.activeColor = inactive
            else:
                obj.activeColor = active

    def draw(self, screen, newlineSpacing = 5, fontPath = None, size = 16, textAlign = 'leftAlign', bgColor = pygame.Color('white'), 
    bdColor = None, bdSize = 1):
        if bdColor != None:
            pygame.draw.rect(screen, bdColor, self.rect, bdSize)
        if self.image == None:
            pygame.draw.rect(screen, bgColor, self.rect, 0)
        else:
            imageSurface = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            screen.blit(imageSurface, (self.rect.x, self.rect.y))
        self.fitText(screen, newlineSpacing, fontPath, size, textAlign)
        if self.type == 1:
            self.b1.draw(screen)
            self.b2.draw(screen)
        elif self.type == 2:
            self.t1.draw(screen)
            self.b1.draw(screen)
            screen.blit(self.t1preText, (self.t1.rect.x - self.t1preText.get_width() - 5, self.b1.rect.centery - self.t1preText.get_height()//2 - 45))
            print(self.t2preText)
            if self.t2preText != '':        
                self.t2.draw(screen)
                screen.blit(self.t2preText, (self.t2.rect.x - self.t2preText.get_width() - 5, self.b1.rect.centery - self.t2preText.get_height()//2 - 45))
        else:
            self.b1.draw(screen)
        self.b3.draw(screen)