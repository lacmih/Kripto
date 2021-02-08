"""Assignment 2.

Name: Mihály László
Id: mlim1850

"""
import utils
import string
import math
import numpy as np
import random

########################################
# MERKLE-HELLMAN KNAPSACK CRYPTOSYSTEM #
########################################

def gcd(p,q):
    while q != 0:
        p, q = q, p%q
    return p

def is_coprime(x, y):
    return gcd(x, y) == 1

def generate_private_key(n=8):

    act = random.randint(2,10)
    sum = act
    w = [act] #The superincreasing sequence

    for i in range(n - 1):
        act = random.randint(sum + 1, 2 * sum)
        sum += act
        w.append(act)

    q = random.randint(sum + 1, 2 * sum)
    r = random.randint(2, q-1)

    while is_coprime(r, q) == False:
        r = random.randint(2, q-1)

    print("w = ",w)
    print("q, r = ",q,r)

    return (w, q, r)

def create_public_key(private_key):

    w = private_key[0]
    q = private_key[1]
    r = private_key[2]
    b = []

    for i in range(len(w)):
        b.append(r * w[i] % q)

    print("b = ",b)

    return b


def encrypt_mh(message, public_key):
    """
    :param message: The message to be encrypted.
    :type message: bytes
    :param public_key: The public key of the message's recipient.
    :type public_key: n-tuple of ints

    :returns: Encrypted message bytes represented as a list of ints.
    """
    print('Encrypting message (crypto.py) ' + message)
    n = len(public_key)

    encrypt_mh = []
    k = 0

    for i in range(math.ceil(len(message) / (int(n/8)))):
        a = []
        l = []

        for j in range(int(n/8)):
            l = list(utils.byte_to_bits(ord(message[k])))
            k += 1
            a += l
            if k >= len(message):
                message += '\0'

        c = 0

        for j in range(len(public_key)):
            c += a[j] * public_key[j]

        encrypt_mh.append(c)

    print("Encrypted message (crypto.py)",encrypt_mh)
    return encrypt_mh


def decrypt_mh(message, private_key):
    """
    :param message: Encrypted message chunks.
    :type message: list of ints
    :param private_key: The private key of the recipient (you).
    :type private_key: 3-tuple of w, q, and r

    :returns: bytearray or str of decrypted characters
    """
    print('Decrypting message (crypto.py) ' + str(message))
    # Your implementation here.
    (w, q, r) = private_key

    s = utils.modinv(r, q)

    c = []

    for i in message:
        c.append((i * s) % q)

    plain_in_bits = []

    for i in c:
        helper = []
        for j in w[::-1]:
            if j <= i:
                i -= j
                helper.insert(0,1)
            else:
                helper.insert(0,0)
        plain_in_bits += helper

    plain = ''
    for i in range(math.ceil(len(plain_in_bits) / 8)):
        plain += (chr(utils.bits_to_byte(plain_in_bits[i * 8 : i * 8 + 8])))

    print("Plain text (crypto.py)", plain)
    return plain

#######################SOLITAIRE ENCRYPTION#########################

def encrypt_message_solitaire(message, deck, myoffset):
    encr_mess = ''
    print(message, deck, myoffset)
    for i in message:
        key_value, deck = generate_keystream_letter(deck)
        # print('A')
        # print(deck, key_value)
        # print('A')
        if ord(i) < 91:
            i = ord(i) - 65
            i = (key_value + i) % 26
            encr_mess += chr(i + 65)
        else:
            i = ord(i) - 97
            i = (key_value + i) % 26
            encr_mess += chr(i + 97)

    # print('Crypto encrypt with soli return')
    return (encr_mess, deck, myoffset + len(message))

def decrypt_message_solitaire(encr_message, deck, base_deck, offset, myoffset):
    plain_text = ''
    # print(deck)

    if offset != myoffset:
        print('Üzenetvesztés történt')
        if myoffset < offset:
            while myoffset != offset:
                _, deck = generate_keystream_letter(deck)
                myoffset += 1
        else:
            myoffset = 0
            deck = base_deck.copy()
            while myoffset != offset:
                _, deck = generate_keystream_letter(deck)
                myoffset += 1

    for i in encr_message:
        key_value, deck = generate_keystream_letter(deck)
        # print('B')
        # print(deck, key_value)
        # print('B')
        if ord(i) < 91:
            i = ord(i) - 65
            i = (i - key_value) % 26
            plain_text += chr(i + 65)
        else:
            i = ord(i) - 97
            i = (i - key_value) % 26
            plain_text += chr(i + 97)

    return (plain_text, deck, myoffset + len(encr_message))

def generate_random_secret():
    chars = string.ascii_uppercase
    n = 100
    return ''.join(random.choice(chars) for _ in range(n))

def generate_common_secret(s1, s2):
    return "".join([chr((ord(a) - 65 + ord(b) - 65) % 26 + 65) for a,b in zip(s1, s2)])

def init_deck(key):
    deck = list(range(1,55))
    jokerA = 53
    jokerB = 54
    offsets = [ord(x) - 96 if ord(x) >= ord('a') else ord(x) - 64 for x in list(key)]
    for i in offsets:
        # step 1
        index_jokerA, deck = step1(deck, jokerA)
        # print(deck)
        # print('after step1: ' + str(len(deck)))

        # step 2
        index_jokerB, deck =  step2(deck, jokerB)
        # print(deck)
        # print('after step2: ' + str(len(deck)))

        # step 3
        deck = step3(index_jokerA, index_jokerB, deck)
        # print(deck)
        # print('after step3: ' + str(len(deck)))

        # step4
        bottom_card = deck[53]
        deck = step4(bottom_card, deck)
        # print(deck)
        # print('after step4: ' + str(len(deck)))

        # altered step4
        deck = step4(i, deck)
        # print(deck)
        # print('after altered step4: ' + str(len(deck)))
    return deck

def generate_keystream_letter(deck):
    # print('Generating_letter, deck: ')
    # print(deck)
    b = True
    jokerA = 53
    jokerB = 54
    index_jokerA = -1
    index_jokerB = -1

    while b == True:
        b = False

        # step 1
        index_jokerA, deck = step1(deck, jokerA)
        # print('------------------STEP1----------------')
        # print(deck)
        # print('---------------------------------------')

        # step 2
        index_jokerB, deck = step2(deck, jokerB)
        # print('------------------STEP2----------------')
        # print(deck)
        # print('---------------------------------------')

        # step 3
        deck = step3(index_jokerA, index_jokerB, deck)
        # print('------------------STEP3----------------')
        # print(deck)
        # print('---------------------------------------')

        # step4
        bottom_card = deck[53]
        deck = step4(bottom_card, deck)
        # print('------------------STEP4----------------')
        # print(deck)
        # print('---------------------------------------')

        # step 5
        bottom_card = deck[53]

        card_value = cardConversion(deck, bottom_card)

        card = deck[card_value]
        if card == 53:
            b = True

        # step 6
        if b == False:
            card_value = cardConversion(deck, card)
            if card_value > 26:
                card_value -= 26
            return card_value, deck

def step1(deck, jokerA):
    index_jokerA = deck.index(jokerA)
    if index_jokerA == 53:
        deck = rotate(deck, 1)
        index_jokerA = 0
    swapPositions(deck, index_jokerA, index_jokerA + 1)
    index_jokerA += 1
    return index_jokerA, deck

def step2(deck, jokerB):
    index_jokerB = deck.index(jokerB)
    if index_jokerB >= 52:
        deck = rotate(deck, 2)
        index_jokerB = 0 - (52 - index_jokerB)
    swapPositions(deck, index_jokerB, index_jokerB + 1)
    swapPositions(deck, index_jokerB + 1, index_jokerB + 2)
    index_jokerB += 2
    return index_jokerB, deck

def step3(index_jokerA, index_jokerB, deck):
    # print('--------------------STEP3!!!!!!!!!!!!!!!!')
    # print(index_jokerA, index_jokerB)
    if index_jokerA < index_jokerB:
        first_joker_index = index_jokerA
        second_joker_index = index_jokerB
    else:
        first_joker_index = index_jokerB
        second_joker_index = index_jokerA
    deck = deck[second_joker_index + 1:] + deck[first_joker_index : second_joker_index + 1] + deck[:first_joker_index]
    return deck

def step4(bottom_card, deck):

    card_value = cardConversion(deck, bottom_card)

    deck = deck[card_value:53] + deck[0:card_value] + deck[53:]

    return deck

def cardConversion(deck, bottom_card):
    card_value = bottom_card
    if bottom_card >= 53:
        card_value = 53
    return card_value


def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

def rotate(l, n):
    return l[-n:] + l[:-n]

# deck2 = init_deck("DFLKEGKLVKOKEMASFOVLASDvmskdfelwl")
# base_deck = deck2.copy()
# mess, deck2, myoffset = encrypt_message_solitaire('szia', deck2, 0)
# print(mess)
# plain_text, deck3, myoffset = decrypt_message_solitaire(mess, base_deck, base_deck, 0, 0)
# print(plain_text)

# deck = [37, 41, 45, 19, 35, 17, 15, 7, 22, 48, 25, 51, 50, 39, 12, 30, 31, 24, 5, 32, 54, 42, 2, 53, 20, 33, 36, 13, 18, 46, 29, 40, 1, 34, 3, 44, 11, 26, 4, 6, 14, 38, 9, 23, 21, 47, 16, 49, 52, 28, 8, 43, 10, 27]
# mess, deck, myoffset = encrypt_message_solitaire('szia', deck, 0)
