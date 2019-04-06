# SSH Tunnels
This document helps you configure your workstation to support SSH tunnels that you can use to access services behind a firewall. This procedure can be used recursively to connect multiple SSH tunnels together for multi-hop configurations, such as when the firewall only accept connections from known public IP addresses.


## Steps
1. Initiate a tunnel from the student's PC to the cloud VM.
2. Initiate a tunnel from the cloud VM to the Lab.
3. On the student's PC, open a browser or SSH client.
4. Connect to the address "localhost" using the port number per the tables below. For example, to connect to SSH on ICN15, you would connect to localhost:51522.



## Port Numbering Schema

**Port Mapping table**

z01xx --> Remote TCP/443 on RMM IP (HTTPS to RMM)
z22xx --> Remote TCP/22 (SSH)
z30xx --> Remote TCP/3000 (Grafana)
z43xx --> Remote TCP/443 (HTTPS)
z80xx --> Remote TCP/80 (HTTP)


**Local Port Redirection Mappings**

Example: 52201

5 22 01  Port 52201
| |  |
| |  |
| |  +-- Double: Server Number (ICN##)
| |
| +----- Double: Port Mapping (See table)
|
+------- Single: Lab Group (5 = Rio Rancho)


### For Example:
* `localhost:50101` Relays to: `192.168.123.1:443`  (RMM: ICN01)
* `localhost:50102` Relays to: `192.168.123.2:443`  (RMM: ICN02)
* `localhost:52201` Relays to: `192.168.120.1:22`   (ICN01 - SSH)
* `localhost:52202` Relays to: `192.168.120.2:22`   (ICN02 - SSH)
* `localhost:53001` Relays to: `192.168.120.1:3000` (ICN01 - Grafana)
* `localhost:53002` Relays to: `192.168.120.2:3000` (ICN02 - Grafana)





## Primary SSH Config file
This is the tunnel endpoint in the cloud. These values should be added to the `~/.ssh/config` file within each VM at the public cloud provider. These VMs will initiate the SSH tunnel to the lab. Students will initiate SSH tunnels to the cloud VMs.
```
Host lab-tunnel
    Hostname x.y.z.68
    IdentityFile ~/.ssh/id_rsa
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
    ControlMaster auto
    ControlPersist 10m
    User (username)
    LocalForward 50101 192.168.123.1:443
    LocalForward 50102 192.168.123.2:443
    LocalForward 50103 192.168.123.3:443
    LocalForward 50104 192.168.123.4:443
    LocalForward 50105 192.168.123.5:443
    LocalForward 50106 192.168.123.6:443
    LocalForward 50107 192.168.123.7:443
    LocalForward 50108 192.168.123.8:443
    LocalForward 50109 192.168.123.9:443
    LocalForward 50110 192.168.123.10:443
    LocalForward 50111 192.168.123.11:443
    LocalForward 50112 192.168.123.12:443
    LocalForward 50113 192.168.123.13:443
    LocalForward 50114 192.168.123.14:443
    LocalForward 50115 192.168.123.15:443
    LocalForward 50116 192.168.123.16:443
    LocalForward 50117 192.168.123.17:443
    LocalForward 50118 192.168.123.18:443
    LocalForward 50119 192.168.123.19:443
    LocalForward 50120 192.168.123.20:443
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
    LocalForward 53001 192.168.120.1:3000
    LocalForward 53002 192.168.120.2:3000
    LocalForward 53003 192.168.120.3:3000
    LocalForward 53004 192.168.120.4:3000
    LocalForward 53005 192.168.120.5:3000
    LocalForward 53006 192.168.120.6:3000
    LocalForward 53007 192.168.120.7:3000
    LocalForward 53008 192.168.120.8:3000
    LocalForward 53009 192.168.120.9:3000
    LocalForward 53010 192.168.120.10:3000
    LocalForward 53011 192.168.120.11:3000
    LocalForward 53012 192.168.120.12:3000
    LocalForward 53013 192.168.120.13:3000
    LocalForward 53014 192.168.120.14:3000
    LocalForward 53015 192.168.120.15:3000
    LocalForward 53016 192.168.120.16:3000
    LocalForward 53017 192.168.120.17:3000
    LocalForward 53018 192.168.120.18:3000
    LocalForward 53019 192.168.120.19:3000
    LocalForward 53020 192.168.120.20:3000
    
```


## Secondary SSH Tunnel
This is the configuration that must be added to the student's machine. It allows them access to any of the servers in the lab. Copy the contents to the `~/.ssh/config` file on the student's computer.

```
Host relay-tunnel
    Hostname 35.x.y.z
    IdentityFile ~/.ssh/id_rsa
    ControlPath ~/.ssh/controlmasters/%r@%h:%p
    ControlMaster auto
    ControlPersist 10m
    LocalForward 50101 localhost:50101
    LocalForward 50102 localhost:50102
    LocalForward 50103 localhost:50103
    LocalForward 50104 localhost:50104
    LocalForward 50105 localhost:50105
    LocalForward 50106 localhost:50106
    LocalForward 50107 localhost:50107
    LocalForward 50108 localhost:50108
    LocalForward 50109 localhost:50109
    LocalForward 50110 localhost:50110
    LocalForward 50111 localhost:50111
    LocalForward 50112 localhost:50112
    LocalForward 50113 localhost:50113
    LocalForward 50114 localhost:50114
    LocalForward 50115 localhost:50115
    LocalForward 50116 localhost:50116
    LocalForward 50117 localhost:50117
    LocalForward 50118 localhost:50118
    LocalForward 50119 localhost:50119
    LocalForward 50120 localhost:50120
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
    LocalForward 53001 localhost:53001
    LocalForward 53002 localhost:53002
    LocalForward 53003 localhost:53003
    LocalForward 53004 localhost:53004
    LocalForward 53005 localhost:53005
    LocalForward 53006 localhost:53006
    LocalForward 53007 localhost:53007
    LocalForward 53008 localhost:53008
    LocalForward 53009 localhost:53009
    LocalForward 53010 localhost:53010
    LocalForward 53011 localhost:53011
    LocalForward 53012 localhost:53012
    LocalForward 53013 localhost:53013
    LocalForward 53014 localhost:53014
    LocalForward 53015 localhost:53015
    LocalForward 53016 localhost:53016
    LocalForward 53017 localhost:53017
    LocalForward 53018 localhost:53018
    LocalForward 53019 localhost:53019
    LocalForward 53020 localhost:53020

```
