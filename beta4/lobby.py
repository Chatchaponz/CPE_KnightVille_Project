import pygame, sys, threading
from button import Button 
from gameManager import GameManager

class Lobby(GameManager):
    
    def __init__(self, control):
        super(Lobby, self).__init__(control)

        # Music
        self.currentMusic = control.currentMusic
        self.musicList = control.musicList
        
        # Image / Button goes here vvvv
        self.buttonLeave = Button(100, 100, 100, 50)
        self.buttonLeave.addText('Leave', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonStart = Button(1000, 600, 100, 50)
        self.buttonStart.addText('Start', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonEditPlayer = Button(1000, 100, 100, 50)
        self.buttonEditPlayer.addText('Edit Player', self.font, 20, (255,255,255), 1, (50,50,50))
        self.popEdit = False

        # Setup edit player
        self.popEditWidth, self.popEditHeight = 400, 600 
        self.popEditX = (self.display.get_width() - self.popEditWidth)//2
        self.popEditY = (self.display.get_height() - self.popEditHeight)//2
        
        self.popEditBg = pygame.Rect((self.popEditX, self.popEditY), (self.popEditWidth, self.popEditHeight))
        self.popEditSummit = Button(self.popEditX + 300, self.popEditY + 520, 100, 50)
        self.popEditSummit.addText('Summit', self.font, 20, (255, 255, 255), 1, (50,50,50))
        
        self.buttonLeft = Button(self.popEditX + 50, self.popEditY + 100, 100, 50)
        self.buttonLeft.addText('←', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonRight = Button(self.popEditX + 250, self.popEditY + 100, 100, 50)
        self.buttonRight.addText('→', self.font, 20, (255,255,255), 1, (50,50,50))

        self.currentSkin = None
        self.currentName = None
        self.skins = self.control.skins
        self.amountSkins = len(self.skins)
    
    def editPlayer(self):
        # Popup background (may change later)
        pygame.draw.rect(self.display, (0, 100, 200), self.popEditBg)
        
        self.display.blit(self.skins[self.currentSkin], (self.popEditX + 100, self.popEditY + 120))

        self.drawText(self.currentName, 20, self.popEditX + 150, self.popEditY + 100, self.font, self.control.white)

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
            self.player.updateSkin(self.currentSkin)
            self.player.updateName(self.currentName)
            self.currentName = None
            self.currentSkin = None
            self.popEdit = False


    # override
    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.player.playerMovement(event)

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

        while self.displayRunning:

            self.checkEvent()

            self.sendData = [self.player.x,
                            self.player.y,
                            self.player.skin,
                            self.player.name,
                            self.player.isPlaying]

            # page blackground
            self.display.fill((0, 0, 0))

            if self.network.connectStatus == True:
                self.updateScreenData()
            self.drawPlayers()

            self.buttonLeave.draw(self.display)
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
                self.sendData = []
                self.othersPlayerInMatch.clear()
                self.playersData.clear()

                # Main music is loaded here
                self.currentMusic.stop()
                self.currentMusic.load(self.musicList[0])
                self.currentMusic.play(-1)

                self.changePageByInput(True, self.control.menu)
            
            self.buttonStart.draw(self.display)
            if self.buttonStart.isButtonClick():
                if self.player.host == True:
                    if (self.network.connectStatus == True and
                        len(self.matchSetting) > 0):
                        currentPlayer = len(self.playersData)
                        maxPlayer = self.matchSetting[0] 
                        if currentPlayer == maxPlayer:
                            self.currentName = None
                            self.currentSkin = None
                            self.allowSendData = False
                            self.sendDataThread.join()
                            self.network.startGame()
                            self.changePageByInput(True, self.control.game)
                        else:
                            print("[GAME] Cannot start match")
                else:
                    print("[GAME] You are not host")
            
            self.buttonEditPlayer.draw(self.display)
            if self.buttonEditPlayer.isButtonClick():
                self.popEdit = True
                if self.currentName == None and self.currentSkin == None:
                    self.currentSkin = self.player.skin
                    self.currentName = self.player.name
            
            if self.popEdit == True:
                self.editPlayer()

            if len(self.matchSetting) > 2:
                gameStart = self.matchSetting[2]
                if self.player.host != True and gameStart == True:
                    self.currentName = None
                    self.currentSkin = None
                    self.allowSendData = False
                    self.sendDataThread.join()
                    self.changePageByInput(True, self.control.game)

            self.biltScreen() # update screen
            self.clock.tick(60) # run at 60 fps