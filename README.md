![Image](https://github.com/user-attachments/assets/3b8011da-a3d2-4f51-acbd-b80e4d5fc604)


## FOcrew --> Future-Oriented crew 
* This project is a MultiAgents for Business 

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
