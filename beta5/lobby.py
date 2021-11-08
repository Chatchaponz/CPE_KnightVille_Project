import pygame, sys, threading
from button import Button 
from gameManager import GameManager
from textbox import Textbox
from popup import Popup

class Lobby(GameManager):
    
    def __init__(self, control):
        super(Lobby, self).__init__(control)

        # Music
        self.currentMusic = control.currentMusic
        self.musicList = control.musicList
        
        # Image / Button goes here vvvv
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

        self.buttonLeave = Button(22, 259, self.startShadowWidth, self.startShadowHeight)
        self.buttonLeave.addImage(self.leaveShadow, self.leaveLight)

        self.buttonStart = Button(self.screenWidth - self.startShadowWidth - 22, 259, self.startShadowWidth, self.startShadowHeight)
        self.buttonStart.addImage(self.startShadow, self.startLight)

        self.buttonEditPlayer = Button(820, 220, 156, 333)
        # self.buttonEditPlayer.addText('Edit Player', self.font, 20, (255,255,255), 1, (50,50,50))
        self.buttonEditPlayer.addImage(self.knightStand, self.knightStandAura)
        self.popEdit = False

        # Setup edit room
        self.buttonRoomSetting = Button((self.screenWidth//2)-(self.mapWidth//2), 215, self.mapWidth, self.map.get_rect().height)
        self.buttonRoomSetting.addImage(self.map, self.mapAura)

        # Setup edit player
        
        self.popEditBg = control.dressingCab.get_rect()
        self.popEditBg.x, self.popEditBg.y = self.screenWidth/2 - self.popEditBg.centerx, self.screenHeight/2 - self.popEditBg.centery
        self.popEditSummit = Button(self.popEditBg.centerx - 50, self.popEditBg.y + 515, 100, 50)
        self.popEditSummit.addText('Submit', self.font, 20, (255, 255, 255), bgColor = (144, 109, 99), bgColorOver = (120, 90, 82))
        
        self.buttonLeft = Button(self.screenWidth//2 - self.control.leftArrow.get_width() - 80, 360, 
        self.control.leftArrow.get_width(), self.control.leftArrow.get_height())
        self.buttonLeft.addImage(self.control.leftArrow)

        self.buttonRight = Button(self.screenWidth//2 + 80, 360, self.control.rightArrow.get_width(), 
        self.control.rightArrow.get_height())
        self.buttonRight.addImage(self.control.rightArrow)

        self.currentSkin = None
        self.currentName = None
        self.skins = self.control.skins
        self.amountSkins = len(self.skins)
        
        self.newPlayername = Textbox(self.popEditBg.centerx - 110, self.popEditBg.y + 70, 220, 30, pygame.Color('white'), 
        pygame.Color('white'), 15, fontPath = self.font1, size = 26)

        self.popupNoIGN = Popup(self.screenWidth//2 - 250, self.screenHeight//2 - 90, 500, 180, 'Please enter your/> In-game name with no spacebar', 
        pygame.Color('white'), pygame.Color('darkblue'))
        self.popupNoIGN.modComponents(self.popupNoIGN.b1, 'button', pygame.Color('darkseagreen4'), pygame.Color('darkslategray'), 'understand')

        self.available = True
        self.triggerNoIGN = False
    
    def editPlayer(self):

        self.available = False
        # Popup background (may change later)
        self.display.blit(self.control.dressingCab, (self.popEditBg.x, self.popEditBg.y))
        
        self.display.blit(self.skins[self.currentSkin], (self.popEditBg.centerx - self.skins[self.currentSkin].get_width()/2, 
        self.popEditBg.y + 230))

        self.currentName = self.newPlayername.getText()
        self.drawText(self.currentName, 20, self.popEditBg.centerx , self.popEditBg.y + 210, self.font1, self.control.white)

        self.newPlayername.draw(self.display)

        self.buttonLeft.draw(self.display)
        if self.buttonLeft.isButtonClick():
            if self.currentSkin == 0:
                self.currentSkin = self.amountSkins-1
            else:
                self.currentSkin -= 1

        self.buttonRight.draw(self.display)
        if self.buttonRight.isButtonClick():
            if self.currentSkin == self.amountSkins-1:
                self.currentSkin = 0
            else:
                self.currentSkin += 1

        self.popEditSummit.draw(self.display)
        if self.popEditSummit.isButtonClick():
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
            self.popupNoIGN.draw(self.display, self.font1, size = 28, textAlign = 'centerAlign', image = self.control.popupBackground)
            if self.popupNoIGN.b1.isButtonClick():
                self.triggerNoIGN = False

    # override
    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.newPlayername.handleEvent(event)
            self.player.playerMovement(event)

            self.handleChatBoxEvent(event)

    def displayScreen(self):

        self.displayRunning = True
        
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

        # for thread in threading.enumerate(): 
        #     print(thread.name)

        # all buttons
        buttonList = [self.buttonEditPlayer, self.buttonRoomSetting, self.buttonStart, self.buttonLeave]

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
            
            # page blackground
            self.display.fill((0, 0, 0))
            self.display.blit(self.lobbyFloor, (0,0))
            self.display.blit(self.lobbyWall, (0,0))

            # draw all button
            for roomButton in buttonList:
                roomButton.draw(self.display, self.available)
            
            self.display.blit(self.lobbyTable, ((self.screenWidth//2) - (self.lobbyTableWidth//2), 385))


            if self.network.connectStatus == True:
                self.updateScreenData()
            self.drawPlayers()
            
            self.drawChatBox(self.display)

            if self.available:

                if self.buttonLeave.isButtonClick():
                    self.allowSendData = False
                    self.sendDataThread.join()

                    if self.network.connectStatus == True:
                        self.network.disconnectFromServer()
                    self.player.setAttribute() # reset current player
                    self.player.host = False
                    self.player.id = None
                    self.currentName = None
                    self.currentSkin = None
                    self.popEdit = False
                    self.available = True
                    self.sendData = []
                    self.othersPlayerInMatch.clear()
                    self.playersData.clear()
                    self.matchSetting.clear()
                    self.allMessages.clear()

                    # Main music is loaded here
                    self.currentMusic.stop()
                    self.currentMusic.load(self.musicList[0])
                    self.currentMusic.play(-1)

                    self.changePageByInput(True, self.control.menu)

                for i in range(5):
                    self.drawText('Edit Player', 30, self.buttonEditPlayer.rect.centerx + i, self.buttonEditPlayer.rect.y - 15 + i, 
                    self.font1, self.control.black)
                    self.drawText('Room Setting', 30, self.buttonRoomSetting.rect.centerx + i, self.buttonRoomSetting.rect.y - 45 + i, 
                    self.font1, self.control.black)
                self.drawText('Edit Player', 30, self.buttonEditPlayer.rect.centerx, self.buttonEditPlayer.rect.y - 15, 
                self.font1, self.control.white)
                self.drawText('Room Setting', 30, self.buttonRoomSetting.rect.centerx, self.buttonRoomSetting.rect.y - 45, 
                self.font1, self.control.white)
            
                
                if self.buttonStart.isButtonClick():
                    if self.player.host == True:
                        if (self.network.connectStatus == True and
                            len(self.matchSetting) > 0):
                            currentPlayer = len(self.playersData)
                            maxPlayer = self.matchSetting[0] 
                            if currentPlayer == maxPlayer:
                                self.currentName = None
                                self.currentSkin = None
                                self.popEdit = False
                                self.available = True
                                self.allowSendData = False
                                self.sendDataThread.join()
                                self.network.startGame()
                                self.changePageByInput(True, self.control.game)
                            else:
                                print("[GAME] Cannot start match")
                    else:
                        print("[GAME] You are not host")
                
                if self.buttonEditPlayer.isButtonClick():
                    self.popEdit = True
                    if self.currentName == None and self.currentSkin == None:
                        self.currentSkin = self.player.skin
                        self.currentName = self.player.name
                    self.newPlayername.text = self.currentName

            if len(self.matchSetting) > 2:
                gameStart = self.matchSetting[2]
                maxplayer = self.matchSetting[0]

                # Pop edit player
                if self.popEdit == True and not gameStart:
                    self.editPlayer()

                if(self.player.host != True and gameStart == True and 
                   maxplayer == len(self.playersData)):
                    self.currentName = None
                    self.currentSkin = None
                    self.popEdit = False
                    self.available = True
                    self.allowSendData = False
                    self.sendDataThread.join()
                    self.changePageByInput(True, self.control.game)
            self.biltScreen() # update screen
            self.clock.tick(60) # run at 60 fps