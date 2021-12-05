import socket
import pickle
from enum import IntEnum, unique
'''
client - Manage server's activity from client side
         including connecting to server, sending and receiving data,
         manage current match and disconnecting from the server

[Class] + Client
        + Signal
        + ClientException
        + CannotConnectToServerException
        + JoinMatchException
        + ServerMatchException
        + DisconnectException

last updated: 27 Oct 2021
'''

@unique
class Signal (IntEnum):
    '''
    Signal - Integer Enum class for client telling server to do some activity
    '''
    JOIN = 1
    CLIENT_DATA = 2
    SET_MATCH = 3
    SETTING_MATCH = 4
    START_MATCH = 5
    STOP_MATCH = 6
    END_MATCH = 7
    GET_MATCH_PLAYERS = 8
    GET_MATCH_SETTING = 9
    SEND_MESSAGE = 10
    RECEIVE_MESSAGE = 11
    EXIT = 12

class ClientException(Exception): 
    ''' ClientException - Parent class of all exception in Client '''
    pass

class CannotConnectToServerException(ClientException): 
    ''' CannotConnectToServerException - Exception occur when unable to connect the server '''
    pass

class JoinMatchException(ClientException):
    ''' JoinMatchException - Exception occur when cannot join match in server '''
    pass

class ServerMatchException(ClientException):
    ''' ServerMatchException - Exception occur when invalid action happened to current match in server '''
    pass

class DisconnectException(ClientException):
    ''' DisconnectException - Exception occur when unable to disconnect from the server '''
    pass

class SendDataException(ClientException):
    ''' SendDataException - Exception occur when unable to send the data '''
    pass


class Client:
    '''
    Client - Provide ways to connect and make activity to the server
    '''
    __IP = "" # IPv4 from client to connect to the server with the same IP
    __PORT = 5555 # Default port
    __SIZE = 4096  # Maximum data receive size

    def __init__(self, ip = __IP, port : int = __PORT):
        '''
        __init__ - Constructor of Client class
        + ip - IPv4 from client to connect to the server with the same IP
               initialize with __IP = ""
        + port - Port number (must be integer)
                 initialize with __PORT = 5555
        '''
        self.__IP = ip  # IPv4 
        self.__PORT = port # Integer port number
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Initialize socket

    def __sendData(self, signal, data):
        '''
        __sendData - Send and receive data from server according to given signal
        + signal - Signal indicate type of request 
        + data - Any type of data for sending to the server

        + return - Response data from server
          - data if successfully get response from the server
          - None if no response from the server
        
        + raise SendDataException in case data cannot be sent
        '''
        try:
            self.client.send(pickle.dumps((signal, data)))
            return pickle.loads(self.client.recv(self.__SIZE))
        except (Exception, socket.error) as e:
            print("[CLIENT_ERROR] " + str(e))
            self.client.close()
            raise SendDataException("Unable to send the data") from e
    
    def connect(self):
        '''
        connect - Connect this client to server

        + return - Boolean
          - True if client can connect to the server successfully

        + raise CannotConnectToServerException in case cannot connect to server
        '''
        try:
            address = (self.__IP, self.__PORT)
            self.client.connect(address)
            if(pickle.loads(self.client.recv(self.__SIZE))):
                print("[CLIENT] Server connected.")
        except (Exception, socket.error) as e:
            self.client.close()
            raise CannotConnectToServerException("Unable to connect server") from e
        return True
    
    def createMatch(self):
        '''
        createMatch - Initiate match in server

        + return
          - success if get response from the server
        
        + raise ServerMatchException
        '''
        try: success = self.__sendData(Signal.SET_MATCH, "")
        except ClientException as e: raise e

        if(success):
            print("[CLIENT] Create match successfully. Ready to join...")
        else:
            raise ServerMatchException("Match is already created.")
        return success
    
    def settingMatch(self, maxPlayer : int = 10, otherSetting = "" ):
        '''
        settingMatch - Modify match setting
        + maxPlayer - Maximum player per match (must be integer)
                      initialize to 10
        + otherSetting - Optional setting depend on how the game have implemented
                         initialize to empty string
        + return
          - success if get response from the server
                    format: [<boolean>, <failStatus : int>]
                     <boolean> indicate success (True) and fail (False)
                     <failStatus : int>
                     1 - No error
                     0 - Unknown error.
                    -1 - Cannot change setting while match is playing.
                    -2 - Current player already exceed new max player.
                    -3 - You are not the host.
                    -4 - Match is not created.
        
        + raise ServerMatchException with different massage depend on "failStatus"
        '''
        try: success = self.__sendData(Signal.SETTING_MATCH, [maxPlayer, otherSetting])
        except ClientException as e: raise e
        if success == []: success = [True, 1]

        if(success[0]):
            print("[CLIENT] Match setting has been change.")
        else:
            if success[1] == 0 : raise ServerMatchException("Unknown error.")
            if success[1] == -1 : raise ServerMatchException("Cannot change setting while match is playing.")
            if success[1] == -2 : raise ServerMatchException("Current player already exceed new max player.")
            if success[1] == -3 : raise ServerMatchException("You are not the host.")
            if success[1] == -4 : raise ServerMatchException("Match is not created.")
        return success[0]

    
    def startMatch(self):
        '''
        startMatch - Send signal tell server to start the match

        + return
          - success if get response from the server
                    format: [<boolean>, <failStatus : int>]
                     <boolean> indicate success (True) and fail (False)
                     <failStatus : int>
                     1 - No error
                     0 - Unknown error.
                    -1 - Match is already started.
                    -2 - Please join this match first.
                    -3 - You are not the host.
        
        + raise ServerMatchException with different massage depend on "failStatus"
        '''
        try: success = self.__sendData(Signal.START_MATCH, "")
        except ClientException as e: raise e
        if success == []: success = [True, 1]

        if(success[0]):
            print("[CLIENT] Start match successfully")
        else:
            if success[1] == 0 : raise ServerMatchException("Unknown error.")
            if success[1] == -1 : raise ServerMatchException("Match is already started.")
            if success[1] == -2 : raise ServerMatchException("Please join this match first.")
            if success[1] == -3 : raise ServerMatchException("You are not the host.")
        return success[0]
    

    def stopMatch(self):
        '''
        stopMatch - Send signal tell server to stop the match (stop playing, still able to join)

        + return
          - success if get response from the server
                    format: [<boolean>, <failStatus : int>]
                     <boolean> indicate success (True) and fail (False)
                     <failStatus : int>
                     1 - No error
                     0 - Unknown error.
                    -1 - Match is not start yet.
                    -2 - Please join this match first.
                    -3 - You are not the host.
        
        + raise ServerMatchException with different massage depend on "failStatus"
        '''
        try: success = self.__sendData(Signal.STOP_MATCH, "")
        except ClientException as e: raise e
        if success == []: success = [True, 1]

        if(success[0]):
            print("[CLIENT] Stop match successfully")
        else:
            if success[1] == 0 : raise ServerMatchException("Unknown error.")
            if success[1] == -1 : raise ServerMatchException("Match is not start yet.")
            if success[1] == -2 : raise ServerMatchException("Please join this match first.")
            if success[1] == -3 : raise ServerMatchException("You are not the host.")
        return success[0]
    
    def endMatch(self):
        '''
        endMatch - Send signal tell server to end the match (close match, unable to join)

        + return
          - success if get response from the server
        
        + raise ServerMatchException in case match isn't created yet
        '''
        try: success = self.__sendData(Signal.END_MATCH, "")
        except ClientException as e: raise e

        if(success):
            print("[CLIENT] Match is ended.")
        else:
            raise ServerMatchException("Match is not created yet.")
        return success
    
    def send(self, data = ""):
        '''
        send - Send this client's data and receive other clients' data

        + return
          - success if get response from the server
                format: depend on user to implemented
                but will return "None" if something went wrong
        '''
        success = self.__sendData(Signal.CLIENT_DATA, data)
        return success
    
    def getAllPlayerAddress(self):
        '''
        getAllPlayerAddress - Get all current player's addresses in match

        + return
          - success if get response from the server
                format: depend on user to implemented
                but will return "None" if something went wrong
        '''
        try: success = self.__sendData(Signal.GET_MATCH_PLAYERS, "")
        except ClientException as e: raise e

        return success
    
    def getMatchSetting(self):
        '''
        getMatchSetting - Get all current player's addresses in match

        + return
          - success if get response from the server
                format: depend on user to implemented
                but will return "None" if something went wrong
        '''
        try: success = self.__sendData(Signal.GET_MATCH_SETTING, "")
        except ClientException as e: raise e

        return success

    def join(self, data = ""):
        '''
        join - Send signal with initial data to join the match
        + data - initial data (optional) 

        + return
          - success if get response from the server
                    format: [<boolean>, <failStatus : int>]
                     <boolean> indicate success (True) and fail (False)
                     <failStatus : int>
                     1 - No error
                     0 - Unknown error.
                    -1 - Match is not created.
                    -2 - Match is already started.
                    -3 - Match is full.
                    -4 - Already join this match.
        
        + raise JoinMatchException with different massage depend on "failStatus"
        '''
        try: success = self.__sendData(Signal.JOIN, data)
        except ClientException as e: raise e
        if success == []: success = [True, 1]

        if(success[0]):
            print("[CLIENT] Join match successfully.")
        else:
            if success[1] == 0 : raise JoinMatchException("Unknown error.")
            if success[1] == -1 : raise JoinMatchException("Match is not created.")
            if success[1] == -2 : raise JoinMatchException("Match is already started.")
            if success[1] == -3 : raise JoinMatchException("Match is full.")
            if success[1] == -4 : raise JoinMatchException("Already join this match.")
        return success[0]
    
    def sendMessage(self, data : str = ""):
        '''
        sendMessage - send message to server
        + data - string data to be send

        + return
          - success if already send the message
            - True if message store in server successfully
            - False if cannot store the message (This client not in the match)
        '''
        try: success = self.__sendData(Signal.SEND_MESSAGE, data)
        except ClientException as e: raise e

        return  success
    
    def receiveMessages(self):
        '''
        receiveMessage - receive all messages from server

        + return
          - success if get all messages from the server (40 message maximum)
                format: [ [<addr>, <message>], ... ]
                but will return "None" if something went wrong
        '''
        try: success = self.__sendData(Signal.RECEIVE_MESSAGE, "")
        except ClientException as e: raise e

        return success

    def disconnect(self):
        '''
        disconnect - Disconnect this client from the server

        raise DisconnectException in case unable to disconnect from server
        '''
        try:
            self.client.send(pickle.dumps((Signal.EXIT, "")))
        except (Exception, socket.error) as e:
            self.client.close()
            raise DisconnectException("Problem with disconnection") from e # maybe socket already close (host close server)
        self.client.close()