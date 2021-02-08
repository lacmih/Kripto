from unittest import TestCase
import sys

sys.path.append('../')
import crypto

class MerkleHellmanTest(TestCase):
    def setUp(self):
        self.PRIVATE_KEY = crypto.generate_private_key()
        self.PUBLIC_KEY = crypto.create_public_key(self.PRIVATE_KEY)

    def testMessaging(self):
        self.message = 'hello'

        encrypted_message = crypto.encrypt_mh(self.message, self.PUBLIC_KEY)
        decrypted_message = crypto.decrypt_mh(encrypted_message, self.PRIVATE_KEY)

        self.assertEqual(self.message, decrypted_message)
