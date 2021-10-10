import socket
import threading
import pickle
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
        
        if thisMatch['players'] == []:
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

    if signal == Signal.END_MATCH:
        if thisMatch['status'] == True:
            resetMatch()
            sendData(conn, True)
        else:
            sendData(conn, False)

    if signal == Signal.JOIN:
        if (thisMatch['status'] == True) and (thisMatch['playing'] == False) and (len(thisMatch['players']) < thisMatch['maxPlayer']):
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
            sendData(conn, [False, failStatus])

    if signal == Signal.CLIENT_DATA:
        if addr in thisMatch['players']:
            othersClientData = []  # Exclude current client data
            for i in range(len(thisMatch['data'])):
                if thisMatch['data'][i][0] == thisMatch['host']: # always check for host (if there is a change)
                    thisMatch['data'][i][1] = 1
                if thisMatch['data'][i][0] == addr:
                    thisMatch['data'][i][2] = data # update data of this client
                else:
                    othersClientData.append(thisMatch['data'][i][1:3]) # get other match['data'] data (element 1 and 2)
            sendData(conn, othersClientData)
        else:
            sendData(conn, None)


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


while True:

    # Start accept incomming data
    conn, addr = thisServer.accept()
    # Start separate thread using "threadedClient" function
    thread = threading.Thread(target= threadedClient, args= (conn, addr))
    thread.start()
    print(f"[SERVER] ACTIVE CONNECTIONS {threading.activeCount() - 1}")


'''
print("[SERVER] Shutting down...")
thisServer.shutdown(socket.SHUT_RDWR)
thisServer.close()
'''