# Accessing the Lab
This guide will help you configure your workstation to setup an SSH tunnel to the lab "jump server". You will then use this SSH tunnel to access your lab server(s). The SSH tunnel is an encrypted session that has the ability to encapsulate many different streams of traffic, including HTTP, DNS, and even other SSH logon sessions. This is accomplished using port redirection on your local workstation.
The script below will assign a high-numbered TCP port to various IP addresses and port combinations that exist within the lab environment. This tells your SSH client to redirect a connection to that high-numbered port to the corresponding server and port within the lab environment. This allows the lab server team to only expose SSH to the Internet, yet still allows you to access all the necessary ports in the lab without installing a special VPN client.

**Note:**
> Once you have established the SSH tunnel, you will make connections to your `localhost` using the port numbers listed at the bottom of this guide. The port numbers are based on your assigned server number, so please be very careful when entering the port numbers.


## Building the SSH tunnel
In this section you will configure your workstation to establish an SSH tunnel that you will later configure to pass specific TCP traffic from your workstation to the remote server.


### Platform-specific Notes
Windows systems may use PuTTY or another terminal emulator to control the SSH tunnel. Review the Mac/Linux setup instructions below to learn the specifics of the configuration. Due to the many permutations of configurations of Windows SSH clients, further details will not be contained here.

If you are running Mac or Linux as your workstation, follow these steps to configure the SSH tunnel.


## Step 1: SSH Keys
You will need to create an SSH key pair to access the lab servers.

1. If you have not created an SSH key pair on your workstation, you will need to run the following command to create a private and public key pair.
```
cd ~/
ssh-keygen -q -N ''
```
2. Copy your **PUBLIC** SSH key to the server. This is the file with the extension: `.pub`
```
ssh-copy-id -i ~/.ssh/id_rsa.pub <your_user_name>@<hostname>
```

## Step 2: Update your SSH config file
You need to alter your SSH configuration files to create a tunnel that redirects specific TCP connections to "localhost" to your remote server on a different port number. 

1. In a terminal window, create the `controlmasters` directory for the SSH tunnel.
```
mkdir ~/.ssh/controlmasters
```

2. Using a text editor, add the following text to the file `~/.ssh/config`. 
**CAUTION!!**
> You must edit the hostname and user fields in the text below.

```
Host lab-tunnel
    Hostname <w.x.y.z.>
    User <username>
    IdentityFile ~/.ssh/id_rsa
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
    ControlMaster auto
    ControlPersist 5m
    LocalForward 52201 192.168.120.1:22
    LocalForward 52202 192.168.120.2:22
    LocalForward 52203 192.168.120.3:22
    LocalForward 52204 192.168.120.4:22
    LocalForward 52205 192.168.120.5:22
    LocalForward 52206 192.168.120.6:22
    LocalForward 52207 192.168.120.7:22
    LocalForward 52208 192.168.120.8:22
    LocalForward 52209 192.168.120.9:22
    LocalForward 52210 192.168.120.10:22
    LocalForward 52211 192.168.120.11:22
    LocalForward 52212 192.168.120.12:22
    LocalForward 52213 192.168.120.13:22
    LocalForward 52214 192.168.120.14:22
    LocalForward 52215 192.168.120.15:22
    LocalForward 52216 192.168.120.16:22
    LocalForward 52217 192.168.120.17:22
    LocalForward 52218 192.168.120.18:22
    LocalForward 52219 192.168.120.19:22
    LocalForward 52220 192.168.120.20:22
```
3. Save the file and close the text editor.


## Step 3: Initializing the SSH tunnel
Once you have configured the key pair and mapped the ports in your SSH configuration file, you can open the SSH tunnel.

1. In a terminal window, launch the SSH tunnel with the `-fN` option. This will quickly run the commmand and return to the command prompt. It will appear as though it did nothing, however in the background it establishes the tunnel that you will use to connect to your lab server.
```
ssh -fN lab-tunnel
```
2. You can determine if the SSH tunnel is open and listening for connections by typing this command:
```
ssh -O status lab-tunnel
```
**Note:**
> The configuration above allows the SSH tunnel to automatically time out if you have no connections active for 5 minutes. If the tunnel closes, just reestablish it as needed.

3. When you are done using the tunnel, you may can manually close it by typing this command:
```
ssh -O stop lab-tunnel'
```
 
 
 
## Step 4: Connect to your lab server
If you used the SSH tunnel configuration above, you can access ports on your server through redirection. 

**Change the last two digits of the port to match your assigned lab server.**
```
ssh <username>@localhost -p 52201
```

**For example:**
> If the student were assigned server 07 in the lab:
> 1. On the student's workstation, open an SSH client.
> 2. Connect to the host address `localhost`, but instead of using `TCP/22`, enter the port number `52207` which redirects port 22 traffic to server 07.
> 
> **Note:**
>> Another way of writing this is `localhost:52207`
>> SSH uses a slightly different syntax from the command line: `ssh root@localhost -p52207`



This process will redirect input and output over the encrypted SSH tunnel. You may add more ports by editing the SSH config file; however for the change to take effect, you must close the SSH tunnel by typing `ssh -O stop lab-tunnel`, and then restart the tunnel by typing `ssh -fN lab-tunnel`.



-----------------------








# Appendix A: Sample High-numbered Port Schema


##Local Port Redirection Mappings

Example: 52201

5 22 01  Port 52201
| |  |
| |  |
| |  +-- Double: Server Number (ICN##)
| |
| +----- Double: Port Mapping (See table)
|
+------- Single: Lab Group (5 = Highest 5-digit prefix..)

The first number is `5` only to keep these ports out of the way of other services on your PC. Feel free to adjust it as desired.


## Port Numbering Schema
Examples:
z01xx --> Remote TCP/443 on RMM IP (HTTPS to RMM)
z22xx --> Remote TCP/22 (SSH)
z43xx --> Remote TCP/443 (HTTPS)
z80xx --> Remote TCP/80 (HTTP)


### For Example:
* `localhost:50101` Relays to: `192.168.123.1:443`  (RMM: ICN01)
* `localhost:50102` Relays to: `192.168.123.2:443`  (RMM: ICN02)
* `localhost:52201` Relays to: `192.168.120.1:22`   (ICN01 - SSH)
* `localhost:52202` Relays to: `192.168.120.2:22`   (ICN02 - SSH)
* `localhost:53001` Relays to: `192.168.120.1:3000` (ICN01 - Grafana)
* `localhost:53002` Relays to: `192.168.120.2:3000` (ICN02 - Grafana)



# Appendix B: Multiple-hop SSH Tunnel
This configuration is not needed for most lab environments. It is included as a reference only.

Some lab environments have additional restrictions in the firewall to protect the 'jump server' from unauthorized access. Often the firewall restricts incoming connections to a specific range of known public IP addresses. If your workstation's IP address isn't on the list, you can't connect.
To counter this problem, you may setup a cloud-based virtual machine with a static IP address, and then program the firewall to accept connections from that machine. Then you will setup a two-hop SSH tunnel that will allow your workstation to tunnel into the cloud VM (with proper authorization), and then tunnel into the lab environment from the cloud VM.

## Public Cloud VM Variant for the SSH Tunnel
This process requires a special SSH configuration that differs from that shown above. In this configuration, you will place the `lab-tunnel` configuration (shown above) on your Cloud VM. Just as the configuration operated on your workstation, the SSH tunnel on the cloud VM will redirect connections to high-numbered TCP ports on its `localhost` to the corresponding host and port within the lab environment.

Next, you will create a separate `relay-tunnel` SSH configuration (shown below) for your workstation which will map those same high-numbered ports to `localhost` on your cloud VM. In this way, when you connect to your `localhost` on one of these high-numbered ports, the SSH tunnel on your workstation will redirect the data to your cloud VM, which in turn redirects the data to the lab environment. 

As before, only SSH (TCP/22) must be opened in the firewall(s), yet thanks to the SSH tunnel and port redirection, you will have access to any number of hosts and ports within the lab environment. 

**CAUTION!**
> Be sure to carefully match the high-numbered ports in your configuration files. If you add a new port to the Cloud VM, your workstation won't have access to the port until you add it to your workstation's SSH configuration. **and restart the SSH tunnel**. (A commonly overlooked step)


**Note:**
> As before, be sure to create the directory `~/.ssh/controlmasters` on both the Cloud VM and your workstation or else the SSH "control master" will be unable to create the sockets it needs to redirect your ports.


## Steps to use the Cloud VM as a relay host
1. On the student's workstation, initiate the `relay-tunnel` to the cloud VM.
2. On the cloud VM, initiate the `lab-tunnel` to the lab environment.

At this point the student's experience will be the same as if they were directly connected to the lab environment. The student will still use their own workstation to establish SSH, HTTP, or other connections to their `localhost` on the appropriate high-numbered TCP port as noted in the configuration file.

**For example:**
> If the student were assigned server 07 in the lab:
> 1. On the student's workstation, open an SSH client.
> 2. Connect to the host address `localhost`, but instead of using `TCP/22`, enter the port number `52207` which redirects port 22 traffic to server 07.
> 
> **Note:**
>> Another way of writing this is `localhost:52207`
>> SSH uses a slightly different syntax from the command line: `ssh root@localhost -p52207`


## Alternate SSH config file when using a Cloud VM relay host
**CAUTION!!**
> You must edit the hostname here, but do **NOT** include the username.
```
Host relay-tunnel
    Hostname 35.x.y.z
    IdentityFile ~/.ssh/id_rsa
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
    ControlMaster auto
    ControlPersist 5m
    LocalForward 52201 localhost:52201
    LocalForward 52202 localhost:52202
    LocalForward 52203 localhost:52203
    LocalForward 52204 localhost:52204
    LocalForward 52205 localhost:52205
    LocalForward 52206 localhost:52206
    LocalForward 52207 localhost:52207
    LocalForward 52208 localhost:52208
    LocalForward 52209 localhost:52209
    LocalForward 52210 localhost:52210
    LocalForward 52211 localhost:52211
    LocalForward 52212 localhost:52212
    LocalForward 52213 localhost:52213
    LocalForward 52214 localhost:52214
    LocalForward 52215 localhost:52215
    LocalForward 52216 localhost:52216
    LocalForward 52217 localhost:52217
    LocalForward 52218 localhost:52218
    LocalForward 52219 localhost:52219
    LocalForward 52220 localhost:52220

```



# Appendix C: Primary SSH Config file
This is repeated above, but included here for those that scroll too quickly. :)
Below is the configuration that must be added to the student's machine. It allows them access to any of the servers in the lab. Copy the contents to the `~/.ssh/config` file on the student's computer, and then create the directory `~/.ssh/controlmasters`.

**Note:**
> Be sure to create the directory `~/.ssh/controlmasters` on your workstation or else the SSH "control master" will be unable to create the sockets it needs to redirect your ports.

**CAUTION!!**
> You must edit the hostname and user fields in the text below.
```
Host lab-tunnel
    Hostname <w.x.y.z.>
    User <username>
    IdentityFile ~/.ssh/id_rsa
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
    ControlMaster auto
    ControlPersist 5m
    LocalForward 52201 192.168.120.1:22
    LocalForward 52202 192.168.120.2:22
    LocalForward 52203 192.168.120.3:22
    LocalForward 52204 192.168.120.4:22
    LocalForward 52205 192.168.120.5:22
    LocalForward 52206 192.168.120.6:22
    LocalForward 52207 192.168.120.7:22
    LocalForward 52208 192.168.120.8:22
    LocalForward 52209 192.168.120.9:22
    LocalForward 52210 192.168.120.10:22
    LocalForward 52211 192.168.120.11:22
    LocalForward 52212 192.168.120.12:22
    LocalForward 52213 192.168.120.13:22
    LocalForward 52214 192.168.120.14:22
    LocalForward 52215 192.168.120.15:22
    LocalForward 52216 192.168.120.16:22
    LocalForward 52217 192.168.120.17:22
    LocalForward 52218 192.168.120.18:22
    LocalForward 52219 192.168.120.19:22
    LocalForward 52220 192.168.120.20:22
```


