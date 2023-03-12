# PCS Project 1: Diffie-Hellman key Exchange 

## A. Team Information:

* Bhargavi Poyekar: CH33454
* Smit Patne: WD31175

## B. Selcted and Computed Values:

* Prime Number (P): 1022201
* Primitive Root (alpha): 3
* Xa : 8172
* Xb : 9880
* Key : 546141

## C. Commands Invoked:

1. We used socket programming for the communication of diffie-hellman key exchange and then the encryption-decryption of message and reply.

VM1:

    python3 dh_user1.py -p 1022201 -m "Hello, it is a nice day and we should enjoy the weather"

![](https://i.postimg.cc/yxPLkyQr/image.png)

VM2:

    python3 dh_user2.py

![](https://i.postimg.cc/7PFz2z8K/image.png)

2. TCP dump with socket programming:

VM1:

    tcpdump -n -i ens160 -w user1.pcap host 130.85.220.42| python3 dh_user1.py -p 1022201 -m "Hello, it is a nice day and we should enjoy the weather"

Vm2:

    tcpdump -n -i ens160 -w user2.pcap host 130.85.121.58| python3 dh_user2.py

## D. Challenges Faced:

1. We tried to implement the computation for primitive root by checking all possible roots, but it took very long to find the root. Then we referred the efficient algorithm for finding the primitive root and it helped us to find the root easily. 

2. We faced challenge in using netcat for communication of Diffie-Hellman. We were not able to communicate more then once using it. So, we implemented socket programming for the communication and merged the rc4 code from part 1 with the diffie hellmand in socket programming. 

## E. Summary:

1. We understand how to find primtive root of a prime number more efficiently. 
2. We could implement Diffie-Hellman Key Exchange algorithm and understood how it is a secured way of sharing key.
3. We understood how socket programming works and could implement it for diffie-hellman and then rc4 encryption and decryption.
4. Socket programming made it easier for us to perform 2 way communication.

## F. References:

1. https://www.geeksforgeeks.org/socket-programming-python/
2. https://gist.github.com/sudhanshuptl/680caf021199d7c84458dd3b3e7670d6
3. https://cp-algorithms.com/algebra/primitive-root.html



