# Mihaly Laszlo 523 mlim1850
import socket
from threading import Thread
import sys
import crypto

TCP_IP = '127.0.0.1'
TCP_PORT = 8000
BUFFER_SIZE = 1024
PRIVATE_TCP_PORT = -1
PRIVATE_KEY = ()
PUBLIC_KEY = []

def recieve(s):
    try:
        data = s.recv(BUFFER_SIZE)
        data = data.decode('ascii')
        if data != '':
            print(data)
        return data
    except Exception as e:
        print(e)

def recieve_as_server(conn):
    try:
        data = conn.recv(BUFFER_SIZE)
        data = data.decode('ascii')
        if data != '':
            print(data)
        return data
    except Exception as e:
        print(e)

def communicate_with_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    print('Start')
    print('Welcome to the chat, what do you want to do?:\n'+
                    'registerPubKey + arg[0] - clientid + arg[1] - pubkey\n'+
                    'getPublicKey + arg[0] - clientid\n'+
                    'getUserIds\n'+
                    'exit\n')
    recieve(s)
    exit = 0
    while exit == 0:
        try:
            MESSAGE = input('Uzenet:')
            if MESSAGE != "" :
                bin = str.encode(MESSAGE)
                s.send(bin)
                recieve(s)
                if MESSAGE == 'exit':
                    s.close()
                    exit = 1
        except Exception as e:
            print(e)
            s.close()
            break
    print('End of communication with the KeyServer')

def getPublicKeyOfUser(clientId):
    print(" Getting the public key of user ", clientId)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((TCP_IP, TCP_PORT))

    recieve(serverSocket)

    mess = 'getPublicKey ' + str(clientId)
    mess = str.encode(mess)
    serverSocket.send(mess)

    pubKey = recieve(serverSocket)
    print(pubKey)
    return deserializeStringList(pubKey)

def registrate_public_key(Id):
    global PRIVATE_TCP_PORT
    PRIVATE_TCP_PORT = int(Id)
    global PRIVATE_KEY
    PRIVATE_KEY = crypto.generate_private_key()
    global PUBLIC_KEY
    PUBLIC_KEY = crypto.create_public_key(PRIVATE_KEY)
    print("PRIVATE_TCP_PORT ", PRIVATE_TCP_PORT)
    print("PRIVATE_KEY ", PRIVATE_KEY)
    print("PUBLIC_KEY ", PUBLIC_KEY)

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.connect((TCP_IP, TCP_PORT))

    recieve(serverSocket)

    mess = 'registerPubKey ' + str(Id) + ' ' + str(PUBLIC_KEY)
    mess = str.encode(mess)
    serverSocket.send(mess)

    recieve(serverSocket)

def routing():
    print('init communicating')
    while True:
        try:
            MESSAGE = input('Options: - communicating with others by Id: Command -> ById + id\n'+
                            '         - communicating with the Keyserver: Command -> Server\n' +
                            '         - registration on server: Command -> Registration + id\n' +
                            '         - exit program: Command -> Exit\n' +
                            '         - listening for cummunication: Command -> Listening\n')

            if MESSAGE.split(' ')[0] == "ById":
                communicate_with_client(int(MESSAGE.split(' ')[1]))

            if MESSAGE.split(' ')[0] == "Server":
                communicate_with_server()

            if MESSAGE.split(' ')[0] == "Listening":
                listening_for_communication()

            if MESSAGE.split(' ')[0] == "Registration":
                registrate_public_key(MESSAGE.split(' ')[1])

            if MESSAGE.split(' ')[0] == "Exit":
                sys.exit()

        except Exception as e:
            print(e)
            sys.exit()

def sendHello(clientId, clientPubKey):
    print(" Sending hello to user",clientId, ", with Public key", clientPubKey )
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, clientId))
    mess = crypto.encrypt_mh('Hello from ' + str(PRIVATE_TCP_PORT), clientPubKey)
    mess = str.encode(str(mess))
    s.send(mess)
    mess = recieve(s)
    mess = deserializeStringList(mess)
    mess = crypto.decrypt_mh(mess, PRIVATE_KEY)
    print("mess",mess)
    return s

def sendHalfSecret(s, halfSecret, clientPubKey):
    mess = crypto.encrypt_mh(halfSecret, clientPubKey)
    mess = str.encode(str(mess))
    s.send(mess)

def communicate_with_client(clientId):
    clientPubKey = getPublicKeyOfUser(clientId)
    s = sendHello(clientId, clientPubKey)
    halfSecret = crypto.generate_random_secret()
    sendHalfSecret(s, halfSecret, clientPubKey)

    # Getting the other half of the secret
    mess = recieve(s)
    mess = deserializeStringList(mess)
    secretPartTwo = crypto.decrypt_mh(mess, PRIVATE_KEY)

    # generate_common_secret, init deck
    common_secret = crypto.generate_common_secret(halfSecret, secretPartTwo)
    deck = crypto.init_deck(common_secret)
    base_deck = deck.copy()
    print(deck)

    # communicating with the other one
    myoffset = 0
    messageFromOther = ''

    while(messageFromOther != 'bye'):
        # Message to the other
        message = input('Message to ' + str(clientId) + ": ")
        encr_message, deck, myoffset = crypto.encrypt_message_solitaire(message, deck, myoffset)
        print("DOLGOK: ", encr_message, deck, myoffset)
        mess = str.encode(str(myoffset - len(message)) + ':' + encr_message)
        s.send(mess)

        # Response message
        messageFromOther = recieve(s).split(':')
        offset = int(messageFromOther[0])
        encMess = messageFromOther[1]
        concreteMessage, deck, myoffset = crypto.decrypt_message_solitaire(encMess, deck, base_deck, offset, myoffset)

        print('Message From ' + str(clientId) + ": " + concreteMessage)

        messageFromOther = concreteMessage

        if messageFromOther == 'bye' and message != 'bye':
            message = 'bye'
            encr_message, deck, myoffset = crypto.encrypt_message_solitaire(message, deck, myoffset)
            mess = str.encode(str(myoffset) + ':' + encr_message)
            s.send(mess)


def deserializeStringList(stringList):
    return [int(x) for x in stringList.strip('][').split(', ')]

def listening_for_communication():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, PRIVATE_TCP_PORT))
        s.listen(1)

        conn, addr = s.accept()
        mess = recieve_as_server(conn)
        mess = deserializeStringList(mess)

        mess = crypto.decrypt_mh(mess, PRIVATE_KEY)
        print("mess",mess)
        clientId = 0

        if mess.split(' ')[0] == "Hello":
            clientId = int(mess.split(' ')[2])

        clientPubKey = getPublicKeyOfUser(clientId)

        mess = crypto.encrypt_mh('Hello from ' + str(PRIVATE_TCP_PORT), clientPubKey)
        mess = str.encode(str(mess))
        conn.send(mess)

        # Generate random secret, getting secret from the other party
        halfSecret = crypto.generate_random_secret()
        mess = recieve_as_server(conn)
        mess = deserializeStringList(mess)
        secretPartOne = crypto.decrypt_mh(mess, PRIVATE_KEY)

        # Sending the other part of the secret to the other one
        mess = crypto.encrypt_mh(halfSecret, clientPubKey)
        mess = str.encode(str(mess))
        conn.send(mess)

        # generate_common_secret, init deck
        common_secret = crypto.generate_common_secret(secretPartOne, halfSecret)
        deck = crypto.init_deck(common_secret)
        print(deck)
        base_deck = deck.copy()

        # communicating with the other one
        myoffset = 0
        messageFromOther = ''

        while(messageFromOther != 'bye'):

            # Response message
            messageFromOther = recieve_as_server(conn).split(':')
            print(messageFromOther)
            offset = int(messageFromOther[0])
            encMess = messageFromOther[1]
            concreteMessage, deck, myoffset = crypto.decrypt_message_solitaire(encMess, deck, base_deck, offset, myoffset)

            print('Message From ' + str(clientId)  + ": " + concreteMessage)

            messageFromOther = concreteMessage

            if concreteMessage == 'bye':
                message = 'bye'
                encr_message, deck, myoffset = crypto.encrypt_message_solitaire(message, deck, myoffset)
                mess = str.encode(str(myoffset  - len(message)) + ':' + encr_message)
                conn.send(mess)
                break


            # Message to the other
            message = input('Message to ' + str(clientId) + ": ")
            encr_message, deck, myoffset = crypto.encrypt_message_solitaire(message, deck, myoffset)
            mess = str.encode(str(myoffset  - len(message)) + ':' + encr_message)
            conn.send(mess)

            if message == 'bye':
                messageFromOther = recieve_as_server(conn).split(':')
                offset = int(messageFromOther[0])
                encMess = messageFromOther[1]
                concreteMessage, deck, myoffset = crypto.decrypt_message_solitaire(encMess, deck, base_deck, offset, myoffset)
                if concreteMessage == 'bye':
                    messageFromOther = concreteMessage
                    break



    except Exception as e:
        print(e)

# communicate_with_server()

# peer_to_peer_communication()

routing()
