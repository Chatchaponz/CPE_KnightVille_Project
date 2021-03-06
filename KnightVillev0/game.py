import pygame, sys, threading
from button import Button 
from gameManager import GameManager
from popup import Popup

'''
game.py - Create and display in the game state
          Including game phases and displaying all game objects

[Class] + Game
        
last updated: 15 Nov 2021
'''
class Game(GameManager):
    
    def __init__(self, control):
        '''
        __init__ - Constructor of Game class.
       
       + control - gameControl variable
        '''
        super(Game, self).__init__(control)

        # Image
        self.popupBackground = control.popupBackground
        self.town = control.town
        self.townSky = control.townSky
        self.townSkyWidth = self.townSky.get_rect().width
        self.townSkyPositionX = 0
        self.sign = control.sign
        self.baseSkip = control.baseSkip
        self.baseSkip = pygame.transform.scale(self.baseSkip, (50, 50))
        self.skip = []
        for n in range(int(len(control.skip))):
            self.skip.append(pygame.transform.scale(control.skip[n], (50, 50)))
        self.missionShow = control.missionShow
        self.successMission = control.success
        self.failMission = control.fail

        self.buttonBG = self.control.buttonBG
        self.blackFilter = pygame.transform.scale(control.offFilter, (400,160))

        self.available = True

        # Button
        self.howToPlaySetup( 30, 20, 'How to play', [0,0,0,1,1,1,1,1,1,1,1])

        self.buttonReveal = Button(30, 100, 170, 60)
        self.buttonReveal.addText('Reveal role', self.font1, 30, control.white, (50,50,50))
        self.buttonReveal.addImage(self.buttonBG)

        # List for all button of name
        self.nameList = []

        self.submit = Button( self.screenWidth//2 - 50 , 145, 100, 30)
        self.submit.addText("Submit", self.font, 20, self.control.white, 1, (50,50,50))

        self.accept = Button( self.screenWidth//2 - 100 , 145, 100, 30)
        self.accept.addText("Accept", self.font, 20, self.control.white, 1, (50,50,50))

        self.reject = Button( self.screenWidth//2 , 145, 100, 30)
        self.reject.addText("Reject", self.font, 20, self.control.white, 1, (50,50,50))

        self.success = Button( self.screenWidth//2 - 100 , 145, 100, 30)
        self.success.addText("Success", self.font, 20, self.control.white, 1, (50,50,50))

        self.fail = Button( self.screenWidth//2 , 145, 100, 30)
        self.fail.addText("Fail", self.font, 20, self.control.white, 1, (50,50,50))

        # Render font
        signSize = 12
        signFont = pygame.font.Font(self.font, signSize)
        self.signText = signFont.render("select your team member", True, self.control.white)
        self.assassinText = signFont.render("kill the merlin", True, self.control.white)

        # Error popup
        self.popupFail = Popup((self.display.get_width() - 500)//2, (self.display.get_height() - 200)//2, 500, 200, 
        'Unknown Error', pygame.Color('white'), pygame.Color('cyan3'), type = 0)
        self.popupFail.adjustComponents(bWidth=70, fontPath = self.font1)
        self.popupFail.modComponents(self.popupFail.b1, 'button', (132, 85, 47), (100, 64, 44), 'Close', self.font1, 22)
        self.isError = False

        # Reveal Role
        self.buttonRevealStatus = False

        # Number of assignment in each round per maxplayer
        self.assignment = {
            5: [2, 3, 2, 3, 3],
            6: [2, 3, 4, 3, 4],
            7: [2, 3, 3, 4, 4],
            8: [3, 4, 4, 5, 5],
            9: [3, 4, 4, 5, 5],
            10: [3, 4, 4, 5, 5]
        }
    
    def checkEvent(self):
        '''
        <<overide>>
        checkEvent - method to check matchsetting,game status, and input from player
        '''
        for event in pygame.event.get():

            gameStart = True
            if len(self.matchSetting) > 2:
                gameStart = self.matchSetting[2]
            else:
                print("No matchsetting")

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and self.player.getRole() != None and not self.gameEnded:
                    self.player.revealRole(self.playersData)

                if event.key == pygame.K_RETURN and self.gameEnded and gameStart == False:
                    if self.network.connectStatus == True:
                        self.allowSendData = False
                        self.sendDataThread.join()
                        self.resetAll()
                    self.changePageByInput(True, self.control.lobby)
            
            self.handleChatBoxEvent(event)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_z and self.player.getRole() != None and not self.gameEnded:
                    self.player.unrevealRole(self.playersData)

            if (gameStart == True and 
                not self.chatText.active):
                self.player.playerMovement(event)
            else:
                self.player.resetMovement()
    
    def resetAll(self):
        '''
        resetAll - reaet all nessessary variables
        '''
        self.buttonRevealStatus = False
        self.available = True
        self.sendData = []
        self.gamePhase = 0
        self.targetPlayer = None
        self.isKilled = False
        self.currentLeader = None
        self.partyMember = []
        self.round = []
        self.voteText = None
        self.missionText = []
        self.roundCount = 0
        self.voteRejected = 0
        self.evilScore = 0
        self.goodScore = 0
        self.totalReject = 0
        self.totalEvil = 0
        self.gameEnded = False
        self.nameList = []
        self.othersGameStatus = []
        self.roleAvailable = False
        self.player.isPlaying = False 
        self.player.updateByPosition(50, 700)
        self.player.unrevealRole(self.playersData)
        for player in self.playersData:   
            player.setRole(None)
            player.choose = 0
            player.syncSignal = 0
            player.isSelected = False
            player.partyLeader = False
            player.isTarget = False
            player.isKilled = False
            player.setRoleReveal(False)

    def makeNameList(self):
        '''
        makeNameList - make a list of names for selection

        + return
            nameList - list of all player name buttons.
        '''
        initPositionY = 100
        nameList = []
        self.playersData.sort(key = lambda player: player.id, reverse = False)
        for player in self.playersData:
            tempButton = Button(1060, initPositionY, 170, 40)
            tempButton.addText(player.name, self.font, 20, self.control.white, 1, (50,50,50))
            tempButton.addImage(self.buttonBG)
            nameList.append(tempButton)
            initPositionY += 50
        return nameList

    def revealAllPlayerRole(self):
        '''
        revealAllPlayerRole - method for display all player roles
        '''
        player_x = 10
        self.buttonRevealStatus = False # Reset reveal role button status
        self.playersData.sort(key = lambda player: player.id, reverse = False)
        for player in self.playersData:
            player.updateByPosition(player_x, 700)
            player.setRoleReveal(True)
            player.setIdentityReveal(False)
            player.setUnknownReveal(False)
            player_x += 150
    
    def updateSelectedPlayer(self, partyMember):
        '''
        updateSelectedPlayer - update the status of players (party member)
        + partyMember - a list of selected players for Party
        '''
        for player in self.playersData:
            if player.id in partyMember:
                player.isSelected = True
            if player.id not in partyMember and player.isSelected:
                player.isSelected = False
    
    def updateTargetPlayer(self, id):
        '''
        updateTargetPlayer - update the status of players (assassin target)
        + id - id of the player that is targeted by assassin
        '''
        for player in self.playersData:
            if player.id == id:
                player.isTarget = True
            if id != player.id and player.isTarget:
                player.isTarget = False
    
    def killPlayer(self, killStatus = False):
        '''
        killPlayer - update player status when is killed by assassin
        + killStatus - the status of player if is killed or not

        + return
            player - the player object that is selected to be killed (return when the player is targeted)
            None - return when it not in the assassin phase and the assassin targeting others and not kill yet
        '''
        if killStatus:
            for player in self.playersData:
                if player.id == self.targetPlayer and player.isTarget:
                    player.isKilled = True
                    return player
        else:
            return None
    
    def revealAssassin(self):
        '''
        revealAssassin - reveal the assassin role player
        '''
        for player in self.playersData:
            if player.getRole() != None:
                if player.getRole().getName() == "Assassin":
                    player.setRoleReveal(True)
                    break
    
    def isOthersGameEnded(self):
        '''
        isOthersGameEnded - for checking if other players game ended

        + return
            status - return true when player game end
                     return false when player game does not end yet
        '''
        status = True
        for gameStatus in self.othersGameStatus:
            if gameStatus == False:
                status = False
                break
        return status

    # choose = 0 : no vote
    # choose = 1 : accept
    # choose = 2 : reject
    # choose = 3 : summit
    # choose = 4 : success
    # choose = 5 : fail
    
    def phaseEvent(self):
        '''
        phaseEvent - containing each phase's tasks and what should be done in each phase
        '''

        # Check match setting
        if len(self.matchSetting) > 2:
            playerNumber = self.matchSetting[0]
            gameStart = self.matchSetting[2]

        # Check current role (is this player already have a role?)
        if self.gamePhase == 0:
            if self.player.getRole() != None:
                self.roleAvailable = True
            else:
                self.roleAvailable = False

        # Reset party member list and party member selected sign 
        if self.gamePhase == 1:
            if self.partyMember != []:
                self.partyMember = []
            if self.player.isSelected == True:
                self.player.isSelected = False

        # List of name to select party member
        if self.gamePhase == 2:
            if self.player.partyLeader == True:
                pygame.draw.rect( self.display, (255, 255, 255), pygame.Rect(self.screenWidth-200, 0, 5,  50 + 50*len(self.nameList)) )
                pygame.draw.rect( self.display, (255, 255, 255), pygame.Rect(self.screenWidth-80, 0, 5,  50 + 50*len(self.nameList)) )
                self.display.blit( self.sign, (self.screenWidth-230, 20))
                self.display.blit( self.signText, (self.screenWidth-222, 40))
                memberLimit = self.assignment[playerNumber][self.roundCount]
                if self.nameList == []:
                    self.nameList = self.makeNameList()
                for id, name in enumerate(self.nameList):
                    name.draw(self.display, self.available)
                    if name.isButtonClick(self.soundList[10],self.control.getSoundEffectVol()) and self.available:
                        if id in self.partyMember:
                            self.partyMember.remove(id)
                            name.textColor = (255, 255, 255)
                        elif (id not in self.partyMember and
                            len(self.partyMember) < memberLimit):
                            self.partyMember.append(id)
                            name.textColor = (0, 255, 0)
                        else:
                            print("[GAME] Cannot assign party member")
                self.updateSelectedPlayer(self.partyMember)
                if len(self.partyMember) == memberLimit:
                    self.submit.draw(self.display, self.available)
                    if self.submit.isButtonClick(self.soundList[11],self.control.getSoundEffectVol()) and self.available:
                        self.player.choose = 3
                        if self.nameList != []: # Reset name's color
                            for name in self.nameList:
                                name.textColor = (255, 255, 255)
            else:
                self.updateSelectedPlayer(self.partyMember)
        
        # Button for select accept or reject
        if self.gamePhase == 3:
            if self.player.choose not in [1, 2]:
                self.accept.draw(self.display, self.available)
                self.reject.draw(self.display, self.available)
                if self.accept.isButtonClick(self.soundList[11],self.control.getSoundEffectVol()) and self.available:
                    self.player.choose = 1
                if self.reject.isButtonClick(self.soundList[11],self.control.getSoundEffectVol()) and self.available:
                    self.player.choose = 2
        
        # Reset player choice
        if self.gamePhase == 5:
            if self.player.choose != 0:
                self.player.choose = 0
        
        # Select success or fail (if you are evil)
        if self.gamePhase == 6:
            if self.player.id in self.partyMember:
                if self.player.choose not in [4, 5]:
                    self.success.draw(self.display, self.available)
                    if self.success.isButtonClick(self.soundList[10],self.control.getSoundEffectVol()) and self.available:
                        self.player.choose = 4
                    if self.player.getRole().getIdentity() == "Evil":
                        self.fail.draw(self.display, self.available)
                        if self.fail.isButtonClick(self.soundList[10],self.control.getSoundEffectVol()) and self.available:
                            self.player.choose = 5
        
        # Reset player choice
        if self.gamePhase == 8:
            if self.player.choose != 0:
                self.player.choose = 0
        
        # End game phase Evil win or Assassin select to kill and/or Good win 
        if self.gamePhase == 9:

            if self.player.partyLeader == True:
                self.player.partyLeader = False
            if self.player.isSelected == True:
                self.player.isSelected = False
                
            if self.evilScore == 3:
                self.gameEnded = True
                self.drawText('Evil Win!!!', 50 ,self.screenWidth//2, self.screenHeight//2 - 100, self.font, self.control.white)
                self.drawText('Enter to exit', 30 , ((self.screenWidth//5) * 4) + 100 , 690, self.font, self.control.white)
                self.revealAllPlayerRole()

                if (self.player.host == True and 
                    gameStart == True and
                    self.isOthersGameEnded()):
                    self.network.stopThisGame()
            
            if self.goodScore == 3:
                killedPlayer = None
                if self.player.getRole() != None:
                    if self.player.getRole().getName() == "Assassin" and not self.gameEnded:
                        self.player.setRoleReveal(True)
                        pygame.draw.rect( self.display, (255, 255, 255), pygame.Rect(self.screenWidth-200, 0, 5,  50 + 50*len(self.nameList)) )
                        pygame.draw.rect( self.display, (255, 255, 255), pygame.Rect(self.screenWidth-80, 0, 5,  50 + 50*len(self.nameList)) )
                        self.display.blit( self.sign, (self.screenWidth-230, 20))
                        self.display.blit( self.assassinText, (self.screenWidth-182, 40))
                        if self.nameList == []:
                            self.nameList = self.makeNameList()
                        for id, name in enumerate(self.nameList):
                            name.draw(self.display, self.available)
                            if name.isButtonClick(self.soundList[10],self.control.getSoundEffectVol()) and self.available:
                                self.targetPlayer = id
                            if id == self.targetPlayer:
                                name.textColor = (255, 0, 0)
                            else:
                                name.textColor = (255, 255, 255)
                            self.updateTargetPlayer(self.targetPlayer)
                        if self.targetPlayer != None:
                            self.submit.draw(self.display, self.available)
                            if self.submit.isButtonClick(self.soundList[11],self.control.getSoundEffectVol()) and self.available:
                                self.isKilled = True
                                killedPlayer = self.killPlayer(self.isKilled)
                    else:
                        self.revealAssassin()
                        self.updateTargetPlayer(self.targetPlayer)
                        killedPlayer = self.killPlayer(self.isKilled)
                    
                if killedPlayer != None:
                    self.gameEnded = True
                    if killedPlayer.getRole() != None and killedPlayer.getRole().getName() == "Merlin":
                        self.drawText('Evil Win!!!', 50 , self.screenWidth//2, self.screenHeight//2 - 100, self.font, self.control.white)
                    else:
                        self.drawText('Good Win!!!', 50 , self.screenWidth//2, self.screenHeight//2 - 100, self.font, self.control.white)
                    self.drawText('Enter to exit', 30 , ((self.screenWidth//5) * 4) + 100 , 690, self.font, self.control.white)
                    self.revealAllPlayerRole()
                    
                    if (self.player.host == True and 
                        gameStart == True and
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
        '''
        displayScreen - display all required objects in the game phase
        '''
        # inintial
        self.displayRunning = True

        self.player.updateByPosition(50, 700)
        self.player.isPlaying = True
        self.isError = False

        self.allowSendData = True
        self.sendDataThread = threading.Thread(target= self.doSendAndReceiveData)
        self.sendDataThread.daemon = True
        self.sendDataThread.start()

        checkHowToPlay = False
        checkHowToPlayPrevious = False

        self.buttonRevealStatus = False
        self.player.unrevealRole(self.playersData)
        
        # Set collision
        self.player.collided = []
        if self.player.collided == []:
            self.player.collided = [[0, self.screenWidth], [600, self.screenHeight + 20]]

        while self.displayRunning:

            # if number of player in match not equal to the maximum player number allow
            if len(self.matchSetting) > 0 and len(self.playersData) != self.matchSetting[0]:
                self.isError = True
                self.popupFail.text = "Some player are missing"
            
            # if network connection issue occur
            if self.network.connectStatus == False:
                self.isError = True
                self.popupFail.text = "Connection lost!"

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
                            self.voteRejected,
                            self.totalReject,
                            self.totalEvil]
            
            # page blackground
            self.display.fill((0, 0, 0))
            self.display.blit(self.townSky, (self.townSkyPositionX,0))
            
            self.townSkyPositionX -= 1
            if self.townSkyPositionX < -(self.townSkyWidth - 1280):
               self.display.blit(self.townSky, (self.townSkyPositionX + self.townSkyWidth,0))
            if self.townSkyPositionX < -self.townSkyWidth:
                self.townSkyPositionX = 0

            self.display.blit(self.town, (0,0))
            self.display.blit(self.blackFilter, (self.screenWidth//2 - 200,0))
            self.display.blit(self.baseSkip, (self.screenWidth//2 - 120, 95))

            # draw mission board
            for i in range(5):
                
                if self.matchSetting[0] >= 7 and i >= 3:
                    self.display.blit(self.missionShow[self.assignment[self.matchSetting[0]][i] + 1], (self.screenWidth//2 - 150 + (i*60), 10))
                else:
                    self.display.blit(self.missionShow[self.assignment[self.matchSetting[0]][i] - 1], (self.screenWidth//2 - 150 + (i*60), 10))

            # reveal button
            self.buttonReveal.draw(self.display, self.available)
            if self.available and self.player.getRole() != None and self.playersData != []:
                if self.buttonReveal.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()):
                    if not self.buttonRevealStatus:
                        self.buttonRevealStatus = True
                    elif self.buttonRevealStatus:
                        self.buttonRevealStatus = False
                        self.player.unrevealRole(self.playersData)
                    else:
                        print("[GAME] Reveal button problem")

            if self.buttonRevealStatus and self.playersData != []:
                self.player.revealRole(self.playersData)

            if self.network.connectStatus == True:
                self.updateScreenData()

            self.drawPlayers()

            if (len(self.matchSetting) > 0 and 
                len(self.playersData) == self.matchSetting[0] and
                self.network.connectStatus == True):
                    self.phaseEvent()

            self.drawChatBox(self.display)
            
            # TEMP
            # draw icon success / fail
            x = 0
            for i in self.round:
                if i == 1:
                    #pygame.draw.rect(self.display, (0,0,255), pygame.Rect(x, 0, 30, 30) )
                    self.display.blit(self.successMission, (self.screenWidth//2 - 150 + (x*60), 10))
                    pygame.draw.circle(self.display, (0,255,0), (self.screenWidth//2 - 125 + (x*60), 75), 10)
                if i == 2:
                    #pygame.draw.rect(self.display, (255,0,0), pygame.Rect(x, 0, 30, 30) )
                    self.display.blit(self.failMission, (self.screenWidth//2 - 150 + (x*60), 10))
                    pygame.draw.circle(self.display, (255,0,0), (self.screenWidth//2 - 125 + (x*60), 75), 10)
                x += 1

            # draw amount of success / fail
            x = 0
            for textSurface in self.missionText:
                rect = textSurface.get_rect()
                rect.center = pygame.Rect(self.screenWidth//2 - 140 + (x*60), 60, 30, 30).center
                self.display.blit( textSurface, rect)
                x += 1

            # draw reject round 
            x = 0
            for i in range(self.voteRejected):
                #pygame.draw.rect(self.display, (255,0,255), pygame.Rect(x, 35, 30, 30) )
                self.display.blit(self.skip[x], (self.screenWidth//2 - 120, 95))
                x += 1

            # draw vote text
            if self.voteText != None:
                self.display.blit( self.voteText, pygame.Rect( self.screenWidth//2 - 25, 95, 30, 30))
            
            # draw how to play button
            checkHowToPlayPrevious = checkHowToPlay
            checkHowToPlay = self.howToPlayDraw(self.available)
            if checkHowToPlay == False and checkHowToPlayPrevious == True:
                self.available = True
            elif checkHowToPlay == True and checkHowToPlayPrevious == False:
                self.available = False

            if self.isError:

                self.popupFail.draw(self.display, self.font1, 30, textAlign= 'centerAlign',  bgColor = None, 
                image = self.popupBackground)
                self.available = False

                if self.popupFail.b1.isButtonClick(self.backButtonSound,self.control.getSoundEffectVol()):
                    
                    self.isError = False

                    # join thread
                    self.allowSendData = False
                    self.sendDataThread.join()
                    
                    if self.network.connectStatus == False:
                        self.resetAll()
                        self.player.setAttribute()
                        self.player.host = False
                        self.player.id = None
                        self.othersPlayerInMatch.clear()
                        self.playersData.clear()
                        self.matchSetting.clear()
                        self.allMessages.clear()
                        self.currentPlayerInMatch.clear()
                        self.othersPlayerData.clear()

                        # Main music is loaded here
                        self.currentMusic.stop()
                        self.currentMusic.load(self.musicList[0])
                        self.currentMusic.play(-1)

                        self.changePageByInput(True, self.control.menu)

                    elif self.network.connectStatus == True:
                        self.resetAll()
                        if self.player.host == True:
                            self.network.stopThisGame()
                        self.changePageByInput(True, self.control.lobby)
                    else:
                        self.isError = False
                        self.available = True

            self.blitScreen() # update screen
            self.clock.tick(60) # run at 60 fps