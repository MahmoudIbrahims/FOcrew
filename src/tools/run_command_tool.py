import subprocess
import os
from crewai.tools import BaseTool
from pydantic import Field
from typing import Optional


class RunCommandTool(BaseTool):
    name: str = "run_command_tool"
    description: str = (
        "A tool that executes shell commands inside a specified working directory "
        "and returns the full output."
    )

    working_dir: Optional[str] = Field("working", description="The working directory (default is 'working')")


    def _run(self, command: str, working_dir: str = "working") -> str:
        """
        Execute a shell command and return its output.
        """
        try:
            # Ensure the directory exists, create it if it doesn't
            os.makedirs(self.working_dir, exist_ok=True)

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=self.working_dir,
            )
            output, _ = process.communicate()
            error_code = process.returncode

            # Clip overly long outputs to avoid flooding the console
            if len(output) > 1400:
                output = (
                    output[:700]
                    + "\n\n[...content clipped...]\n\n"
                    + output[-700:]
                )

            if error_code == 0:
                return f"✅ Command executed successfully:\n{output}"
            else:
                return f"❌ Command failed (exit code={error_code}):\n{output}"

        except Exception as e:
            return f"⚠️ An exception occurred: {str(e)}"
