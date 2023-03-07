from random import randint
import argparse
import socket

''' Referred https://cp-algorithms.com/algebra/primitive-root.html for 
efficient algorithm to find primitive root, otherwise, testing every value with their powers 
takes a very long time.
'''

# Finds prime factors of a number:
def prime_factors(n):

    # Extracted code fragment from https://www.codesansar.com/python-programming-examples/prime-factors.htm 
    
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)

    if n > 1:
        factors.append(n)
    return factors

# Use of Euler Totient function => P-1 for prime number P
 
def primitive(i,P):

    prime_fact=prime_factors(P-1)

    f=0
    for p in prime_fact:
        if (i**((P-1)//p)%P)==1:
            f=1
            break
    
    if f==0:
        return True

# For 2 to P, testing if any of it is primitive root
def find_primitive_root(P):

    for i in range(2,P):
        if primitive(i,P):
            return i

# RC4 Code extracted from Professor's code
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

# Command Line Argument
parser = argparse.ArgumentParser()
parser.add_argument("-p") # Argument for primitive root
parser.add_argument("-m") # Argument for plaintext message

args = parser.parse_args()
P=int(args.p) # Primitive Root
plaintext=(args.m) 

s=socket.socket() 
host='130.85.220.42' # Server ip
port=12345 # Server port

s.connect((host,port)) # Connecting with server

while True:

    s.send(bytes(str(P),"ascii")) # Send primitive root to vm2
    alpha=find_primitive_root(P) # Calculate primitive root
    print(f'Alpha:{alpha}') 

    Xa=randint(1000,9999) # random 4 digit Xa
    Ya=(alpha**Xa)%P # Calculate Ya
    print(f'Xa:{Xa}')
    print(f'Ya:{Ya}')

    s.send(bytes(str(Ya),"ascii")) # Send Ya
    Yb=int(s.recv(1024).decode()) # Receive Yb
    print(f'Yb:{Yb}')

    Key=(Yb**Xa)%P # Compute Key
    print(f'Key:{Key}')

    print(f'\nPlaintext:{plaintext}')

    ciphertext=rc4(str(Key),plaintext) # encrypt plaintext using key

    print(f'\nCiphertext:{ciphertext}') 
    s.send(ciphertext.encode()) # Send the encrypted message

    ciphertext2=s.recv(1024).decode() # Receive reply ciphertext
    print(f'\nreply Cipher: {ciphertext2}') 

    replyplain=rc4(str(Key),ciphertext2) # Decrypt reply
    print(f'\nReply Plain: {replyplain}')

    break

s.close()





