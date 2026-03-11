import streamlit as st

from src.io_utils import load_dataframe, list_excel_sheets
from src.analyzer import assess_readiness, detect_outliers
from src.ai_assistant import ask_gpt
from src.charts import missing_chart, outlier_chart
from src.pdf_report import generate_pdf

st.title("AI Data Quality Analyst")

if "history" not in st.session_state:
    st.session_state.history = []

uploaded = st.file_uploader("Upload CSV or Excel")

analysis_type = st.sidebar.selectbox(
    "Analysis Type",
    ["general", "missing", "outliers", "duplicates"]
)

question = st.text_input("Ask a question about your data")

if uploaded:

    if uploaded.name.endswith(".xlsx"):

        sheets = list_excel_sheets(uploaded)

        sheet = st.selectbox("Choose sheet", sheets)

        df = load_dataframe(uploaded, sheet)

    else:
        df = load_dataframe(uploaded)

    st.subheader("Preview")

    st.dataframe(df.head())

    score, issues = assess_readiness(df)

    outliers = detect_outliers(df)

    st.metric("Data Quality Score", score)

    if st.button("Analyze"):

        context = f"""
Rows: {df.shape[0]}
Columns: {df.shape[1]}
Missing: {issues['missing_ratio']}
Duplicates: {issues['duplicate_ratio']}
Outliers: {issues['outlier_ratio']}
"""

        result = ask_gpt(question, context, analysis_type)

        st.session_state.history.append((question, result))

        st.subheader("Executive Summary")
        st.write(result["executive_summary"])

        st.subheader("Direct Answer")
        st.write(result["direct_answer"])

        st.subheader("Findings")
        for f in result["findings"]:
            st.write("-", f)

        st.subheader("Recommendations")
        for r in result["recommendations"]:
            st.write("-", r)

        st.pyplot(missing_chart(df))
        st.pyplot(outlier_chart(outliers))

        pdf = generate_pdf(result)

        st.download_button(
            "Download PDF Report",
            pdf,
            file_name="report.pdf"
        )

st.sidebar.subheader("Question History")

for q, _ in st.session_state.history[-5:]:
    st.sidebar.write(q)
