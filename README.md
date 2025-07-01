![Image](https://github.com/user-attachments/assets/3b8011da-a3d2-4f51-acbd-b80e4d5fc604)


<h1 align="center">
  🌟 FOcrew
</h1>

<p align="center">
  <strong>Future-Oriented Crew</strong><br>
</p>

## What is FOcrew?

* FOcrew is an open-source Multi-Agent System powered by AI,
* designed for business productivity, automation, and intelligent decision support. Built using Python, FastAPI, and CrewAI,
* FOcrew provides a modular platform to automate data analysis, generate actionable reports, and streamline business operations.

### Requirements
* python 3.10 
* install python using Miniconda
* Download and install Miniconda .


#### Create a new environment using the following command:
```bash
$ conda create -n coreAgent python=3.10
```
#### Activate coreAgent
```bash
conda activate coreAgent
```
### How to run the FOcrew:

#### First run the image postgres 
```bash
cd docker
```
```bash
sudo docker compose up -d
```
#### Open new terminal and run the app

```bash
cd src
```
#### Install the dependencis
```bash
pip install -r requirements.txt
```

#### Copy file .env from .env.example:

```bash
cp .env.example .env
```

#### Run the app:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Result for Agent inventory managment:
[report.md](src/results/inventory_management/comprehensive_inventory_analysis_report.md)


### Result for Agent Marketing Stratgey:
[report.md](src/results/Agent_marketing/marketing_analysis_english.md )

