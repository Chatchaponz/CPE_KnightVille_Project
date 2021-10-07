import socket
import pickle
from enum import IntEnum, unique

# [TEST VER] full ver shouldn't have print in method

@unique
class Signal (IntEnum):
    JOIN = 1
    CLIENT_DATA = 2
    SET_MATCH = 3
    END_MATCH = 4
    EXIT = 5

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
            print("[ERROR] " + str(e))
            self.client.close()
            return False
        return True
    
    def createMatch(self):
        success = self.__sendData(Signal.SET_MATCH, "")
        if(success):
            print("[CLIENT] Create match successfully. Ready to join...")
        else:
            print("[CLIENT] Match is already created.")
        return success
    
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
    
    # success return [<boolean>, <failStatus>]
    # failStatus = 0 Unknown error, -1 Match is not created, -2 Match is already started, -3 Match is full
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
        return success[0]
    
    def disconnect(self):
        try:
            self.client.send(pickle.dumps((Signal.EXIT, "")))
        except (Exception, socket.error) as e:
            print("[ERROR] " + str(e))
            self.client.close()
        self.client.close()