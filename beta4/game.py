import pygame, sys, threading
from button import Button 
from gameManager import GameManager

class Game(GameManager):
    
    def __init__(self, control):
        super(Game, self).__init__(control)

        self.nameList = []

        self.summit = Button( 50 , 100, 100, 30)
        self.summit.addText("Summit", self.font, 20, self.control.white, 1, (50,50,50))

        self.accept = Button( 50 , 100, 100, 30)
        self.accept.addText("Accept", self.font, 20, self.control.white, 1, (50,50,50))

        self.reject = Button( 150 , 100, 100, 30)
        self.reject.addText("Reject", self.font, 20, self.control.white, 1, (50,50,50))

        self.success = Button( 50 , 100, 100, 30)
        self.success.addText("Success", self.font, 20, self.control.white, 1, (50,50,50))

        self.fail = Button( 150 , 100, 100, 30)
        self.fail.addText("fail", self.font, 20, self.control.white, 1, (50,50,50))

        self.assignment = {
            5: [2, 3, 2, 3, 3],
            6: [2, 3, 4, 3, 4],
            7: [2, 3, 3, 4, 4],
            8: [3, 4, 4, 5, 5],
            9: [3, 4, 4, 5, 5],
            10: [3, 4, 4, 5, 5]
        }
    
    # override
    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #[TEMP]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and self.player.getRole() != None:
                    self.player.revealRole(self.playersData)

                if event.key == pygame.K_RETURN and self.gameEnded and self.matchSetting[2] == False:
                    if self.network.connectStatus == True:
                        self.allowSendData = False
                        self.sendDataThread.join()
                        self.resetAll()
                    self.changePageByInput(True, self.control.lobby)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z and self.player.getRole() != None:
                    self.player.unrevealRole(self.playersData)

            if self.matchSetting[2] == True:
                self.player.playerMovement(event)
    
    def resetAll(self):
        self.currentPlayerInMatch = None
        self.othersPlayerData = None
        self.sendData = []
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
        self.nameList = []
        self.othersGameStatus = []
        self.roleAvailable = False
        self.player.isPlaying = False 
        self.player.updateByPosition(50, 700)
        for player in self.playersData:   
            player.setRole(None)
            player.choose = 0
            player.syncSignal = 0
            player.isSelected = False
            player.partyLeader = False
            player.isTarget = False
            player.isKilled = False
            player.setRoleReveal(False)

    # vvv Name list make here (Can Change)
    def makeNameList(self):
        initPositionY = 50
        nameList = []
        self.playersData.sort(key = lambda player: player.id, reverse = False)
        for player in self.playersData:
            tempButton = Button(950, initPositionY, 100, 30)
            tempButton.addText(player.name, self.font, 20, self.control.white, 1, (50,50,50))
            nameList.append(tempButton)
            initPositionY += 50
        return nameList

    def revealAllPlayerRole(self):
        player_x = 10
        self.playersData.sort(key = lambda player: player.id, reverse = False)
        for player in self.playersData:
            player.updateByPosition(player_x, 700)
            player.setRoleReveal(True)
            player_x += 150
    
    def updateSelectedPlayer(self, partyMember):
        for player in self.playersData:
            if player.id in partyMember:
                player.isSelected = True
            if player.id not in partyMember and player.isSelected:
                player.isSelected = False
    
    def updateTargetPlayer(self, id):
        for player in self.playersData:
            if player.id == id:
                player.isTarget = True
            if id != player.id and player.isTarget:
                player.isTarget = False
    
    def killPlayer(self, killStatus = False):
        if killStatus:
            for player in self.playersData:
                if player.id == self.targetPlayer and player.isTarget:
                    player.isKilled = True
                    return player
        else:
            return None
    
    def revealAssassin(self):
        for player in self.playersData:
            if player.getRole().getName() == "Assassin":
                player.setRoleReveal(True)
                break
    
    def isOthersGameEnded(self):
        status = True
        for gameStatus in self.othersGameStatus:
            if gameStatus == False:
                status = False
                break
        return status

    # choose = 0 : no Vote
    # choose = 1 : accept
    # choose = 2 : reject
    # choose = 3 : summit
    # choose = 4 : success
    # choose = 5 : fail
    
    def phaseEvent(self):
        playerNumber = self.matchSetting[0]

        if self.gamePhase == 0:
            if self.player.getRole() != None:
                self.roleAvailable = True
            else:
                self.roleAvailable = False

        if self.gamePhase == 1:
            if self.partyMember != []:
                self.partyMember = []
            if self.player.isSelected == True:
                self.player.isSelected = False

        if self.gamePhase == 2:
            if self.player.partyLeader == True:
                memberLimit = self.assignment[playerNumber][self.roundCount]
                if self.nameList == []:
                    self.nameList = self.makeNameList()
                for id, name in enumerate(self.nameList):
                    name.draw(self.display)
                    if name.isButtonClick():
                        if id in self.partyMember:
                            self.partyMember.remove(id)
                        elif (id not in self.partyMember and
                            len(self.partyMember) < memberLimit):
                            self.partyMember.append(id)
                        else:
                            print("[GAME] Error assign party member")
                self.updateSelectedPlayer(self.partyMember)
                if len(self.partyMember) == memberLimit:
                    self.summit.draw(self.display)
                    if self.summit.isButtonClick():
                        self.player.choose = 3
            else:
                self.updateSelectedPlayer(self.partyMember)
        
        if self.gamePhase == 3:
            if self.player.choose not in [1, 2]:
                self.accept.draw(self.display)
                self.reject.draw(self.display)
                if self.accept.isButtonClick():
                    self.player.choose = 1
                if self.reject.isButtonClick():
                    self.player.choose = 2
        
        if self.gamePhase == 5:
            if self.player.choose != 0:
                self.player.choose = 0
        
        if self.gamePhase == 6:
            if self.player.id in self.partyMember:
                if self.player.choose not in [4, 5]:
                    self.success.draw(self.display)
                    if self.success.isButtonClick():
                        self.player.choose = 4
                    if self.player.getRole().getIdentity() == "Evil":
                        self.fail.draw(self.display)
                        if self.fail.isButtonClick():
                            self.player.choose = 5
        
        if self.gamePhase == 8:
            if self.player.choose != 0:
                self.player.choose = 0
        
        if self.gamePhase == 9:

            if self.player.partyLeader == True:
                self.player.partyLeader = False
            if self.player.isSelected == True:
                self.player.isSelected = False
                
            if self.evilScore == 3:
                self.gameEnded = True
                self.drawText('Evil Win!!!', 50 , 500, 300, self.font, self.control.white)
                self.drawText('Enter to exit', 30 , 500, 700, self.font, self.control.white)
                self.revealAllPlayerRole()

                if (self.player.host == True and 
                    self.matchSetting[2] == True and
                    self.isOthersGameEnded()):
                    self.network.stopThisGame()
            
            if self.goodScore == 3:
                killedPlayer = None
                if self.player.getRole().getName() == "Assassin" and not self.gameEnded:
                    self.player.setRoleReveal(True)
                    if self.nameList == []:
                        self.nameList = self.makeNameList()
                    for id, name in enumerate(self.nameList):
                        name.draw(self.display)
                        if name.isButtonClick():
                            self.targetPlayer = id
                        self.updateTargetPlayer(self.targetPlayer)
                    if self.targetPlayer != None:
                        self.summit.draw(self.display)
                        if self.summit.isButtonClick():
                            self.isKilled = True
                            killedPlayer = self.killPlayer(self.isKilled)
                else:
                    self.revealAssassin()
                    self.updateTargetPlayer(self.targetPlayer)
                    killedPlayer = self.killPlayer(self.isKilled)
                    
                if killedPlayer != None:
                    self.gameEnded = True
                    if killedPlayer.getRole().getName() == "Merlin":
                        self.drawText('Evil Win!!!', 50 , 500, 300, self.font, self.control.white)
                    else:
                        self.drawText('Good Win!!!', 50 , 500, 300, self.font, self.control.white)
                    self.drawText('Enter to exit', 30 , 500, 700, self.font, self.control.white)
                    self.revealAllPlayerRole()
                    
                    if (self.player.host == True and 
                        self.matchSetting[2] == True and
                        self.isOthersGameEnded()):
                        self.network.stopThisGame()

    
    # Phase 0 : Random role

    # Phase 1 : Check score if their is a winner go to phase 9 
    #           / get party leader and reset party member

    # Phase 2 : Party leader select party member and summit
    
    # Phase 3 : Each player vote accept or reject
    
    # Phase 4 : Calculate vote and sync all player score 
    
    # Phase 5 : Decide to go next phase or back to phase 1
    
    # Phase 6 : Party member vote

    # Phase 7 : Calculate vote and sync all player score
    
    # Phase 8 : Go to phase 1 again
    
    # Phase 9 : Conclusion
    
    def displayScreen(self):

        self.displayRunning = True
        # inintial
        self.player.updateByPosition(50, 700)
        self.player.isPlaying = True

        self.allowSendData = True
        self.sendDataThread = threading.Thread(target= self.doSendAndReceiveData)
        self.sendDataThread.daemon = True
        self.sendDataThread.start()

        # for thread in threading.enumerate(): 
        #     print(thread.name)
        
        # Set collision
        self.player.collided = []
        if self.player.collided == []:
            self.player.collided = [[0, self.screenWidth], [360, self.screenHeight]]

        while self.displayRunning:

            # if number of player in match not equal to the maximum player number allow
            if len(self.playersData) != self.matchSetting[0]:
                print("Some player are missing")
                if self.network.connectStatus == True:
                    self.allowSendData = False
                    self.sendDataThread.join()
                    self.resetAll()
                    if self.player.host == True:
                        self.network.stopThisGame()
                self.changePageByInput(True, self.control.lobby)

            self.checkEvent()

            self.sendData = [self.player.x,
                            self.player.y,
                            self.player.skin,
                            self.player.name,
                            self.player.isPlaying,
                            self.player.choose,
                            self.player.syncSignal,
                            self.player.isSelected,
                            self.player.partyLeader,
                            self.partyMember,
                            self.currentLeader,
                            [self.targetPlayer, self.isKilled],
                            self.gameEnded,
                            self.roleAvailable,
                            self.roundCount,
                            self.goodScore,
                            self.evilScore,
                            self.voteRejected]
            
            # page blackground
            self.display.fill((0, 0, 0))

            # if self.waitForOthers():
            self.phaseEvent()

            #[TEST PRINT]
            # print(self.currentLeader,self.gamePhase, self.player.syncSignal, self.player.choose, self.missionSuccess, self.goodScore, self.evilScore, self.partyMember)
            # print(self.currentLeader, self.gamePhase, self.player.syncSignal, self.player.choose,self.roundCount, self.round, self.goodScore, self.evilScore)
            # if self.player.host == True:
            #     print(sendData)
            # print(self.gamePhase)
            # for player in self.playersData:
            #     print( player.syncSignal, player.choose, end= " ")

            if self.network.connectStatus == True:
                self.updateScreenData()
            #     self.sendAndReceiveData(sendData)
            self.drawPlayers()
            
            # TEMP
            x = 0
            for i in self.round:
                if i == 1:
                    pygame.draw.rect(self.display, (0,0,255), pygame.Rect(x, 0, 30, 30) )
                if i == 2:
                    pygame.draw.rect(self.display, (255,0,0), pygame.Rect(x, 0, 30, 30) )
                x += 35
            x = 0
            for i in range(self.voteRejected):
                pygame.draw.rect(self.display, (255,0,255), pygame.Rect(x, 35, 30, 30) )
                x += 35

            self.biltScreen() # update screen
            self.clock.tick(60) # run at 60 fps