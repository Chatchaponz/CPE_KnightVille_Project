import pygame, os
from gameSystem.network import Network
from gameSystem.scene.player import Player
from gameSystem.scene.host import HostMenu
from gameSystem.scene.menu import MainMenu
from gameSystem.scene.option import OptionMenu
from gameSystem.scene.createPlayer import CreatePlayer
from gameSystem.scene.lobby import Lobby
from gameSystem.scene.game import Game

'''
gameControl.py - main game controller and local variable

[Class] + GameSetting
        + GameControl

last updated: 27 Oct 2021
'''

class GameSetting:
    '''
    GameSetting - main setting of the game and match
    '''
    def __init__(self):
        '''
        __init__ - Constructor of GameSetting class
        '''
        pygame.init()
        
        pygame.display.set_caption('KnightVILLe')

        # List of sound effects
        self.soundList = ['sounds/button-30.wav',
                        'sounds/button-1.wav',
                        'sounds/clickSound.wav',
                        'sounds/back.wav',
                        'sounds/select.wav',
                        'sounds/aclick.wav',
                        'sounds/lock.wav',
                        'sounds/paper4.wav',
                        'sounds/metal2.wav',
                        'sounds/metalHit.wav.',
                        'sounds/missionButt1.wav',
                        'sounds/missionButt2.wav',
                        'sounds/missionFail.wav',
                        'sounds/missionSuccess.wav']

        self.paperSoundList = ['sounds/paper1.wav','sounds/paper4.wav']

        self.running = True

        # Display size
        self.displayWidth = 1280
        self.displayHeight = 720

        self.screen = pygame.display.set_mode((self.displayWidth, self.displayHeight))

        # Default color
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        # Network
        self.network = Network()

        # Global data
        # 0 -> players in match
        # 1 -> players data
        # 2 -> current match setting
        # 3 -> chat data
        # 4 -> current player in match
        # 5 -> other player's data
        self.globalData = [[], [], [], [], [], []]

        # Load game image
        self.knightCover = pygame.image.load("images\menuUI\knightCover.PNG")
        self.BGCover = pygame.image.load("images\menuUI\BGCover.PNG")
        self.skyCover = pygame.image.load("images\menuUI\skyCover.JPG")
        self.woodBoard = pygame.image.load("images\menuUI\woodBoard.PNG")
        self.choice = pygame.image.load("images\menuUI\choice.PNG")
        self.logo = pygame.image.load("images\menuUI\gameLogo.PNG")
        self.buttonBG = pygame.image.load("images\menuUI\BGbutton.PNG")

        self.popupBackground = pygame.image.load("images\popup1.PNG")

        self.hostBoard = pygame.image.load("images\host\hostBoard.JPG")

        self.dressingCab = pygame.image.load("images\createPlayer\dressingCab.PNG")
        self.dressingRoom = pygame.image.load("images\createPlayer\dressingRoom.JPG")

        self.oberonIcon = pygame.image.load("images\icon\oberonIcon.PNG")
        self.rightArrow = pygame.image.load("images\icon\pointerRight.PNG")
        self.leftArrow = pygame.image.load("images\icon\pointerLeft.PNG")
        self.tapeRightArrow = pygame.image.load("images\icon\TapeRightArrow.PNG")
        self.tapeLeftArrow = pygame.image.load("images\icon\TapeLeftArrow.PNG")
        self.tapeClose = pygame.image.load("images\icon\TapeClose.PNG")

        # Lobby elements 
        self.lobbyFloor = pygame.image.load("images\lobby\lobbyFloor.JPG")
        self.lobbyWall = pygame.image.load("images\lobby\lobbyWall.PNG")
        self.startShadow = pygame.image.load("images\lobby\startShadow.PNG")
        self.startLight = pygame.image.load("images\lobby\startLight.PNG")
        self.leaveShadow = pygame.image.load("images\lobby\leaveShadow.PNG")
        self.leaveLight = pygame.image.load("images\lobby\leaveLight.PNG")
        self.knightStand = pygame.image.load("images\lobby\knightStand.PNG")
        self.knightStandAura = pygame.image.load("images\lobby\knightStandAura.PNG")
        self.map = pygame.image.load("images\lobby\map.PNG")
        self.mapAura = pygame.image.load("images\lobby\mapAura.PNG")
        self.lobbyTable = pygame.image.load("images\lobby\lobbyTable.PNG")
        self.boardSetting = pygame.image.load("images/lobby/boardGameSetting.JPG")

        # Match setting elements
        self.morgana = pygame.image.load("images\profile\Morgana.JPG")
        self.mordred = pygame.image.load("images\profile\Mordred.JPG")
        self.oberon = pygame.image.load("images\profile\Oberon.JPG")
        self.percival = pygame.image.load("images\profile\Percival.JPG")
        self.morganaPercival = pygame.image.load("images\profile\MorganaPercival.JPG")
        self.servant = pygame.image.load("images\profile\Servant.JPG")
        self.merlin = pygame.image.load("images\profile\Merlin.JPG")
        self.minion = pygame.image.load("images\profile\Minion.JPG")
        self.assasin = pygame.image.load("images\profile\Assassin.JPG")
        self.offFilter = pygame.image.load("images/profile/blackFilter.PNG")
        self.roleFrame = pygame.image.load("images/profile/frame.JPG")
        self.lock = pygame.image.load("images/profile/lock.PNG")
        self.checked = pygame.image.load("images/profile/yes.PNG")

        # Mission map elements
        self.town = pygame.image.load("images/game/town.PNG")
        self.townSky = pygame.image.load("images/game/townSky.JPG")
        self.sign = pygame.image.load("images/game/sign.JPG")
        self.baseSkip = pygame.image.load("images/game/BaseSkip.PNG")
        self.skip = []
        self.skip.append(pygame.image.load("images/game/Skip1.PNG"))
        self.skip.append(pygame.image.load("images/game/Skip2.PNG"))
        self.skip.append(pygame.image.load("images/game/Skip3.PNG"))
        self.skip.append(pygame.image.load("images/game/Skip4.PNG"))
        self.skip.append(pygame.image.load("images/game/Skip5.PNG"))
        self.missionShow = []
        self.missionShow.append(pygame.image.load("images/game/Mission1.PNG"))
        self.missionShow.append(pygame.image.load("images/game/Mission2.PNG"))
        self.missionShow.append(pygame.image.load("images/game/Mission3.PNG"))
        self.missionShow.append(pygame.image.load("images/game/Mission4.PNG"))
        self.missionShow.append(pygame.image.load("images/game/Mission5.PNG"))
        self.missionShow.append(pygame.image.load("images/game/Mission4F.PNG"))
        self.missionShow.append(pygame.image.load("images/game/Mission5F.PNG"))
        self.success = pygame.image.load("images/game/success.PNG")
        self.fail = pygame.image.load("images/game/fail.PNG")

        # Game icon
        pygame.display.set_icon(self.oberonIcon)

        # Load How-to-play material
        self.howToPlay = []
        howToPlayPath = "images/howToPlay/"
        howToPlayList = os.listdir(howToPlayPath)
        for howToPlayPage in howToPlayList:
            self.howToPlay.append(pygame.image.load( howToPlayPath + howToPlayPage).convert_alpha())

        # Load skins
        self.skins = []
        imagePath = "images/skins/"
        skinList = os.listdir(imagePath)
        for nameSkin in skinList:
            self.skins.append(pygame.image.load( imagePath + nameSkin).convert_alpha())

        
        # Load icons
        self.evil = pygame.image.load("images\icon\Evil.PNG")
        self.death = pygame.image.load("images\icon\Death.PNG")
        self.leader = pygame.image.load("images\icon\leader.PNG")
        self.merlinIcon = pygame.image.load("images\icon\Merlin.PNG")
        self.member = pygame.image.load("images\icon\member.PNG")
        self.aim = pygame.image.load("images\icon\Aim.PNG")
        self.host = pygame.image.load("images\icon\Host.PNG")

        self.evil = pygame.transform.scale(self.evil, (40,40))
        self.death = pygame.transform.scale(self.death, (40,40))
        self.leader = pygame.transform.scale(self.leader, (40,40))
        self.merlinIcon = pygame.transform.scale(self.merlinIcon, (40,40))
        self.member = pygame.transform.scale(self.member, (40,40))
        self.aim = pygame.transform.scale(self.aim, (120,120))
        self.host = pygame.transform.scale(self.host, (40,40))

        self.iconList = []
        self.iconList.append(self.host)
        self.iconList.append(self.evil)
        self.iconList.append(self.merlinIcon)
        self.iconList.append(self.leader)
        self.iconList.append(self.member)
        self.iconList.append(self.death)
        self.iconList.append(self.aim)

        # Global player object
        self.player = Player(icons = self.iconList)
        
        # Initialize music player
        pygame.mixer.init(frequency = 44100, size = -16, channels = 2, buffer = 512)
        self.currentMusic = pygame.mixer.music
        self.musicList = ['musics/JOAK_Final.wav','musics/BGM.wav']
        
        # Set default volume to 50%
        self.currentMusic.set_volume(0.25)

        # Sound volume
        self.soundEffectVol = 0.5
    
    def getSoundEffectVol(self):
        '''
        getSoundEffectVol - method to get sound effect volume

        + return - soundEffectVol which is in 0.0 - 1.0 range
        '''
        return self.soundEffectVol

    def playSoundWithVol(self,soundPath,vol):
        '''
        playSoundWithVol - play sound effect that is able to set the volume
        + soundPath - The string name of sound effect to be played
        + vol - local sound effect volume 
        '''
        sound = pygame.mixer.Sound(soundPath)
        sound.set_volume(vol)
        sound.play()
        

class StateControl(GameSetting):
    '''
    StateControl - Screen's state controller inherited from GameSetting
    '''
    def __init__(self):
        '''
        __init__ - Constructor of StateControl class
        + GameSetting - GameSetting variable
        '''
        super(StateControl, self).__init__()

        # All game's state
        self.menu = MainMenu(self)
        self.option = OptionMenu(self)
        self.host = HostMenu(self)
        self.createPlayer = CreatePlayer(self)
        self.lobby = Lobby(self)
        self.game = Game(self)

        self.currentState = self.menu
        self.previousState = []
    

    def saveState(self):
        '''
        saveState - Save the current state of the game (state of the screen)
        '''
        self.previousState.append(self.currentState)
    
    def changeState(self, state):
        '''
        chaneState - change to the direction state, reset all previous state when come back to main manu
        + state - the direction state 
        '''
        if state == self.menu:
            self.previousState.clear()
        self.currentState = state

    def goBack(self):
        '''
        goBack - method to return to the previous state
        '''
        try:
            returnState = self.previousState.pop()
        except Exception as e:
            returnState = self.menu
            print("[ERROR] Problem with state list\n", e)
        return returnState
