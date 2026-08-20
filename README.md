# 🤖 AI Data Analyst

An intelligent, interactive, and full-featured data analysis application built with Python and Streamlit for automated dataset analysis, data cleaning, advanced Plotly visualizations, sales forecasting, AI insights, executive PDF report generation, and natural language CSV query chat.

---

## 🚀 Features

1. **📂 1. Upload CSV & Excel**: Easily drag and drop CSV or XLSX files with auto-encoding detection and delimiter parsing.
2. **📊 2. Data Overview & Audit**: Dimensions, dataset taxonomy, missing value matrices, and automated Data Quality Health Scores (0-100%).
3. **🧹 3. Data Cleaning Studio**: Impute missing values (Mean/Median/Mode), remove duplicate rows, handle IQR outliers, and download sanitized datasets.
4. **📈 4. Advanced Visualization**: Plotly interactive line charts, bar charts, scatter plots, box plots, histograms, pie charts, and correlation heatmaps.
5. **📅 5. Sales Trend Analysis**: Extract timeline metrics and analyze temporal changes.
6. **🔮 6. Sales Forecasting**: Time-series predictive modeling (Exponential Smoothing / Holt's linear trend) with 95% confidence bands.
7. **🧠 7. AI Insights & KPIs**: Automated statistical pattern recognition, correlation analysis, anomaly detection, and executive scorecards via OpenAI, Gemini, or local offline engine.
8. **📄 8. Executive Reports**: One-click generation of ReportLab PDF reports, multi-tab Excel workbooks, and Markdown summaries.
9. **💬 9. Chat with Data**: Ask questions in natural language and receive formatted data answers.

---

## 📁 Project Structure

```
AI-Data-Analyst/
│
├── assets/
│   ├── manifest.json            # PWA manifest for iOS/Android home screen install
│   └── sw.js                    # PWA Service worker
│
├── data/
│   └── sales_data.csv           # Rich sample dataset
│
├── build_scripts/
│   ├── desktop_app.py           # Native pywebview window wrapper
│   ├── build_windows.bat        # Windows .exe compiler script
│   ├── build_mac.sh             # macOS .app bundle compiler script
│   └── Dockerfile               # Production Docker container
│
├── pages/
│   ├── 1_📊_Overview.py
│   ├── 2_🧹_Cleaning.py
│   ├── 3_📈_Visualization.py
│   ├── 4_🔮_Forecasting.py
│   ├── 5_🧠_Insights.py
│   ├── 6_📄_Reports.py
│   └── 7_💬_Chat.py
│
├── reports/
│   ├── pdf_report.py            # ReportLab PDF exporter
│   └── report_generator.py      # Excel & Markdown exporter
│
├── utils/
│   ├── components/
│   │   ├── header.py
│   │   └── sidebar.py
│   │
│   ├── ai_chat.py
│   ├── ai_insights.py
│   ├── chart_generator.py
│   ├── data_cleaner.py
│   ├── data_loader.py
│   ├── data_summary.py
│   ├── health_score.py
│   └── statistics.py
│
├── app.py                       # Main Streamlit application entrypoint
├── requirements.txt             # Dependencies
├── .env.example                 # Environment keys template
└── README.md
```

---

## ⚡ Quick Start (Local Run)

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch Streamlit App**:
   ```bash
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your browser.

---

## 📱 & 💻 Build & Installation Guide for All Platforms

### 🪟 1. Windows Installation (.exe Desktop App)
To install as a native Windows desktop app:
1. Open terminal inside `AI-Data-Analyst/build_scripts/`.
2. Run `build_windows.bat`.
3. Locate your compiled app under `dist/AI-Data-Analyst/AI-Data-Analyst.exe`.
4. Double-click to run directly as a standalone Windows app!

### 🍏 2. macOS Installation (.app Bundle)
To install on macOS (Intel or Apple Silicon):
1. Open terminal in `AI-Data-Analyst/build_scripts/`.
2. Run:
   ```bash
   chmod +x build_mac.sh
   ./build_mac.sh
   ```
3. Move `dist/AI-Data-Analyst.app` to your `/Applications` folder.

### 📱 3. Mobile Installation (iOS & Android)
The application includes a Progressive Web App (PWA) configuration with `manifest.json` and service worker `sw.js`.

#### **For iOS (iPhone / iPad)**:
1. Deploy the app to Streamlit Cloud, Railway, Render, or run using Docker (`docker build -t ai-analyst build_scripts/`).
2. Open the URL in **Safari** on your iOS device.
3. Tap the **Share** icon (bottom bar).
4. Select **"Add to Home Screen"**.
5. The **AI Data Analyst** icon will now appear on your iPhone/iPad home screen like a native mobile app!

#### **For Android**:
1. Open the hosted URL in **Google Chrome** on Android.
2. Tap the **three dots menu** (top right).
3. Select **"Install App"** or **"Add to Home Screen"**.
4. Launch directly from your Android app drawer.

---

## 🛠️ Technology Stack
- **Python 3.9+**
- **Streamlit** (UI Framework)
- **Pandas & NumPy** (Data Processing)
- **Plotly** (Interactive Graphics)
- **Statsmodels & Scikit-learn** (Forecasting & Statistics)
- **ReportLab & OpenPyXL** (PDF & Excel Exporters)
- **PyWebView** (Native Desktop Wrapper)
