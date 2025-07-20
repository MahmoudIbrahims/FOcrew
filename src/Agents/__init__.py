from .AgentProvider import DataAnalysisSpecialist
from .AgentProvider import DemandForecastingAnalyst
from .AgentProvider import InventoryOptimizationExpert
from .AgentProvider import InventoryAnalysisReportingSpecialist
from .AgentProvider import DataVisualizationExpert
#______________________________________________________________
from .AgentProvider import TranslationEnglishArabic
#=======================================================================
# ------> prompts

from .Prompts.InventoryAnalysisReportPrompt import finally_description_prompt, finally_expected_output_prompt
from .Prompts.DataِAnalysisPrompt import Analysis_description_prompt
from .Prompts.DataVisulizationPrompt import Visualization_description_prompt ,Visualization_expected_output_prompt
from .Prompts.TranslationPrompt import translation_description_prompt