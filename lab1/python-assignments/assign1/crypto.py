"""Assignment 1.

Name: Mihály László
Id: mlim1850

"""
import utils
import string
import math
import numpy as np

#################
# CAESAR CIPHER #
#################

def encrypt_caesar(plaintext):
    return ''.join(map(lambda x: x if (x not in string.ascii_uppercase) else \
    chr(ord(x) + 3) if chr(ord(x) + 3) <= "Z" else chr(ord(x) - 23), plaintext))

def decrypt_caesar(ciphertext):
    return ''.join(map(lambda x: x if (x not in string.ascii_uppercase) else \
    chr(ord(x) - 3) if chr(ord(x) - 3) >= "A" else chr(ord(x) + 23), ciphertext))

###################
# VIGENERE CIPHER #
###################

def encrypt_vigenere(plaintext, keyword):
    keyword *= math.ceil(len(plaintext) / len(keyword))
    text = list(zip(plaintext, keyword))
    return ''.join(map(lambda x: chr(ord(x[0]) + ord(x[1]) - 65) if chr(ord(x[0]) + ord(x[1]) - 65) <= "Z"
    else chr(ord(x[0]) + ord(x[1]) - 65 - 26), text))


def decrypt_vigenere(ciphertext, keyword):
    keyword = keyword.upper()
    keyword *= math.ceil(len(ciphertext) / len(keyword))
    text = list(zip(ciphertext, keyword))
    return ''.join(map(lambda x: x[0] if ord(x[0]) < 65 or ord(x[0]) > 90 else chr(ord(x[0]) - ord(x[1]) + 65) if chr(ord(x[0]) - ord(x[1]) + 65) >= "A"
    else chr(ord(x[0]) - ord(x[1]) + 65 + 26), text))

##################
# SCYTALE CIPHER #
##################

def encrypt_scytale(plaintext, circumference):
    j = 0
    s = ''
    for i in range(len(plaintext)):
        s += plaintext[j]
        j += circumference
        if j >= len(plaintext):
            while j >= len(plaintext):
                j -= len(plaintext)
            j += 1
    return s
    #return ''.join([x for x in range(0, len(plaintext), circumference)])

def decrypt_scytale(ciphertext, circumference):
    j = 0
    s = ''
    if circumference > len(ciphertext):
        return ciphertext
    for i in range(len(ciphertext)):
        s += ciphertext[j]
        j += circumference - 1
        if j >= len(ciphertext):
            while j >= len(ciphertext):
                j -= len(ciphertext)
            j += 1
    return s

####################
# Railfence Cipher #
####################

def encrypt_railfence(plaintext, num_rails):
    m = (num_rails - 1) * 2
    s = ''
    for i in range(num_rails):
        if i % (num_rails - 1) == 0:
            s += plaintext[i::m]
        else:
            char_pairs = zip(plaintext[i::m], list(plaintext[m-i::m]) + [''])
            s += ''.join(map(''.join, char_pairs))
    return s

def decrypt_railfence(ciphertext, num_rails):

    positions = list(encrypt_railfence(''.join([chr(i) for i in range(len(ciphertext))]), num_rails))

    for i in range(len(ciphertext)):
        positions[i] = ord(positions[i])

    plaintext = list(ciphertext)

    for (i,k) in enumerate(positions):
        plaintext[k] = ciphertext[i]

    return ''.join(plaintext)

########################################
# MERKLE-HELLMAN KNAPSACK CRYPTOSYSTEM #
########################################

def generate_private_key(n=8):
    """Generate a private key to use with the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key
    components of the MH Cryptosystem. This consists of 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        Note: You can double-check that a sequence is superincreasing by using:
            `utils.is_superincreasing(seq)`
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q`
        Note: You can use `utils.coprime(r, q)` for this.

    You'll also need to use the random module's `randint` function, which you
    will have to import.

    Somehow, you'll have to return all three of these values from this function!
    Can we do that in Python?!

    :param n: Bitsize of message to send (defaults to 8)
    :type n: int

    :returns: 3-tuple private key `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    # Your implementation here.
    raise NotImplementedError('generate_private_key is not yet implemented!')


def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in
    the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one or two lines using list comprehensions.

    :param private_key: The private key created by generate_private_key.
    :type private_key: 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    :returns: n-tuple public key
    """
    # Your implementation here.
    raise NotImplementedError('create_public_key is not yet implemented!')


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    Following the outline of the handout, you will need to:
    1. Separate the message into chunks based on the size of the public key.
        In our case, that's the fixed value n = 8, corresponding to a single
        byte. In principle, we should work for any value of n, but we'll
        assert that it's fine to operate byte-by-byte.
    2. For each byte, determine its 8 bits (the `a_i`s). You can use
        `utils.byte_to_bits(byte)`.
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk of the message.

    Hint: Think about using `zip` and other tools we've discussed in class.

    :param message: The message to be encrypted.
    :type message: bytes
    :param public_key: The public key of the message's recipient.
    :type public_key: n-tuple of ints

    :returns: Encrypted message bytes represented as a list of ints.
    """
    # Your implementation here.
    raise NotImplementedError('encrypt_mh is not yet implemented!')


def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key.

    Following the outline of the handout, you will need to:
    1. Extract w, q, and r from the private key.
    2. Compute s, the modular inverse of r mod q, using the Extended Euclidean
        algorithm (implemented for you at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum problem using c' and w to recover
        the original plaintext byte.
    5. Reconstitute the decrypted bytes to form the original message.

    :param message: Encrypted message chunks.
    :type message: list of ints
    :param private_key: The private key of the recipient (you).
    :type private_key: 3-tuple of w, q, and r

    :returns: bytearray or str of decrypted characters
    """
    # Your implementation here.
    raise NotImplementedError('decrypt_mh is not yet implemented!')


########################
#INTELLIGEN CODEBREAKER#
########################

def codebreak_vigenere(ciphertext, possible_key):
    f = open("american-english.txt", "r")
    keytexts = f.readlines()
    keytexts = [x.strip().upper() for x in keytexts]
    # ciphertext = ciphertext.strip()
    # print(ciphertext)
    wordcount = 0
    key = ''
    plaintext = ''

    for i in keytexts:
        # print(i)
        word_count = 0
        text = decrypt_vigenere(ciphertext, i)
        #print(text)
        for j in keytexts:
            if j.upper() in text:
                word_count += 1
            # print(word_count)
            if(word_count > wordcount):
                wordcount = word_count
                key = j
                plaintext = text
                # print(word_count)
                # print(key)
                # print(plaintext)
    print(plaintext)
    print(key)
    # print(keytexts)

def initCaesar(codes, lenCodes):
    encryptedMsg = ''
    decryptedMsg = ''
    for i in range(0, lenCodes, 2):
        currentEncryption = encrypt_caesar(codes[i])
        encryptedMsg = encryptedMsg + ' ' + currentEncryption
        decryptedMsg = decryptedMsg + ' ' + decrypt_caesar(currentEncryption)

    return ('Encrypted message: ' + encryptedMsg, 'Decrypted message: ' + decryptedMsg)

def initVigenere(codes, lenCodes):
    encryptedMsg = ''
    decryptedMsg = ''
    original = ''
    for i in range(0, lenCodes, 3):
        keyWord = codes[i+1]
        original += ' ' + codes[i]
        currentEncryption = encrypt_vigenere(codes[i], keyWord)
        encryptedMsg = encryptedMsg + ' ' + currentEncryption
        decryptedMsg = decryptedMsg + ' ' + decrypt_vigenere(currentEncryption, keyWord)

    print(original)
    return ('Encrypted message: ' + encryptedMsg, 'Decrypted message: ' + decryptedMsg)

def readTexts(fileName, encryptionType):
    with open(fileName, "r") as f:
        codes = f.read().split()

    return (codes, int(len(codes)))

def main():
    codes, lenCodes = readTexts('./tests/caesar-tests.txt', 'caesar')
    encryptedMsg, decryptedMsg = initCaesar(codes, lenCodes)
    print(encryptedMsg + '\n' + decryptedMsg)

    codes, lenCodes = readTexts('./tests/vigenere-tests.txt', 'vigenere')
    encryptedMsg, decryptedMsg = initVigenere(codes, lenCodes)
    print(encryptedMsg + '\n' + decryptedMsg)

    print(encrypt_scytale("IAMHURTVERYBADLYHELP", 5))
    print(decrypt_scytale("IRYYATBHMVAEHEDLURLP", 5))

    print(encrypt_railfence("WEAREDISCOVEREDFLEEATONCE", 3))
    print(decrypt_railfence("WECRLTEERDSOEEFEAOCAIVDEN", 3))

    # codebreak_vigenere("BRG ACL! ZCPPCSC NHQ Q CFV FI TTCR KUUG GQI'IR CADGGKVANBKBX GBVA CGJVAAUGBK! FI, LWW'FV CLBJCPCL CABGFVFNRL VC JRY JPCH KUCF VQH JB MRKTSK ZYFACUV VM? NB VVZF JBQPH, Z'Z DHAV OUQCAO C ZFG IS BGLK FI GPCH ZG'M RIUWVE ZBZ ACL GI QMEFPCN GPKG. ZG QBZMG SRNGMT WW V LRAVOKR LRAVOKR LRAVOKR LRAVOKR LRAVOKR QBZFG KUUG ITS KUY FIOS CRHTBJ OJ GBR SGM (RAX, DCKHV UIAMUHCL, C JIPHVQ NB ACM IRJRIV, PLG NUM MSP UUF AGJVA FRBVSIF... NUMUOLEOF BQ HYR LRAEIV!). OOG EJOK NLR BJS FQXF GQI AHMG OWSJFYQ BJS BRS NVAKRL? QRTN, GZAWR GQI DNXR QV HYVM SIT, KYL XBV'V MFH GNSG O GECIIVS GBMG WP DZNTMI YWKU NUM USTEYG XJFRFY OWOPRFNVK ROIEIG IPR Z'YF TMV MFH U AQES 10 VKNEI DCEHM CWKBKF.", 1)

if __name__ == "__main__":
    main()
