from unittest import TestCase
import sys
import socket

class KeyServerTest(TestCase):
    def setUp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 8000
        self.publicKey = [1519, 568, 819, 2140, 1110, 926, 1852, 522]
        self.id = 8001
        self.BUFFER_SIZE = 1024

    def testServerResponses(self):
        self.s.connect((self.TCP_IP, self.TCP_PORT))
        data = self.s.recv(self.BUFFER_SIZE)
        data = data.decode('ascii')
        if data != '':
            print(data)

        mess = 'registerPubKey ' + str(self.id) + ' ' + str(self.publicKey)
        data = self.sendAndRecieve(mess)
        self.assertEqual('Succsessfuly registered', data)

        mess = 'registerPubKey ' + str(self.id) + ' ' + str(self.publicKey)
        data = self.sendAndRecieve(mess)
        self.assertEqual('Succsessfuly updated the pubkey', data)

        mess = 'getUserIds'
        data = self.sendAndRecieve(mess)
        self.assertEqual('[' + str(self.id) + ']', data)

        mess = 'getPublicKey ' + str(self.id)
        data = self.sendAndRecieve(mess)
        self.assertEqual(str(self.publicKey), data)

        mess = 'getPublicKey ' + str(self.id + 1)
        data = self.sendAndRecieve(mess)
        self.assertEqual("Invalid id", data)

        mess = 'Exit'
        mess = str.encode(mess)
        self.s.send(mess)
        self.s.close()

    def sendAndRecieve(self, mess):
        mess = str.encode(mess)
        self.s.send(mess)
        data = self.s.recv(self.BUFFER_SIZE)
        data = data.decode('ascii')
        if data != '':
            print(data)
        return data
