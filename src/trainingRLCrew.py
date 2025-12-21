from Agents import (DataReaderAgent, DataCleanerAgent, DataAnalyzerAgent, 
                DataVisualizerAgent, ReportWriterAgent, ReportGeneratorAgent)

from crewai import Crew
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_analysis_training():
    
    problem_file = os.path.join(BASE_DIR, "Train_crew", "financial.csv")
    output_pkl = os.path.join(BASE_DIR, "Train_crew", "data_analysis_expertise.pkl")

    if not os.path.exists(problem_file):
        print(f"❌ File not found at: {problem_file}")
        return

    inputs = {
        "file_path": problem_file,  
        "company_name": "Power",
        "industry_name": "online groceries",
        "language": "English"}
    
    agents = [
        DataReaderAgent().get_agent(),
        DataCleanerAgent().get_agent(),
        DataAnalyzerAgent().get_agent(),
        DataVisualizerAgent().get_agent(),
        ReportWriterAgent().get_agent(),
        ReportGeneratorAgent().get_agent()
    ]
    tasks = [
        DataReaderAgent().get_task(),
        DataCleanerAgent().get_task(),
        DataAnalyzerAgent().get_task(),
        DataVisualizerAgent().get_task(),
        ReportWriterAgent().get_task(),
        ReportGeneratorAgent().get_task()
    ]

    my_crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True
    )

    try:
        my_crew.train(
            n_iterations=3, 
            filename=str(output_pkl),        
            inputs=inputs
        )
        print("Success: Training session finished and file saved.")
    except Exception as e:
        print(f"Error during training: {e}")

if __name__ == "__main__":
    run_analysis_training() 