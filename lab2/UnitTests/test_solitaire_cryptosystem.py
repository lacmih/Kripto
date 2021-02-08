from unittest import TestCase
import sys

sys.path.append('../')
import crypto

class SolitaireTest(TestCase):
    def setUp(self):
        self.halfSecretOne = crypto.generate_random_secret()
        self.halfSecretTwo = crypto.generate_random_secret()
        self.commonSecret = crypto.generate_common_secret(self.halfSecretOne, self.halfSecretTwo)
        self.deck1 = crypto.init_deck(self.commonSecret)
        self.deck2 = self.deck1.copy()
        self.base_deck = self.deck2.copy()
        self.offset1 = 0
        self.offset2 = 0

    def testMessaging(self):
        message = 'szia'

        # Encrypting the message
        encr_mess, self.deck1, self.offset1 = crypto.encrypt_message_solitaire(message, self.deck1, self.offset1)
        print(encr_mess)

        # Decrypting
        plain_text, self.deck2, self.offset2 = crypto.decrypt_message_solitaire(encr_mess,
            self.deck2, self.base_deck, self.offset2, self.offset1 - len(encr_mess))
        print(plain_text)

        # Check if the other one decrypted it properly
        self.assertEqual(plain_text, message)

    def testOffsetDifference(self):
        self.offset1 = 0
        self.offset2 = 0
        message = 'szia'

        # Simulating that he transferred 3 character, but the other did not get it
        encr_mess, self.deck2, self.offset2 = crypto.encrypt_message_solitaire('asd', self.deck2, self.offset2)
        print(encr_mess)

        # Encrypting the message by the second participant
        encr_mess, self.deck2, self.offset2 = crypto.encrypt_message_solitaire(message, self.deck2, self.offset2)
        print(encr_mess)

        # Decrypting by the first(the offset will not be okey,
        # myofset(self.offset1) will be less than needed)
        plain_text, self.deck1, self.offset1 = crypto.decrypt_message_solitaire(encr_mess,
            self.deck1, self.base_deck, self.offset2 - len(encr_mess), self.offset1)
        print(plain_text)

        # Check if the other one decrypted it properly
        self.assertEqual(plain_text, message)

    def testOffsetDifference2(self):

        self.offset1 = 0
        self.offset2 = 0
        message = 'szia'

        # Simulating that the first one transferred 3 character, but the other did not get it
        encr_mess, self.deck1, self.offset1 = crypto.encrypt_message_solitaire('asd', self.deck1, self.offset1)
        print(encr_mess)

        # Encrypting the message by the second participant
        encr_mess, self.deck2, self.offset2 = crypto.encrypt_message_solitaire(message, self.deck2, self.offset2)
        print(encr_mess)

        # Decrypting by the first(the offset will not be okey,
        # myofset(self.offset1) will be higher than expected)
        plain_text, self.deck1, self.offset1 = crypto.decrypt_message_solitaire(encr_mess,
            self.deck1, self.base_deck, self.offset2 - len(encr_mess), self.offset1)
        print(plain_text)

        # Check if the other one decrypted it properly
        self.assertEqual(plain_text, message)










pass
