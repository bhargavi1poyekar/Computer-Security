# PCS Project 1: Communicating using RC4 Stream Encryption

## A. Team Information:

* Bhargavi Poyekar: CH33454
* Smit Patne: WD31175

## B. Secret Key: "bhargavi_smit"

## C.  Commands used:

1.  First we wanted to make sure, we could communicate with both machines using netcat.

        Receiver VM 2(Smit)=> nc -l 12345 (portnumber)

        Sender VM 1(Bhargavi)=> nc 130.85.220.42 12345

    After executing commands in this order, whatever we typed on vm1 was seen on vm2. 

        Netcat basic command on vm1
    ![Netcat basic command on vm1](https://i.postimg.cc/ht4kFHK5/image.png "Netcat basic command on vm1")

        Netcat basic command on vm2
    ![Netcat basic command on vm1](https://i.postimg.cc/vB2hCNH5/image.png )

2. Created fifo files vm1pipe and vm2pipe on the vm1 (Bhargavi VM) and vm2 (Smit Vm) respectively for 2-way communication between vm's.

        Receiver VM 2(Smit)=> mkfifo vm2pipe

        Sender VM 1(Bhargavi)=> mkfifo vm1pipe

3. RC4 encryption on vm1 and decryption on vm2:

        Receiver VM 2(Smit): nc -l 12345 > vm2pipe | python3 rc4.py <vm2pipe 

        Sender VM 1(Bhargavi): python3 rc4.py -k "bhargavi_smit" -m "This is our first pcs project" <vm1pipe | nc 130.85.220.42 12345 >vm1pipe 

Netcat command on receiver vm
![Netcat basic command on vm1](https://i.postimg.cc/tJnWs6Y8/image.png )


Netcat command on sender vm
![Netcat basic command on vm2](https://i.postimg.cc/brKf5nP9/image.png)

Code on Sender VM for encryption of message:

![](https://i.postimg.cc/4dPSt9nx/image.png )

Code on Receiver VM for encryption of message:

![](https://i.postimg.cc/pXCKHJ4T/image.png )

4. TcpDump Capture:

Command for tcpdump on vm1:

    tcpdump -n -i ens160 -w vm1capture.pcap host 130.85.220.42|python3 rc4.py -k "bhargavi_smit" -m "This is our first pcs project."<vm1pipe |nc 130.85.220.42 12345 >vm1pipe

![](https://i.postimg.cc/kMTjmHGV/image.png)


TCP dump capture:

    tcpdump -r vm1captue.pcap

![](https://i.postimg.cc/J0W3MbJz/image.png)

TCP dump capture in ASCII format for vm1:

    tcpdump -XX -r vm1campture.pcap

![](https://i.postimg.cc/8C0tQJt7/image.png)

VM2: 

Command for tcpdump on vm2: 

    tcpdump -n -i ens160 -w vm2capture.pcap host 130.85.121.58 |nc -l 12345 > vm2pipe | python3 rc4.py < vm2pipe

![](https://i.postimg.cc/qMtGdMWY/image.png)

TCP dump capture:

    tcpdump -r vm2captue.pcap
![](https://i.postimg.cc/KjFcZzY2/image.png)

TCP dump capture in ASCII format for vm2:

    tcpdump -XX -r vm1campture.pcap

![](https://i.postimg.cc/PryswySY/image.png)

## D. Challenges Faced: 

We faced challenge in communication with pipes. When we tried to execute  netcat with piping the rc4 python program on receiver vm, the execution was supposed to happen in this way. The nc -l port number would listen on the given port and then once sender vm sends the cipher message, it is sent to the listening port of vm2, which is then used as an input for receiver decyption program. But when we were trying to execute the command: 
    
    nc -l “port on vm2” < vm2pipe | python rc4.py >vm2pipe

it  executed the python rc4 before netcat could listen to the sender program. 

We tried to find the solution by referring to different sources, but were unable to understand the problem. But then after understanding how exactly the pipes work. And then we found the problem, we were using < vm2pipe instead of > vm2pipe. '>' stands for sending the output to the program after it, and we were doing opposite. 

Once we rectified our mistake, we were able to communicate without any problem.

## E. Summary:

1. We understood stream cipher, how to implement rc4 and encrypt and decrypt using XOR operation.
2. We now know how to take multiple command line arguments in python.
3. We learned how netcat works and how to do basic communication between 2 machines.
4. We understood how pipe works and how to create a named pipe and use it for communicating.
5. We understood use of '>' and '<' in linux commands.
6. We learned how to capture packets using tcpdump and the various options in tcp dump.
7. We now know how to read the saved pcap file and also how to download a file from local machine to remote server.  
8. We have become more friendly with linux machines and their communications.

## F. References:

1. Professor's RC4 encryption code given on blackboard
2. https://www.geeksforgeeks.org/introduction-to-netcat/
3. https://www.tecmint.com/12-tcpdump-commands-a-network-sniffer-tool/
4. http://jordanmorris.com/remote-network-capture-with-tcpdump-and-ncat/





