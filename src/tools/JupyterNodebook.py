from crewai.tools import BaseTool
from pydantic import BaseModel
from typing import Type, Optional
from jupyter_client import KernelManager, BlockingKernelClient 
from .Schema.JuptyerSchema import JupyterKernelInput


class LiveJupyterKernelTool(BaseTool):
    name: str = "LiveJupyterKernelTool"
    description: str = (
        "Executes Python code in a persistent Jupyter kernel session, maintaining all previous variables."
    )
    args_schema: Type[BaseModel] = JupyterKernelInput

    km: Optional[KernelManager] = None
    kc: Optional[BlockingKernelClient] = None 

    def _ensure_kernel(self):
        """Ensure a persistent kernel is running only once for this specific Agent instance."""

        if not self.km or not self.kc:
            self.km = KernelManager()
            self.km.start_kernel()
            self.kc = self.km.client(
           
            ) 
            self.kc.start_channels()
            try:
                self.kc.wait_for_ready(timeout=60)
            except Exception as e:
                raise RuntimeError(f"Failed to start Jupyter kernel: {e}")

    def _run(self, code: str):
        self._ensure_kernel()
        kc = self.kc 
        
    def restart_kernel(self):
        try:
            if self.kc:
                self.kc.stop_channels()
            if self.km:
                self.km.shutdown_kernel(now=True)
            self.km = None
            self.kc = None
            return "🔁 Kernel restarted successfully."
        except Exception as e:
            return f"❌ Kernel restart failed: {e}"

    def __del__(self):
        try:
            if self.kc:
                self.kc.stop_channels()
            if self.km:
                self.km.shutdown_kernel(now=True)
        except Exception:
            pass