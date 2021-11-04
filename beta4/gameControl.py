import pygame, os
from network import Network
from player import Player
from host import HostMenu
from menu import MainMenu
from option import OptionMenu
from createPlayer import CreatePlayer
from lobby import Lobby
from game import Game

class GameSetting:
    def __init__(self):
        pygame.init()
        self.running = True

        # Display size
        self.displayWidth = 1280
        self.displayHeight = 720

        self.screen = pygame.display.set_mode((self.displayWidth, self.displayHeight))

        # Default color
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        # network
        self.network = Network()

        # global player object
        self.player = Player()

        # global data
        # 0 -> players in match
        # 1 -> players data
        # 2 -> current match setting
        self.globalData = [[], [], []]

        #load game image
        self.knightCover = pygame.image.load("images\menuUI\knightCover.PNG")
        self.BGCover = pygame.image.load("images\menuUI\BGCover.PNG")
        self.skyCover = pygame.image.load("images\menuUI\skyCover.JPG")
        self.woodBoard = pygame.image.load("images\menuUI\woodBoard.PNG")
        self.choice = pygame.image.load("images\menuUI\choice.PNG")
        self.popupBackground = pygame.image.load("images\popup1.PNG")
        self.woodBoard2 = pygame.image.load("images\woodtexture.PNG")

        #load skins
        self.skins = []
        imagePath = "images/skins/"
        skinList = os.listdir(imagePath)
        for nameSkin in skinList:
            self.skins.append(pygame.image.load( imagePath + nameSkin).convert_alpha())

        # Initialize music player
        pygame.mixer.init(frequency = 44100, size = -16, channels = 2, buffer = 512)
        self.currentMusic = pygame.mixer.music
        self.musicList = ['musics/JOAK_Final.wav','musics/BGM.wav']
        # Set default volume to 50%
        self.currentMusic.set_volume(0.5)

        #load sounds effect
        self.soundList = ['sounds/button-24.wav','sounds/button-27.wav','sounds/button-30.wav','sounds/button-50.wav','sounds/button-1.wav','sounds/click.wav']
        self.soundEffectVol = 1

class StateControl(GameSetting):

    def __init__(self):
        super(StateControl, self).__init__()

        # add state here
        self.menu = MainMenu(self)
        self.option = OptionMenu(self)
        self.host = HostMenu(self)
        self.createPlayer = CreatePlayer(self)
        self.lobby = Lobby(self)
        self.game = Game(self)

        self.currentState = self.menu
        self.previousState = []
    

    def saveState(self):
        self.previousState.append(self.currentState)
    
    def changeState(self, state):
        # reset all previous state when come back to main manu
        if state == self.menu:
            self.previousState.clear()
        self.currentState = state

    def goBack(self):
        try:
            returnState = self.previousState.pop()
        except Exception as e:
            returnState = self.menu
            print("[ERROR] Problem with state list\n", e)
        return returnState
