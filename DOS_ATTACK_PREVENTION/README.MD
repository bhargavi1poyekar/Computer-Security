# PCS Assignment 3: Firewalls to prevent Denial of Service attacks.

## A. General Information:

    Name: Bhargavi Poyekar
    University ID: CH33454
    IP Addresses:
    Ubuntu 22: 130.85.121.58 => (ens192) 133.228.86.2
    Kali (Attacker) => 133.228.86.1
    Ubuntu 20 (target) => 133.228.86.3

## B: DOS Attacks and their prevention:

    1. ICMP Flood Attack:

        Attack: 

            time sudo ping -f -c 100000 133.228.86.3

            => This floods the target machine with icmp packets with count of 100000.

        Prevention:

            For icmp packets, we have to write the rule in /etc/ufw/before.rules

            In before.rules, before ok icmp codes, I wrote:

                -A ufw-before-input -p icmp -s 133.228.86.1 -j DROP

            -p => packet type 
            -s => source ip address 
            -j => Action 

            => This drops all the ICMP packets coming from the attacker ip address.
            => So, when the attacker machine sends ping request, it suffers 100% packet loss. 
                The target machine drops it at firewall level.
            => I also got to know that, we can see the icmp packets in tcpdump, because tcpdump occurs 
                before ufw and hence the packets are dropped after tcpdump captures them. 
            => I also checked pinging from Ubuntu 22 machine, whose packets were not dropped.
        

    2.  ICMP Smurf Attack:

        Attack:

            sudo hping3 -1 -q -c 1000 133.228.86.3 -a 133.228.72.1 (10 times with different machines)

            => Sending 1000 packets to target machine from spoofed source ids from 133.228.72.0/24 network.

        Prevention:

            In before.rules, write before ok imcp codes and comment the previous icmp flood prevention.

                -A ufw-before-input -p icmp -s 133.228.86.0/24 -j ACCEPT
                -A ufw-before-input -p icmp -j DROP

            => This allows icmp packets only from the source id's belonging to 133.228.86.0/24 
                and denies all other packets which might come from spoofed sources.
            => The order of the rules is also very important, since ufw checks rules in order.
            => Hence, the specific one is written first and the default considiton later. 

    3. UDP Flood Attack:

        Attack:

            sudo hping3 -c 10 -2 -p 3454 -q 133.228.86.3 (10 times using bash shell)

            => Sends udp packets (-2 set) at port 3454 of 133.228.86.3 (target) 

        Prevention:

            sudo ufw reject proto udp from 133.228.86.1 to any port 3454
            sudo ufw allow proto udp to any port 3454

            => These commands reject udp packets coming from 133.228.86.1 but allows udp from other sources.
            => In case of reject, port unreachable error is sent back.

            sudo ufw deny proto udp from 133.228.86.1 to any port 3454

            => In case of deny, no reply is sent. The packets are just dropped. 


    4. HTTP Slowloris attack:

        Attack: 
            
            while true; do wget http://133.228.86.3; sleep 1; done

            => Sending Http request every 1 second using wget

        Prevention:

            sudo ufw limit from 133.228.86.1 to any port 80 proto tcp

            => This limits the connection to 6 connections every 30 second. 
            => Hence, it allows if you send 1 onnection after every 5 second, but doesn't allow 
            if sent at a faster rate. 

    5. TCP_SYN Flooding:

        => The TCP_SYN cookies is already enabled in Ubuntu machines. 
        => The process of verifying that TCP SYN cookies are working involves checking the number 
        of TCP connections in the SYN_RECV state on the victim machine.
        => When an attacker sends a flood of SYN requests to a victim machine, the victim machine responds to 
        each of those SYN requests with a SYN-ACK packet. But if the attacker does not send an ACK packet in response 
        to the SYN-ACK packet, the TCP connection will remain in the SYN_RECV state.
        => If the victim machine is configured to use TCP SYN cookies, it will start using SYN cookies to respond 
        to the incoming SYN requests once the queue for SYN-ACK responses is full. This means that it will not 
        allocate resources for half-open connections until it receives the ACK packet from the client. 
        => Hence, the TCP connection will remain in the SYN_RECV state. By counting the number of TCP connections in the 
        SYN_RECV state using the netstat command on the victim machine, we can verify that TCP SYN cookies are 
        working as expected. 
        => If the number of connections in the SYN_RECV state is less than or equal to the value of 
        net.ipv4.tcp_max_syn_backlog (which is 256 by default), it means that SYN cookies are not being used. 
        On the other hand, if the number of connections in the SYN_RECV state is greater than 256, 
        it means that the victim machine is using SYN cookies to respond to the incoming SYN requests.


        Attack: I am writing this bash code in tcp_syn.sh for downloading the photo.jpg with 500 concurrent wgets.

            #!/bin/bash

            for i in {1..500}
            do
                wget --limit-rate=2000 http:133.228.86.3/photo.jpg &
            done

            wait
        
        Prevention:

            => The Ubuntu already prevents and used tcp syn cookies, we just need to verify it by checking the number of 
            connections as I explained above.
            => When I sent 500 tcp packets using hping I got the number of connections as 255 (<256).
            => And when I used simultaneous 500 wget, I got the number of connections as 500, which means the SYN cookies 
            are working.


## C: Challenges Faced:

1. While starting with the icmp attacks, we had to write the rules in before.rules and the syntax of 
those rules is not same as the syntax present in ufw reference website, so I had to search for more 
references and try to understand how to write the rules in before.rules.

2. For the udpflood attack, I wrote the rules correctly, but I was bit confused in how to check if the udp 
is working from other source as hping was not working from ubuntu 22 machine, and I asked Prof about it, then 
when he told me, I understood that we can use spoofed ip from Kali machine. 

3. In the Http Slowloris attack, even after adding the rules, it was not refusing connection, but then after 
observing the ufw status, I saw that the ufw limit rule was below udp allow rule for the http request, and since,
we have to add the specific rules before the default rules, it was not working. Once I removed the allow rules, 
the connection was limited.  

4. For the photo.jpg in TCP-SYN attack, I was confused from where to get the photo.jpg, then I remembered that we can use 
scp to send files from local machine to remote, so I used scp twice to send the photo from my machine to the target machine.

## C: Summary:

1. I understood how to use ufw for prevention of ddos attacks. 
2. I understood how to configure the rules and how the rules are checked in order, hence the order of the rules is very important. 
3. I got to know the difference between reject and deny rule. 
4. I thought that if the packets are rejected it wont get captured in tcpdump, but they were getting captured, so I 
tried to find out how it works. Then I got to know that the tcpdump captures packets before the ufw drops them, hence we can see 
the incoming packets, but since they are dropped, there is no reply for icmp packets. 
5. I got to know some basics of how to write shell script. 
6. I got more familiar with Linux commands.


## D: References:

1. https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands
2. https://help.ubuntu.com/community/UFW
3. https://www.clusterednetworks.com/blog/post/ratelimit-http-https-using-ufw
4. https://wiki.archlinux.org/title/Uncomplicated_Firewall#Rate_limiting_with_ufw
5. https://askubuntu.com/questions/851785/how-to-block-specific-ip-range-in-ufw
6. https://www.reddit.com/r/linuxadmin/comments/nlciaq/ufw_howto_block_outgoing_icmp_packets_to_any/




