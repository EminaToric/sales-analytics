import streamlit as st
import pandas as pd
import plotly.express as px

# --- Data Loading & Cleaning ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/EminaToric/sales-analytics/main/OnlineRetail.xlsx"
    df = pd.read_excel(url, engine='openpyxl')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]  # drop canceled orders
    df = df[df['Country'] == 'United Kingdom']  # filter to one country
    df['Month'] = df['InvoiceDate'].dt.to_period('M')
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    return df

df = load_data()

# --- Sidebar ---
st.sidebar.title("Sales Explorer")
min_date = df['InvoiceDate'].min().date()
max_date = df['InvoiceDate'].max().date()
date_cutoff = st.sidebar.slider('Through date', min_date, max_date, max_date)
filtered_df = df[df['InvoiceDate'].dt.date <= date_cutoff]

# --- Title ---
st.title("🛍️ UK Sales Analytics Dashboard")

# --- Revenue Over Time ---
monthly = filtered_df.resample('M', on='InvoiceDate')['Revenue'].sum()
fig_monthly = px.line(
    monthly,
    x=monthly.index,
    y=monthly.values,
    labels={'x': 'Month', 'y': 'Revenue'},
    title="Monthly Revenue Trend"
)
st.plotly_chart(fig_monthly, use_container_width=True)

# --- Top Products ---
top_products = (
    filtered_df.groupby('Description')['Revenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig_top = px.bar(
    top_products,
    x='Revenue',
    y='Description',
    orientation='h',
    title='Top 10 Products by Revenue'
)
st.plotly_chart(fig_top, use_container_width=True)

# --- Raw Data ---
with st.expander("See raw data"):
    st.dataframe(filtered_df)
