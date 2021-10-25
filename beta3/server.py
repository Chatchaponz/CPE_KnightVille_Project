import socket
import threading
import pickle
import time
import random
import configparser
from os import path
from client import Signal

config = configparser.ConfigParser()
if not path.exists("server_config.ini"):
    config["SETTING"] = {
        'Server_IP': socket.gethostbyname(socket.gethostname()), # Get local ip by computer name e.g. 192.168.X.X
        'Server_Port': 5555,
    }
    with open('server_config.ini', 'w') as configfile:
        config.write(configfile)


# Try read Setting from config file
try:
    config.read('server_config.ini')
    IP = config["SETTING"]['Server_IP'] # local ip e.g. 192.168.X.X
    PORT = int(config["SETTING"]['Server_Port']) # Default port
    SIZE = 4096 # Maximum data recieve size

except ( Exception, configparser.Error ) as e:
    print("There are something wrong with 'server_config.ini'\n\n" +
          "[ERROR] " + str(e) + "\n\nPlease fix it! Otherwise, [Delete] 'server_config.ini'\n" + 
          "Now server will use default setting instead.\n")
    # Default Setting
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 5555
    SIZE = 4096

ADDR = (IP, PORT) # Address

thisMatch = {
    'status': False,
    'maxPlayer': 10,
    'playing': False,
    'host': (),
    'players': [],
    'data': [],     # list of client in server plus its data 
                    # ex: [ [(192.168.X.X, 5555), 1, <data>], ... ]
    'setting': []
}

# Initiate server
# AF_INET = IPv4
# SOCK_STREAM = TPC
thisServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try connect to socket
try:
    thisServer.bind(ADDR)
except (Exception, socket.error) as e:
    print(f"[ERROR] Cannot bind address {ADDR} : " + str(e))
    thisServer.close()
    exit()

print("[SERVER] Server Started, Waiting for a connection...")
print(f"[SERVER] Server IP: [{IP}], Server Port: [{PORT}]")

def resetMatch():
    thisMatch['status'] = False
    thisMatch['maxPlayer'] = 10
    thisMatch['playing'] = False
    thisMatch['host'] = ()
    thisMatch['players'] = []
    thisMatch['data'] = []
    thisMatch['setting'] = []
    print('[SERVER] Match has been ended')




# manage game event
class GameEvent:
    def __init__(self):
        self.gamePhase = 0
        self.round = 0
        self.playerRoles = []
        self.currentPartyLeader = None
        self.doMission = None
        self.missionSuccess = None
        self.voteRejected = 0
        self.goodScore = 0
        self.evilScore = 0
    
    def randomRoles(self, allowRoles: list):
        randomRoles = []
        playerNumber = thisMatch['maxPlayer']
        playerRules = {
            5: {"good": 3, "evil": 2},
            6: {"good": 4, "evil": 2},
            7: {"good": 4, "evil": 3},
            8: {"good": 5, "evil": 3},
            9: {"good": 6, "evil": 3},
            10: {"good": 6, "evil": 4}
        }

        randomRoles += [2] * playerRules[playerNumber]["good"]
        randomRoles += [6] * playerRules[playerNumber]["evil"]
        goodIndex = 0
        evilIndex = playerRules[playerNumber]["good"] # evil start index equal to end index of good
        for role, roleAllow in enumerate(allowRoles):
            if roleAllow and role in [0, 1]:
                randomRoles[goodIndex] = role
                goodIndex += 1
            if roleAllow and role in [3, 4, 5, 7]:
                randomRoles[evilIndex] = role
                evilIndex += 1
        random.shuffle(randomRoles)
        return randomRoles
    
    def countScore(self, scoreToCount):
        scoreCount = 0
        if thisMatch['data'] != []:
            for thisData in thisMatch['data']:
                thisPlayer = thisData[2]
                if len(thisPlayer) > 5:
                    if thisPlayer[5] == scoreToCount:
                        scoreCount += 1
        return scoreCount
    
    def changeLeader(self):
        if self.currentPartyLeader + 1 < thisMatch['maxPlayer']:
            self.currentPartyLeader += 1
        else:
            self.currentPartyLeader = 0

    def checkAllData(self, dataIndex: int, checkData, condition: bool = False):
        allSame = True
        countId = 0
        if thisMatch['data'] != []:
            for thisData in thisMatch['data']:
                thisPlayer = thisData[2]
                if len(thisPlayer) > dataIndex:

                    if condition and type(checkData) == list:
                        leaderData = self.getPartyLeader(self.currentPartyLeader)
                        if len(leaderData) > 9:
                            if (countId in leaderData[9] and 
                                thisPlayer[dataIndex] not in checkData):
                                allSame = False
                                break
                        countId += 1
                    elif (type(thisPlayer[dataIndex]) != list and 
                         type(checkData) == list):
                        if thisPlayer[dataIndex] not in checkData:
                            allSame = False
                            break
                    else:
                        if thisPlayer[dataIndex] != checkData:
                            allSame = False
                            break
                else:
                    allSame = False
                    break
        return allSame
    
    def getPartyLeader(self, dataIndex: int):
        if thisMatch['data'] != [] and len(thisMatch['data']) > dataIndex:
            return thisMatch['data'][dataIndex][2]
        return None
    
    def checkCondition(self):
        checkPass = False
        if self.gamePhase == 0:
            if self.checkAllData(13, True):
                checkPass = True
        
        if self.gamePhase == 1:
            # check round
            self.missionSuccess = None
            self.doMission = None
            if self.round <= 5:
                if self.goodScore == 3 or self.evilScore == 3:
                    self.gamePhase = 9
            # check leader
            if (self.checkAllData(10, self.currentPartyLeader) and
                self.checkAllData(9, []) and self.gamePhase == 1):
                checkPass = True
        
        if self.gamePhase == 2:
            leaderData = self.getPartyLeader(self.currentPartyLeader)
            if leaderData != None and len(leaderData) > 9:
                # check leader choice and check partyMember of everyone
                if leaderData[5] == 3 and self.checkAllData(9, leaderData[9]):
                    checkPass = True

        if self.gamePhase == 3:
            if self.checkAllData(5, [1,2]):
                checkPass = True
        
        if self.gamePhase == 4:
            if (self.checkAllData(15, self.goodScore) and
                self.checkAllData(16, self.evilScore) and
                self.checkAllData(17, self.voteRejected)):
                checkPass = True
        
        if self.gamePhase == 5:
            if self.checkAllData(5, 0):
                if self.doMission:
                    self.doMission = None
                    checkPass = True
                elif not self.doMission:
                    self.doMission = None
                    self.changeLeader()
                    self.gamePhase = 1
                else:
                    checkPass = False
        
        if self.gamePhase == 6:
            if self.checkAllData(5, [4, 5], True):
                checkPass = True
        
        if self.gamePhase == 7:
            if (self.checkAllData(15, self.goodScore) and
                self.checkAllData(16, self.evilScore) and
                self.checkAllData(17, self.voteRejected)):
                checkPass = True
        
        if self.gamePhase == 8:
            if self.checkAllData(5, 0):
                if self.missionSuccess != None:
                    self.missionSuccess = None
                    self.changeLeader()
                    self.gamePhase = 1
                else:
                    checkPass = False

        if self.gamePhase == 9:
            checkPass = False

        return checkPass

    def doEvent(self):
        while True:
            if thisMatch['playing']:

                if thisMatch['setting'] != [] and len(thisMatch['setting']) > 2:    
                    thisMatch['setting'][1] = self.gamePhase
                    thisMatch['setting'][2] = self.round

                    if self.gamePhase == 0:
                        if self.playerRoles == []:
                            self.playerRoles = self.randomRoles(thisMatch['setting'][0])
                            thisMatch['setting'] += [self.playerRoles]
                        if len(thisMatch['setting']) > 3:
                            thisMatch['setting'][3] = self.playerRoles

                    if self.gamePhase == 1:
                        if self.currentPartyLeader == None and self.round == 0:
                            self.currentPartyLeader = random.choice(list(range(thisMatch['maxPlayer'])))
                        if len(thisMatch['setting']) > 3:
                            thisMatch['setting'][3] = self.currentPartyLeader
                    
                    if self.gamePhase == 4:
                        if self.doMission == None:
                            passScore = thisMatch['maxPlayer'] * 0.5
                            rejectVote = self.countScore(2)
                            if rejectVote >= passScore:
                                self.doMission = False
                                self.voteRejected += 1
                                if self.voteRejected == 5:
                                    self.evilScore += 1
                                    self.round += 1
                                    self.voteRejected = 0
                            else:
                                self.doMission = True
                                if self.voteRejected != 0:
                                    self.voteRejected = 0
                        if len(thisMatch['setting']) > 3:
                            thisMatch['setting'][3] = [self.goodScore, self.evilScore, self.voteRejected]
                    
                    if self.gamePhase == 7:
                        if self.missionSuccess == None:
                            failCount = self.countScore(5)
                            if failCount > 0:
                                if thisMatch['maxPlayer'] > 6 and self.round == 4:
                                    if failCount > 1:
                                        self.missionSuccess = False
                                    else:
                                        self.missionSuccess = True
                                else:
                                    self.missionSuccess = False
                            elif failCount == 0:
                                self.missionSuccess = True
                            
                            if self.missionSuccess:
                                self.goodScore += 1
                            elif not self.missionSuccess:
                                self.evilScore += 1
                            self.round += 1

                        if len(thisMatch['setting']) > 3:
                            thisMatch['setting'][3] = [self.goodScore, self.evilScore, self.voteRejected]

                if self.checkCondition():
                    self.gamePhase += 1
            
            if not thisMatch['playing']:
                self.gamePhase = 0
                self.round = 0
                self.playerRoles = []
                self.currentPartyLeader = None
                self.doMission = None
                self.missionSuccess = None
                self.voteRejected = 0
                self.goodScore = 0
                self.evilScore = 0

            # time delay for while loop
            time.sleep(0.001)








# change host to the next player near the host
def changeHost(addr):
    for i in range(len(thisMatch['players'])):
        if thisMatch['players'][i] != addr:
            thisMatch['host'] = thisMatch['players'][i]
            print(f"[SERVER] Host has been change to {thisMatch['host']}")
            break

def closeThread(conn, addr):
    try:
        # case host lost connection, need to change host
        if thisMatch['host'] == addr and len(thisMatch['players']) > 1:
            changeHost(addr)

        for i in range(len(thisMatch['players'])):
            # pop players from list
            if thisMatch['players'][i] == addr:
                thisMatch['players'].pop(i)
                break
        
        if thisMatch['players'] == [] and thisMatch['status'] == True:
            resetMatch()

        for i in range(len(thisMatch['data'])):
            if(thisMatch['data'][i][0] == addr):
                thisMatch['data'].pop(i)
                break
        
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
        print(f"[SERVER] {addr} Lost connection")
        
    except (Exception, socket.error) as e:
        print('[ERROR] Cannot close thread : ' + str(e))

def sendData(conn, data):
    try:
        conn.send(pickle.dumps(data))
    except (EOFError, socket.error) as e:
        print('[ERROR] Sending Data : ' + str(e))
    except Exception as e:
        print('[ERROR] Unknown exception, please take a look\n', str(e))


def handleSignal(signal, data, addr, conn):
    
    if signal == Signal.SET_MATCH:
        if thisMatch['status'] == False:
            thisMatch['status'] = True
            thisMatch['host'] = addr
            print(f'[SERVER] Match has been created by {addr}')
            sendData(conn, True)
        else:
            sendData(conn, False)

    if signal == Signal.SETTING_MATCH:
        newMaxPlayer = data[0]
        newSetting = data[1]
        if (not thisMatch['playing'] and 
            len(thisMatch['players']) <= newMaxPlayer and
            addr == thisMatch['host'] and
            thisMatch['status'] == True):
            thisMatch['maxPlayer'] = newMaxPlayer
            thisMatch['setting'] = newSetting
            sendData(conn, [True, 1])
        else:
            failStatus = 0
            if thisMatch['playing'] == True: failStatus = -1
            if len(thisMatch['players']) > newMaxPlayer : failStatus = -2
            if addr != thisMatch['host']: failStatus = -3
            if thisMatch['status'] == False: -4
            sendData(conn, [False, failStatus])


    if signal == Signal.END_MATCH:
        if thisMatch['status'] == True:
            resetMatch()
            sendData(conn, True)
        else:
            sendData(conn, False)

    if signal == Signal.JOIN:
        if ((thisMatch['status'] == True) and 
            (thisMatch['playing'] == False) and 
            (len(thisMatch['players']) < thisMatch['maxPlayer']) and
            (addr not in thisMatch['players'])):
            if thisMatch['host'] == addr:
                thisMatch['data'].append([addr, 1, data]) # format [<user_address>, <host or not>, <this user data>]
            else:
                thisMatch['data'].append([addr, 0, data])
            thisMatch['players'].append(addr)
            print(f'[SERVER] {addr} join the match.')
            sendData(conn, [True, 1])
        else:
            failStatus = 0
            if thisMatch['status'] == False: failStatus = -1
            if thisMatch['playing'] == True: failStatus = -2
            if len(thisMatch['players']) == thisMatch['maxPlayer']: failStatus = -3
            if addr in thisMatch['players']: failStatus = -4
            sendData(conn, [False, failStatus])
    
    ###### Need to join first vvv

    if signal == Signal.CLIENT_DATA:
        if addr in thisMatch['players']:
            othersClientData = []  # Exclude current client data
            for i in range(len(thisMatch['data'])):
                if thisMatch['data'][i][0] == thisMatch['host']: # always check for host (if there is a change)
                    thisMatch['data'][i][1] = 1
                if thisMatch['data'][i][0] == addr:
                    thisMatch['data'][i][2] = data # update data of this client
                else:
                    othersClientData.append(thisMatch['data'][i] + [i]) # get other [<address>, <host status>, <data>, <id>] data (element 1 and 2)
            sendData(conn, othersClientData)
        else:
            sendData(conn, None)
    
    if signal == Signal.GET_MATCH_PLAYERS:
        if addr in thisMatch['players']:
            sendData(conn, thisMatch['players'])
        else:
            sendData(conn, None)
    
    if signal == Signal.GET_MATCH_SETTING:
        if addr in thisMatch['players']:
            sendData(conn, [thisMatch['maxPlayer'], thisMatch['setting'], thisMatch['playing']])
        else:
            sendData(conn, None)
    
    if signal == Signal.START_MATCH:
        if (not thisMatch['playing'] and
            addr in thisMatch['players'] and
            addr == thisMatch['host']):
            thisMatch['playing'] = True
            sendData(conn, [True, 1])
        else:
            failStatus = 0
            if thisMatch['playing'] == True: failStatus = -1
            if addr not in thisMatch['players']: failStatus = -2
            if addr != thisMatch['host']: failStatus = -3
            sendData(conn, [False, failStatus])
    
    if signal == Signal.STOP_MATCH:
        if (thisMatch['playing'] and 
            addr in thisMatch['players'] and
            addr == thisMatch['host']):
            thisMatch['playing'] = False
            sendData(conn, [True, 1])
        else:
            failStatus = 0
            if thisMatch['playing'] == False: failStatus = -1
            if addr not in thisMatch['players']: failStatus = -2
            if addr != thisMatch['host']: failStatus = -3
            sendData(conn, [False, failStatus])


# Thread for each client
def threadedClient(conn, addr):

    sendData(conn, True) # send to client
    print(f"[SERVER] NEW CONNECTION {addr} Connected.")
    while True:
        try:
            rawData = conn.recv(SIZE)
            signal, data = pickle.loads(rawData)

            if signal == Signal.EXIT:
                print(f"[SERVER] {addr} Disconnected")
                break
            else:
                # print("[SERVER] Received: ", signal, data)
                handleSignal(signal, data, addr, conn)

        except (EOFError, socket.error) as e:
            print('[ERROR] ' + str(e))
            break
        except Exception as e:
            print('[ERROR] Unknown exception, please take a look\n', str(e))
            break

    closeThread(conn, addr)
    
# Start listen for connection
thisServer.listen()

gameEvent = GameEvent()

eventThread = threading.Thread(target= gameEvent.doEvent)
eventThread.daemon = True
eventThread.start()

while True:
    
    # Start accept incomming data
    conn, addr = thisServer.accept()
    # Start separate thread using "threadedClient" function
    thread = threading.Thread(target= threadedClient, args= (conn, addr))
    thread.start()
    print(f"[SERVER] ACTIVE CONNECTIONS {threading.activeCount() - 2}")





'''
print("[SERVER] Shutting down...")
thisServer.shutdown(socket.SHUT_RDWR)
thisServer.close()
'''