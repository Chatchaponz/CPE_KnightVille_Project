from pickle import TRUE
from client import Client
'''
network - Manage connection between game(client) and server

[Class] + Network

last updated: 31 Oct 2021
'''

class Network :
    '''
    Network - Manage activity between game(client) and server
              by specifically focusing on the use of the game in particular.
    '''
    def __init__(self):
        '''
        __init__ - Constructor of Network class
        '''
        self.__connect = None # Hold the connection to the server
        self.connectStatus = False # Show the current connection status 

    def tryConnectServer(self, ip: str, port: int):
        '''
        tryConnectServer - Make an attempt for connection 
        + ip - IPv4 of server to connect
        + port - Port number of server to connect

        + return - Boolean
          - True if success
          - False if fail
        '''
        try:
            self.__connect = Client(str(ip), int(port))
            self.__connect.connect()
            self.connectStatus = True
            return True
        except Exception as e:
            print("[ERROR] ",e)
        return False
    
    def disconnectFromServer(self):
        '''
        disconnectFromServer - Try disconnect from server

        + return - Boolean
          - True if success
          - False if fail
        '''
        try:
            self.connectStatus = False
            self.__connect.disconnect()
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False
    
    def createLobby(self, maxPlayer : int, availableRole, syncPhase : int, syncRound : int):
        '''
        createLobby - Create match with initial setting
        + maxPlayer - Maximum player in this match (must be integer)
        + availableRole - List of boolean indicate role that allow in this match
        + syncPhase - Integer indicate initial phase
        + syncRound - Integer indicate initial round

        + return - Boolean
          - True if success
          - False if fail
        '''
        try:
            self.__connect.createMatch()
            self.changeMatchSetting(maxPlayer, [availableRole, syncPhase, syncRound])
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False
    
    def changeMatchSetting(self, maxPlayer : int, availableRole):
        '''
        changeMatchSetting - Modify current match setting
        + maxPlayer - Maximum player in this match (must be integer)
        + availableRole - List of boolean indicate role that allow in this match

        + return - Boolean
          - True if success
          - False if fail
        '''
        try:
            self.__connect.settingMatch(maxPlayer, availableRole)
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False

    def tryGetData(self, sendData):
        '''
        tryGetData - Try sending this client's data and receiving necessary data from server
                     (Players' data, All players' addresses, Match setting)
        + sendData - data to be send

        + return - list of receiving data
          - [[<addr_player1, addr_player2, ...>], [<data1>, <data2>, ...], [<Setting>]] if success
          - None if fail
        '''
        try:
            othersPlayerData = self.__connect.send(sendData)
            currentPlayersInMatch = self.__connect.getAllPlayerAddress()
            matchSetting = self.__connect.getMatchSetting()
            chatMessages = self.__connect.receiveMessages()
            # eg: [[<addr_player1, addr_player2, ...>], [<data1>, <data2>, ...], [<Setting>], [ [<addr>, <message>], ... ]]
            return [currentPlayersInMatch, othersPlayerData, matchSetting, chatMessages]
        except Exception as e:
            print("[ERROR] ", e)
        return None
    
    def trySendMessage(self, sendMessage: str):
        try:
            return self.__connect.sendMessage(sendMessage)
        except Exception as e:
            print("[ERROR] ", e)
        return False
        
    def startGame(self):
        '''
        startGame - Start this match

        + return - Boolean
          - True if success
          - False if fail
        '''
        try:
            self.__connect.startMatch()
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False
    
    def stopThisGame(self):
        '''
        stopThisGame - Stop playing the match and back to lobby

        + return - Boolean
          - True if success
          - False if fail
        '''
        try:
            self.__connect.stopMatch()
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False
    
    def endThisGame(self):
        '''
        endThisGame - Ending current match ( Closing entirely )

        + return - Boolean
          - True if success
          - False if fail
        '''
        try:
            self.__connect.endMatch()
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False

    def joinGame(self):
        '''
        joinGame - Join current match

        + return - Boolean
          - True if success
          - False if fail
        '''
        try:
            self.__connect.join()
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False