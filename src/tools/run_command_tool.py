import subprocess
import os
from crewai.tools import BaseTool
from pydantic import Field
from typing import Optional, Tuple

class RunCommandTool(BaseTool):
    name: str = "run_command_tool"
    description: str = (
        "Execute shell or Python commands safely inside an isolated working directory. "
        "Use this tool to install packages, run scripts, and perform data analysis tasks. "
        "For large outputs (e.g., big data dumps), the output will be automatically saved to a file, "
        "and the file path will be returned instead of the raw output."
    )
    # The working directory where all files/scripts will be executed and saved
    working_dir: Optional[str] = Field("working", description="Working directory")

    def _run(self, command: str) -> str:
        """Executes a command (shell or multi-line Python) and manages large output."""
        
        # We use a large threshold for better handling of standard data analysis logs
        LARGE_OUTPUT_THRESHOLD = 50000 
        OUTPUT_FILENAME = "output_log.txt"

        try:
            # 1. Ensure the isolated working directory exists
            os.makedirs(self.working_dir, exist_ok=True)

            # 2. Prepare multi-line Python code for execution
            # if "\n" in command:
                # This uses a 'here-document' to pass the multi-line Python code 
                # as input to the python3 interpreter.
                # command = f'python3 - << "EOF"\n{command}\nEOF'
            if "\n" in command and not command.strip().startswith('python3 -c') and not command.strip().startswith('python'):
                command = f'python3 - << "EOF"\n{command}\nEOF'

            # 3. Execute the command using subprocess.Popen
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Merge stderr into stdout for single capture
                text=True,
                cwd=self.working_dir,  # Crucial for data analysis to keep files isolated
            )

            # 4. Wait for the process to complete and capture all output
            # This is efficient for capturing full output needed for logging/file saving.
            output, _ = process.communicate()
            code = process.returncode

            # 5. Handle large output by saving to a file
            if len(output) > LARGE_OUTPUT_THRESHOLD:
                path = os.path.join(self.working_dir, OUTPUT_FILENAME)
                with open(path, "w") as f:
                    f.write(output)
                
                # Return the file path to the LLM instead of the massive string
                return (
                    f"✅ Command executed successfully. "
                    f"Output was too large ({len(output)} chars) and saved to file: `{path}`"
                )

            # 6. Return standard success/failure message
            if code == 0:
                return f"✅ Command executed successfully:\n{output}"
            else:
                return f"❌ Command failed (exit code={code}):\n{output}"

        except Exception as e:
            return f"⚠️ Internal exception: {str(e)}"

