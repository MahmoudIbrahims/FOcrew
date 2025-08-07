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

### Structure Project:

├── .gitignore
├── LICENSE
├── README.md
├── docker
    ├── .env.example
    ├── .gitignore
    ├── README.md
    └── docker-compose.yml
├── frontend
    ├── .env.example
    ├── .gitignore
    ├── Dockerfile
    ├── __init__.py
    ├── package.json
    └── src
    │   └── components
    │       ├── AgentRunner.js
    │       ├── App.js
    │       ├── FileUpload.js
    │       ├── ReportViewer.js
    │       └── index.js
└── src
    ├── .env.example
    ├── .gitignore
    ├── Agents
        ├── AgentEnums.py
        ├── AgentProvider
        │   ├── BaseAgent.py
        │   ├── InventoryManagment
        │   │   ├── AnalysisReportingSpecialist.py
        │   │   ├── DataProcessing_Agent.py
        │   │   ├── DataVisualizationExpert.py
        │   │   ├── DemandForecastingAnalyst.py
        │   │   ├── InventoryOptimizationExpert.py
        │   │   └── __init__.py
        │   ├── MarketingStratgeyPlanner
        │   │   ├── __init__.py
        │   │   ├── content_agent.py
        │   │   ├── marketing_agent.py
        │   │   ├── swot_agent.py
        │   │   └── translation_agent.py
        │   └── __init__.py
        ├── AgentProviderFactory.py
        ├── Prompts
        │   ├── AnalysisReportPrompt.py
        │   └── __init__.py
        └── __init__.py
    ├── Controllers
        ├── BaseController.py
        ├── DataController.py
        ├── ProjectController.py
        └── __init__.py
    ├── Dataset
        └── Sales.xlsx
    ├── Models
        ├── AgentResultModel.py
        ├── BaseDataModel.py
        ├── FileAgentRelationModel.py
        ├── ProjectModel.py
        ├── UserFileModel.py
        ├── __init__.py
        ├── enums
        │   ├── DataBaseEnum.py
        │   ├── ResponseEnum.py
        │   └── __init__.py
        └── schema
        │   ├── .gitignore
        │   ├── DBSchemas
        │       ├── AgentResult.py
        │       ├── FOcrew_base.py
        │       ├── FileAgentRelation.py
        │       ├── UserFile.py
        │       ├── __init__.py
        │       └── project.py
        │   ├── README.md
        │   ├── __init__.py
        │   ├── alembic.ini.example
        │   └── alembic
        │       ├── README
        │       ├── env.py
        │       ├── script.py.mako
        │       └── versions
        │           ├── 24ea267ba8b6_update_version.py
        │           └── f1a2b85ae371_initial_commit.py
    ├── Providers
        ├── DataBaseProvider
        │   ├── DBProviders
        │   │   ├── PGDataBase.py
        │   │   └── __init__.py
        │   ├── DataBaseEnums.py
        │   ├── DataBaseInterface.py
        │   ├── DataBaseProviderFactory.py
        │   └── __init__.py
        ├── LLMProvider
        │   ├── LLM.py
        │   └── __init__.py
        └── __init__.py
    ├── assets
        └── __init__.py
    ├── backend
        └── Dockerfile
    ├── helpers
        ├── __init__.py
        └── config.py
    ├── main.py
    ├── requirements.txt
    ├── results
        ├── Agent_marketing
        │   └── marketing_analysis_arabic.md
        └── inventory_management
        │   └── comprehensive_inventory_analysis_report.md
    ├── routes
        ├── AGRouterEnums.py
        ├── InventoryManagmentEndpoint.py
        ├── Prompts
        │   ├── InventoryTemplate.py
        │   └── __init__.py
        ├── Schemes
        │   ├── __init__.py
        │   └── data.py
        ├── UploadfileEndpoint.py
        ├── __init__.py
        └── base.py
    └── tools
        ├── FileReading.py
        ├── Schema
            ├── FileReadingSchema.py
            └── __init__.py
        ├── __init__.py
        └── dashboard_tool.py



