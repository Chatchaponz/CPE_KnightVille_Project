import pygame, sys, random
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
                if event.key == pygame.K_z:
                    self.player.revealRole(self.playersData)

                if event.key == pygame.K_RETURN and self.gameEnded and self.matchSetting[2] == False:
                    if self.network.connectStatus == True:
                        self.resetAll()
                    self.changePageByInput(True, self.control.lobby)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    self.player.unrevealRole(self.playersData)
            if self.matchSetting[2] == True:
                self.player.playerMovement(event)
    
    def resetAll(self):
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
        self.nameList = []
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
    
    def randomRoles(self):
        randomRoles = []
        playerNumber = self.matchSetting[0]
        playerRules = {
            5: {"good": 3, "evil": 2},
            6: {"good": 4, "evil": 2},
            7: {"good": 4, "evil": 3},
            8: {"good": 5, "evil": 3},
            9: {"good": 6, "evil": 3},
            10: {"good": 6, "evil": 4}
        }
        allowRoles = self.matchSetting[1]
        randomRoles += [2] * playerRules[playerNumber]["good"]
        randomRoles += [6] * playerRules[playerNumber]["evil"]
        goodIndex = 0
        evilIndex = playerRules[playerNumber]["good"] # evil start index equal to end index of good
        for role, roleAllow in enumerate(allowRoles):
            if roleAllow and role in [0, 1]:
                randomRoles[goodIndex] = role
                goodIndex += 1
            if roleAllow and role in [3, 4, 5, 7]:
                randomRoles[evilIndex] = role
                evilIndex += 1
        random.shuffle(randomRoles)
        return randomRoles
    
    def waitForOthers(self, phase):
        isSync = True
        for player in self.playersData:
            if player.syncSignal < phase:
                isSync = False
                break
        return isSync

    def changeLeader(self):
        playerNumber = self.matchSetting[0]
        
        if self.currentLeader + 1 < playerNumber:
            self.currentLeader += 1
        else:
            self.currentLeader = 0
        self.setPartyLeader(self.currentLeader)

    def resetPlayersActivity(self, status):
        for player in self.playersData:
            if status == False:
                self.partyMember = []
                if player.isSelected == True:
                    player.isSelected = False
            player.choose = 0

    # vvv May change later
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
    
    def countScore(self):
        rejectVote = 0
        for player in self.playersData:
            if player.choose == 2:
                rejectVote += 1
        return rejectVote

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
    
    def isChoiceReady(self, phase, choice = []):
        ready = True
        for player in self.playersData:
            if( player.choose in choice and player.syncSignal != phase ):
                print(player.address, player.choose)
                ready = False
        return ready
    
    def isSignalSync(self):
        sync = True
        for player in self.playersData:
            if player.syncSignal != self.gamePhase:
                sync = False
        return sync

    # choose = 0 : no Vote
    # choose = 1 : accept
    # choose = 2 : reject
    # choose = 3 : summit
    # choose = 4 : success
    # choose = 5 : fail
    
    def phaseEvent(self):
        playerNumber = self.matchSetting[0]

        if self.gamePhase == 3 and self.isSignalSync():
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
        
        if self.gamePhase == 4 and self.isSignalSync():
            if self.player.choose not in [1, 2]:
                self.accept.draw(self.display)
                self.reject.draw(self.display)
                if self.accept.isButtonClick():
                    self.player.choose = 1
                if self.reject.isButtonClick():
                    self.player.choose = 2
        
        if self.gamePhase == 5 and self.isSignalSync():
            if self.doMission == None:
                passScore = playerNumber * 0.5
                rejectVote = self.countScore()
                if rejectVote >= passScore:
                    self.doMission = False
                    self.resetPlayersActivity(self.doMission)
                    self.changeLeader()
                else:
                    self.doMission = True
                    self.resetPlayersActivity(self.doMission)
        
        if self.gamePhase == 6 and self.isSignalSync():
            if self.player.id in self.partyMember:
                if self.player.choose not in [4, 5]:
                    self.success.draw(self.display)
                    if self.success.isButtonClick():
                        self.player.choose = 4
                    if self.player.getRole().getIdentity() == "Evil":
                        self.fail.draw(self.display)
                        if self.fail.isButtonClick():
                            self.player.choose = 5
            else:
                self.resetPlayersActivity(True)

        if self.gamePhase == 7 and self.isSignalSync():
            if self.missionSuccess == None:
                failCount = 0
                for player in self.playersData:
                    if (player.id in self.partyMember and
                        player.choose == 5):
                        failCount += 1
                if failCount > 0:
                    if playerNumber > 6 and self.roundCount == 4:
                        if failCount > 1:
                            self.missionSuccess = False
                        else:
                            self.missionSuccess = True
                    else:
                        self.missionSuccess = False
                elif failCount == 0:
                    self.missionSuccess = True

                self.resetPlayersActivity(False)
                self.changeLeader()
        
        if self.gamePhase == 8 and self.isSignalSync():

            if self.evilScore == 3:
                self.gameEnded = True
                self.drawText('Evil Win!!!', 50 , 500, 300)
                self.drawText('Enter to exit', 30 , 500, 700)
                self.revealAllPlayerRole()

                if self.player.host == True and self.matchSetting[2] == True:
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
                    print("aaa")
                    self.gameEnded = True
                    if killedPlayer.getRole().getName() == "Merlin":
                        self.drawText('Evil Win!!!', 50 , 500, 300)
                    else:
                        self.drawText('Good Win!!!', 50 , 500, 300)
                    self.drawText('Enter to exit', 30 , 500, 700)
                    self.revealAllPlayerRole()
                    
                    if self.player.host == True and self.matchSetting[2] == True:
                        self.network.stopThisGame()
    
    def checkCondition(self):
        checkPass = False
        # =============== PHASE 0 =============== #
        if self.gamePhase == 0:
            if self.player.getRole() != None: # check role
                checkPass = True
        
        # =============== PHASE 1 =============== #
        if self.gamePhase == 1:
            self.missionSuccess = None
            self.doMission = None
            if self.roundCount <= 5:
                if self.goodScore == 3 or self.evilScore == 3:
                    self.gamePhase = 8
                    self.player.syncSignal = 8
            checkPass = True
        
        # =============== PHASE 2 =============== #
        if self.gamePhase == 2:
            # is current leader are he same with others
            if (self.othersCurrentLeader.count(self.currentLeader)
                == len(self.othersCurrentLeader)):
                checkPass = True

        # =============== PHASE 3 =============== #
        if self.gamePhase == 3:
            for player in self.playersData:
                if (player.partyLeader == True and
                    player.choose == 3):
                    checkPass = True
                    break

        # =============== PHASE 4 =============== #
        if self.gamePhase == 4:
            isVote = 1
            for player in self.playersData:
                if player.choose not in [1, 2]:
                    isVote = 0
                    break
            if isVote == 1:
                checkPass = True
            else:
                checkPass = False
        
        # =============== PHASE 5 =============== #
        if self.gamePhase == 5:
            if self.doMission == True:
                self.doMission = None
                if self.voteRejected != 0:
                    self.voteRejected = 0
                checkPass = True
            elif self.doMission == False:
                self.voteRejected += 1
                if self.voteRejected == 5:
                    self.evilScore += 1
                    self.round.append(2)
                    self.roundCount += 1
                    self.voteRejected = 0
                self.gamePhase = 1
                self.player.syncSignal = 1
            else:
                checkPass = False
        
        # =============== PHASE 6 =============== #
        if self.gamePhase == 6:
            voteCount = 0
            for player in self.playersData:
                if( player.id in self.partyMember and
                    player.choose in [4, 5] and 
                    player.syncSignal >= 6):
                    voteCount += 1

            if voteCount == len(self.partyMember):
                checkPass = True
            else:
                checkPass = False
        
        # =============== PHASE 7 =============== #
        if self.gamePhase == 7 :
            if self.missionSuccess != None:
                if self.missionSuccess:
                    self.goodScore += 1
                    self.round.append(1)
                elif not self.missionSuccess:
                    self.evilScore += 1
                    self.round.append(2)
                self.roundCount += 1
                self.gamePhase = 1
                self.player.syncSignal = 1
            else:
                checkPass = False
        
        # =============== PHASE 8 =============== #
        if self.gamePhase == 8:
            checkPass = False
        
        return checkPass

    
    # Phase 0 : random role

    # Phase 1 : check score if their is a winner go to phase 8

    # Phase 2 : get party leader

    # Phase 3 : party leader select party member and summit

    # Phase 4 : each player vote accept or reject

    # Phase 5 : calculate vote and decide to go next phase or back to phase 1

    # Phase 6 : party member vote

    # Phase 7 : calculate score and go to phase 1 again

    # Phase 8 : conclusion
    
    def displayScreen(self):

        self.displayRunning = True
        # inintial
        self.player.updateByPosition(50, 700)
        self.player.isPlaying = True

        if self.player.host == True:
            randomRoles = self.randomRoles()
            self.currentLeader = random.choice(list(range(self.matchSetting[0])))
            self.setPartyLeader(self.currentLeader)
            self.setAllPlayersRole(randomRoles)

        while self.displayRunning:

            # if number of player in match not equal to the maximum player number allow
            if len(self.playersData) != self.matchSetting[0]:
                print("Some player are missing")
                if self.network.connectStatus == True:
                    self.resetAll()
                    self.network.stopThisGame()
                self.changePageByInput(True, self.control.lobby)

            if self.checkCondition():
                self.gamePhase += 1
                self.player.syncSignal = self.gamePhase

            self.checkEvent()

            sendData = [self.player.x,
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
                        [self.targetPlayer, self.isKilled]]
            if (self.player.host == True and 
                self.waitForOthers(1) == False):
                sendData += [randomRoles]
            
            # page blackground
            self.display.fill((0, 0, 0))

            # if self.waitForOthers():
            self.phaseEvent()

            #[TEST PRINT]
            print(self.currentLeader,self.gamePhase, self.player.syncSignal, self.player.choose, self.missionSuccess, self.goodScore, self.evilScore, self.partyMember)
            # print(self.currentLeader, self.gamePhase, self.player.syncSignal, self.player.choose,self.roundCount, self.round, self.goodScore, self.evilScore)
            # if self.player.host == True:
            #     print(sendData)
            # print(self.gamePhase)
            # for player in self.playersData:
            #     if player.partyLeader == True:
            #         print( player.id, player.choose)

            if self.network.connectStatus == True:
                self.sendAndReceiveData(sendData)
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