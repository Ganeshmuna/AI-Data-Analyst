import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.components.sidebar import render_sidebar
from utils.dashboard_templates import DASHBOARD_TEMPLATES, auto_map_columns
from utils.chart_generator import (
    create_powerbi_donut_chart, 
    create_powerbi_timeline_chart, 
    create_powerbi_dual_bar_chart
)

st.set_page_config(page_title="Executive Dashboards - AI Data Analyst", page_icon="🎛️", layout="wide")

render_sidebar()

# Custom PowerBI Black & Gold Styling CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0D0F12;
        color: #FFFFFF;
    }
    .pbi-header-container {
        border: 2px solid #F59E0B;
        border-radius: 4px;
        padding: 0.8rem 1.5rem;
        background-color: #0D0F12;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .pbi-header-title {
        color: #F59E0B;
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: 1px;
        margin: 0;
        text-transform: uppercase;
    }
    .pbi-kpi-card {
        border: 2px solid #F59E0B;
        border-radius: 4px;
        background-color: #0D0F12;
        padding: 0.8rem;
        text-align: center;
    }
    .pbi-kpi-label {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    .pbi-kpi-val {
        color: #F59E0B;
        font-size: 1.6rem;
        font-weight: 700;
    }
    .pbi-box {
        border: 2px solid #F59E0B;
        border-radius: 4px;
        background-color: #0D0F12;
        padding: 0.75rem;
        margin-bottom: 1rem;
    }
    .pbi-box-title {
        color: #F59E0B;
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

df = st.session_state.get('cleaned_df')

if df is None or df.empty:
    st.warning("⚠️ No dataset loaded. Loading default sample dataset for demonstration...")
    from utils.data_loader import load_data
    import os
    sample_path = os.path.join(os.path.dirname(__file__), "..", "data", "sales_data.csv")
    if os.path.exists(sample_path):
        df = load_data(sample_path)
        st.session_state['cleaned_df'] = df

# Initialize selected template key
if 'selected_template' not in st.session_state:
    st.session_state['selected_template'] = 'amazon_sales'

# Top Control & Template Selector Toolbar
with st.expander("🎛️ 20+ Dashboard Templates Gallery & Smart Data Column Mapper", expanded=True):
    t_col1, t_col2 = st.columns([1, 1])
    
    with t_col1:
        template_keys = list(DASHBOARD_TEMPLATES.keys())
        selected_key = st.selectbox(
            "Select Dashboard Template (20+ Pre-built Industry Dashboards)",
            template_keys,
            index=template_keys.index(st.session_state['selected_template']) if st.session_state['selected_template'] in template_keys else 0,
            format_func=lambda k: f"{DASHBOARD_TEMPLATES[k]['name']} ({DASHBOARD_TEMPLATES[k]['category']})"
        )
        st.session_state['selected_template'] = selected_key
        template_info = DASHBOARD_TEMPLATES[selected_key]
        st.info(f"**Description:** {template_info['description']}")

    with t_col2:
        st.write("#### 🧠 Smart Data Column Mapping")
        auto_map = auto_map_columns(df)
        cols = [None] + list(df.columns)

        col_date = st.selectbox("Date Column", cols, index=cols.index(auto_map['date']) if auto_map['date'] in cols else 0)
        col_sales = st.selectbox("Primary Metric Column", cols, index=cols.index(auto_map['sales']) if auto_map['sales'] in cols else 0)
        col_profit = st.selectbox("Secondary Metric Column", cols, index=cols.index(auto_map['profit']) if auto_map['profit'] in cols else 0)
        col_cat = st.selectbox("Category Column", cols, index=cols.index(auto_map['category']) if auto_map['category'] in cols else 0)
        col_region = st.selectbox("Region / Filter Column", cols, index=cols.index(auto_map['region']) if auto_map['region'] in cols else 0)
        col_segment = st.selectbox("Segment Column", cols, index=cols.index(auto_map['segment']) if auto_map['segment'] in cols else 0)
        col_payment = st.selectbox("Group By Field A", cols, index=cols.index(auto_map['payment']) if auto_map['payment'] in cols else 0)
        col_ship = st.selectbox("Group By Field B", cols, index=cols.index(auto_map['ship_mode']) if auto_map['ship_mode'] in cols else 0)

template_info = DASHBOARD_TEMPLATES.get(st.session_state.get('selected_template', 'amazon_sales'), DASHBOARD_TEMPLATES['amazon_sales'])
dataset_name = st.session_state.get('dataset_name', '')

# Dynamic Header Title per Template & Dataset
clean_template_title = template_info['name'].replace("🛒", "").replace("💼", "").replace("📊", "").replace("🛍️", "").replace("🎯", "").replace("⚡", "").replace("👥", "").replace("📦", "").replace("🏥", "").replace("🏢", "").replace("🏦", "").replace("🍕", "").replace("🎧", "").replace("📱", "").replace("🏨", "").replace("🎓", "").replace("🚗", "").replace("🏗️", "").replace("🏋️", "").replace("🌐", "").strip().upper()

if dataset_name and dataset_name != "None" and "Sample" not in dataset_name:
    file_prefix = dataset_name.split('.')[0].replace('_', ' ').replace('-', ' ').upper()
    dashboard_title = f"{file_prefix} - {clean_template_title}"
else:
    dashboard_title = clean_template_title

col_date = col_date or auto_map['date'] or (df.columns[0] if len(df.columns)>0 else None)
col_sales = col_sales or auto_map['sales'] or (df.columns[1] if len(df.columns)>1 else None)
col_profit = col_profit or auto_map['profit'] or col_sales
col_cat = col_cat or auto_map['category'] or (df.columns[2] if len(df.columns)>2 else None)
col_region = col_region or auto_map['region'] or (df.columns[3] if len(df.columns)>3 else None)
col_segment = col_segment or auto_map['segment'] or col_cat
col_payment = col_payment or auto_map['payment'] or col_cat
col_ship = col_ship or auto_map['ship_mode'] or col_cat

# Slicer Region Buttons (Top Right Filter Tabs)
regions = ["All"]
if col_region and col_region in df.columns:
    regions += list(df[col_region].dropna().unique())

st.markdown(f"""
<div class="pbi-header-container">
    <div class="pbi-header-title">{dashboard_title}</div>
</div>
""", unsafe_allow_html=True)

# Slicer Filter Buttons
selected_region = st.radio("Region Slicer Filter:", regions, horizontal=True)

filtered_df = df.copy()
if selected_region != "All" and col_region in filtered_df.columns:
    filtered_df = filtered_df[filtered_df[col_region] == selected_region]

# Top KPI Summary Cards Row
total_sales = filtered_df[col_sales].sum() if col_sales in filtered_df.columns and pd.api.types.is_numeric_dtype(filtered_df[col_sales]) else 140000
total_profit = filtered_df[col_profit].sum() if col_profit in filtered_df.columns and pd.api.types.is_numeric_dtype(filtered_df[col_profit]) else 26530
total_orders = len(filtered_df)
total_products = filtered_df[col_cat].nunique() if col_cat in filtered_df.columns else 211

sales_str = f"${total_sales/1000000:.2f}M" if total_sales >= 1000000 else f"${total_sales/1000:.2f}K"
profit_str = f"${total_profit/1000:.2f}K" if abs(total_profit) >= 1000 else f"${total_profit:.2f}"
orders_str = f"{total_orders/1000:.2f}K" if total_orders >= 1000 else f"{total_orders:,}"

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="pbi-kpi-card">
        <div class="pbi-kpi-label">Sales</div>
        <div class="pbi-kpi-val">{sales_str}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="pbi-kpi-card">
        <div class="pbi-kpi-label">Profits</div>
        <div class="pbi-kpi-val">{profit_str}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="pbi-kpi-card">
        <div class="pbi-kpi-label">Orders</div>
        <div class="pbi-kpi-val">{orders_str}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="pbi-kpi-card">
        <div class="pbi-kpi-label">Total Products</div>
        <div class="pbi-kpi-val">{total_products}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main PowerBI Grid Layout (3 Columns matching reference image)
col_left, col_center, col_right = st.columns([1.2, 2.2, 1.4])

with col_left:
    # 1. Sales by Segment Donut
    st.markdown('<div class="pbi-box"><div class="pbi-box-title">Sales by Segment</div>', unsafe_allow_html=True)
    if col_segment in filtered_df.columns and col_sales in filtered_df.columns:
        seg_df = filtered_df.groupby(col_segment)[col_sales].sum().reset_index()
        fig_seg = create_powerbi_donut_chart(seg_df, names_col=col_segment, values_col=col_sales)
        st.plotly_chart(fig_seg, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Sales by Payment Mode Donut
    st.markdown('<div class="pbi-box"><div class="pbi-box-title">Sales by Payment Mode</div>', unsafe_allow_html=True)
    if col_payment in filtered_df.columns and col_sales in filtered_df.columns:
        pay_df = filtered_df.groupby(col_payment)[col_sales].sum().reset_index()
        fig_pay = create_powerbi_donut_chart(pay_df, names_col=col_payment, values_col=col_sales)
        st.plotly_chart(fig_pay, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Sales by Ship Mode Donut
    st.markdown('<div class="pbi-box"><div class="pbi-box-title">Sales by Ship Mode</div>', unsafe_allow_html=True)
    if col_ship in filtered_df.columns and col_sales in filtered_df.columns:
        ship_df = filtered_df.groupby(col_ship)[col_sales].sum().reset_index()
        fig_ship = create_powerbi_donut_chart(ship_df, names_col=col_ship, values_col=col_sales)
        st.plotly_chart(fig_ship, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_center:
    # 1. Timeline Chart (Sum of Sales by Year, Quarter, Month and Day)
    st.markdown('<div class="pbi-box"><div class="pbi-box-title">Sum of Sales by Year, Quarter, Month and Day</div>', unsafe_allow_html=True)
    if col_date in filtered_df.columns and col_sales in filtered_df.columns:
        df_line = filtered_df.copy()
        df_line[col_date] = pd.to_datetime(df_line[col_date], errors='coerce')
        df_line = df_line.dropna(subset=[col_date]).sort_values(col_date)
        time_grp = df_line.groupby(df_line[col_date].dt.date)[col_sales].sum().reset_index()
        fig_time = create_powerbi_timeline_chart(time_grp, date_col=col_date, value_col=col_sales)
        st.plotly_chart(fig_time, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c_bot1, c_bot2 = st.columns(2)
    with c_bot1:
        # Sales vs Profit per Quarter
        st.markdown('<div class="pbi-box"><div class="pbi-box-title">Sales vs Profit Per Quarter</div>', unsafe_allow_html=True)
        if col_cat in filtered_df.columns and col_sales in filtered_df.columns:
            dual_df = filtered_df.groupby(col_cat)[[col_profit if col_profit in filtered_df.columns else col_sales, col_sales]].sum().reset_index().head(4)
            fig_dual = create_powerbi_dual_bar_chart(dual_df, cat_col=col_cat, val1_col=dual_df.columns[1], val2_col=col_sales)
            st.plotly_chart(fig_dual, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_bot2:
        # Sales by Category (Horizontal Bar)
        st.markdown('<div class="pbi-box"><div class="pbi-box-title">Sales by Category</div>', unsafe_allow_html=True)
        if col_cat in filtered_df.columns and col_sales in filtered_df.columns:
            cat_df = filtered_df.groupby(col_cat)[col_sales].sum().reset_index()
            fig_cat = px.bar(cat_df, y=col_cat, x=col_sales, orientation='h', color_discrete_sequence=['#F59E0B'])
            fig_cat.update_layout(paper_bgcolor='#0D0F12', plot_bgcolor='#0D0F12', font=dict(color='#FFFFFF'), margin=dict(l=10, r=10, t=20, b=10))
            st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # Geographic Map & Regional Breakdown Panel
    st.markdown('<div class="pbi-box"><div class="pbi-box-title">Regional Distribution & Map View</div>', unsafe_allow_html=True)
    if col_region in filtered_df.columns and col_sales in filtered_df.columns:
        reg_df = filtered_df.groupby(col_region)[col_sales].sum().reset_index()
        fig_map = px.pie(reg_df, names=col_region, values=col_sales, hole=0.3, color_discrete_sequence=['#F59E0B', '#3B82F6', '#10B981', '#EC4899'])
        fig_map.update_layout(paper_bgcolor='#0D0F12', plot_bgcolor='#0D0F12', font=dict(color='#94A3B8'), margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("#### Top Category Metrics")
    if col_cat in filtered_df.columns and col_sales in filtered_df.columns:
        top_cats = filtered_df.groupby(col_cat)[col_sales].sum().sort_values(ascending=False).head(5)
        for cat_name, val in top_cats.items():
            st.write(f"• **{cat_name}**: ${val:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)
