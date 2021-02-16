#Mihaly Laszlo 523 mlim1850
import socket
import _thread
import sys
import time
import datetime

TCP_IP = '127.0.0.1'
TCP_PORT = 8000
BUFFER_SIZE = 1024
print("TCP_IP: " + str(TCP_IP))
print("TCP_PORT: " + str(TCP_PORT))

client_id = []
client_public_key = []
client_conn = []

def process_response(conn):
    print('varom az uzenetet hogy milyen tipusu lesz az uzenet')
    cli_req = conn.recv(1024).decode("ascii")
    print("Recieved client request: " + cli_req)
    command_validity = 0

    if cli_req.split(' ')[0] == 'registerPubKey':
        command_validity = 1
        try:
            print(cli_req.split(' ', 2)[1], client_id)
            if int(cli_req.split(' ', 2)[1]) in client_id:
                index = client_id.index(int(cli_req.split(' ', 2)[1]))
                client_public_key[index] = cli_req.split(' ', 2)[2]
                conn.sendall(b'Succsessfuly updated the pubkey')
            else:
                client_id.append(int(cli_req.split(' ', 2)[1]))
                client_public_key.append(cli_req.split(' ', 2)[2])
                conn.sendall(b'Succsessfuly registered')
            print(client_id)
            print(client_public_key)
        except Exception as e:
            print(e)

    if cli_req.split(' ')[0] == 'getPublicKey':
        command_validity = 1
        try:
            print(cli_req.split(' ')[1])
            print(client_id)
            print(client_public_key)
            if int(cli_req.split(' ')[1]) in client_id:
                index = client_id.index(int(cli_req.split(' ')[1]))
                print(index)
                mess = '' + str(client_public_key[index])
                mess = str.encode(mess)
                conn.sendall(mess)
            else:
                mess = 'Invalid id'
                mess = str.encode(mess)
                conn.sendall(mess)
        except Exception as e:
            print(e)

    if cli_req.split(' ')[0] == 'getUserIds':
        command_validity = 1
        mess = '' + str(client_id)
        mess = str.encode(mess)
        conn.sendall(mess)

    if cli_req.split(' ', 1)[0] == 'exit':
        command_validity = 1
        conn.sendall(b'Bye')
        conn.close()

    if command_validity == 0:
        conn.sendall(b'Unknown command')

def kliens_thread(conn, addr):
    print("Kezdet thread")
    conn.sendall(b'Welcome to the KeyServer')
    while True:
        try:
            process_response(conn)

        except Exception as e:
            print(e)
            break

    print("-------------VEGE A THREADNEK A KLIENSSEL--------------")
    conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

data = ""
try:
    while 1:
        conn, addr = s.accept()
        print ('Connection address:', addr)
        _thread.start_new_thread( kliens_thread, (conn,addr))
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\nA szervert leallitottak\n")
    sys.exit(0)
