from crewai import Agent,Task
from tools.run_command_tool import RunCommandTool
from Providers import ProviderLLM
from ..BaseAgent import BaseAgent

class DataVisualizerAgent(BaseAgent):
    def __init__(self):
        llm = ProviderLLM().get_llm()
        cmd_tool = RunCommandTool()

        super().__init__(
            name="DataVisualizerAgent",
            role="Data Visualizer",
            goal="Generate visualizations using matplotlib and seaborn.",
            backstory="Creates compelling graphs to highlight insights and trends.",
            llm=llm,
            tools=[cmd_tool],
        )
        
    def get_task(self):
           return Task(
                description=(
                    "Generate visualizations based on the analytical insights.\n\n"
                    "Steps:\n"
                    "1. Create Python code using matplotlib/seaborn for relevant charts.\n"
                    "2. Execute visualization code using RunCommandTool.\n"
                    "3. Save the charts and summarize what each chart shows.\n"
                    "4. Return visualization paths and descriptions for report writing."
                ),
                expected_output="A set of visualizations (paths + descriptions) illustrating data insights.",
                agent=self.get_agent(),
                context_keys=["analysis_summary"],
                output_key="visualization_summary"
            )