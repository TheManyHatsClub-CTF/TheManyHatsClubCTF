import numpy as np

#Constants
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '.', ',']
alphabet_size = len(alphabet)
block_size = 6

#Hillcipher stuff - taken from the internet and partially written by myself
def adjugate(matrix):
    rows, columns = matrix.shape

    def cofactor(i, j):
        rows_to_keep = [True]*(i) + [False] + [True]*(rows - (i+1))
        rows_to_keep = np.array(rows_to_keep)
        cols_to_keep = [True]*(j) + [False] + [True]*(columns - (j+1))
        cols_to_keep = np.array(cols_to_keep)

        submatrix = matrix[rows_to_keep, :][:, cols_to_keep]
        determinant = int(round(np.linalg.det(submatrix)))
        sign = (-1)**(i+j)
        return (sign * int(determinant)) % alphabet_size


    cofactor_matrix = np.zeros(matrix.shape, dtype=int)
    for i in range(rows):
        for j in range(columns):
            cofactor_matrix[i,j] = cofactor(i,j)

    return cofactor_matrix.T

def inverseKey(key):
    mod_matrix = np.full(key.shape, alphabet_size, dtype=int)
    adjugate_matrix = adjugate(key)
    determinant = int(round(np.linalg.det(key)))
    inverse_determinant = pow(determinant%alphabet_size, alphabet_size-2, alphabet_size)
    return np.mod(adjugate_matrix * inverse_determinant, mod_matrix)

def validateMessage(message):
    for letter in message:
        if letter not in alphabet:
            return False
    return True

def encryptBlock(block, key, block_size):
    chars = list(map(lambda char: alphabet.index(char), list(block)))
    char_matrix = np.array(chars)
    mod_matrix = np.full(char_matrix.shape, alphabet_size, dtype=int)
    encrypted_char_matrix = np.mod(np.dot(char_matrix, key), mod_matrix)
    return "".join(list(map(lambda char: alphabet[char], encrypted_char_matrix)))

def encryptString(message, key, block_size):
    if validateMessage(message) == True:
        #Split into Blocks
        encrypted_message = ""
        for i in range(0, len(message), block_size):
            #Encrypt Blocks
            encrypted_message += encryptBlock(message[i:i+block_size], key, block_size)
        return encrypted_message
    else:
        print("Invalid Input Alphabet: " + str(alphabet))

def encrypt(message, key):

    encryption_key = key

    decryption_key = inverseKey(encryption_key)

    while len(message) % block_size != 0:
        message = message + "X"

    encrypted = encryptString(message, encryption_key, block_size)
    return encrypted


#A plain text / cipher text pair needs to be of sufficient length
plain = "THIS NEW ENCRYPTION METHOD IS EXCELLENT NO ONE WILL BREAK IT. I HAVE THE UPMOST CONFIDENCE. KIND REGARDS, KYLE"
cipher= "AHTNTRZPBEMVVUGIKBZNEYN,IPAZPWEQZBROKYSAG, GLNSMIZPPNAGAUCLFRKJKHVCSTSZDSCJFMSBKMHMMRA,THANLDUULHG  WDPVUQKNATYMRA"

cipherTextMatrix = []
plainTextMatrix = []

#Converts the inputs to matricies
for i in range(0, 36, 6):
    cipherBlock = cipher[i:i+6]
    plainBlock = plain[i:i+6]

    cipherBlockChars = list(map(lambda char: alphabet.index(char), list(cipherBlock)))
    cipherTextMatrix.append(cipherBlockChars)
    plainBlockChars = list(map(lambda char: alphabet.index(char), list(plainBlock)))
    plainTextMatrix.append(plainBlockChars)

#Inverts the ciphertext matrix
cipherTextMatrix = np.array(cipherTextMatrix)
invertedCipherTextMatrix = inverseKey(cipherTextMatrix)

#Completes a modular multiplication of the plaintext and the inverted ciphertext matrix
plainTextMatrix = np.array(plainTextMatrix)
modMatrix = np.full(plainTextMatrix.shape, alphabet_size, dtype=int)
decryptionMatrix = np.mod(np.dot(invertedCipherTextMatrix, plainTextMatrix), modMatrix)

#Encrypting with an inverted key is the same as decrypting with a decryption matrix
encryptionMatrix = inverseKey(decryptionMatrix)
print(encrypt('V,CFNOQQOMVBFY, FITGZML BUN,THBM XJPGMKHITAY SNTX,IKXFQKMOJF,QF,DO..SJV LKASFYNV.ZDBPGYDDUWUHIUMW,LQSCTK.KEHIPNG,V', decryptionMatrix))