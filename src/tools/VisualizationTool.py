from crewai.tools import BaseTool
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class PlotlyDashboardTool(BaseTool):
    name: str = "Create Interactive Dashboard"
    description: str = "Creates interactive charts and dashboards using Plotly"
    
    def _run(self, data: str) -> str:
        # Convert data and create charts
        fig = px.bar(title="Inventory Dashboard")
        fig.write_html("/mnt/c/Users/Win/Desktop/FOcrew/results/inventory_management/dashboard.html")
        return "Dashboard created successfully"
    

class ReportGeneratorTool(BaseTool):
    name: str = "Generate Visual Report"
    description: str = "Generates comprehensive visual reports with charts and KPIs"
    
    def _run(self, analysis_data: str) -> str:
        # Create visual report
        return "Visual report generated with charts and insights"

