import argparse

# Extracted code fragment from program uploaded by Professor on blackboard.

def rc4(key, plaintext):
    S = list(range(256))
    j = 0
    plain = []

    # Key-scheduling algorithm
    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudo-random generation algorithm
    i = j = 0
    for char in plaintext:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        plain.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))

    return ''.join(plain)

key='bhargavi_smit' # Key used
ciphertext=input() # Input from vm1 through net cat

print(f'The ciphertext is : {ciphertext}') 
print(f'The original message is : {rc4(key,ciphertext)}') # Decrypted Message

