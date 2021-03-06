import pygame, sys, threading
from button import Button 
from gameManager import GameManager
from textbox import Textbox
from popup import Popup

'''
lobby.py - page to display the lobby.

[Class] + Lobby

last updated: 22 Nov 2021
'''
class Lobby(GameManager):
    '''
    Lobby - Page uses to display the lobby.
    '''
    def __init__(self, control):
        '''
        __init__ - Constructor of lobby page.
        + control - gameControl variable.
        '''
        super(Lobby, self).__init__(control)

        # Music
        self.currentMusic = control.currentMusic
        self.musicList = control.musicList

        # Sound Effect state
        self.lockSoundOn = False
        self.alreadyPlay = False
        
        # Components image
        self.lobbyWall = control.lobbyWall
        self.lobbyFloor = control.lobbyFloor
        self.startShadow = control.startShadow
        self.startLight = control.startLight
        self.startShadowWidth = self.startShadow.get_rect().width
        self.startShadowHeight = self.startShadow.get_rect().height
        self.leaveShadow = control.leaveShadow
        self.leaveLight = control.leaveLight
        self.knightStand = control.knightStand
        self.knightStandAura = control.knightStandAura
        self.map = control.map
        self.mapWidth = self.map.get_rect().width
        self.mapAura = control.mapAura
        self.mapAuraWidth = self.mapAura.get_rect().width
        self.lobbyTable = control.lobbyTable
        self.lobbyTableWidth = self.lobbyTable.get_rect().width
        self.popupBackground = control.popupBackground
        
        # How to play Popup
        self.howToPlaySetup(self.screenWidth - 200, 20, 'How to play')

        # Button
        self.buttonLeave = Button(22, 259, self.startShadowWidth, self.startShadowHeight)
        self.buttonLeave.addImage(self.leaveShadow, self.leaveLight)

        self.buttonStart = Button(self.screenWidth - self.startShadowWidth - 22, 259, self.startShadowWidth, self.startShadowHeight)
        self.buttonStart.addImage(self.startShadow, self.startLight)

        # Edit player
        self.buttonEditPlayer = Button(820, 220, 156, 333)
        self.buttonEditPlayer.addImage(self.knightStand, self.knightStandAura)
        self.popEdit = False

        # Match Setting
        self.buttonMatchSetting = Button((self.screenWidth//2)-(self.mapWidth//2), 215, self.mapWidth, self.map.get_rect().height)
        self.buttonMatchSetting.addImage(self.map, self.mapAura)
        self.popSetting = False


        # Setup Edit player
        self.popEditBg = control.dressingCab.get_rect()
        self.popEditBg.x, self.popEditBg.y = self.screenWidth/2 - self.popEditBg.centerx, self.screenHeight/2 - self.popEditBg.centery
        self.popEditSummit = Button(self.popEditBg.centerx - 50, self.popEditBg.y + 515, 100, 50)
        self.popEditSummit.addText('Submit', self.font2, 20, (255, 255, 255), bgColor = (144, 109, 99), bgColorOver = (120, 90, 82))
        
        self.buttonLeft = Button(self.screenWidth//2 - self.control.leftArrow.get_width() - 80, 360, 
        self.control.leftArrow.get_width(), self.control.leftArrow.get_height())
        self.buttonLeft.addImage(self.control.leftArrow)

        self.buttonRight = Button(self.screenWidth//2 + 80, 360, self.control.rightArrow.get_width(), 
        self.control.rightArrow.get_height())
        self.buttonRight.addImage(self.control.rightArrow)

        # Text Map Button
        self.topicMap = pygame.font.Font(self.font1, 30).render('Match Setting', True, self.control.black)
        self.topicMapRect = self.topicMap.get_rect()
        # Text Edit player Button
        self.topicKnight = pygame.font.Font(self.font1, 30).render('Edit Player', True, self.control.black)
        self.topicKnightRect = self.topicKnight.get_rect()

        # Player Information
        self.currentSkin = None # Current skin.
        self.currentName = None # Current name.
        self.skins = self.control.skins # list of skins.
        self.amountSkins = len(self.skins) # skins number.
        
        # Textbox to get Player's new name.
        self.newPlayername = Textbox(self.popEditBg.centerx - 110, self.popEditBg.y + 70, 220, 30, pygame.Color('white'), 
        pygame.Color('white'), 15, fontPath = self.font, size = 20)

        # Popup Error for textbox newPlayername.
        self.popupNoIGN = Popup(self.screenWidth//2 - 250, self.screenHeight//2 - 90, 500, 180, 
        'Please enter your/> In-game name with no spacebar', pygame.Color('white'), pygame.Color('darkblue'))
        self.popupNoIGN.modComponents(self.popupNoIGN.b1, 'button', pygame.Color('darkseagreen4'), pygame.Color('darkslategray'), 
        'Understand', self.font2)

        # Popup Error of lobby.
        self.popupFail = Popup((self.display.get_width() - 500)//2, (self.display.get_height() - 200)//2, 500, 200, 
        'Unknown Error', pygame.Color('white'), pygame.Color('cyan3'), type = 0)
        self.popupFail.adjustComponents(bWidth = 70, fontPath = self.font1)
        self.popupFail.modComponents(self.popupFail.b1, 'button', (132, 85, 47), (100, 64, 44), 'Close', self.font1, 22)
        self.isError = False

        # Setup match setting
        roleWidth, roleHeight = 80, 80
        self.closeSetting = Button(self.screenWidth - 370, self.screenHeight - 168 - 40, 100, 35)
        self.closeSetting.addText('SAVE', self.font2, 30, bgColor = pygame.Color('grey35'), bgColorOver = pygame.Color('grey27'))

        # Special role image/button
        self.buttonRole1 = Button(self.screenWidth//2 + 40, 265, roleWidth, roleHeight)
        self.buttonRole1.addImage(self.control.oberon)

        self.buttonRole2 = Button(self.buttonRole1.rect.right + 40, self.buttonRole1.rect.y, roleWidth, roleHeight)
        self.buttonRole2.addImage(self.control.mordred)

        self.buttonRole3 = Button((self.buttonRole1.rect.x + self.buttonRole2.rect.x)/2, self.buttonRole1.rect.bottom + 70, 
        roleWidth, roleHeight)
        self.buttonRole3.addImage(self.control.morganaPercival)

        # Standard role image
        self.minion = pygame.transform.scale(self.control.minion, (roleWidth, roleHeight))
        self.minionRect = pygame.Rect(self.screenWidth//2 - ((self.buttonRole1.rect.width) + 40), 
        self.buttonRole3.rect.y, roleWidth, roleHeight)

        self.assasin = pygame.transform.scale(self.control.assasin, (roleWidth, roleHeight))
        self.assasinRect = pygame.Rect(self.screenWidth//2 - ((self.buttonRole1.rect.width * 2) + 80), 
        self.buttonRole3.rect.y, roleWidth, roleHeight)

        self.servant = pygame.transform.scale(self.control.servant, (roleWidth, roleHeight))
        self.servantRect = pygame.Rect(self.screenWidth//2 - ((self.buttonRole1.rect.width) + 40), 
        self.buttonRole1.rect.y, roleWidth, roleHeight)

        self.merlin = pygame.transform.scale(self.control.merlin, (roleWidth, roleHeight))
        self.merlinRect = pygame.Rect(self.screenWidth//2 - ((self.buttonRole1.rect.width * 2) + 80), 
        self.buttonRole1.rect.y, roleWidth, roleHeight)

        # Decoration Layer
        self.offFilter = pygame.transform.scale(self.control.offFilter, (roleWidth, roleHeight))
        
        self.lock = pygame.transform.scale(self.control.lock, (int(roleWidth*3/4), roleHeight))

        self.roleFrame = pygame.transform.scale(self.control.roleFrame, (roleWidth + 15, roleHeight + 15))
        
        self.checked = pygame.transform.scale(self.control.checked, (roleWidth - 45, roleHeight - 45))

        self.role = [False, False, False, True, False]
        self.setRoleFirstTime = False

        self.count = 0 

        # Popup state
        self.available = True
        self.triggerNoIGN = False
    
    def configRole(self, maxrole, specialRoleList, standardRoleList):
        '''
        configRole - method to config role.
        + maxrole - max number of role can be selects.
        + specialRoleList - List of special role button object.
        + standardRoleList - List of standard role surface.
        '''
        # Draw role selector button
        for spRole, name in specialRoleList:
            self.display.blit(self.roleFrame, (spRole.rect.centerx - self.roleFrame.get_width()//2, 
            spRole.rect.centery - self.roleFrame.get_height()//2))
            spRole.draw(self.display)
            self.drawText(name, 18 , spRole.rect.centerx, spRole.rect.bottom + 15, self.font2, self.control.black)
        for role, rect, name in standardRoleList:
            self.display.blit(self.roleFrame, (rect.centerx - self.roleFrame.get_width()//2, 
            rect.centery - self.roleFrame.get_height()//2))
            self.display.blit(role, rect)  
            if not rect is self.minionRect:
                self.display.blit(self.checked, (rect.right - self.checked.get_width()//2, 
                rect.top - self.checked.get_height()//2))
            elif rect is self.minionRect:
                if self.role[3]:
                    self.display.blit(self.checked, (rect.right - self.checked.get_width()//2, 
                    rect.top - self.checked.get_height()//2))
            self.drawText(name, 18 , rect.centerx, rect.bottom + 15, self.font2, self.control.black)

        # Role Oberon
        if self.buttonRole1.isButtonClick():
            # Check Role Number can be available
            if not self.role[4] and self.count < maxrole:
                self.count += 1
                self.role[4] = True
            elif self.role[4]:
                self.count -= 1
                self.role[4] = False
        # Display role available
        if self.role[4]:
            self.display.blit(self.checked, (self.buttonRole1.rect.right - self.checked.get_width()//2, 
            self.buttonRole1.rect.top - self.checked.get_height()//2))
        
        # Role Mordred
        if self.buttonRole2.isButtonClick():
            # Check Role Number can be available
            if not self.role[1] and self.count < maxrole:
                self.count += 1
                self.role[1] = True
            elif self.role[1]:
                self.count -= 1
                self.role[1] = False
        # Display role available
        if self.role[1]:
            self.display.blit(self.checked, (self.buttonRole2.rect.right - self.checked.get_width()//2, 
            self.buttonRole2.rect.top - self.checked.get_height()//2))

        # Role Morgana and Percival
        if self.buttonRole3.isButtonClick():
            # Check Role Number can be available
            if not self.role[2] and self.count < maxrole:
                self.count += 1
                self.role[2] = True
                self.role[0] = True
            elif self.role[2] and self.role[0]:
                self.count -= 1
                self.role[2] = False
                self.role[0] = False
        # Display role available
        if self.role[2] and self.role[0]:
            self.display.blit(self.checked, (self.buttonRole3.rect.right - self.checked.get_width()//2, 
            self.buttonRole3.rect.top - self.checked.get_height()//2))

        # Display not available role
        if self.count == maxrole:
            self.role[3] = False
            if not self.role[4]:
                self.display.blit(self.offFilter, self.buttonRole1.rect)
                self.display.blit(self.lock, (self.buttonRole1.rect.centerx - self.lock.get_width()//2, self.buttonRole1.rect.y))
                self.lockSoundOn = True            
            if not self.role[1]:
                self.display.blit(self.offFilter, self.buttonRole2.rect)
                self.display.blit(self.lock, (self.buttonRole2.rect.centerx - self.lock.get_width()//2, self.buttonRole2.rect.y))
                self.lockSoundOn = True
            if not self.role[2] and not self.role[0]:
                self.display.blit(self.offFilter, self.buttonRole3.rect)
                self.display.blit(self.lock, (self.buttonRole3.rect.centerx - self.lock.get_width()//2, self.buttonRole3.rect.y))
                self.lockSoundOn = True
            if not self.role[3]:
                self.display.blit(self.offFilter, self.minionRect)
                self.display.blit(self.lock, (self.minionRect.centerx - self.lock.get_width()//2, self.minionRect.y))
                self.lockSoundOn = True
        elif self.count < maxrole:
            self.role[3] = True
            self.lockSoundOn = False
            self.alreadyPlay = False

        if self.lockSoundOn == True and self.alreadyPlay == False:
            self.control.playSoundWithVol(self.soundList[6],self.control.getSoundEffectVol())
            self.alreadyPlay = True

    def editMatch(self, maxPlayer, roleList):
        '''
        editMatch - method to edit match setting.
        + maxPlayer - max number of player can be in the match.
        + roleList - List of role.
        '''
        self.available = False
        # Popup background.
        self.display.blit(self.control.boardSetting, ((self.screenWidth - 800)/2, (self.screenHeight - 450)/2))
        self.drawText('MATCH  SETTING', 40, self.screenWidth/2, (self.screenHeight - 450)/2 + 55, self.font2, self.control.black)
        # Popup button.
        self.closeSetting.draw(self.display)
        
        # Setting match due to the max number player.
        if maxPlayer <= 6:
            self.configRole(1, roleList[0], roleList[1])
        if maxPlayer > 6 and maxPlayer < 10:
            self.configRole(2, roleList[0], roleList[1])
        if maxPlayer > 9:
            self.configRole(3, roleList[0], roleList[1])
        if self.closeSetting.isButtonClick():
            roleList = [True, self.role[0], True, self.role[1], True, self.role[2], self.role[3], self.role[4]]
            settingResult, settingError = self.network.changeMatchSetting(maxPlayer, [roleList, 0, 0])
            if settingResult:
                self.popSetting = False
                self.available = True
            else:
                self.available = False
        
    
    def editPlayer(self):
        '''
        editPlayer - method to edit player data.
        '''
        self.available = False
        # Popup background
        self.display.blit(self.control.dressingCab, (self.popEditBg.x, self.popEditBg.y))
        
        # Skin.
        self.display.blit(self.skins[self.currentSkin], (self.popEditBg.centerx - self.skins[self.currentSkin].get_width()/2, 
        self.popEditBg.bottom - self.skins[self.currentSkin].get_rect().bottom - 125))

        self.currentName = self.newPlayername.getText()
        self.drawText(self.currentName, 20, self.popEditBg.centerx , self.popEditBg.y + 210, self.font, self.control.white)

        self.newPlayername.draw(self.display)

        # Previous skin in list of skin.
        self.buttonLeft.draw(self.display)
        if self.buttonLeft.isButtonClick(self.soundList[4],self.control.getSoundEffectVol()):
            if self.currentSkin == 0:
                self.currentSkin = self.amountSkins-1
            else:
                self.currentSkin -= 1

        # Next skin in list of skin.
        self.buttonRight.draw(self.display)
        if self.buttonRight.isButtonClick(self.soundList[4],self.control.getSoundEffectVol()):
            if self.currentSkin == self.amountSkins-1:
                self.currentSkin = 0
            else:
                self.currentSkin += 1

        self.popEditSummit.draw(self.display)
        if self.popEditSummit.isButtonClick(self.clickChoiceSound,self.control.getSoundEffectVol()):
            if len(self.currentName) > 1:
                if self.currentName[-1] == ' ':
                    self.currentName = self.currentName[:-1]
            if self.currentName and not ' ' in self.currentName:
                self.player.updateSkin(self.currentSkin)
                self.player.updateName(self.currentName)
                self.currentName = None
                self.currentSkin = None
                self.available = True
                self.popEdit = False
            else:
                self.triggerNoIGN = True
        if self.triggerNoIGN:
            self.popupNoIGN.draw(self.display, self.font2, size = 28, textAlign = 'centerAlign', image = self.control.popupBackground)
            if self.popupNoIGN.b1.isButtonClick():
                self.triggerNoIGN = False
    
    def resetLobby(self, leaveToMain = False):
        '''
        resetLobby - method to reset data in the lobby.
        + leaveToMain - is the player leave the lobby to main menu state.
        '''
        # join thread
        self.allowSendData = False
        self.sendDataThread.join()

        self.currentName = None
        self.currentSkin = None
        self.isError = False
        self.popEdit = False
        self.popSetting = False
        self.available = True

        if leaveToMain:
            if self.network.connectStatus == True:
                self.network.disconnectFromServer()
            self.player.setAttribute() # reset current player
            self.player.host = False
            self.player.id = None
            self.sendData = []
            self.othersPlayerInMatch.clear()
            self.playersData.clear()
            self.matchSetting.clear()
            self.allMessages.clear()
            self.currentPlayerInMatch.clear()
            self.othersPlayerData.clear()

            self.role = [False, False, False, True, False]
            self.setRoleFirstTime = False
            self.count = 0

            # Main music is loaded here
            self.currentMusic.stop()
            self.currentMusic.load(self.musicList[0])
            self.currentMusic.play(-1)

            self.changePageByInput(True, self.control.menu)

    def isAllPlayerReady(self):
        '''
        isAllPlayerReady - method to check whether player is in ready state to start the match.
        '''
        ready = True
        for player in self.playersData:
            if player.isPlaying == True:
                ready = False
                break
        return ready

    def checkEvent(self):
        '''
        <<overide>>
        checkEvent - method to check event and input to textbox class.
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.newPlayername.handleEvent(event)

            doMovement = True
            if self.chatText.active or self.popEdit: 
                doMovement = False
            else: 
                doMovement = True

            if doMovement:
                self.player.playerMovement(event)
            else:
                self.player.resetMovement()

            self.handleChatBoxEvent(event, self.available)

    def displayScreen(self):
        '''
        displayScreen - method to display the screen page.
        '''
        self.displayRunning = True

        self.player.isPlaying = False
        roleList = [[[self.buttonRole1, 'Oberon'], [self.buttonRole2, 'Mordred'], [self.buttonRole3, 'Morgana and Percival']],
        [[self.merlin, self.merlinRect, 'Merlin'], [self.servant, self.servantRect, 'Royal Servant'], [self.assasin, 
        self.assasinRect, 'Assasin'], [self.minion, self.minionRect, 'Minion of Mordred']]]
        checkHowToPlay = False
        checkHowToPlayPrevious = False

        if(self.player not in self.playersData):
            self.playersData.append(self.player)

        # Stop Main music and start BGM
        self.currentMusic.stop()
        self.currentMusic.load(self.musicList[1])
        self.currentMusic.play(loops=-1,fade_ms = 1000)

        self.allowSendData = True
        self.sendDataThread = threading.Thread(target= self.doSendAndReceiveData)
        self.sendDataThread.daemon = True
        self.sendDataThread.start()

        # All buttons
        buttonList = [self.buttonEditPlayer, self.buttonMatchSetting, self.buttonStart, self.buttonLeave]

        # Set collision
        self.player.collided = []
        if self.player.collided == []:
            self.player.collided = [[0, self.screenWidth], [580, self.screenHeight + 20]]
        

        while self.displayRunning:

            self.checkEvent()

            self.sendData = [self.player.x,
                            self.player.y,
                            self.player.skin,
                            self.player.name,
                            self.player.isPlaying]
            
            # Page blackground
            self.display.fill((0, 0, 0))
            self.display.blit(self.lobbyFloor, (0,0))
            self.display.blit(self.lobbyWall, (0,0))

            # Draw all button
            for roomButton in buttonList:
                roomButton.draw(self.display, self.available)
            
            self.display.blit(self.lobbyTable, ((self.screenWidth//2) - (self.lobbyTableWidth//2), 385))

            if self.network.connectStatus == True:
                self.updateScreenData()
            self.drawPlayers()
            
            self.drawChatBox(self.display)

            # If network connection issue occur
            if self.network.connectStatus == False:
                self.isError = True
                self.available = False
                self.popupFail.text = "CONNECTION LOST!"

            if self.available:

                if self.buttonLeave.isButtonClick():
                    self.resetLobby(leaveToMain = True)

                # Display the shadow text on top of the button edit match and player
                for i in range(5):
                    self.display.blit(self.topicKnight, ((self.buttonEditPlayer.rect.centerx + 2 + i) - 
                    self.topicKnightRect.centerx, self.buttonEditPlayer.rect.y - 33 + i))
                    self.display.blit(self.topicMap, ((self.buttonMatchSetting.rect.centerx + 2 + i) - 
                    self.topicMapRect.centerx, self.buttonMatchSetting.rect.y - 63 + i))
            
                # Display the text on top of the button edit match and player
                self.drawText('Edit Player', 30, self.buttonEditPlayer.rect.centerx, self.buttonEditPlayer.rect.y - 15, 
                self.font1, self.control.white)
                self.drawText('Match Setting', 30, self.buttonMatchSetting.rect.centerx, self.buttonMatchSetting.rect.y - 45, 
                self.font1, self.control.white)
            
                if self.buttonStart.isButtonClick():
                    if self.player.host == True:
                        self.isError = False
                        if (self.network.connectStatus == True and
                            len(self.matchSetting) > 0):
                            currentPlayer = len(self.playersData)
                            maxPlayer = self.matchSetting[0] 
                            if currentPlayer == maxPlayer:
                                if self.isAllPlayerReady():
                                    self.resetLobby(leaveToMain = False)
                                    self.network.startGame()
                                    self.changePageByInput(True, self.control.game)
                                else:
                                    self.isError = True
                                    failText = f"Some player currently in match"
                                    self.popupFail.text = failText.upper()
                                    print("[Error] Cannot start match : ", failText)
                            else:
                                self.isError = True
                                failText = f"Not enough players {currentPlayer}/{maxPlayer}"
                                self.popupFail.text = failText.upper()
                                print("[Error] Cannot start match : ", failText)
                    else:
                        self.isError = True
                        failText = "You are not the host"
                        self.popupFail.text = failText.upper()
                        print("[Error] ", failText)
                
                if self.buttonEditPlayer.isButtonClick(self.soundList[9],self.control.getSoundEffectVol()):
                    self.popEdit = True
                    if self.currentName == None and self.currentSkin == None:
                        self.currentSkin = self.player.skin
                        self.currentName = self.player.name
                    self.newPlayername.text = self.currentName
                
                if self.buttonMatchSetting.isButtonClick(self.soundList[7],self.control.getSoundEffectVol()):
                    if self.player.host == True:
                        if len(self.matchSetting) > 1 and self.setRoleFirstTime == False:
                            setting = self.matchSetting[1]
                            if type(setting) is list and len(setting) > 0:
                                if type(setting[0]) is list and len(setting[0]) == 8:
                                    role = setting[0]
                                    self.role = [role[1], role[3], role[5], role[6], role[7]]
                                    for i in range(5):
                                        if self.role[i] == True and i in [1, 2, 4]:
                                            self.count += 1
                        self.setRoleFirstTime = True
                        self.popSetting = True
                    else:
                        self.isError = True
                        failText = "You are not the host"
                        self.popupFail.text = failText.upper()
                        print("[Error] ", failText)

            if len(self.matchSetting) > 2:
                gameStart = self.matchSetting[2]
                maxPlayer = self.matchSetting[0]

                # Popup edit player
                if self.popEdit == True and not gameStart:
                    self.editPlayer()
                
                if self.popSetting and not gameStart:
                    self.editMatch(maxPlayer, roleList)

                if(self.player.host != True and gameStart == True and 
                   maxPlayer == len(self.playersData)):
                    self.resetLobby(leaveToMain = False)
                    self.changePageByInput(True, self.control.game)

            if self.isError:
                self.popupFail.draw(self.display, self.font2, 30, textAlign= 'centerAlign',  bgColor = None, 
                image = self.popupBackground)
                self.available = False
                if self.popupFail.b1.isButtonClick(self.backButtonSound,self.control.getSoundEffectVol()):
                    if self.network.connectStatus == False:
                        self.resetLobby(leaveToMain=True)
                    else:
                        self.isError = False
                        self.available = True
                    
            checkHowToPlayPrevious = checkHowToPlay
            checkHowToPlay = self.howToPlayDraw(self.available)

            if checkHowToPlay == False and checkHowToPlayPrevious == True:
                self.available = True
            elif checkHowToPlay == True and checkHowToPlayPrevious == False:
                self.available = False

            self.blitScreen() # update screen
            self.clock.tick(60) # run at 60 fps