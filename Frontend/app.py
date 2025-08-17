
import os
import json
import requests
import streamlit as st

st.set_page_config(page_title="Inventory Pro Dashboard", page_icon="📦", layout="wide")

API_BASE = os.getenv("API_BASE", "http://localhost:8000/api/v1")
DEFAULT_PROJECT_ID = int(os.getenv("PROJECT_ID", "1"))

with st.sidebar:
    st.header("📤 Upload & Run")
    project_id = st.number_input("Project ID", min_value=1, value=DEFAULT_PROJECT_ID, step=1)
    company = st.text_input("🏢 Company Name", "My Company")
    industry = st.text_input("🏭 Industry Name", "Retail")
    lang = st.selectbox("🌍 Language", ["ENGLISH", "ARABIC"])

    uploaded_file = st.file_uploader("Choose file (CSV/XLSX)", type=["csv", "xlsx"])

    col1, col2 = st.columns(2)
    with col1:
        do_upload = st.button("⬆️ Upload")
    with col2:
        do_generate = st.button("🚀 Generate Report")

    st.caption("API Base: " + API_BASE)

if "project_id" not in st.session_state:
    st.session_state["project_id"] = DEFAULT_PROJECT_ID

if do_upload:
    if uploaded_file is None:
        st.error("Please choose a file first.")
    else:
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type or "application/octet-stream")}
        try:
            resp = requests.post(f"{API_BASE}/file/upload/{project_id}", files=files, timeout=120)
            if resp.status_code == 200:
                st.session_state["project_id"] = project_id
                st.success("File uploaded ✅")
            else:
                st.error(f"Upload failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            st.exception(e)

if do_generate:
    payload = {"COMPANY_NAME": company, "INDUSTRY_NAME": industry, "Language": lang}
    try:
        resp = requests.post(f"{API_BASE}/agent/inventory/{project_id}", json=payload, timeout=600)
        if resp.status_code == 200:
            data = resp.json()
            st.session_state["report_text"] = data.get("results", "")
            st.session_state["created_at"] = data.get("created_at", "")
            st.success("Report generated ✅ Go to pages 👉")
        else:
            st.error(f"Generation failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        st.exception(e)

st.title("📦 Inventory Pro Dashboard")
st.markdown("""
Welcome! Use the sidebar to upload your data and generate the inventory report.  
Navigate via the pages to view the **Markdown report**, **Charts & Tables**, and an **HTML Dashboard**.
""")
