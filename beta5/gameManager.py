import pygame, time
from screen import GameScreen
from player import Player
from role import Role
from textbox import Textbox

class GameManager(GameScreen):
    
    def __init__(self, control):
        super(GameManager, self).__init__(control)
        self.network = control.network
        self.player = control.player

        self.othersPlayerInMatch = control.globalData[0]
        self.playersData = control.globalData[1]
        self.matchSetting = control.globalData[2]
        self.allMessages = control.globalData[3]
        self.currentPlayerInMatch = None
        self.othersPlayerData = None

        self.sendData = []
        self.sendDataThread = None

        self.gamePhase = 0
        self.targetPlayer = None
        self.isKilled = False
        self.currentLeader = None
        self.partyMember = []
        self.round = []
        self.roundCount = 0
        self.voteRejected = 0
        self.evilScore = 0
        self.goodScore = 0
        self.gameEnded = False
        self.othersGameStatus = []
        self.roleAvailable = False

        # Chat box 
        self.chatPosX, self.chatPosY = 10, 380
        chatWidth, self.chatHeight = 415, 300
        self.chatBox = pygame.Surface((chatWidth, self.chatHeight))
        self.chatBox.set_colorkey(self.control.black) # this color will be transparent
        self.chatBox.fill(self.control.black)
        self.chatBoxBg = pygame.Surface((chatWidth, self.chatHeight))
        self.chatBoxBg.set_alpha(100)
        self.fontsize = 20
        self.textFont = pygame.font.Font(self.font, self.fontsize)
        self.chatText = Textbox(self.chatPosX, self.chatPosY + self.chatHeight, 
                                chatWidth, 30, self.control.white, limit = 89, text= "Chat with others", 
                                fontPath= self.font, size = self.fontsize)
        
        self.offset = 0 # to make chat box scroll
        self.lastTextPos = self.chatHeight - self.fontsize
        self.startTextPos = self.chatHeight - self.fontsize
        self.myText = ""
        self.pressEnter = False
    
    def handleChatBoxEvent(self, event):
        if self.chatText.active:

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:

                    self.myText = self.chatText.getText()

                    if self.myText != "":
                        if not self.network.trySendMessage(self.myText):
                            print("Cannot send message")
                        self.pressEnter = True
                    else:
                        self.pressEnter = False

                    self.chatText.resetText()
                    self.myText = ""
            
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    self.pressEnter = False
            
            # scroll surface
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and (self.lastTextPos + self.fontsize - 10 + self.offset) < 0: #up
                    self.offset += 20
                if event.button == 5 and (self.startTextPos + self.offset) > self.chatHeight - self.fontsize: #down
                    self.offset -= 20

        else:
            self.pressEnter = False
            self.startTextPos = self.chatHeight - self.fontsize

        if not self.pressEnter:
            self.chatText.handleEvent(event)
    
    def getNameByAddr(self, addr):
        name = ""
        ishost = False
        if(self.currentPlayerInMatch != None and self.playersData != []):
            if addr in self.currentPlayerInMatch and addr not in self.othersPlayerInMatch:
                name =  self.player.name
                ishost = True
            elif addr not in self.currentPlayerInMatch and addr not in self.othersPlayerInMatch:
                name = "Unknown"
            else:
                for player in self.playersData:
                    if player.address == addr:
                        name = player.name
                        break
        return name, ishost

    def drawMessage(self, message: str, nameWidth, namelen, thisPos):
        n = 30
        if(len(message) + namelen < n):
            thisPos -= 20
            drawMessage = self.textFont.render(message, False, self.control.white)
            self.chatBox.blit(drawMessage, (self.chatPosX + nameWidth, thisPos + self.offset))
        else:
            splitMessages = []
            # message after name
            splitMessages.append(message[0: (n - namelen)])
            # other messages
            for index in range( (n - namelen), len(message), n):
                splitMessages.append(message[index: index + n ])

            # draw messages
            for subMessage in range(len(splitMessages), 0, -1):
                drawMessage = self.textFont.render(splitMessages[subMessage - 1], False, self.control.white)
                thisPos -= 20
                if subMessage - 1 == 0: self.chatBox.blit(drawMessage, (self.chatPosX + nameWidth, thisPos + self.offset))
                else: self.chatBox.blit(drawMessage, (self.chatPosX, thisPos + self.offset))

        return thisPos
    
    def drawChatBox(self, screen):
        
        # draw Text box
        self.chatText.draw(screen)

        self.chatText.update()

        if self.chatText.active:
            # draw chat box
            self.chatBox.fill(self.control.black)

            # draw name + message
            textPos = self.startTextPos # get start text position

            for messageIndex in range(len(self.allMessages), 0, -1):
                thisMessage = self.allMessages[messageIndex - 1]
                if (type(thisMessage) is list and len(thisMessage) > 1):
                    name, ishost = self.getNameByAddr(thisMessage[0])
                    if name != "":
                        # draw name
                        if ishost: fontColor = (0, 255, 255)
                        elif not ishost: fontColor = (255, 255, 0)
                        else: fontColor = (255, 0, 0)
                        drawName = self.textFont.render("<" + name + ">: ", False, fontColor)

                        # draw messages
                        textPos = self.drawMessage(thisMessage[1], drawName.get_width(), len(name) + 4, textPos)

                        self.chatBox.blit(drawName, (self.chatPosX, textPos + self.offset))
            
            screen.blit(self.chatBoxBg, (self.chatPosX, self.chatPosY) )
            screen.blit(self.chatBox, (self.chatPosX, self.chatPosY) )
            self.lastTextPos = textPos # get end text position

    def doSendAndReceiveData(self):
        while self.allowSendData:
            if self.network.connectStatus == True and self.sendData != []:
                self.sendAndReceiveData(self.sendData)
            if self.network.connectStatus == False:
                break
            time.sleep(0.001)
    
    def setAllPlayersRole(self, randomRoles):
        for player in self.playersData:
            id = player.id
            player.setRole(Role(randomRoles[id]))
    
    def setPartyLeader(self, leaderId):
        for player in self.playersData:
            if player.id == leaderId:
                player.partyLeader = True
                self.currentLeader = player.id
            if player.partyLeader and player.id != leaderId:
                player.partyLeader = False
            self.partyMember = []
    
    def drawPlayers(self):
        canUpdate = False
        self.playersData.sort(key = lambda player: player.y, reverse = False)
        
        for player in self.playersData:
            
            if ((self.control.currentState == self.control.lobby and
                 player.isPlaying == False) or
                (self.control.currentState == self.control.game and
                 player.isPlaying == True)):
                player.draw(self.display)
                if player == self.player:
                    canUpdate = True
        if canUpdate:
            self.player.update()
    
    def checkExistPlayer(self, currentPlayerInMatch):
        # check player in match (if they are leave// remove their data)
        for address in self.othersPlayerInMatch :
            if address not in currentPlayerInMatch :
                self.othersPlayerInMatch.remove(address)
                for player in self.playersData:
                    if player.address == address:
                        self.playersData.remove(player)
                        break
    
    def updatePlayersData(self, othersPlayerData):

        foundHost = False
        othersPlayerId = []
        othersStatus = []
        gameStart = False
        
        if len(self.matchSetting) > 2:
            gameStart = self.matchSetting[2]

        for thisData in othersPlayerData:
            if type(thisData) == list and len(thisData) > 3:
                thisAddr = thisData[0]
                isHost = thisData[1]
                thisPlayer = thisData[2]
                thisPlayerId = thisData[3]

                othersPlayerId.append(thisPlayerId)
                if isHost == 1:
                    foundHost = True
                    
                if thisAddr not in self.othersPlayerInMatch and thisPlayer != "":
                    tempPlayer = Player(thisPlayer[0], thisPlayer[1], thisPlayer[2], thisPlayer[3])
                    tempPlayer.address = thisAddr
                    tempPlayer.id = thisPlayerId
                    self.playersData.append(tempPlayer)
                    self.othersPlayerInMatch.append(thisAddr)
                elif thisAddr in self.othersPlayerInMatch:
                    for player in self.playersData:
                        if player != self.player and player.address == thisAddr:
                            player.updateByPosition(thisPlayer[0], thisPlayer[1])
                            if player.skin != thisPlayer[2]:
                                player.updateSkin(thisPlayer[2])
                            if player.name != thisPlayer[3]:
                                player.updateName(thisPlayer[3])
                            player.id = thisPlayerId
                            player.isPlaying = thisPlayer[4]
                            if gameStart and len(thisPlayer) > 12:
                                player.choose = thisPlayer[5]
                                player.syncSignal = thisPlayer[6]
                                player.isSelected = thisPlayer[7]
                                player.partyLeader = thisPlayer[8]
                                if player.partyLeader == True and player.syncSignal == self.gamePhase:
                                    self.partyMember = thisPlayer[9]
                                if player.getRole() != None:
                                    if player.getRole().getName() == "Assassin":
                                        self.targetPlayer = thisPlayer[11][0]
                                        self.isKilled = thisPlayer[11][1]
                                othersStatus.append(thisPlayer[12])
                            break
                else:
                    if thisPlayer != "":
                        print("[GAME] Something wrong with update player data")

        # check that others already end there game
        self.othersGameStatus = othersStatus

        # set my host
        if not foundHost:
            self.player.host = True
        if foundHost:
            self.player.host = False
        
        # set my id
        listOfAllId = list(range(len(self.playersData)))
        myId = list(set(listOfAllId) - set(othersPlayerId))
        if len(myId) > 0:
            self.player.id = myId[0]


    def sendAndReceiveData(self, sendData = []):
        data = self.network.tryGetData(sendData)
        if data != None:
            if len(data) > 3:
                if type(data[0]) is list: self.currentPlayerInMatch = data[0]
                if type(data[1]) is list: self.othersPlayerData = data[1]
                if type(data[2]) is list: self.matchSetting = data[2]
                if type(data[3]) is list: self.allMessages = data[3]
            # if len(data) > 2 and data[2] != None:
            #     if self.matchSetting == []:
            #         self.matchSetting += data[2]
            #     else:
            #         self.matchSetting.clear()
            #         self.matchSetting += data[2]
    
    def updateScreenData(self):

        if self.othersPlayerData != None and self.currentPlayerInMatch != None:

            if self.matchSetting != [] and type(self.matchSetting) is list:
            # print(self.matchSetting)

                gameStart = self.matchSetting[2]
                matchData = self.matchSetting[1]
                
                # sync game phase and update match data
                if gameStart:

                    if len(matchData) > 2:
                        self.gamePhase = matchData[1]
                        self.player.syncSignal = self.gamePhase
                        self.roundCount = matchData[2]

                    # if len(matchData) > 3:
                    #     print(matchData[1], matchData[3])
                    
                    if self.gamePhase == 0:
                        if len(matchData) > 3:
                            self.setAllPlayersRole(matchData[3])

                    if self.gamePhase == 1:
                        if len(matchData) > 3:
                            self.setPartyLeader(matchData[3])
                    
                    if self.gamePhase == 4 or self.gamePhase == 7:
                        if len(matchData) > 3 and type(matchData[3]) == list:
                            if self.goodScore < matchData[3][0]:
                                self.round.append(1)
                                self.goodScore = matchData[3][0]
                            if self.evilScore < matchData[3][1]:
                                self.round.append(2)
                                self.evilScore = matchData[3][1]
                            self.voteRejected = matchData[3][2]
            
            self.checkExistPlayer(self.currentPlayerInMatch)

            self.updatePlayersData(self.othersPlayerData)