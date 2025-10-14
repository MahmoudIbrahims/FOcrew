from crewai.tools import BaseTool
from pydantic import BaseModel
from typing import Type
import threading, subprocess, sys, os


class NotebookInput(BaseModel):
    code: str


class WindowNotebookTool(BaseTool):
    name: str = "Live Jupyter Notebook (Web)"
    description: str = (
        "Runs and displays Python code execution visually like Jupyter Notebook using Streamlit, "
        "keeping variables persistent and stacking new cells automatically."
    )
    args_schema: Type[BaseModel] = NotebookInput

    def _run(self, code: str):
       
        os.makedirs("notebook_cells", exist_ok=True)
        cell_path = f"notebook_cells/cell_{len(os.listdir('notebook_cells'))+1}.py"
        with open(cell_path, "w", encoding="utf-8") as f:
            f.write(code)

      
        with open("live_notebook_app.py", "w", encoding="utf-8") as f:
            f.write(self._generate_app())

        
        if not getattr(self, "_server_running", False):
            threading.Thread(target=self._run_streamlit_server, daemon=True).start()
            self._server_running = True

        return f"✅ Added new code cell → open http://localhost:8501 to see it live."

    def _run_streamlit_server(self):
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "live_notebook_app.py", "--server.headless=true"]
        )

    def _generate_app(self) -> str:
        """يبني تطبيق Streamlit يحاكي Jupyter Notebook بالكامل"""
        return """
import streamlit as st
import io, contextlib, traceback, glob, os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

st.set_page_config(page_title="🧠 Live Jupyter Notebook", layout="wide")
st.markdown("<h1 style='color:#00FFAA; text-align:center;'>🧠 AI Data Analyst - Interactive Notebook</h1>", unsafe_allow_html=True)

if "globals_dict" not in st.session_state:
    st.session_state.globals_dict = {}

cell_files = sorted(glob.glob("notebook_cells/cell_*.py"))

for i, cell in enumerate(cell_files, start=1):
    with open(cell, "r", encoding="utf-8") as f:
        code = f.read()
    st.markdown(f"### 🧩 Cell {i}")
    st.code(code, language="python")

    f_output = io.StringIO()
    with contextlib.redirect_stdout(f_output), contextlib.redirect_stderr(f_output):
        try:
            plt.close("all")
            exec(code, st.session_state.globals_dict)
            out_text = f_output.getvalue()
            if out_text.strip():
                st.text_area("Output", out_text, height=180, key=f"out_{i}")
            if plt.get_fignums():
                st.pyplot(plt.gcf())
        except Exception:
            st.text_area("❌ Error", traceback.format_exc(), height=200, key=f"err_{i}")

"""
