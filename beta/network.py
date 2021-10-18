from client import Client


class Network :

    def __init__(self):
        self.connect = None
        self.connectStatus = False

    def tryConnectServer(self, ip, port):
        try:
            self.connect = Client(ip, port)
            self.connect.connect()
            self.connectStatus = True
            return True
        except Exception as e:
            print("[ERROR] ",e)
        return False
    
    def disconnectFromServer(self):
        try:
            self.connect.disconnect()
            self.connectStatus = False
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False
    
    def createLobby(self, maxPlayer : int, availableRole):
        try:
            self.connect.createMatch()
            self.changeMatchSetting(maxPlayer, availableRole)
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False
    
    def changeMatchSetting(self, maxPlayer : int, availableRole):
        try:
            self.connect.settingMatch(maxPlayer, availableRole)
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False

    def tryGetData(self, sendData):
        try:
            othersPlayerData = self.connect.send(sendData)
            currentPlayersInMatch = self.connect.getAllPlayerAddress()
            matchSetting = self.connect.getMatchSetting()
            # eg: [[<addr_player1, addr_player2, ...>], [<data1>, <data2>, ...], [<Setting>]]
            return [currentPlayersInMatch, othersPlayerData, matchSetting]
        except Exception as e:
            print("[ERROR] ", e)
        return False
    
    def startGame(self):
        try:
            self.connect.startMatch()
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False
    
    def stopThisGame(self):
        try:
            self.connect.stopMatch()
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False
    
    def endThisGame(self):
        try:
            self.connect.endMatch()
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False

    def joinGame(self):
        try:
            self.connect.join()
            return True
        except Exception as e:
            print("[ERROR] ", e)
        return False