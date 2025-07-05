from fastapi import APIRouter ,status,Request
from Models.ProjectModel import ProjectModel
from Models.AgentResultModel import AgentResultModel
from Models.FileAgentRelationModel import FileAgentRelationModel
from Models.UserFileModel import UserFileModel

from Agents import (DataProcessing,DemandForecastingAnalyst,InventoryOptimizationExpert,
                    InventoryAnalysisReportingSpecialist,TranslationEnglishArabic)

from Models.schema.DBSchemas import AgentResult  
import uuid
from .Schemes.data import ProcessRequest
from .AGRouterEnums import UsageType
from .AGRouterEnums import Languages 
from Models.enums import ResponseSignal
from crewai import Crew
from fastapi.responses import JSONResponse
from datetime import datetime

agent_router = APIRouter(
    prefix ="/api/v1/agent",
    tags =["api_v1","agent"],
)

@agent_router.post('/inventory/{project_id}')
async def inventory_agent(request : Request ,project_id:int,Process_Request:ProcessRequest):
    
    userfile_model =await UserFileModel.create_instance(
         db_client = request.app.db_client
                     )

    project_model = await ProjectModel.create_instance( 
        db_client = request.app.db_client
        
                    )
    
    agent_model =await AgentResultModel.create_instance(
        db_client = request.app.db_client
        )
    
    agent_Relation_model =await FileAgentRelationModel.create_instance(
         db_client = request.app.db_client
                     )
    
    model = await project_model.get_project_or_create_one(
                project_id = project_id
                )
    
    latest_file = await userfile_model.get_latest_user_file_by_project(
                 project_id =model.project_id
                    )
        
    if not latest_file:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "No uploaded file found for this project"}
        )
        
        
    Data_Processing =DataProcessing()
    Demand_ForecastingAnalyst =DemandForecastingAnalyst()
    Inventory_OptimizationExpert =InventoryOptimizationExpert()
    Inventory_AnalysisReportingSpecialist =InventoryAnalysisReportingSpecialist()
        
    Data_Processing_Agent =Data_Processing.get_agent()
    Data_Processing_task =Data_Processing.get_task()
    Data_Processing_task.description ="\n".join([
                            f"Process the inventory data file: {latest_file.full_data}",
                            
                            "Your responsibilities:",
                            "1. Read and analyze the file structure",
                            "2. Validate data quality and identify any issues",
                            "3. Extract key information about inventory items",
                            "4. Prepare clean data summary for further analysis",
                            "5. Identify data patterns and basic statistics",
                            
                            "Provide a comprehensive data summary."
                            ])
            
    Demand_ForecastingAnalyst_Agent =Demand_ForecastingAnalyst.get_agent()
    Demand_ForecastingAnalyst_task =Demand_ForecastingAnalyst.get_task()
            
    Inventory_OptimizationExpert_Agent =Inventory_OptimizationExpert.get_agent()
    Inventory_OptimizationExpert_task =Inventory_OptimizationExpert.get_task()
            
    Inventory_AnalysisReportingSpecialist_Agent =Inventory_AnalysisReportingSpecialist.get_agent()
    Inventory_AnalysisReportingSpecialist_task =Inventory_AnalysisReportingSpecialist.get_task()
    Inventory_AnalysisReportingSpecialist_task.expected_output="\n".join([
                "A professional markdown report with the following structure:",
                "",
                "# Inventory Management Analysis Report",
                f"**Company:** {Process_Request.COMPANY_NAME}",
                f"**Date:** {datetime.now().strftime('%Y-%m-%d, %H:%M')}",
                f"**INDUSTRY_NAME:** {Process_Request.INDUSTRY_NAME}"
                "",
                "## 📊 Executive Summary",
                "- Key findings summary (200-300 words)",
                "- Critical business impacts",
                "- Priority recommendations",
                "",
                "## 🚨 Critical Alerts",
                "| Alert Type | Item | Severity | Impact | Action Required | Timeline |",
                "|------------|------|----------|--------|-----------------|----------|",
                "| .......... | .... | ........ | ...... | ............... | ........ |",
                "",
                "## 📈 Key Performance Indicators",
                "### Inventory Turnover",
                "| Category | Current | Target | Status | Trend |",
                "|----------|---------|--------|--------|-------|",
                "| ........ | ....... | ...... | ...... | ..... |",
                "",
                "### Service Levels",
                "| Metric | Current | Target | Gap | Action |",
                "|--------|---------|--------|-----|--------|",
                "| .......| ....... | ...... | ... | ...... |",
                "",
                "## 🔍 ABC Analysis",
                "### Classification Summary",
                "| Class | Items | Value % | Recommendations |",
                "|-------|-------|---------|-----------------|",
                "| A     |...... |........ | ................|",
                "| B     |...... |........ | ................|",
                "| C     |...... |........ | ................|",
                "",
                "## 🎯 Action Plan",
                "### Immediate Actions (0-48 hours)",
                "1. **Action 1:** Description, timeline, responsible party",
                "2. **Action 2:** Description, timeline, responsible party",
                "",
                "### Short-term Improvements (1-4 weeks)",
                "1. **Initiative 1:** Objective, resources needed, success metrics",
                "2. **Initiative 2:** Objective, resources needed, success metrics",
                "",
                "### Long-term Strategy (1-6 months)",
                "1. **Strategy 1:** Goals, ROI projection, implementation plan",
                "2. **Strategy 2:** Goals, ROI projection, implementation plan",
                "",
                "## 📋 Implementation Timeline",
                "| Phase | Duration | Key Milestones | Success Metrics |",
                "|-------|----------|----------------|-----------------|",
                "| ... ..| ........ | .............. | ............... |",
                "",
                f"**please use the Language:** {Process_Request.Language} **for this report",
                "",
                "**Quality Requirements:**",
                "- Each section must be clearly separated with proper headers",
                "- All tables must be properly formatted with consistent columns",
                "- No raw CSV data presentation",
                "- Include specific, measurable recommendations",
                "- Use professional, executive-friendly language",
                "- NEVER output raw CSV data"
                "- ALWAYS convert to markdown tables",
                "- ALWAYS use | separators"
            ])
            
    translation_agent_provider = TranslationEnglishArabic()
    translation_agent = translation_agent_provider.get_agent()
    translation_task = translation_agent_provider.get_task()
    translation_task.description ="\n".join([
                        "Translate the comprehensive inventory analysis report from English to Arabic.",
                        "Ensure technical terms are accurately translated and the report maintains its professional structure and actionable insights."
                                        ])
            
    if Process_Request.Language== Languages.ARABIC.value:
                              
        crew = Crew(
                    agents=[Data_Processing_Agent,
                            Demand_ForecastingAnalyst_Agent,
                            Inventory_OptimizationExpert_Agent,
                            Inventory_AnalysisReportingSpecialist_Agent,
                            translation_agent
                            ],
                    
                    tasks=[Data_Processing_task ,
                           Demand_ForecastingAnalyst_task,
                           Inventory_OptimizationExpert_task,
                           Inventory_AnalysisReportingSpecialist_task,
                           translation_task],
                            verbose=True
                                )
                
        result = crew.kickoff()
        
        agent_result_Arabic = AgentResult(
                    result_uuid=uuid.uuid4(),
                    result_data=str(result), 
                    project_id=project_id,
                    agent_name="Inventory Managment Arabic",
                    status="completed"
                )
        
        agent  = await agent_model.create_agent_result(
                result = agent_result_Arabic
                )
        
        agent_Relation  = await agent_Relation_model.get_relation_or_create_one(
                     file_id=latest_file.file_id, 
                     agent_result_id = agent.result_id, 
                     usage_type =UsageType.INPUT.value
                     
                            )
        
        
        return JSONResponse(
                content ={
                    "signal" : ResponseSignal.RESPONSE_SUCCESS.value,
                    "resultS" : str(agent.result_data),
                    "created_at":str(agent_Relation.created_at)
                    
                }
        )
    
                    
    elif Process_Request.Language== Languages.ENGLISH.value:
        crew = Crew( 
                agents=[Data_Processing_Agent,
                        Demand_ForecastingAnalyst_Agent,
                        Inventory_OptimizationExpert_Agent,
                        Inventory_AnalysisReportingSpecialist_Agent
                                ],
                        
                tasks=[Data_Processing_task ,
                       Demand_ForecastingAnalyst_task,
                       Inventory_OptimizationExpert_task,
                       Inventory_AnalysisReportingSpecialist_task],
                       verbose=True
                            )
                
        res = crew.kickoff()
        
        agent_result_English = AgentResult(
                    result_uuid=uuid.uuid4(),
                    result_data=str(res), 
                    project_id=project_id,
                    agent_name="Inventory Managment English",
                    status="completed"
                )
        
        agent  = await agent_model.create_agent_result(
                result = agent_result_English
                )
        
        
        agent_Relation  = await agent_Relation_model.get_relation_or_create_one(
                     file_id=latest_file.file_id, 
                     agent_result_id = agent.result_id, 
                     usage_type =UsageType.INPUT.value
                     
                            )
        
        return JSONResponse(
                content ={
                    "signal" : ResponseSignal.RESPONSE_SUCCESS.value,
                    "resultS" : str(agent.result_data),
                    "created_at":str(agent_Relation.created_at)
                    
                }
        )
                


        
        
        
  
    
    
   
    
    

            
    
  
    
  
    
   
    
    
                                
    
    
    
   
    