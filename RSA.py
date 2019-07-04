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
def generateKeys():
    p = 2074722246773485207821695222107608587480996474721117292752992589912196684750549658310084416732550077
    q = 6513516734600035718300327211250928237178281758494417357560086828416863929270451437126021949850746381

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
    #TODO que publicKey sea el string completeo del txt
    publicKey = "13513738074006080862264476443977166349086361660577276683539071573295457313514603062249049313215121635233965221964743270358541941492028942548846407860040755759932529457346440118365714783352895909021337\n65537"


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
    privateKey = "13513738074006080862264476443977166349086361660577276683539071573295457313514603062249049313215121635233965221964743270358541941492028942548846407860040755759932529457346440118365714783352895909021337\n739949174948057145951692535807437957851235314692182391303842994656007271763235318810453842264254756202117713877070988636842550848177921861646327947751806756428161027875149716196849665495737834892713"  #TODO

    #TODO que lea un archivo de texto con la madre encriptada
    encrypted = "6046571899514177607531732056191113412460325269297337034540382775938248660098500685672707879367252857130041772720107785512322970004515947926122302827174932213841055563980837923859949037887228740105943" #TODO que reciba el texto encrypted

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

generateKeys()
encrypt()
decrypt()

