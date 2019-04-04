# Containerization

This document will help you setup Docker and pull down the appropriate containers for the lab server.


### Containerize
To keep the host as clean as possible, use containers were possible. Containers may also be used to pin uncooperative services to specific cores without the use of tasksets.

1. Install Docker

```
curl -fsSL https://get.docker.com/ | sh
```

2. Test Docker
```
docker run hello-world
```
### Install Barometer

docker pull opnfv/barometer-collectd

