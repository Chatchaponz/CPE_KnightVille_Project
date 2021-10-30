import time
from screen import GameScreen
from player import Player
from role import Role

class GameManager(GameScreen):
    
    def __init__(self, control):
        super(GameManager, self).__init__(control)
        self.network = control.network
        self.player = control.player

        self.othersPlayerInMatch = control.globalData[0]
        self.playersData = control.globalData[1]
        self.matchSetting = control.globalData[2]
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

    def doSendAndReceiveData(self):
        while self.allowSendData:
            if self.network.connectStatus == True and self.sendData != []:
                self.sendAndReceiveData(self.sendData)
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
        # othersLeader = []
        othersStatus = []
        if len(self.matchSetting) > 2:
            gameStart = self.matchSetting[2]

        for thisData in othersPlayerData:
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
        if foundHost == False:
            self.player.host = True
        
        # set my id
        if self.player.id == None:
            listOfAllId = list(range(len(self.playersData)))
            myId = list(set(listOfAllId) - set(othersPlayerId))
            self.player.id = myId[0]


    def sendAndReceiveData(self, sendData = []):
        data = self.network.tryGetData(sendData)
        if data != None:
            self.currentPlayerInMatch = data[0]
            self.othersPlayerData = data[1]
            if len(data) > 2 and data[2] != None:
                if self.matchSetting == []:
                    self.matchSetting += data[2]
                else:
                    self.matchSetting.clear()
                    self.matchSetting += data[2]
    
    def updateScreenData(self):

        if self.othersPlayerData != None and self.currentPlayerInMatch != None:

            if self.matchSetting != []:
            # print(self.matchSetting)
                gameStart = self.matchSetting[2]
                matchData = self.matchSetting[1]
                
                # sync game phase and update match data
                if gameStart:

                    if len(matchData) > 2:
                        self.gamePhase = matchData[1]
                        self.player.syncSignal = self.gamePhase
                        self.roundCount = matchData[2]

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