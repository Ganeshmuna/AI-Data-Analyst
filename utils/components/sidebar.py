import streamlit as st
import os
from utils.data_loader import load_data

def render_sidebar():
    """Renders the sidebar navigation and configuration panel."""
    with st.sidebar:
        st.image("https://img.icons8.com/isometric/96/combo-chart.png", width=70)
        st.title("⚙️ Data Settings")
        
        st.markdown("---")
        st.subheader("📂 1. Dataset Selection")

        uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

        col1, col2 = st.columns(2)
        with col1:
            use_sample = st.button("📊 Load Sample Data", use_container_width=True)
        with col2:
            reset_data = st.button("🔄 Reset", use_container_width=True)

        if reset_data:
            st.session_state['df'] = None
            st.session_state['cleaned_df'] = None
            st.session_state['dataset_name'] = "None"
            st.rerun()

        if use_sample:
            sample_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sales_data.csv")
            if os.path.exists(sample_path):
                df = load_data(sample_path)
                st.session_state['df'] = df
                st.session_state['cleaned_df'] = df.copy()
                st.session_state['dataset_name'] = "sales_data.csv (Sample)"
                st.success("Loaded sample dataset!")
                st.rerun()

        if uploaded_file is not None:
            df = load_data(uploaded_file)
            if df is not None:
                st.session_state['df'] = df
                st.session_state['cleaned_df'] = df.copy()
                st.session_state['dataset_name'] = uploaded_file.name
                st.sidebar.success(f"Loaded {uploaded_file.name}!")

        st.markdown("---")
        st.subheader("🧠 2. AI Intelligence Engine")

        ai_provider = st.selectbox(
            "Select AI Engine",
            ["local", "openai", "gemini"],
            format_func=lambda x: {
                "local": "⚡ Local Offline Engine (Free)",
                "openai": "🤖 OpenAI (GPT-4o)",
                "gemini": "✨ Google Gemini (Flash)"
            }[x]
        )
        st.session_state['ai_provider'] = ai_provider

        api_key = ""
        if ai_provider != "local":
            api_key = st.text_input(f"{ai_provider.upper()} API Key", type="password", help="Entered key remains local in your session state.")
        st.session_state['api_key'] = api_key

        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.8rem; color: #94A3B8; text-align: center;">
            AI Data Analyst v1.0.0<br>
            Multi-Platform Ready App
        </div>
        """, unsafe_allow_html=True)
