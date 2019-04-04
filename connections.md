# Connecting to the Lab
This guide will help you connect to the lab servers through an SSH tunnel. Inside that tunnel you will use SSH and HTTP to manage the lab servers and perform the lab exercises.

## Building the SSH tunnel
In this section you will configure your workstation to establish an SSH tunnel that you will later configure to pass specific TCP traffic from your workstation to the remote server.

### Mac or Linux
If you are running Mac or Linux as your workstation, follow these steps to configure the SSH tunnel.

#### Step 1: SSH Key Generation
You will need to create an SSH key pair to access the lab servers.

1. In a terminal window, run the following command to create a public/private key pair.
```
cd
ssh-keygen -q -b 2048 -N '' -t rsa -f .ssh/lab_rsa.key
```
2. Copy your SSH key to the server
```
ssh-copy-id -i .ssh/lab_rsa.key.pub <your_user_name>@<hostname>
```

#### Step 2: Update your SSH config file
You need to alter your SSH configuration files to create a tunnel that redirects specific TCP connections to "localhost" to your remote server on a different port number. For example, if your remote server is hosting Grafana on HTTP over TCP/3000, you could enter a configuration statement that would allow you to open a web browser on your local workstation to the address "http://localhost:3000" or you could choose another TCP port if port 3000 was already used by another service on your workstation. In this way you can pass multiple streams of traffic through the encrypted SSH tunnel, and yet only TCP/22 is open between your workstation and the lab firewall.

1. In a terminal window, create the `controlmasters` directory for the SSH tunnel.
```
mkdir ~/.ssh/controlmasters
```

2. Using a text editor, add the following text to the file `~/.ssh/config`:
```
Host lab-tunnel
    Hostname XXX.XXX.XXX.XXX
    IdentityFile ~/.ssh/lab_rsa.key
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
    ControlMaster auto
    ControlPersist 5m
    LocalForward 10022 192.168.120.1:22
    LocalForward 13000 192.168.120.1:3000
    User your_user_name

```
3. Save the file and close the text editor.


#### Step 3: Initializing the SSH tunnel
Once you have configured the key pair and mapped the ports in your SSH configuration file, you can open the SSH tunnel.

1. In a terminal window, launch the SSH tunnel with the -fN option to open the connection, but run it in the background without opening a shell or running any commands. This will establish the tunnel that you will use to connect to your lab server.
```
ssh -fN lab-tunnel
```
2. You can determine if the SSH tunnel is open and listening for connections by typing this command:
```
ssh -O status lab-tunnel
```

**Note:**
> You have configured the SSH tunnel to automatically time out if you have no connections open for 5 minutes; however you can manually close the SSH tunnel by typing: `ssh -O stop lab-tunnel'
 
 
### Windows Instructions

*Coming Soon!*

For now, use PuTTY or a similar terminal emulator to create the keys and manage the SSH tunnel and subsequent connections.


 
## Using the SSH tunnel
If you used the SSH tunnel configuration above, you can access ports on your server through redirection.

1. Open an SSH connection to your localhost on port 10022. This will actually connect to port 22 on your lab server.
```
ssh <username>@localhost -p 10022
```
2. Alternatively, if you have Grafana running on your lab server, which uses TCP/3000 by default, you can open a web browser on your workstation.
```
http://localhost:13000
```
***Note:**
> Both of these commands redirect input and output over the encrypted SSH tunnel. You may add more ports by editing the SSH config file; however for the change to take effect, you must close the SSH tunnel by typing `ssh -O stop lab-tunnel`, and then restart the tunnel by typing `ssh -fN lab-tunnel'.

