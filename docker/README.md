# FOcrew – Dockerized Development & Monitoring Stack

This repository contains a complete **Docker-based setup** for the **FOcrew** application, including backend services, vector databases, and a full monitoring stack using **Prometheus** and **Grafana**.

---

## Architecture Overview

The Docker environment consists of the following services:

### Core Services
- **FastAPI** – Main backend application running on Uvicorn
- **Nginx** – Reverse proxy serving the FastAPI application

### Databases
- **PostgreSQL (pgvector)** – Relational database with vector support

### Monitoring & Observability
- **Prometheus** – Metrics collection and scraping
- **Grafana** – Metrics visualization and dashboards
- **Postgres Exporter** – PostgreSQL metrics exporter
- **Node Exporter** – Host-level system metrics

---

## 📁 Directory Structure

```text
docker/
├── envs/                 # Environment variables
│   ├── .env.example.app
│   ├── .env.example.postgres
│   ├── .env.example.grafana
│   └── .env.example.postgres-exporter
├── FOcrew/
│   └── alembic.example.ini
├── docker-compose.yml
```

### Environment Configuration
```bash
cd docker/envs

cp .env.example.app .env.app
cp .env.example.postgres .env.postgres
cp .env.example.grafana .env.grafana
cp .env.example.postgres-exporter .env.postgres-exporter
```
### Set up Alembic for database migrations:
```bash
cd FOcrew
cp alembic.example.ini alembic.ini
```

### Start the Services:
```bash
cd docker
docker compose up --build -d
```

### Start selected services only:
```bash
docker compose up -d fastapi nginx pgvector

```

### Recommended Startup Order (Avoid Connection Issues)

#### To prevent database connection errors, start databases first:
```bash
docker compose up -d pgvector qdrant postgres-exporter
sleep 30
docker compose up --build -d fastapi nginx prometheus grafana node-exporter
```
### Clean Reset (Containers + Volumes):
```bash
docker compose down -v --remove-orphans

```

### 3. Access the services

- FastAPI Application: http://localhost:8000
- FastAPI Documentation: http://localhost:8000/docs
- Nginx (serving FastAPI): http://localhost
- Prometheus: http://localhost:9090
- Grafana: http://localhost:4000

#### Docker Volume Management:
```bash
# List volumes
docker volume ls

# Inspect a volume
docker volume inspect <volume_name>

# Browse volume files
docker run --rm -v <volume_name>:/data busybox ls -l /data

# Remove a volume
docker volume rm <volume_name>

# Remove unused volumes
docker volume prune

```

### Backup & Restore Volumes
#### Backup:
```bash
docker run --rm \
  -v <volume_name>:/volume \
  -v $(pwd):/backup \
  alpine tar cvf /backup/backup.tar /volume
```
#### Restore:
```bash
docker run --rm \
  -v <volume_name>:/volume \
  -v $(pwd):/backup \
  alpine sh -c "cd /volume && tar xvf /backup/backup.tar --strip 1"
```

### logs for anly image :
```bash
cd docker
docker compose logs -f fastapi
```

### You should add build:
```bash
sudo docker compose up -d --build
```