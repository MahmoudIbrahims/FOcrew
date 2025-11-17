from enum import Enum

class InventorManagmentEunms(Enum):
    AGENT_NAME ="Inventory Managment"
    STATUS="completed" 
    
    
class PathResults(Enum):
    ANALYSIS_REPORT_PATH ="results/inventory_management/Analysis_Report.md"
    PROFILLING_REPORT_PATH = "results/Dashboard/Profiling_Report.html"
    REPORT_PDF ="results/inventory_management/report.pdf"