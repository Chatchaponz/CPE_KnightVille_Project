'''
popup.py -  Create a popup object which have 3 type.
            the first one is popup that let user know some information then have a button to close popup.
            the second one is popup that user have to take an action from two of choice that appear as a button that being show on popup.
            the last one is popup that ask the user to fill some information right at the popup which has a textbox so user can fill and
            click a button to submit the information.
last updated: 25 oct 2021
'''
from textbox import *
from button import *

'''
Popup - Create a popup object.
'''
class Popup:
    '''
    __init__ - Constructor for create an object which will also use to set-up an object.
    + x, y - coordinate position of an object.
    + width, height - width and height of an object.
    + rect - area of an object.
    + textRect - area of a text.
    + text - text that display on an object.
    + textColor - color of a text.
    + textHighlight - color of a text that highlight.
    + type - type code of an object.
    + b1, b2 - button object.
    + t1 - textbox object.
    '''
    def __init__(self, x, y, width, height, textline, textColor, textHighlight = None, type = 0):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect =  pygame.Rect(x, y, width, height)
        self.textRect = self.rect.inflate(-30, -30)
        self.text = textline
        self.textColor = textColor
        if textHighlight:
            self.textHighlight = textHighlight
        else:
            self.textHighlight = None
        self.type = type
        if self.type == 1:
            self.b1 = Button(self.rect.centerx - 30 - 60, self.height + self.y - 30 - 25, 60, 30)
            self.b1.addText('Yes', bgColor=pygame.Color('green2'), bgColorOver=pygame.Color('green3'))
            self.b2 = Button(self.rect.centerx + 30, self.height + self.y - 30 - 25, 60, 30)
            self.b2.addText('No', bgColor=pygame.Color('red2'), bgColorOver=pygame.Color('red3'))
        elif self.type == 2:
            self.t1 = Textbox(self.x + 15, self.height + self.y - 30 - 15, self.width - 60 - 30, 30, pygame.Color('gainsboro'))
            self.b1 = Button(self.x + self.width - 60 - 15, self.height + self.y - 30 - 25, 60, 30)
            self.b1.addText('DONE', bgColor=pygame.Color('black'), bgColorOver=pygame.Color('grey'))
        else:
            self.b1 = Button(self.rect.centerx - 90//2, self.height + self.y - 30 -25, 90, 30)
            self.b1.addText('Understand', bgColor=pygame.Color('black'), bgColorOver=pygame.Color('grey'))
        
    '''
    fitText - method to fit a text inside of box and determine how text should be like color, font and so on.
    to detailed is  text being split into word then store in list. 
                    word should be highlight when suffix with /> and display without suffix.
                    word being joint into a line without overlaping with the textRect.
                    if over textRect it should be newline and align to and so on.
    + screen - display screen object. 
    + newlineSpacing - space between a line.
    + fontPath - location of font file.
    + size - text size.
    + textAlign - Align of text.
    + font - loading font.
    + width - width of line.
    + spaceWidth - width of spacebar.
    + fontHeight - height of font.
    + wordsList - list of words that split from text.
    + line - list of line by combining word.
    + word - word that being split from text inside wordsList.
    + text - text that display on an object.
    + textColor - color of a text.
    + textHighlight - color of a text that highlight.
    + maxLen - width limit of line.
    + lineLenList - list of line's width.
    + lineList - list of line.
    + lineFit - fitted line.
    + lineBottom - line under current line.
    + lastLine - last line.
    + i - count to keep track of line.
    + drawLine - sum of line's lenght.
    + remainingText - text that over the textRect.
    '''
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

    '''
    modTextbox - method to modified textbox in popup object.
    + inactiveColor - border color for inactive textbox object.
    + activeColor - border color for active textbox object.
    + x, y - coordinate position of textbox object.
    + color - border color of an object to update.
    + textSurface - render a text with set-up properties.
    + active - status of an object.
    + limit - limit input character of an object.
    + width, height - width and height of an object.
    + rect - area of an object.
    + t1 - textbox object.
    '''
    def modTextbox(self, inactiveColor = pygame.Color('gainsboro'), activeColor = pygame.Color('black'), x = None, y = None, 
    width = 250, height = 30, limit = None, text = ''):
        if x == None:
            x = self.rect.centerx - width//2 - 40
        if y == None:
            y = self.height + self.y - 55
        self.t1 = Textbox(x, y, width, height, inactiveColor, activeColor, limit, text)

    '''
    modButton - method to modified button object in popup object.
    + b1Text, b2Text - text on the button 1 and 2.
    + b1TextColor, b2TextColor - color for text on button 1 and 2.
    + b1TextOver, b2TextOver - color for text on button 1 and 2 when mouse is over a button.
    + b1Color, b2Color - color of button 1 and 2.
    + b1Over, b2Over - color of button 1 and 2 when mouse is over a button.
    + x1, x2, y - coordinate position of button 1 and 2.
    + width, height - width and height of button.
    + fonttPath - location of font.
    + size - size of font.
    + outline - outline size of button.
    + b1, b2 - Button 1, Button 2
    '''
    def modButton(self, b1Text = None, b1Color = None, b1Over = None, b2Text = None, b2Color = None, b2Over = None, x1 = None, 
    x2 = None, y = None, width = 90, height = 30, fontPath = None, size = 20, b1TextColor = pygame.Color('white'), 
    b2TextColor = pygame.Color('white'), b1TextOver = pygame.Color('white'), outline = 0, b2TextOver = pygame.Color('white')):
        if y == None:
            y = self.height + self.y - height//2 - 40
        if self.type == 1:
            if b1Text == None:
                b1Text = 'Yes'
            if b2Text == None:
                b2Text = 'No'
            if b1Color == None:
                b1Color = pygame.Color('green2')
            if b2Color == None:
                b2Color = pygame.Color('red2')
            if b1Over == None:
                b1Over = pygame.Color('green3')
            if b2Over == None:
                b2Over = pygame.Color('red3')
            if x1 == None:
                x1 = self.rect.centerx - 30 - width
            if x2 == None:
                x2 = self.rect.centerx + 30
            self.b1 = Button(x1, y, width, height)
            self.b2 = Button(x2, y, width, height)
            self.b1.addText(b1Text, fontPath, size, b1TextColor, outline, b1TextOver, b1Color, b1Over)
            self.b2.addText(b2Text, fontPath, size, b2TextColor, outline, b2TextOver, b2Color, b2Over)
        if self.type == 2:
            if b1Text == None:
                b1Text = 'DONE'
            if b1Color == None:
                b1Color = pygame.Color('black')
            if b1Over == None:
                b1Over = pygame.Color('grey')
            if x1 == None:
                x1 = self.rect.centerx + self.t1.width//2 - 30 #centerx of box + width of textbox/2
            self.b1 = Button(x1, y, width, height)
            self.b1.addText(b1Text, fontPath, size, b1TextColor, outline, b1TextOver, b1Color, b1Over)
        else:
            if x1 == None:
                x1 = self.rect.centerx - width//2
            if b1Text == None:
                b1Text = 'Understand'
            if b1Color == None:
                b1Color = pygame.Color('orange3')
            if b1Over == None:
                b1Over = pygame.Color('orange2')
            self.b1 = Button(x1, y, width, height)
            self.b1.addText(b1Text, fontPath, size, b1TextColor, outline, b1TextOver, b1Color, b1Over)

    '''
    draw - method to draw popup object due to the type then draw with necessary object such as button etc.
    + screen - display screen object. 
    + newlineSpacing - space between a line.
    + fontPath - location of font file.
    + size - text size.
    + textAlign - Align of text.
    + bgColor - popup background color.
    + bdColor - popup border color.
    + bdSize - size of popup's border.
    + b1, b2 - button object.
    + t1 - textbox object.
    '''
    def draw(self, screen, newlineSpacing = 5, fontPath = None, size = 16, textAlign = 'leftAlign', bgColor = pygame.Color('white'), 
    bdColor = None, bdSize = 1):
        if bdColor != None:
            pygame.draw.rect(screen, bdColor, self.rect, bdSize)
        pygame.draw.rect(screen, bgColor, self.rect, 0)
        self.fitText(screen, newlineSpacing, fontPath, size, textAlign)
        if self.type == 1:
            self.b1.draw(screen)
            self.b2.draw(screen)
        elif self.type == 2:
            self.t1.draw(screen)
            self.b1.draw(screen)
        else:
            self.b1.draw(screen)