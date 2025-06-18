# CoreMind

## MultiAgents for improve the Business 

### Requirements
* python 3.10 
* install python using Miniconda
* Download and install Miniconda .

#### create a new environment using the following command:
```
$ conda create -n coreAgent python=3.10
```
#### Activate coreAgent
```
conda activate coreAgent
```
### How to run the  CoreMind:

#### install the dependencis
```bash
pip install -r requirements.txt
```
#### copy file .env from .env.example:
```bash
cp .env.example .env
```

#### Run the app:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
