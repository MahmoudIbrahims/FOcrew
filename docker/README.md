## How to run the docker compose and copy env  :

```bash
cd docker
```

```bash
cp .env.example .env
```

```bash
sudo docker compose up -d
```

#### stop the docker compose:
```bash
sudo docker compose stop
```

### You can remove anything in the docker and restart docker :

#### stop the containers :
```bash
docker stop $(docker ps -aq)
```
#### remove the containers :
```bash
docker rm $(docker ps -aq)
```

#### remove all images :
```bash
docker rmi $(docker images -q) --force
```
#### remove all volumes :
```bash
docker volume rm $(docker volume ls -q) --force
```
#### remove all networks :
```bash
docker network prune --force
```

#### remove any cache:
```bash
docker builder prune --all --force
```
#### remove anything:
```bash
docker system prune --all --volumes --force
```