from random import randint
import socket

''' Referred https://www.geeksforgeeks.org/primitive-root-of-a-prime-number-n-modulo-n/ for 
efficient algorithm to find primitive root, otherwise, testing every value with their powers 
takes a very long time
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
def rc4(key, ciphertext):
    S = list(range(256))
    j = 0
    plain = []

    # Key-scheduling algorithm
    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudo-random generation algorithm
    i = j = 0
    for char in ciphertext:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        plain.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))

    return ''.join(plain)

s=socket.socket()
port=12345
s.bind(('',port)) # Bind with the port

s.listen(5) # Listen mode

while True:

    c,addr=s.accept() # connection with client
    print('Connection from',addr)

    P=int(c.recv(1024).decode()) # receive P
    alpha=find_primitive_root(P) # Find alpha
    print(f'Alpha:{alpha}')

    Ya=int(c.rec(1024).decode()) # Receive Ya
    print(f'Ya:{Ya}')

    Xb=randint(1000,9999) # Xb random 4 digit number
    Yb=(alpha**Xb)%P # Calculate Yb
    print(f'Xb:{Xb}')
    print(f'Yb:{Yb}')

    c.send(bytes(str(Yb),'ascii')) # Send Yb

    Key=(Ya**Xb)%P # Calculate Key
    print(f'Key:{Key}')

    ciphertext=c.recv(1024).decode() # Receive Encrypted message
    print(f'\nCiphertext:{ciphertext}')

    plaintext=rc4(str(Key),ciphertext) # Decrypt message
    print(f'Plaintext:{plaintext}')

    reply='Busy with assignment right now.' # Reply
    print(f'Reply Plain:{reply}')

    replycipher=rc4(str(Key),reply) # Encrypt Reply
    print(f'\nReply Cipher: {replycipher}')

    c.send(replycipher.encode()) # Send Reply

    c.close() # Close connection
    break




