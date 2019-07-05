import os
import random

# ax + by = g = gcd(a,b)
def extEuclideanGCD(a,b):
    if a==0:
        return (b,0,1)
    else:
        g,x,y = extEuclideanGCD(b%a,a)
        return (g,y-(b//a)*x, x)

# (x*a)%b == 1
def modularMultInv(a,b):
    g,x,y = extEuclideanGCD(a,b)
    if g==1: #if they are co-prime
        return x % b


def LCM(a,b):
    gcd, x, y = extEuclideanGCD(a,b)
    lcm = (a*b)//gcd
    return lcm


#Will save public and private keys to different files
'''
We are using os.urandom() to generate a random number because it uses synchronization methods, 
which means that another process can't receive the same random number at the same time, which
makes this method cryptographically secure. 
We then use Miller-Rabin to see if the generated number is random, until we find a number
'''
def generateKeys():
    randPrime = int.from_bytes(os.urandom(50), byteorder="little")
    while not is_Prime(randPrime):
        randPrime = int.from_bytes(os.urandom(50), byteorder="little")
    p = randPrime

    randPrime = int.from_bytes(os.urandom(50), byteorder="little")
    while not is_Prime(randPrime):
        randPrime = int.from_bytes(os.urandom(50), byteorder="little")
    q = randPrime

    n = p * q
    totient = (p - 1) * (q - 1)
    e = 65537

    L = LCM(p - 1, q - 1)

    d = modularMultInv(e, L)

    publicKey = open("publicKey.txt", "w")
    publicKey.write(str(n) + "\n" + str(e))
    publicKey.close()

    privateKey = open("privateKey.txt", "w")
    privateKey.write(str(n) + "\n" + str(d))
    privateKey.close()

def encrypt():
    #TODO que publicKey sea el string completeo del txt, pidiendo archivo
    publicKeyFile = open("publicKey.txt", "r")
    publicKey = publicKeyFile.read()
    publicKeyFile.close()

    #TODO que agarre un archivo
    textFile = open("text.txt", "r")
    text = textFile.read()
    textFile.close()

    publicKey = publicKey.splitlines()
    n = int(publicKey[0])
    e = int(publicKey[1])

    cipher = []
    for char in text:
        cipher.append(str(ord(char)).zfill(3))
    cipher = int("".join(cipher))

    cipher = pow(cipher,e,n)

    encrypted = open("encrypted.txt", "w") #TODO
    encrypted.write(str(cipher))
    encrypted.close()


def decrypt():
    #TODO que reciba el archivo con la privateKey
    privateKeyFile = open("privateKey.txt", "r")
    privateKey = privateKeyFile.read()
    privateKeyFile.close()

    #TODO que lea un archivo de texto con la madre encriptada
    encryptedFile = open("encrypted.txt", "r")
    encrypted = encryptedFile.read()
    encryptedFile.close()

    privateKey = privateKey.splitlines()
    n = int(privateKey[0])
    d = int(privateKey[1])

    encrypted = int(encrypted)
    decrypted = str(pow(encrypted,d,n))

    if (len(decrypted) % 3 != 0):  # This means that the first number is less than 3 digits long
        if (len(decrypted) % 3 == 1):
            decrypted = "00" + decrypted
        else:
            decrypted = "0" + decrypted

    decryptedList = [int(str(decrypted)[i:i + 3]) for i in range(0, len(str(decrypted)), 3)]
    readableList = [chr(decryptedList[i]) for i in range(0, len(decryptedList))]

    readable = "".join(readableList)

    decrypted = open("decrypted.txt", "w+")
    decrypted.write(readable)
    decrypted.close()

#Miller-Rabin algorithm for checking primality taken from Rosetta Code
def is_Prime(n):
    """
    Miller-Rabin primality test.

    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    """
    if n != int(n):
        return False
    n = int(n)
    # Miller-Rabin test for prime
    if n == 0 or n == 1 or n == 4 or n == 6 or n == 8 or n == 9:
        return False

    if n == 2 or n == 3 or n == 5 or n == 7:
        return True
    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert (2 ** s * d == n - 1)

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for i in range(8):  # number of trials
        a = random.randrange(2, n)
        if trial_composite(a):
            return False

    return True

generateKeys()
encrypt()
decrypt()

