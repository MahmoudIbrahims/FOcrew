
import streamlit as st
from fpdf import FPDF
from io import BytesIO

st.title("📄 Inventory Report (Markdown)")

report_text = st.session_state.get("report_text", "")
created_at = st.session_state.get("created_at", "")

if not report_text:
    st.warning("No report available yet. Generate it from the sidebar in the Home page.")
    st.stop()

st.caption(f"Created at: {created_at}")
st.markdown(report_text)

st.download_button("📥 Download Markdown", data=report_text, file_name="inventory_report.md", mime="text/markdown")

def to_pdf_bytes(text: str) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.splitlines():
        pdf.multi_cell(0, 8, line)
    bio = BytesIO()
    pdf.output(bio)
    return bio.getvalue()

pdf_bytes = to_pdf_bytes(report_text)
st.download_button("📄 Download PDF", data=pdf_bytes, file_name="inventory_report.pdf", mime="application/pdf")
