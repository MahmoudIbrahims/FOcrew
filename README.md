<p align="center">
  <img src="https://github.com/user-attachments/assets/3b8011da-a3d2-4f51-acbd-b80e4d5fc604" alt="FOcrew Logo" width="150"/>
</p>

![FOcrew Website Screenshot](docs/web_v01.png)

<h1 align="center">
  🌟 FOcrew: Future-Oriented Crew
</h1>

<p align="center">
  <strong>Automate, Decide, Scale: Your AI Multi-Agent Operating System.</strong><br>
  A powerful open-source framework for enterprise productivity and intelligent decision support.
</p>

---

<p align="center">
  <a href="https://github.com/MahmoudIbrahims/FOcrew/actions/workflows/ci.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/MahmoudIbrahims/FOcrew/ci.yml?branch=main&label=CI%20Build" alt="CI Build Status">
  </a>
  <a href="#license">
    <img src="https://img.shields.io/github/license/MahmoudIbrahims/FOcrew" alt="License">
  </a>
  <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-CrewAI%2FFastAPI-red" alt="Frameworks Used">
</p>

---

## 💡 What is FOcrew?

FOcrew is a highly modular, open-source **Multi-Agent System** designed to revolutionize business automation. Built on Python, FastAPI, and CrewAI, it provides a robust platform for creating specialized, collaborative AI agents that:

* **⚡ Boost Productivity:** Automate time-consuming business processes.
* **📊 Enable Intelligence:** Generate sophisticated data analysis and actionable reports.
* **🧩 Ensure Scalability:** Use a decoupled architecture for easy integration and deployment.

### Key Features

* **Modular Agent Design:** Easily add, remove, or customize specialized agents.
* **Asynchronous Task Handling:** Ready for production with FastAPI backend.
* **PostgreSQL Integration:** Robust data storage for agent memory and history.

---
# Installation Guide

Follow these steps to set up the project environment and run the system locally:

=======
* First Download and install Miniconda .

### 1. Clone the Repository
```bash
git clone https://github.com/MahmoudIbrahims/FOcrew.git
cd FOcrew
```
#### 1. Environment Setup

Create and activate a dedicated Python environment:

```bash
$conda create -n coreAgent python=3.10

$conda activate coreAgent

$uv pip install -r requirements.txt
```
### Configuration
#### The first src
```bash
cd src
cp .env.example .env
```
#### The second docker
```bash
cd docker
cp .env.example .env
```
#### Third alembic for data migration:
### [Readme](./src/Models/schema/README.md)

#### 2. Run the app:

```bash
cd docker
sudo docker compose up -d
```

 ```bash
 cd src
 $uvicorn main:app --reload --host 0.0.0.0 --port 8000
 ```

 ```bash
cd Frontend
npm run dev
```
#### Access Backend URL: http://localhost:8000
#### Access Website URL: http://localhost:3000

