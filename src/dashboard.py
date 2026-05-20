# ============================================
# Project: Revenue Leakage + Margin Analysis
# Script: dashboard.py
# Purpose: Interactive Streamlit Dashboard
# ============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Revenue Leakage + Margin Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
    <style>
    .main {background-color: #0E1117;}
    .metric-card {
        background-color: #1E2530;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border: 1px solid #2E3A4A;
    }
    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: #00D4FF;
    }
    .metric-label {
        font-size: 14px;
        color: #ABB2B9;
        margin-top: 5px;
    }
    .metric-delta {
        font-size: 12px;
        color: #E74C3C;
        margin-top: 3px;
    }
    .section-header {
        font-size: 20px;
        font-weight: bold;
        color: #FFFFFF;
        margin-top: 30px;
        margin-bottom: 10px;
        padding-bottom: 5px;
        border-bottom: 2px solid #00D4FF;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================

@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/superstore_clean.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

# ============================================
# SIDEBAR FILTERS
# ============================================

st.sidebar.image(
    "https://img.icons8.com/color/96/000000/combo-chart--v1.png",
    width=60
)
st.sidebar.title("Dashboard Filters")
st.sidebar.markdown("Use filters to explore the data")

selected_year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df['Order Year'].unique()),
    default=sorted(df['Order Year'].unique())
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

selected_segment = st.sidebar.multiselect(
    "Select Segment",
    options=df['Segment'].unique(),
    default=df['Segment'].unique()
)

# Apply filters
filtered_df = df[
    (df['Order Year'].isin(selected_year)) &
    (df['Category'].isin(selected_category)) &
    (df['Region'].isin(selected_region)) &
    (df['Segment'].isin(selected_segment))
]

# ============================================
# HEADER
# ============================================

st.markdown("""
    <h1 style='text-align: center; color: #00D4FF; 
    font-size: 36px; padding: 20px 0px;'>
    📊 Revenue Leakage + Margin Analysis
    </h1>
    <p style='text-align: center; color: #ABB2B9; font-size: 16px;'>
    Identifying where profit is leaking across products, 
    categories, and customer segments
    </p>
    <hr style='border: 1px solid #2E3A4A;'>
""", unsafe_allow_html=True)

# ============================================
# KPI TILES
# ============================================

st.markdown(
    "<div class='section-header'>Key Performance Indicators</div>",
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)

total_revenue = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
avg_margin = filtered_df['Profit'].sum() / filtered_df['Sales'].sum() * 100
total_discount = filtered_df['Discount Amount'].sum()
loss_transactions = filtered_df['Is Loss'].sum()

with col1:
    st.metric(
        label="Total Revenue",
        value=f"${total_revenue:,.0f}"
    )

with col2:
    st.metric(
        label="Total Profit",
        value=f"${total_profit:,.0f}"
    )

with col3:
    st.metric(
        label="Avg Margin %",
        value=f"{avg_margin:.2f}%"
    )

with col4:
    st.metric(
        label="Discounts Given",
        value=f"${total_discount:,.0f}",
        delta=f"-${total_discount:,.0f} from revenue",
        delta_color="inverse"
    )

with col5:
    st.metric(
        label="Loss Transactions",
        value=f"{int(loss_transactions):,}",
        delta=f"{loss_transactions/len(filtered_df)*100:.1f}% of orders",
        delta_color="inverse"
    )

st.markdown("<hr style='border: 1px solid #2E3A4A;'>", unsafe_allow_html=True)

# ============================================
# ROW 1 — CATEGORY AND DISCOUNT CHARTS
# ============================================

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        "<div class='section-header'>Gross Margin % by Category</div>",
        unsafe_allow_html=True
    )
    cat_df = filtered_df.groupby('Category').agg(
        Revenue=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()
    cat_df['Margin %'] = (cat_df['Profit'] / cat_df['Revenue'] * 100).round(2)
    cat_df = cat_df.sort_values('Margin %')

    fig1 = px.bar(
        cat_df,
        x='Margin %',
        y='Category',
        orientation='h',
        color='Margin %',
        color_continuous_scale='RdYlGn',
        text='Margin %',
        template='plotly_dark'
    )
    fig1.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig1.update_layout(
        plot_bgcolor='#1E2530',
        paper_bgcolor='#1E2530',
        font_color='white',
        showlegend=False,
        height=300,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown(
        "<div class='section-header'>Profit by Discount Level</div>",
        unsafe_allow_html=True
    )

    def discount_bucket(d):
        if d == 0:
            return "0% No Discount"
        elif d <= 0.10:
            return "1 to 10%"
        elif d <= 0.20:
            return "11 to 20%"
        elif d <= 0.30:
            return "21 to 30%"
        elif d <= 0.50:
            return "31 to 50%"
        else:
            return "Over 50%"

    filtered_df = filtered_df.copy()
    filtered_df['Discount Bucket'] = filtered_df['Discount'].apply(discount_bucket)

    bucket_order = [
        "0% No Discount", "1 to 10%", "11 to 20%",
        "21 to 30%", "31 to 50%", "Over 50%"
    ]

    disc_df = filtered_df.groupby('Discount Bucket').agg(
        Profit=('Profit', 'sum')
    ).reset_index()
    disc_df['Color'] = disc_df['Profit'].apply(
        lambda x: '#2ECC71' if x > 0 else '#E74C3C'
    )
    disc_df['Discount Bucket'] = pd.Categorical(
        disc_df['Discount Bucket'],
        categories=bucket_order,
        ordered=True
    )
    disc_df = disc_df.sort_values('Discount Bucket')

    fig2 = go.Figure(go.Bar(
        x=disc_df['Profit'],
        y=disc_df['Discount Bucket'],
        orientation='h',
        marker_color=disc_df['Color'],
        text=disc_df['Profit'].apply(lambda x: f"${x:,.0f}"),
        textposition='outside'
    ))
    fig2.update_layout(
        plot_bgcolor='#1E2530',
        paper_bgcolor='#1E2530',
        font_color='white',
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(zeroline=True, zerolinecolor='white', zerolinewidth=2)
    )
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# ROW 2 — REGIONAL AND LEAKAGE CHARTS
# ============================================

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        "<div class='section-header'>Margin and Revenue by Region</div>",
        unsafe_allow_html=True
    )
    region_df = filtered_df.groupby('Region').agg(
        Revenue=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()
    region_df['Margin %'] = (
        region_df['Profit'] / region_df['Revenue'] * 100
    ).round(2)
    region_df = region_df.sort_values('Margin %')

    fig3 = px.bar(
        region_df,
        x='Margin %',
        y='Region',
        orientation='h',
        color='Margin %',
        color_continuous_scale='RdYlGn',
        text='Margin %',
        template='plotly_dark'
    )
    fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig3.add_vline(
        x=0,
        line_dash='dash',
        line_color='white',
        line_width=2
    )
    fig3.update_layout(
        plot_bgcolor='#1E2530',
        paper_bgcolor='#1E2530',
        font_color='white',
        showlegend=False,
        height=300,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown(
        "<div class='section-header'>Revenue at Risk by Category and Segment</div>",
        unsafe_allow_html=True
    )
    loss_df = filtered_df[filtered_df['Is Loss'] == True].groupby(
        ['Category', 'Segment']
    ).agg(
        Revenue_at_Risk=('Sales', 'sum')
    ).reset_index()

    fig4 = px.bar(
        loss_df,
        x='Revenue_at_Risk',
        y='Category',
        color='Segment',
        orientation='h',
        barmode='stack',
        template='plotly_dark',
        text='Revenue_at_Risk',
        color_discrete_sequence=['#3498DB', '#E67E22', '#E74C3C']
    )
    fig4.update_traces(texttemplate='$%{text:,.0f}', textposition='inside')
    fig4.update_layout(
        plot_bgcolor='#1E2530',
        paper_bgcolor='#1E2530',
        font_color='white',
        height=300,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig4, use_container_width=True)

# ============================================
# ROW 3 — YEARLY TREND
# ============================================

st.markdown(
    "<div class='section-header'>Yearly Margin and Revenue Trend</div>",
    unsafe_allow_html=True
)

yearly_df = filtered_df.groupby('Order Year').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Discount=('Discount Amount', 'sum')
).reset_index()
yearly_df['Margin %'] = (
    yearly_df['Profit'] / yearly_df['Revenue'] * 100
).round(2)

fig5 = go.Figure()

fig5.add_trace(go.Bar(
    x=yearly_df['Order Year'],
    y=yearly_df['Revenue'],
    name='Revenue',
    marker_color='#3498DB',
    yaxis='y'
))

fig5.add_trace(go.Bar(
    x=yearly_df['Order Year'],
    y=yearly_df['Discount'],
    name='Discounts Given',
    marker_color='#E74C3C',
    yaxis='y'
))

fig5.add_trace(go.Scatter(
    x=yearly_df['Order Year'],
    y=yearly_df['Margin %'],
    name='Margin %',
    mode='lines+markers',
    marker=dict(size=10, color='#F1C40F'),
    line=dict(width=3, color='#F1C40F'),
    yaxis='y2'
))

fig5.update_layout(
    plot_bgcolor='#1E2530',
    paper_bgcolor='#1E2530',
    font_color='white',
    barmode='group',
    height=350,
      xaxis=dict(
        tickmode='array',
        tickvals=[2014, 2015, 2016, 2017],
        ticktext=['2014', '2015', '2016', '2017'],
        gridcolor='#2E3A4A'
    ),
    yaxis=dict(title='Amount ($)', gridcolor='#2E3A4A'),
    yaxis2=dict(
        title='Margin %',
        overlaying='y',
        side='right',
        gridcolor='#2E3A4A'
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig5, use_container_width=True)

# ============================================
# FOOTER
# ============================================

st.markdown("<hr style='border: 1px solid #2E3A4A;'>", unsafe_allow_html=True)
st.markdown("""
    <p style='text-align: center; color: #ABB2B9; font-size: 12px;'>
    Built by Tarun Kumar Bosupally | 
    Data: Sample Superstore (Kaggle) | 
    Tools: Python, DuckDB, SQL, Streamlit, Plotly
    </p>
""", unsafe_allow_html=True)