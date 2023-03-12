import argparse

# Extracted code fragment from program uploaded by Professor on blackboard.

def rc4(key, plaintext):
    S = list(range(256))
    j = 0
    cipher = []

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
        cipher.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))

    return ''.join(cipher)

parser = argparse.ArgumentParser()
parser.add_argument("-k") # Argument for key
parser.add_argument("-m") # Argument for message

args = parser.parse_args() 

key=args.k
plaintext=args.m

cipher=rc4(key,plaintext) # Encrypt message
print(f'{cipher}') # Print encrypted message to stdout which will be sent to vm2 using netcat

