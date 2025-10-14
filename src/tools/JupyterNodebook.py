from crewai.tools import BaseTool
from pydantic import BaseModel
from typing import Type, Optional, ClassVar
from jupyter_client import KernelManager
from .Schema.JuptyerSchema import JupyterKernelInput
import time
import traceback

class LiveJupyterKernelTool(BaseTool):
    name: str = "LiveJupyterKernelTool"
    description: str = (
        "Executes Python code in a persistent Jupyter kernel session, maintaining all previous variables."
    )
    args_schema: Type[BaseModel] = JupyterKernelInput

    km: ClassVar[Optional[KernelManager]] = None
    kc: ClassVar[Optional[object]] = None

    def _ensure_kernel(self):
        """Ensure a persistent kernel is running only once."""
        if not type(self).km or not type(self).kc:
            type(self).km = KernelManager()
            type(self).km.start_kernel()
            type(self).kc = type(self).km.client()
            type(self).kc.start_channels()
            time.sleep(0.5)

    def _run(self, code: str):
        """Execute code persistently and return outputs/errors."""
        self._ensure_kernel()
        kc = type(self).kc

        try:
            msg_id = kc.execute(code)
            output_lines = []

            while True:
                msg = kc.get_iopub_msg(timeout=10)
                msg_type = msg["header"]["msg_type"]

                if msg_type == "stream":
                    output_lines.append(msg["content"]["text"])
                elif msg_type == "display_data":
                    output_lines.append(str(msg["content"]["data"]))
                elif msg_type == "execute_result":
                    output_lines.append(str(msg["content"]["data"]))
                elif msg_type == "error":
                    traceback_text = "\n".join(msg["content"]["traceback"])
                    output_lines.append(f"❌ Error:\n{traceback_text}")
                elif msg_type == "status" and msg["content"]["execution_state"] == "idle":
                    break

            return "\n".join(output_lines) if output_lines else "✅ Executed successfully with no output."

        except Exception as e:
            tb = traceback.format_exc()
            return f"❌ Execution error: {e}\n\n{tb}"

    def restart_kernel(self):
        """Optional manual kernel reset."""
        try:
            if type(self).kc:
                type(self).kc.stop_channels()
            if type(self).km:
                type(self).km.shutdown_kernel(now=True)
            type(self).km = None
            type(self).kc = None
            return "🔁 Kernel restarted successfully."
        except Exception as e:
            return f"❌ Kernel restart failed: {e}"

    def __del__(self):
        try:
            if type(self).kc:
                type(self).kc.stop_channels()
            if type(self).km:
                type(self).km.shutdown_kernel(now=True)
        except Exception:
            pass
