from pydantic import BaseModel, Field

class JupyterKernelInput(BaseModel):
    code: str = Field(..., description="Python code to execute inside a live Jupyter kernel")
