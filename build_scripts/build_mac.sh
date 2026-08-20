#!/bin/bash
echo "========================================================"
echo "Building AI Data Analyst App Bundle for macOS"
echo "========================================================"

pip install pyinstaller streamlit pywebview pandas plotly scikit-learn statsmodels reportlab openpyxl python-dotenv

pyinstaller --noconfirm --windowed \
    --name "AI-Data-Analyst" \
    --add-data "../pages:pages" \
    --add-data "../utils:utils" \
    --add-data "../reports:reports" \
    --add-data "../data:data" \
    --add-data "../assets:assets" \
    desktop_app.py

echo "Build complete! Check dist/AI-Data-Analyst.app"
