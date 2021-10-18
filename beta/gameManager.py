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

        self.gamePhase = 0
        self.targetPlayer = None
        self.isKilled = False
        self.currentLeader = None
        self.othersCurrentLeader = []
        self.partyMember = []
        self.round = []
        self.roundCount = 0
        self.voteRejected = 0
        self.evilScore = 0
        self.goodScore = 0
        self.doMission = None
        self.missionSuccess = None
        self.gameEnded = False
    
    def setAllPlayersRole(self, randomRoles):
        for player in self.playersData:
            id = player.id
            player.setRole(Role(randomRoles[id]))
    
    def setPartyLeader(self, leaderId):
        for player in self.playersData:
            if player.id == leaderId:
                player.partyLeader = True
            if player.partyLeader and player.id != leaderId:
                player.partyLeader = False
            self.partyMember = []
    
    def drawPlayers(self):
        self.playersData.sort(key = lambda player: player.y, reverse = False)
        for player in self.playersData:
            player.draw(self.display)
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
        othersLeader = []
        gameStart = self.matchSetting[2]

        for thisData in othersPlayerData:
            thisAddr = thisData[0]
            isHost = thisData[1]
            thisPlayer = thisData[2]
            thisPlayerId = thisData[3]

            othersPlayerId.append(thisPlayerId)
            if isHost == 1:
                foundHost = True
                if gameStart and len(thisPlayer) > 11 and self.gamePhase == 0:
                    self.setAllPlayersRole(thisPlayer[11])
                if gameStart and len(thisPlayer) > 9:
                    if self.currentLeader != thisPlayer[9]:
                        self.currentLeader = thisPlayer[9]
                        self.setPartyLeader(thisPlayer[9])
                
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
                        player.id = thisPlayerId
                        if gameStart and len(thisPlayer) > 9:
                            player.choose = thisPlayer[4]
                            player.syncSignal = thisPlayer[5]
                            player.isSelected = thisPlayer[6]
                            player.partyLeader = thisPlayer[7]
                            if player.partyLeader == True and player.syncSignal == self.gamePhase:
                                self.partyMember = thisPlayer[8]
                            othersLeader.append(thisPlayer[9])
                            if player.getRole().getName() == "Assassin":
                                self.targetPlayer = thisPlayer[10][0]
                                self.isKilled = thisPlayer[10][1]
                        break
            else:
                if thisPlayer != "":
                    print("[GAME] Something wrong with update player data")
        self.othersCurrentLeader = othersLeader

        # set my host
        if foundHost == False:
            self.player.host = True
        
        # set my id
        listOfAllId = list(range(len(self.playersData)))
        myId = list(set(listOfAllId) - set(othersPlayerId))
        self.player.id = myId[0]


    def sendAndReceiveData(self, sendData = []):
        data = self.network.tryGetData(sendData)
        if data != None:
            currentPlayerInMatch = data[0]
            othersPlayerData = data[1]
            if self.matchSetting == []:
                self.matchSetting += data[2]
            else:
                self.matchSetting.clear()
                self.matchSetting += data[2] 

        if othersPlayerData != None and currentPlayerInMatch != None:
            
            self.checkExistPlayer(currentPlayerInMatch)

            self.updatePlayersData(othersPlayerData)

        # print(data)
        # print(othersPlayerData)
        # print(currentPlayerInMatch)