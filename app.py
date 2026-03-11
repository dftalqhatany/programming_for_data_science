import streamlit as st
from src.data_loader import load_data
from src.agent import run_agent

st.set_page_config(page_title="AI Data Quality Analyst", layout="wide")

st.title("🤖 AI Data Quality Analyst")
st.write("Upload your dataset and ask your question in English or Arabic.")

st.info("""
Example questions:
- Analyze data quality
- Find missing values
- Detect duplicates
- Analyze data quality and answer in Arabic
- حلل جودة البيانات
- اكتشف القيم المفقودة
""")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    df = load_data(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    user_question = st.text_area(
        "What would you like to analyze?",
        value="Analyze the overall data quality and give me the main issues and recommendations.",
        height=120
    )

    if st.button("Analyze Data"):
        with st.spinner("Analyzing data..."):
            analysis, report = run_agent(df, user_question)

        st.subheader("📊 Report")
        st.write(report)

        st.subheader("📑 Technical Results")
        st.json(analysis)
