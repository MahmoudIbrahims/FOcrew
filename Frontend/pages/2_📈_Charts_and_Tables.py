
import io
import re
import pandas as pd
import plotly.express as px
import streamlit as st

st.title("📈 Charts & Tables")

report_text = st.session_state.get("report_text", "")

if not report_text:
    st.warning("No report available yet. Generate it from the sidebar in the Home page.")
    st.stop()

st.info("Trying to detect Markdown tables in your report...")

def extract_markdown_tables(md: str):
    import re, pandas as pd, io
    parts = re.split(r"```.*?```", md, flags=re.S)
    tables = []
    for part in parts:
        blocks = re.split(r"\n\s*\n", part)
        for block in blocks:
            lines = [ln.strip() for ln in block.strip().splitlines() if ln.strip()]
            if len(lines) >= 2 and all("|" in ln for ln in lines[:2]):
                csv_like = "\n".join(lines)
                try:
                    df = pd.read_csv(io.StringIO(csv_like), sep="|", engine="python")
                    df = df.drop(columns=[c for c in df.columns if "Unnamed" in c], errors="ignore")
                    df.columns = [c.strip() for c in df.columns]
                    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                    if df.shape[0] and any(set(str(x)) <= {"-"} for x in df.iloc[0].astype(str)):
                        df = df.iloc[1:].reset_index(drop=True)
                    if len(df.columns) >= 2:
                        tables.append(df)
                except Exception:
                    pass
    return tables

tables = extract_markdown_tables(report_text)

if not tables:
    st.warning("No tables were detected in the report. Make sure the report contains Markdown tables.")
    st.stop()

tab_titles = [f"Table {i+1} ({t.shape[0]}×{t.shape[1]})" for i, t in enumerate(tables)]
selected = st.selectbox("Select a table to explore:", options=range(len(tables)), format_func=lambda i: tab_titles[i])

df = tables[selected]
st.subheader("📋 Selected Table")
st.dataframe(df, use_container_width=True)

qty_cols = [c for c in df.columns if c.lower() in {"available quantity", "quantity", "stock", "on_hand"}]
name_cols = [c for c in df.columns if any(k in c.lower() for k in ["product", "item", "sku", "name"])]

if qty_cols and name_cols:
    ycol = qty_cols[0]
    xcol = name_cols[0]
    st.markdown("#### Bar Chart: Stock Levels")
    fig = px.bar(df.sort_values(by=ycol, ascending=False).head(25), x=xcol, y=ycol, title="Top 25 by Quantity")
    st.plotly_chart(fig, use_container_width=True)

date_cols = [c for c in df.columns if any(k in c.lower() for k in ["expiration", "expiry", "removal", "date"])]
if date_cols:
    import pandas as pd
    temp = df.copy()
    for c in date_cols:
        temp[c] = pd.to_datetime(temp[c], errors="coerce")
    dcol = next((c for c in date_cols if temp[c].notnull().any()), None)
    if dcol:
        st.markdown(f"#### Timeline: {dcol}")
        ts = temp[[dcol]].dropna()
        ts["month"] = ts[dcol].dt.to_period("M").dt.to_timestamp()
        grp = ts.groupby("month").size().reset_index(name="count")
        if not grp.empty:
            fig2 = px.line(grp, x="month", y="count", markers=True, title=f"Items over time by {dcol}")
            st.plotly_chart(fig2, use_container_width=True)

st.download_button("⬇️ Download table as CSV", data=df.to_csv(index=False), file_name="table.csv", mime="text/csv")
