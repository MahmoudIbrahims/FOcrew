# Deploy Mistral-7B-Instruct to Beam cloud

### Install Dependencies:
```bash
uv pip install -r requirements.txt
```
--------

### Connect to Beam:
```bash
beam configure default --token Uik_cfGVv............
```
#### Create token by Huggingface and save in beam secret :
```bash
 beam secret create HF_TOKEN "hf......"
 ```
 ---------
 ### beam serve 
 ```bash
 beam serve Generationmodel.py:generate_text
 ```