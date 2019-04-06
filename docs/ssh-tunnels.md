# SSH Tunnels
This document helps you configure your workstation to support SSH tunnels that you can use to access services behind a firewall. This procedure can be used recursively to connect multiple SSH tunnels together for multi-hop configurations, such as when the firewall only accept connections from known public IP addresses.


## Steps
1. Initiate a tunnel from the student's PC to the cloud VM.
2. Initiate a tunnel from the cloud VM to the Lab.
3. On the student's PC, open a browser or SSH client.
4. Connect to the address "localhost" using the port number per the tables below. For example, to connect to SSH on ICN15, you would connect to localhost:51522.



## Port Numbering Schema

**Port Mapping table**

xyy01 --> Remote TCP/443 on RMM IP (HTTPS to RMM)
xyy22 --> Remote TCP/22 (SSH)
xyy30 --> Remote TCP/3000 (Grafana)
xyy43 --> Remote TCP/443 (HTTPS)
xyy80 --> Remote TCP/80 (HTTP)


**Local Port Redirection Mappings**

Example: 50122    (SSH on server ICN01)

 5 01 22  Port 50122
 | |  |
 | |  |
 | |  +-- Double: Port Mapping (See table)
 | |
 | +----- Double: Server Number (ICN##)
 |
 +------- Single: Lab Group (5 = Rio Rancho)


### For Example:
* `localhost:50101` Relays to: `192.168.123.1:443`  (RMM: ICN01)
* `localhost:50201` Relays to: `192.168.123.2:443`  (RMM: ICN02)
* `localhost:50122` Relays to: `192.168.120.1:22`   (ICN01 - SSH)
* `localhost:50222` Relays to: `192.168.120.2:22`   (ICN02 - SSH)
* `localhost:50130` Relays to: `192.168.120.1:3000` (ICN01 - Grafana)
* `localhost:50230` Relays to: `192.168.120.2:3000` (ICN02 - Grafana)





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
    LocalForward 50201 192.168.123.2:443
    LocalForward 50301 192.168.123.3:443
    LocalForward 50401 192.168.123.4:443
    LocalForward 50501 192.168.123.5:443
    LocalForward 50601 192.168.123.6:443
    LocalForward 50701 192.168.123.7:443
    LocalForward 50801 192.168.123.8:443
    LocalForward 50901 192.168.123.9:443
    LocalForward 51001 192.168.123.10:443
    LocalForward 51101 192.168.123.11:443
    LocalForward 51201 192.168.123.12:443
    LocalForward 51301 192.168.123.13:443
    LocalForward 51401 192.168.123.14:443
    LocalForward 51501 192.168.123.15:443
    LocalForward 51601 192.168.123.16:443
    LocalForward 51701 192.168.123.17:443
    LocalForward 51801 192.168.123.18:443
    LocalForward 51901 192.168.123.19:443
    LocalForward 52001 192.168.123.20:443
    LocalForward 50122 192.168.120.1:22
    LocalForward 50222 192.168.120.2:22
    LocalForward 50322 192.168.120.3:22
    LocalForward 50422 192.168.120.4:22
    LocalForward 50522 192.168.120.5:22
    LocalForward 50622 192.168.120.6:22
    LocalForward 50722 192.168.120.7:22
    LocalForward 50822 192.168.120.8:22
    LocalForward 50922 192.168.120.9:22
    LocalForward 51022 192.168.120.10:22
    LocalForward 51122 192.168.120.11:22
    LocalForward 51222 192.168.120.12:22
    LocalForward 51322 192.168.120.13:22
    LocalForward 51422 192.168.120.14:22
    LocalForward 51522 192.168.120.15:22
    LocalForward 51622 192.168.120.16:22
    LocalForward 51722 192.168.120.17:22
    LocalForward 51822 192.168.120.18:22
    LocalForward 51922 192.168.120.19:22
    LocalForward 52022 192.168.120.20:22
    LocalForward 50130 192.168.120.1:3000
    LocalForward 50230 192.168.120.2:3000
    LocalForward 50330 192.168.120.3:3000
    LocalForward 50430 192.168.120.4:3000
    LocalForward 50530 192.168.120.5:3000
    LocalForward 50630 192.168.120.6:3000
    LocalForward 50730 192.168.120.7:3000
    LocalForward 50830 192.168.120.8:3000
    LocalForward 50930 192.168.120.9:3000
    LocalForward 51030 192.168.120.10:3000
    LocalForward 51130 192.168.120.11:3000
    LocalForward 51230 192.168.120.12:3000
    LocalForward 51330 192.168.120.13:3000
    LocalForward 51430 192.168.120.14:3000
    LocalForward 51530 192.168.120.15:3000
    LocalForward 51630 192.168.120.16:3000
    LocalForward 51730 192.168.120.17:3000
    LocalForward 51830 192.168.120.18:3000
    LocalForward 51930 192.168.120.19:3000
    LocalForward 52030 192.168.120.20:3000
    
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
    LocalForward 50201 localhost:50201
    LocalForward 50301 localhost:50301
    LocalForward 50401 localhost:50401
    LocalForward 50501 localhost:50501
    LocalForward 50601 localhost:50601
    LocalForward 50701 localhost:50701
    LocalForward 50801 localhost:50801
    LocalForward 50901 localhost:50901
    LocalForward 51001 localhost:51001
    LocalForward 51101 localhost:51101
    LocalForward 51201 localhost:51201
    LocalForward 51301 localhost:51301
    LocalForward 51401 localhost:51401
    LocalForward 51501 localhost:51501
    LocalForward 51601 localhost:51601
    LocalForward 51701 localhost:51701
    LocalForward 51801 localhost:51801
    LocalForward 51901 localhost:51901
    LocalForward 52001 localhost:52001
    LocalForward 50122 localhost:50122
    LocalForward 50222 localhost:50222
    LocalForward 50322 localhost:50322
    LocalForward 50422 localhost:50422
    LocalForward 50522 localhost:50522
    LocalForward 50622 localhost:50622
    LocalForward 50722 localhost:50722
    LocalForward 50822 localhost:50822
    LocalForward 50922 localhost:50922
    LocalForward 51022 localhost:51022
    LocalForward 51122 localhost:51122
    LocalForward 51222 localhost:51222
    LocalForward 51322 localhost:51322
    LocalForward 51422 localhost:51422
    LocalForward 51522 localhost:51522
    LocalForward 51622 localhost:51622
    LocalForward 51722 localhost:51722
    LocalForward 51822 localhost:51822
    LocalForward 51922 localhost:51922
    LocalForward 52022 localhost:52022
    LocalForward 50130 localhost:50130
    LocalForward 50230 localhost:50230
    LocalForward 50330 localhost:50330
    LocalForward 50430 localhost:50430
    LocalForward 50530 localhost:50530
    LocalForward 50630 localhost:50630
    LocalForward 50730 localhost:50730
    LocalForward 50830 localhost:50830
    LocalForward 50930 localhost:50930
    LocalForward 51030 localhost:51030
    LocalForward 51130 localhost:51130
    LocalForward 51230 localhost:51230
    LocalForward 51330 localhost:51330
    LocalForward 51430 localhost:51430
    LocalForward 51530 localhost:51530
    LocalForward 51630 localhost:51630
    LocalForward 51730 localhost:51730
    LocalForward 51830 localhost:51830
    LocalForward 51930 localhost:51930
    LocalForward 52030 localhost:52030
    
```
