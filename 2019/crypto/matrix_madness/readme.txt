Matrix Madness

We are given a cipher text / plain text pair and a cipher text to decode as well as the cipher text alphabet.

The name of the challenge and the fact that a known plaintext attack is possible with the challenge setup suggests a hill cipher has been used.

This is further hinted at by the fact that the length of the plain and cipher texts don't match suggesting a padding has been applied.
The cipher text is 114 bytes long and the plaintext is 110 bytes. The factors of 114 are 1, 2, 3, 6, 19, 38, 57, 114 one of these will be the block size used by the cipher.
Although possible some of the larger and smaller factors are unlikely.
The correct block size is 6. 3 can be eliminated by the fact that the cipher text is 114 bytes not 111 bytes which would be the nearest multiple of 3 to the length of the plain text. Block sizes can also be eliminated by trial and error.

The hillcipher works by multiplying matricies by a key matrix an over view is below.

Where:
K = Key Matrix
B = Block of Plain Text Matrix
C = Block of Cipher Text Matrix
a = Alphabet length

Encrypt
KB = C mod a

Decrypt
K^(-1)C = B mod a

These equations can be rearanged to be the same as such the following is true.

Attack
C^(-1)B = K^(-1) mod a

Given a block of cipher text and inverted plaintext the inverted key can be obtained.
This can then be used in the decryption equation to obtain further cipher texts encrypted with the same key.
(In the case of the POC I used the encrypt equation and inverted the key as I already had the code for this)