# coding: utf-8

'''
Authors:
Joaquin Rios Corvera
Jordan Gonzalez Bustamante
Roberto Tellez Perezyera
'''

import os
import random
from tkinter import *
from tkinter import filedialog

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
    global app, tbutton
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

    rlabel = Label(app, text="Two files were created, one for the Public Key, other for the Private Key", font=("Arial", 14))
    rlabel.grid(pady=5, row=4, column=1)
    tbutton.configure(state=NORMAL)

def getFile():
    global file, ebutton
    temporal = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    file = open(temporal, 'r').read()

    label_text = "The message which will be encrypted is: '" + file + "'"
    rlabel = Label(app, text=label_text, font=("Arial", 14))
    rlabel.grid(pady=5, row=5, column=1)
    ebutton.configure(state=NORMAL)

def encrypt():
    global app, file, dbutton

    publicKeyFile = open("publicKey.txt", "r")
    publicKey = publicKeyFile.read()
    publicKeyFile.close()

    #textFile = open("text.txt", "r")
    text = file
    #textFile.close()

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

    rlabel = Label(app, text="A file with the encryption has been created.", font=("Arial", 14))
    rlabel.grid(pady=5, row=6, column=1)
    dbutton.configure(state=NORMAL)

def decrypt():
    global app
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

    rlabel = Label(app, text="A file with the decryption has been created.", font=("Arial", 14))
    rlabel.grid(pady=5, row=7, column=1)

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

def main():
    global app, file, tbutton, ebutton, dbutton
    app = Tk()
    app.title("RSA Multi-purpose system.")
    # labels
    mlabel = Label(app, text="This applications offers:", font=("Arial", 14))
    glabel = Label(app, text="Random key generation.", font=("Arial", 14))
    tlabel = Label(app, text="Text to encrypt/decrypt.", font=("Arial", 14))
    elabel = Label(app, text="Encrypt.", font=("Arial", 14))
    dlabel = Label(app, text="Decrypt.", font=("Arial", 14))
    # buttons
    gbutton = Button(app, text="Generate keys", font=("Arial", 12), command=generateKeys)
    tbutton = Button(app, text="Select text file...", font=("Arial", 12), command=getFile)
    tbutton.configure(state=DISABLED)
    ebutton = Button(app, text="Encrypt", font=("Arial", 12), command=encrypt)
    ebutton.configure(state=DISABLED)
    dbutton = Button(app, text="Decrypt", font=("Arial", 12), command=decrypt)
    dbutton.configure(state=DISABLED)

    # grid
    mlabel.grid(pady=5, row=0, column=1)
    glabel.grid(pady=5, padx=5, row=1, column=0)
    tlabel.grid(pady=5, padx=5, row=1, column=1)
    elabel.grid(pady=5, padx=5, row=1, column=2)
    dlabel.grid(pady=5, padx=5, row=1, column=3)
    gbutton.grid(pady=5, row=2, column=0)
    tbutton.grid(pady=5, row=2, column=1)
    ebutton.grid(pady=5, row=2, column=2)
    dbutton.grid(pady=5, row=2, column=3)

    app.mainloop()


global app, tbutton, ebutton, dbutton
main()




