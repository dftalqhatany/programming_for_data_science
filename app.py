import os
from io import BytesIO

import streamlit as st

from src.io_utils import load_dataframe, list_excel_sheets
from src.analyzer import assess_readiness, detect_outliers
from src.ai_assistant import ask_gpt, detect_language
from src.charts import missing_chart, outlier_chart
from src.pdf_report import generate_pdf


def get_ui_labels(language="en"):
    if language == "ar":
        return {
            "title": "محلل جودة البيانات بالذكاء الاصطناعي",
            "upload_label": "ارفع ملف CSV أو Excel",
            "analysis_type": "نوع التحليل",
            "analysis_options": {
                "تحليل عام": "general",
                "القيم المفقودة": "missing",
                "القيم الشاذة": "outliers",
                "التكرارات": "duplicates",
            },
            "question_label": "اكتب سؤالك عن البيانات",
            "sheet_label": "اختر الورقة",
            "preview_title": "معاينة البيانات",
            "score_label": "درجة جودة البيانات",
            "analyze_button": "تحليل",
            "executive_summary": "الملخص التنفيذي",
            "direct_answer": "الإجابة المباشرة",
            "findings": "النتائج",
            "recommendations": "التوصيات",
            "next_steps": "الخطوات التالية",
            "download_pdf": "تحميل تقرير PDF",
            "history_title": "سجل الأسئلة",
            "dataset_info": "معلومات البيانات",
            "rows": "عدد الصفوف",
            "columns": "عدد الأعمدة",
            "missing_ratio": "نسبة القيم المفقودة",
            "duplicate_ratio": "نسبة التكرارات",
            "outlier_ratio": "نسبة القيم الشاذة",
            "empty_columns": "الأعمدة الفارغة",
            "constant_columns": "الأعمدة الثابتة",
            "issues_tab": "مشاكل الجودة",
            "charts_tab": "الرسوم البيانية",
            "data_tab": "البيانات",
            "no_question_warning": "اكتبي سؤالًا أولًا ثم اضغطي تحليل.",
            "file_ready": "تم الاحتفاظ بالملف بنجاح.",
            "api_key_missing": "متغير OPENAI_API_KEY غير موجود.",
        }

    return {
        "title": "AI Data Quality Analyst",
        "upload_label": "Upload CSV or Excel",
        "analysis_type": "Analysis Type",
        "analysis_options": {
            "General Analysis": "general",
            "Missing Values": "missing",
            "Outliers": "outliers",
            "Duplicates": "duplicates",
        },
        "question_label": "Ask a question about your data",
        "sheet_label": "Choose sheet",
        "preview_title": "Data Preview",
        "score_label": "Data Quality Score",
        "analyze_button": "Analyze",
        "executive_summary": "Executive Summary",
        "direct_answer": "Direct Answer",
        "findings": "Findings",
        "recommendations": "Recommendations",
        "next_steps": "Next Steps",
        "download_pdf": "Download PDF Report",
        "history_title": "Question History",
        "dataset_info": "Dataset Info",
        "rows": "Rows",
        "columns": "Columns",
        "missing_ratio": "Missing Ratio",
        "duplicate_ratio": "Duplicate Ratio",
        "outlier_ratio": "Outlier Ratio",
        "empty_columns": "Empty Columns",
        "constant_columns": "Constant Columns",
        "issues_tab": "Quality Issues",
        "charts_tab": "Charts",
        "data_tab": "Data",
        "no_question_warning": "Please enter a question first, then click Analyze.",
        "file_ready": "File is stored successfully.",
        "api_key_missing": "OPENAI_API_KEY is missing.",
    }


def summarize_context(df, issues, outliers, max_columns=12, max_outlier_cols=10):
    column_names = df.columns.tolist()[:max_columns]
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.head(max_columns).items()}
    outlier_items = list(outliers.items())[:max_outlier_cols]

    context = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names_sample": column_names,
        "dtypes_sample": dtypes,
        "missing_ratio": round(float(issues["missing_ratio"]), 4),
        "duplicate_ratio": round(float(issues["duplicate_ratio"]), 4),
        "outlier_ratio": round(float(issues["outlier_ratio"]), 4),
        "empty_columns": issues["empty_columns"][:10],
        "constant_columns": issues["constant_columns"][:10],
        "outliers_sample": dict(outlier_items),
        "sample_rows": df.head(3).fillna("").astype(str).to_dict(orient="records"),
    }
    return str(context)


def init_session_state():
    defaults = {
        "history": [],
        "last_language": "en",
        "uploaded_file_name": None,
        "uploaded_file_bytes": None,
        "selected_sheet": None,
        "latest_result": None,
        "latest_outliers": None,
        "latest_df": None,
        "latest_issues": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_uploaded_file_from_session():
    file_bytes = st.session_state.get("uploaded_file_bytes")
    file_name = st.session_state.get("uploaded_file_name")

    if not file_bytes or not file_name:
        return None

    buffer = BytesIO(file_bytes)
    buffer.name = file_name
    return buffer


st.set_page_config(page_title="AI Data Quality Analyst", layout="wide")
init_session_state()

question_preview = st.session_state.get("question_input", "")
current_language = detect_language(question_preview) if question_preview else st.session_state["last_language"]
ui = get_ui_labels(current_language)

st.title(ui["title"])

if not os.getenv("OPENAI_API_KEY"):
    st.error(ui["api_key_missing"])
    st.stop()

with st.sidebar:
    st.subheader(ui["analysis_type"])
    analysis_label = st.selectbox(
        ui["analysis_type"],
        list(ui["analysis_options"].keys()),
        key="analysis_type_select",
    )
    analysis_type = ui["analysis_options"][analysis_label]

uploaded_file = st.file_uploader(
    ui["upload_label"],
    type=["csv", "xlsx"],
    key="file_upload",
)

if uploaded_file is not None:
    st.session_state["uploaded_file_name"] = uploaded_file.name
    st.session_state["uploaded_file_bytes"] = uploaded_file.getvalue()
    st.session_state["latest_result"] = None
    st.session_state["latest_outliers"] = None
    st.session_state["latest_df"] = None
    st.session_state["latest_issues"] = None

uploaded = get_uploaded_file_from_session()

question = st.text_input(
    ui["question_label"],
    key="question_input",
)

if question.strip():
    detected_language = detect_language(question)
    st.session_state["last_language"] = detected_language
    ui = get_ui_labels(detected_language)
else:
    detected_language = st.session_state["last_language"]
    ui = get_ui_labels(detected_language)

if uploaded is not None:
    st.success(ui["file_ready"])

    if uploaded.name.lower().endswith(".xlsx"):
        sheet_source = BytesIO(st.session_state["uploaded_file_bytes"])
        sheet_source.name = st.session_state["uploaded_file_name"]
        sheets = list_excel_sheets(sheet_source)

        default_index = 0
        if st.session_state["selected_sheet"] in sheets:
            default_index = sheets.index(st.session_state["selected_sheet"])

        selected_sheet = st.selectbox(
            ui["sheet_label"],
            sheets,
            index=default_index,
            key="sheet_select",
        )
        st.session_state["selected_sheet"] = selected_sheet

        data_source = BytesIO(st.session_state["uploaded_file_bytes"])
        data_source.name = st.session_state["uploaded_file_name"]
        df = load_dataframe(data_source, sheet_name=selected_sheet)
    else:
        data_source = BytesIO(st.session_state["uploaded_file_bytes"])
        data_source.name = st.session_state["uploaded_file_name"]
        df = load_dataframe(data_source)

    score, issues = assess_readiness(df)
    outliers = detect_outliers(df)

    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader(ui["preview_title"])
        st.dataframe(df.head())

    with right_col:
        st.subheader(ui["dataset_info"])
        st.metric(ui["score_label"], score)
        st.write(f"**{ui['rows']}:** {df.shape[0]}")
        st.write(f"**{ui['columns']}:** {df.shape[1]}")
        st.write(f"**{ui['missing_ratio']}:** {issues['missing_ratio']:.2%}")
        st.write(f"**{ui['duplicate_ratio']}:** {issues['duplicate_ratio']:.2%}")
        st.write(f"**{ui['outlier_ratio']}:** {issues['outlier_ratio']:.2%}")

    if st.button(ui["analyze_button"], use_container_width=True, key="analyze_button"):
        if not question.strip():
            st.warning(ui["no_question_warning"])
        else:
            language = detect_language(question)
            st.session_state["last_language"] = language

            context = summarize_context(df, issues, outliers)
            result = ask_gpt(question, context, analysis_type)
            result["_language"] = language

            st.session_state["history"].append((question, result))
            st.session_state["history"] = st.session_state["history"][-5:]

            st.session_state["latest_result"] = result
            st.session_state["latest_outliers"] = outliers
            st.session_state["latest_df"] = df
            st.session_state["latest_issues"] = issues

if st.session_state.get("latest_result") is not None:
    result = st.session_state["latest_result"]
    language = result.get("_language", st.session_state["last_language"])
    ui = get_ui_labels(language)

    outliers = st.session_state["latest_outliers"]
    df = st.session_state["latest_df"]
    issues = st.session_state["latest_issues"]

    st.subheader(ui["executive_summary"])
    st.write(result.get("executive_summary", ""))

    st.subheader(ui["direct_answer"])
    st.write(result.get("direct_answer", ""))

    tab1, tab2, tab3 = st.tabs([ui["issues_tab"], ui["charts_tab"], ui["data_tab"]])

    with tab1:
        st.subheader(ui["findings"])
        findings = result.get("findings", [])
        if findings:
            for item in findings:
                st.write(f"- {item}")

        st.subheader(ui["recommendations"])
        recommendations = result.get("recommendations", [])
        if recommendations:
            for item in recommendations:
                st.write(f"- {item}")

        next_steps = result.get("next_steps", [])
        if next_steps:
            st.subheader(ui["next_steps"])
            for item in next_steps:
                st.write(f"- {item}")

        st.write(f"**{ui['empty_columns']}:** {issues['empty_columns']}")
        st.write(f"**{ui['constant_columns']}:** {issues['constant_columns']}")

    with tab2:
        st.pyplot(missing_chart(df, language=language))
        st.pyplot(outlier_chart(outliers, language=language))

    with tab3:
        st.dataframe(df)

    pdf = generate_pdf(result)

    st.download_button(
        ui["download_pdf"],
        pdf,
        file_name="report.pdf",
        mime="application/pdf",
        key="download_pdf_button",
    )

with st.sidebar:
    st.subheader(ui["history_title"])
    for q, _ in st.session_state["history"][-5:]:
        st.write(f"- {q}")
