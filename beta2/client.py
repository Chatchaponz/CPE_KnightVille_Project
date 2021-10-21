import socket
import pickle
from enum import IntEnum, unique

# [TEST VER] full ver shouldn't have print in method
'''
Signal - Integer Enum class for client telling server to do some activity

'''
@unique
class Signal (IntEnum):
    JOIN = 1
    CLIENT_DATA = 2
    SET_MATCH = 3
    SETTING_MATCH = 4
    START_MATCH = 5
    STOP_MATCH = 6
    END_MATCH = 7
    GET_MATCH_PLAYERS = 8
    GET_MATCH_SETTING = 9
    EXIT = 10

class CannotConnectToServerException(Exception):
    pass

'''
Client - provide ways to connect and make activity to the server

'''
class Client:
    __IP = ""
    __PORT = 5555 # default port
    __SIZE = 4096  # maximum data recieve size
    # __FORMAT = 'utf-8' # data format

    def __init__(self, ip = __IP, port = __PORT ):
        self.__IP = ip
        self.__PORT = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __sendData(self, signal, data):
        try:
            self.client.send(pickle.dumps((signal, data)))
            return pickle.loads(self.client.recv(self.__SIZE))
        except (Exception, socket.error) as e:
            print("[ERROR] " + str(e))
            self.client.close()
            return None
    
    def connect(self):
        try:
            address = (self.__IP, self.__PORT)
            self.client.connect(address)
            if(pickle.loads(self.client.recv(self.__SIZE))):
                print("[CLIENT] Server connected.")
        except (Exception, socket.error) as e:
            self.client.close()
            raise CannotConnectToServerException(str(e))
        return True
    
    def createMatch(self):
        success = self.__sendData(Signal.SET_MATCH, "")
        if(success):
            print("[CLIENT] Create match successfully. Ready to join...")
        else:
            print("[CLIENT] Match is already created.")
        return success
    
    def settingMatch(self, maxPlayer : int = 10, otherSetting = "" ):

        success = self.__sendData(Signal.SETTING_MATCH, [maxPlayer, otherSetting])
        
        if(success[0]):
            print("[CLIENT] Match setting has been change.")
        else:
            if success[1] == 0 : print("[CLIENT] Unknown error.")
            if success[1] == -1 : print("[CLIENT] Cannot change setting while match is playing")
            if success[1] == -2 : print("[CLIENT] Current player already exceed new max player.")
            if success[1] == -3 : print("[CLIENT] You are not the host.")
            if success[1] == -4 : print("[CLIENT] Match is not created.")
        return success

    
    # success return [<boolean>, <failStatus>]
    # failStatus = 0 Unknown error, -1 Match is already started, 
    # -2 need to be in the match (not join), -3 not the host of the match
    # 1 No Error
    def startMatch(self):
        success = self.__sendData(Signal.START_MATCH, "")
        if(success[0]):
            print("[CLIENT] Start match successfully")
        else:
            if success[1] == 0 : print("[CLIENT] Unknown error.")
            if success[1] == -1 : print("[CLIENT] Match is already started.")
            if success[1] == -2 : print("[CLIENT] Please join this match first.")
            if success[1] == -3 : print("[CLIENT] You are not the host.")
        return success[0]
    
    # success return [<boolean>, <failStatus>]
    # failStatus = 0 Unknown error, -1 Match is not start yet, 
    # -2 need to be in the match (not join), -3 not the host of the match
    # 1 No Error
    def stopMatch(self):
        success = self.__sendData(Signal.STOP_MATCH, "")
        if(success[0]):
            print("[CLIENT] Start match successfully")
        else:
            if success[1] == 0 : print("[CLIENT] Unknown error.")
            if success[1] == -1 : print("[CLIENT] Match is not start yet.")
            if success[1] == -2 : print("[CLIENT] Please join this match first.")
            if success[1] == -3 : print("[CLIENT] You are not the host.")
        return success[0]
    
    def endMatch(self):
        success = self.__sendData(Signal.END_MATCH, "")
        if(success):
            print("[CLIENT] Match is ended.")
        else:
            print("[CLIENT] Match is not created yet.")
        return success
    
    # return None if error / None if not join first / Data if success
    def send(self, data = ""):
        success = self.__sendData(Signal.CLIENT_DATA, data)
        return success
    
    # return None if error / None if not join first / Data if success
    def getAllPlayerAddress(self):
        success = self.__sendData(Signal.GET_MATCH_PLAYERS, "")
        return success
    
    # return None if error / None if not join first / Data if success
    def getMatchSetting(self):
        success = self.__sendData(Signal.GET_MATCH_SETTING, "")
        return success

    # success return [<boolean>, <failStatus>]
    # failStatus = 0 Unknown error, -1 Match is not created, 
    # -2 Match is already started, -3 Match is full
    # -4 Already join this match
    # 1 No Error
    def join(self, data = ""):
        success = self.__sendData(Signal.JOIN, data)
        if(success[0]):
            print("[CLIENT] Join match successfully.")
        else:
            if success[1] == 0 : print("[CLIENT] Unknown error.")
            if success[1] == -1 : print("[CLIENT] Match is not created.")
            if success[1] == -2 : print("[CLIENT] Match is already started.")
            if success[1] == -3 : print("[CLIENT] Match is full.")
            if success[1] == -4 : print("[CLIENT] Already join this match.")
        return success[0]

    def disconnect(self):
        try:
            self.client.send(pickle.dumps((Signal.EXIT, "")))
        except (Exception, socket.error) as e:
            print("[ERROR] " + str(e))
            self.client.close()
        self.client.close()