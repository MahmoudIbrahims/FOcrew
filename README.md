# CoreMind

## MultiAgents for improve the Business 

### Requirements
* python 3.10 
* install python using Miniconda
* Download and install Miniconda .

#### Create a new environment using the following command:
```
$ conda create -n coreAgent python=3.10
```
#### Activate coreAgent
```
conda activate coreAgent
```
### How to run the  CoreMind:

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
