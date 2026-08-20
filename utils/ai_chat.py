import pandas as pd
import numpy as np
import os
import requests
import json
import re

def ask_data_chat(df, user_query, provider="local", api_key=None, chat_history=None):
    """
    Processes natural language queries against the dataframe and generates intelligent answers.
    """
    if df is None or df.empty:
        return "Please upload a valid dataset first before asking questions."

    query_clean = user_query.strip().lower()

    # 1. Check if LLM API can handle it
    if provider == "openai" and (api_key or os.getenv("OPENAI_API_KEY")):
        try:
            return query_llm_chat(df, user_query, provider="openai", api_key=api_key or os.getenv("OPENAI_API_KEY"))
        except Exception:
            pass
    elif provider == "gemini" and (api_key or os.getenv("GEMINI_API_KEY")):
        try:
            return query_llm_chat(df, user_query, provider="gemini", api_key=api_key or os.getenv("GEMINI_API_KEY"))
        except Exception:
            pass

    # 2. Local Pandas Smart Agent (Works 100% Offline)
    return query_local_smart_agent(df, user_query)

def query_local_smart_agent(df, query):
    """Offline natural language pandas question answering engine."""
    q = query.lower()
    numeric_cols = list(df.select_dtypes(include=[np.number]).columns)
    cat_cols = list(df.select_dtypes(include=['object', 'category']).columns)

    # Question 1: Total / Sum queries
    if any(word in q for word in ['total', 'sum', 'overall']) and numeric_cols:
        matched_col = next((c for c in numeric_cols if c.lower() in q), numeric_cols[0])
        total_val = df[matched_col].sum()
        return f"📊 The **total {matched_col}** across all {len(df):,} records is **${total_val:,.2f}** (or {total_val:,.2f} units)."

    # Question 2: Average / Mean queries
    if any(word in q for word in ['average', 'mean', 'avg']) and numeric_cols:
        matched_col = next((c for c in numeric_cols if c.lower() in q), numeric_cols[0])
        avg_val = df[matched_col].mean()
        return f"📈 The **average {matched_col}** per record is **${avg_val:,.2f}** (or {avg_val:,.2f} units)."

    # Question 3: Highest / Highest / Top category queries
    if any(word in q for word in ['highest', 'top', 'max', 'best']) and cat_cols and numeric_cols:
        target_cat = next((c for c in cat_cols if c.lower() in q), cat_cols[0])
        target_num = next((n for n in numeric_cols if n.lower() in q), numeric_cols[0])
        grouped = df.groupby(target_cat)[target_num].sum().sort_values(ascending=False)
        top_name = grouped.index[0]
        top_val = grouped.iloc[0]
        return f"🏆 The **top performing {target_cat}** by total {target_num} is **'{top_name}'** with **${top_val:,.2f}**."

    # Question 4: Lowest / Minimum queries
    if any(word in q for word in ['lowest', 'bottom', 'min', 'worst']) and cat_cols and numeric_cols:
        target_cat = next((c for c in cat_cols if c.lower() in q), cat_cols[0])
        target_num = next((n for n in numeric_cols if n.lower() in q), numeric_cols[0])
        grouped = df.groupby(target_cat)[target_num].sum().sort_values(ascending=True)
        bot_name = grouped.index[0]
        bot_val = grouped.iloc[0]
        return f"🔻 The **lowest performing {target_cat}** by total {target_num} is **'{bot_name}'** with **${bot_val:,.2f}**."

    # Question 5: Count / Rows queries
    if any(word in q for word in ['how many', 'count', 'rows', 'number of']):
        return f"🔢 The dataset contains **{len(df):,} total records** across **{len(df.columns)} columns**."

    # Question 6: Unique items queries
    if any(word in q for word in ['unique', 'categories', 'types', 'distinct']):
        if cat_cols:
            summary = [f"- **{c}**: {df[c].nunique()} unique items" for c in cat_cols[:5]]
            return "🏷️ **Unique items breakdown:**\n" + "\n".join(summary)

    # Fallback dataset context summary
    cols_str = ", ".join([f"`{c}`" for c in df.columns[:8]])
    return (
        f"I analyzed your dataset of **{len(df):,} rows**. Available columns include {cols_str}.\n\n"
        f"💡 **Try asking:**\n"
        f"- *What is the total sales?*\n"
        f"- *Which category has the highest profit?*\n"
        f"- *What is the average discount?*\n"
        f"- *How many unique records are there?*"
    )

def query_llm_chat(df, user_query, provider, api_key):
    """Executes prompt engineering with LLM API."""
    schema_info = {col: str(df[col].dtype) for col in df.columns}
    sample_data = df.head(3).to_dict(orient="records")
    
    prompt = (
        f"You are an expert AI Data Analyst. Answer the user question based on this dataframe context:\n"
        f"Columns & Types: {schema_info}\n"
        f"Sample Rows: {sample_data}\n"
        f"User Question: {user_query}\n"
        f"Provide a clear, formatted markdown response with numbers formatted cleanly."
    )

    if provider == "openai":
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]}
        res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=15)
        return res.json()["choices"][0]["message"]["content"]
    elif provider == "gemini":
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        res = requests.post(url, json=payload, timeout=15)
        return res.json()["candidates"][0]["content"]["parts"][0]["text"]

    return query_local_smart_agent(df, user_query)
