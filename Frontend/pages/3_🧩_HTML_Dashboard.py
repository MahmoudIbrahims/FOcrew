
import os
import json
import streamlit as st
import streamlit.components.v1 as components

st.title("🧩 HTML Dashboard (Embedded)")

report_text = st.session_state.get("report_text", "")
if not report_text:
    st.warning("No report available yet. Generate it from the sidebar in the Home page.")
    st.stop()

sample_payload = {
    "kpis": {"total_items": 9274, "low_stock": 142, "near_expiry": 88, "recommended_reorders": 61},
    "series": {"labels": ["A", "B", "C", "D", "E"], "values": [120, 90, 60, 45, 30]},
    "pie": {"labels": ["On Hand", "Reserved", "Damaged"], "values": [8200, 700, 374]}
}

html_path = os.path.join("assets", "templates", "dashboard.html")
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("{{DATA_JSON}}", json.dumps(sample_payload))
components.html(html, height=900, scrolling=True)
