# AI Data Quality Analyst 📊

## 📌 Overview

Before building reports, performing analysis, or training machine learning models, one critical question must be answered: **Is this dataset actually ready for the task?**

Many datasets appear usable but contain hidden problems:
- Missing values that skew results
- Duplicate rows that bias analysis
- Inconsistent data types that break workflows
- Extreme outliers that distort predictions
- Poor column structure that complicates processing

**AI Data Quality Analyst** solves this by providing an intelligent, automated assessment of dataset readiness. It combines traditional data quality metrics with AI-powered analysis to give you a clear answer: "Is my data ready, and if not, what should I fix?"

## 🎯 The Problem It Solves

Data professionals waste countless hours cleaning datasets, often discovering issues midway through analysis. This tool eliminates guesswork by:

- **Quantifying quality** with a 0-100 readiness score
- **Contextual evaluation** based on your specific goal (reporting, analysis, or modeling)
- **Actionable recommendations** prioritized by impact
- **Visual insights** that highlight problems at a glance
- **Professional documentation** via PDF reports for stakeholders

## ✨ Core Features

### 1. Smart Data Upload
- Support for CSV and Excel formats
- Automatic encoding detection
- Real-time validation

### 2. Goal-Based Evaluation
Three distinct assessment modes:

| Goal | Focus | Requirements |
|------|-------|--------------|
| **Build Report** | Business intelligence, dashboards | Tolerates some issues, needs clean labels |
| **Data Analysis** | Statistical analysis, insights | Requires consistent types, reasonable completeness |
| **Build Model** | Machine learning, predictions | Strict quality, needs numeric features, no duplicates |

### 3. Comprehensive Quality Metrics
- **Structure Analysis**: Rows, columns, data types
- **Missing Values**: Count, percentage, per-column breakdown
- **Duplicate Detection**: Exact duplicates, near-duplicates
- **Outlier Identification**: IQR-based detection with visual indicators
- **Consistency Checks**: Data type uniformity, value distributions

### 4. AI-Powered Assessment
Integrated with OpenAI to provide:
- Executive summary of dataset quality
- Goal-specific suitability analysis
- Prioritized fix recommendations
- Risk assessment for your use case
- Answers to natural language questions

### 5. Interactive Dashboard
Real-time visualizations including:
- Missing values heatmap
- Data type distribution
- Outlier charts by column
- Quality score progress bar
- Key metrics at a glance

### 6. Professional PDF Reports
Generate comprehensive reports containing:
- Dataset metadata and overview
- Quality score and status
- AI assessment summary
- Recommended actions
- Quality visualizations
- Export-ready formatting

### 7. Multi-Language Support
- Full English interface
- Arabic text support (RTL, proper shaping)
- Ready for additional language integration

## 🏗 Architecture
├── 📱 Frontend (Streamlit)
│ ├── File upload interface
│ ├── Goal selection
│ ├── Interactive dashboard
│ └── Report download
│
├── 🧠 Core Engine
│ ├── Data quality analyzer
│ ├── Scoring algorithm
│ ├── Outlier detector
│ └── Metrics calculator
│
├── 🤖 AI Integration
│ ├── OpenAI client
│ ├── Context builder
│ └── Response parser
│
├── 📊 Visualization
│ ├── Chart generators
│ ├── Dashboard components
│ └── Interactive elements
│
└── 📄 Report Generator
├── PDF builder
├── Multi-language support
└── Chart embedding


## 🚀 Installation Guide

### Prerequisites
- **Python 3.10 or higher**
- **OpenAI API key** (for AI features)
- **Git** (optional, for cloning)

### Step 1: Get the Code

```bash
# Clone the repository
git clone https://github.com/dftalqhatany/AI-Data-Quality-Analystv2.git

# Navigate to project directory
cd AI-Data-Quality-Analystv2
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
pip install -r requirements.txt
# On Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-api-key-here"

# On Mac/Linux
export OPENAI_API_KEY="sk-your-api-key-here"
streamlit run app.py
AI-Data-Quality-Analystv2/
│
├── app.py                      # Main application entry point
│   ├── UI layout and routing
│   ├── Session state management
│   ├── File upload handling
│   └── Dashboard rendering
│
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
├── devcontainer.json           # GitHub Codespaces config
├── sample_data.csv             # Example dataset for testing
│
├── fonts/                       # Font files for PDF
│   └── Cairo-Regular.ttf       # Arabic font (auto-downloaded)
│
└── src/                         # Source code modules
    │
    ├── analyzer.py              # Core quality analysis
    │   ├── detect_outliers()    # IQR-based outlier detection
    │   ├── assess_readiness()   # Goal-based scoring
    │   └── goal_recommendations() # Actionable fixes
    │
    ├── agent.py                  # AI task focus
    │   ├── infer_task_focus()    # Detect user intent
    │   ├── build_analysis_context() # Prepare AI context
    │   └── generate_final_report() # Structure AI output
    │
    ├── ai_assistant.py           # OpenAI integration
    │   ├── ask_gpt()             # Query OpenAI
    │   └── build_prompt()        # Construct prompts
    │
    ├── io_utils.py               # File operations
    │   ├── load_dataframe()      # CSV/Excel loader
    │   └── dataframe_overview()  # Basic metrics
    │
    ├── charts.py                  # Visualization
    │   ├── build_missing_chart() # Missing values bar chart
    │   ├── build_dtype_chart()   # Data types distribution
    │   ├── build_outlier_chart() # Outlier counts
    │   └── fig_to_bytes()        # Convert to bytes for PDF
    │
    └── pdf_report.py              # PDF generation
        ├── build_pdf_report()    # Main report builder
        ├── register_arabic_font() # Font setup
        ├── contains_arabic()     # Language detection
        ├── prepare_arabic_text() # RTL text processing
        └── draw_* functions      # PDF layout helpers
