# AI Data Quality Analyst 📊

Intelligent data quality assessment tool that evaluates dataset readiness for different business goals using automated analysis and AI insights.

## ✨ Features
- **Upload CSV/Excel** files instantly
- **3 Goal Options**: Report, Analysis, or ML Model
- **Quality Score** (0-100) with detailed metrics  
- **AI-Powered Analysis** via OpenAI
- **Interactive Dashboard** with visualizations
- **PDF Report Generation**
- **Arabic/English Support**

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API key

### Installation
```bash
# Clone & enter
git clone https://github.com/dftalqhatany/AI-Data-Quality-Analystv2.git
cd AI-Data-Quality-Analystv2

# Setup virtual env
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install & run
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"  # Windows: $env:OPENAI_API_KEY="your-key"
streamlit run app.py
├── app.py                 # Main app
├── requirements.txt       # Dependencies
└── src/
    ├── analyzer.py       # Quality logic
    ├── agent.py          # AI focus detection
    ├── ai_assistant.py   # OpenAI integration
    ├── io_utils.py       # File handling
    ├── charts.py         # Visualizations
    └── pdf_report.py     # PDF builder
