from crewai.tools import BaseTool
from pydantic import BaseModel, PrivateAttr
from typing import Type
import threading, os, io, contextlib, traceback
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import base64
import matplotlib.pyplot as plt


class NotebookInput(BaseModel):
    code: str


class FastAPINotebookTool(BaseTool):
    name: str = "Live Jupyter Notebook (Web)"
    description: str = (
        "Runs and displays Python code execution visually like Jupyter Notebook "
        "using FastAPI web interface with persistent variables and stacked cells."
    )
    args_schema: Type[BaseModel] = NotebookInput

    _globals_dict: dict = PrivateAttr()
    _cells: list = PrivateAttr()
    _server_started: bool = PrivateAttr()
    _port: int = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)

        self._globals_dict = {}
        self._cells = []
        self._server_started = False
        self._port = 8001

    def _run(self, code: str):
        """run the code as new cell"""
        os.makedirs("fastapi_notebook", exist_ok=True)
        output, error, image_data = self._execute_code(code)

        self._cells.append({
            "code": code.strip(),
            "output": output.strip(),
            "error": error.strip() if error else None,
            "image": image_data
        })

        if not self._server_started:
            threading.Thread(target=self._start_server, daemon=True).start()
            self._server_started = True

        return f"✅ Code executed and added as a new cell → open http://localhost:{self._port} to view the live notebook."

    def _execute_code(self, code: str):
        f_output = io.StringIO()
        img_data = None
        with contextlib.redirect_stdout(f_output), contextlib.redirect_stderr(f_output):
            try:
                plt.close("all")
                exec(code, self._globals_dict)
                if plt.get_fignums():
                    buf = io.BytesIO()
                    plt.savefig(buf, format="png")
                    buf.seek(0)
                    img_data = base64.b64encode(buf.read()).decode("utf-8")
                return f_output.getvalue(), None, img_data
            except Exception:
                return "", traceback.format_exc(), None

    def _start_server(self):
        app = self._build_app()
        uvicorn.run(app, host="0.0.0.0", port=self._port, log_level="error")

    def _build_app(self):
        app = FastAPI(title="FOcrew Live Notebook")
        app.mount("/docs", StaticFiles(directory="../docs"), name="docs")

        @app.get("/", response_class=HTMLResponse)
        def home():
            return self._generate_notebook_view()

        @app.get("/cells")
        def get_cells():
            return JSONResponse({"cells": self._cells})

        return app

    def _generate_notebook_view(self) -> str:
        """Generate a simple HTML page showing executed cells dynamically."""
        return f"""
        <html>
        <head>
            <title>FOcrew Notebook</title>
            <style>
                body {{
                    background-color: #fafafa;
                    color: #1a1a1a;
                    font-family: 'Source Code Pro', monospace;
                    padding: 30px;
                }}
                h1 {{
                    text-align: center;
                    color: #0055cc;
                    margin-bottom: 30px;
                }}
                .cell {{
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 15px;
                    background: #fff;
                    margin-bottom: 20px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                    transition: all 0.3s ease-in-out;
                }}
                pre {{
                    background: #f5f5f5;
                    border-radius: 5px;
                    padding: 10px;
                    white-space: pre-wrap;
                    overflow-x: auto;
                    color: #333;
                }}
                .error {{
                    background: #ffeaea;
                    border-left: 4px solid #ff5555;
                    padding: 10px;
                    color: #a00000;
                    border-radius: 5px;
                }}
                img {{
                    max-width: 100%;
                    border-radius: 5px;
                    margin-top: 10px;
                }}
                .label {{
                    font-weight: bold;
                    color: #888;
                }}
                .input {{
                    color: #0d6efd;
                }}
                .output {{
                    color: #444;
                }}
            </style>
        </head>
        <body>
            <h1>FOcrew Live Notebook</h1>
            <div id="cells"></div>
            <script>
                let lastCount = 0;
                async function loadCells() {{
                    const res = await fetch('/cells');
                    const data = await res.json();
                    const container = document.getElementById('cells');

                    if (data.cells.length === lastCount) return;
                    lastCount = data.cells.length;

                    container.innerHTML = '';
                    data.cells.forEach((cell, i) => {{
                        container.innerHTML += `
                            <div class='cell'>
                                <div class='label input'>In [${{i+1}}]:</div>
                                <pre>${{cell.code}}</pre>
                                ${{
                                    cell.error
                                        ? `<div class='label output'>Error:</div><pre class='error'>${{cell.error}}</pre>`
                                        : `<div class='label output'>Out [${{i+1}}]:</div><pre>${{cell.output || ''}}</pre>`
                                }}
                                ${{cell.image ? `<img src='data:image/png;base64,${{cell.image}}'/>` : ''}}
                            </div>
                        `;
                    }});

                    window.scrollTo({{ top: document.body.scrollHeight, behavior: 'smooth' }});
                }}

                setInterval(loadCells, 1000);
                loadCells();
            </script>
        </body>
        </html>
        """
    