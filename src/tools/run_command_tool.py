import subprocess
from crewai.tools import BaseTool
from pydantic import Field


class RunCommandTool(BaseTool):
    name: str = "run_command_tool"
    description: str = (
        "A tool that executes shell commands inside a specified working directory "
        "and returns the full output."
    )

    working_dir: str = Field(".", description="The working directory (default is current directory)")

    def _run(self, command: str, working_dir: str = ".") -> str:
        """
        Execute a shell command and return its output.
        """
        try:
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
            if len(output) > 2000:
                output = (
                    output[:500]
                    + "\n\n[...content clipped...]\n\n"
                    + output[-500:]
                )

            if error_code == 0:
                return f"✅ Command executed successfully:\n{output}"
            else:
                return f"❌ Command failed (exit code={error_code}):\n{output}"

        except Exception as e:
            return f"⚠️ Exception occurred: {str(e)}"
