import os
import pandas as pd
import numpy as np
import requests
import json

def generate_ai_insights(df, provider="local", api_key=None):
    """
    Generates automated executive insights using OpenAI, Gemini API, or local rule-engine fallback.
    """
    if df is None or df.empty:
        return {"summary": "No data available.", "key_metrics": [], "insights": [], "recommendations": []}

    # 1. First build statistical summary
    stats_data = extract_statistical_facts(df)
    
    # 2. Try Provider-specific AI if API key is supplied
    if provider == "openai" and (api_key or os.getenv("OPENAI_API_KEY")):
        try:
            return call_openai_insights(stats_data, api_key or os.getenv("OPENAI_API_KEY"))
        except Exception as e:
            pass # Fallback to local
            
    elif provider == "gemini" and (api_key or os.getenv("GEMINI_API_KEY")):
        try:
            return call_gemini_insights(stats_data, api_key or os.getenv("GEMINI_API_KEY"))
        except Exception as e:
            pass # Fallback to local

    # 3. Local Rule Engine (Always Works Offline!)
    return generate_local_insights(df, stats_data)

def extract_statistical_facts(df):
    """Extracts factual data metrics for prompt feeding or local engine."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    date_cols = df.select_dtypes(include=['datetime64', 'datetime']).columns

    facts = {
        "num_rows": len(df),
        "num_cols": len(df.columns),
        "columns": list(df.columns),
        "total_nulls": int(df.isnull().sum().sum()),
        "numeric_summaries": {},
        "top_categories": {}
    }

    for col in numeric_cols:
        facts["numeric_summaries"][col] = {
            "mean": round(df[col].mean(), 2),
            "total": round(df[col].sum(), 2),
            "max": round(df[col].max(), 2),
            "min": round(df[col].min(), 2),
            "median": round(df[col].median(), 2)
        }

    for col in categorical_cols:
        mode_val = df[col].mode()
        facts["top_categories"][col] = {
            "top_item": str(mode_val[0]) if not mode_val.empty else "N/A",
            "unique_count": int(df[col].nunique())
        }

    return facts

def generate_local_insights(df, facts):
    """Intelligent offline rule-engine insights generator."""
    insights = []
    recommendations = []
    key_metrics = []

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    date_cols = df.select_dtypes(include=['datetime64', 'datetime']).columns

    # Dynamic Key Metrics
    for col in numeric_cols:
        if any(term in col.lower() for term in ['sales', 'revenue', 'profit', 'total', 'amount']):
            key_metrics.append({
                "label": f"Total {col}",
                "value": f"${facts['numeric_summaries'][col]['total']:,.2f}",
                "sub": f"Avg: ${facts['numeric_summaries'][col]['mean']:,.2f}"
            })
    
    if not key_metrics and len(numeric_cols) > 0:
        col = numeric_cols[0]
        key_metrics.append({
            "label": f"Total {col}",
            "value": f"{facts['numeric_summaries'][col]['total']:,.2f}",
            "sub": f"Average: {facts['numeric_summaries'][col]['mean']:,.2f}"
        })

    key_metrics.append({
        "label": "Total Records",
        "value": f"{facts['num_rows']:,}",
        "sub": f"{facts['num_cols']} attributes"
    })

    # Insights Rules
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr().abs()
        corr_values = corr_matrix.to_numpy(copy=True)
        np.fill_diagonal(corr_values, 0)
        corr_matrix_copy = pd.DataFrame(corr_values, index=corr_matrix.index, columns=corr_matrix.columns)
        max_corr_idx = corr_matrix_copy.stack().idxmax()
        val = corr_matrix_copy.loc[max_corr_idx]
        if val > 0.5:
            insights.append(f"Strong statistical correlation ({val:.2f}) found between '{max_corr_idx[0]}' and '{max_corr_idx[1]}'.")

    for col in cat_cols:
        top_info = facts['top_categories'][col]
        insights.append(f"Primary category in '{col}' is '{top_info['top_item']}' out of {top_info['unique_count']} unique values.")
        break

    for col in numeric_cols:
        skew = df[col].skew()
        if abs(skew) > 1.0:
            insights.append(f"Field '{col}' exhibits high distribution skewness ({skew:.2f}), suggesting high-value outliers or concentrated segments.")
            recommendations.append(f"Apply segment filtering or log-scaling when analyzing high-skew column '{col}'.")
            break

    if date_cols.any() and len(numeric_cols) > 0:
        date_col = date_cols[0]
        num_col = numeric_cols[0]
        df_sorted = df.sort_values(by=date_col)
        first_val = df_sorted[num_col].iloc[0]
        last_val = df_sorted[num_col].iloc[-1]
        pct_change = ((last_val - first_val) / first_val * 100) if first_val != 0 else 0
        direction = "upward" if pct_change >= 0 else "downward"
        insights.append(f"Overall timeline shows an {direction} movement of {abs(pct_change):.1f}% in '{num_col}' across the dataset timeframe.")

    if not recommendations:
        recommendations.append("Regularly clean missing values and remove duplicate entries before automated model training.")
        recommendations.append("Focus marketing or budget allocation on high-performing category segments identified in the visualization tab.")

    summary = f"Analysis completed across {facts['num_rows']} rows and {facts['num_cols']} columns. Data quality is good with {facts['total_nulls']} null values."

    return {
        "summary": summary,
        "key_metrics": key_metrics[:4],
        "insights": insights,
        "recommendations": recommendations
    }

def call_openai_insights(facts, api_key):
    """Calls OpenAI API for insights generation."""
    prompt = f"Analyze these statistical dataset facts and provide a structured JSON response with keys 'summary', 'insights' (list of strings), and 'recommendations' (list of strings):\n{json.dumps(facts)}"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=15)
    res_json = response.json()
    content = json.loads(res_json["choices"][0]["message"]["content"])
    content["key_metrics"] = generate_local_insights(None, facts)["key_metrics"]
    return content

def call_gemini_insights(facts, api_key):
    """Calls Google Gemini API for insights generation."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    prompt = f"Analyze these statistical dataset facts and return JSON with 'summary', 'insights' (list), and 'recommendations' (list):\n{json.dumps(facts)}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=payload, timeout=15)
    res_json = response.json()
    text = res_json["candidates"][0]["content"]["parts"][0]["text"]
    # Clean potential markdown formatting
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    content = json.loads(text.strip())
    content["key_metrics"] = generate_local_insights(None, facts)["key_metrics"]
    return content
