import pygame, sys, threading
from button import Button 
from gameManager import GameManager

class Lobby(GameManager):
    
    def __init__(self, control):
        super(Lobby, self).__init__(control)
        
        # Image / Button goes here vvvv
        self.buttonLeave = Button(100, 100, 100, 50)
        self.buttonLeave.addText('Leave', self.font, 20, (255,255,255), 1, (50,50,50))

        self.buttonStart = Button(1000, 600, 100, 50)
        self.buttonStart.addText('Start', self.font, 20, (255,255,255), 1, (50,50,50))

        self.currentMusic = control.currentMusic
        self.musicList = control.musicList
    
    # override
    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.player.playerMovement(event)   

    def displayScreen(self):

        print(self.player.skin)

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

                # Main music is loaded here
                self.currentMusic.stop()
                self.currentMusic.load(self.musicList[0])
                self.currentMusic.play(-1)

                if self.network.connectStatus == True:
                    self.network.disconnectFromServer()
                self.player.setAttribute() # reset current player
                self.player.host = False
                self.player.id = None
                self.sendData = []
                self.othersPlayerInMatch.clear()
                self.playersData.clear()
                self.changePageByInput(True, self.control.menu)
            
            self.buttonStart.draw(self.display)
            if self.buttonStart.isButtonClick():
                if self.player.host == True:
                    if (self.network.connectStatus == True and
                        len(self.matchSetting) > 0):
                        currentPlayer = len(self.playersData)
                        maxPlayer = self.matchSetting[0] 
                        if currentPlayer == maxPlayer:
                            self.allowSendData = False
                            self.sendDataThread.join()
                            self.network.startGame()
                            self.changePageByInput(True, self.control.game)
                        else:
                            print("[GAME] Cannot start match")
                else:
                    print("[GAME] You are not host")

            if len(self.matchSetting) > 2:
                gameStart = self.matchSetting[2]
                if self.player.host != True and gameStart == True:
                    self.allowSendData = False
                    self.sendDataThread.join()
                    self.changePageByInput(True, self.control.game)

            self.biltScreen() # update screen
            self.clock.tick(60) # run at 60 fps