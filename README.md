![Image](https://github.com/user-attachments/assets/3b8011da-a3d2-4f51-acbd-b80e4d5fc604)


## FOcrew is a MultiAgents for Business 

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

#### Result for Agent Marketing Stratgey:
[report.md](src/results/Agent_marketing/marketing_analysis_arabic.md )



