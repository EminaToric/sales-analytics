import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# --- Data Loading & Cleaning ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/EminaToric/sales-analytics/main/OnlineRetail.xlsx"
    df = pd.read_excel(url, engine='openpyxl')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df = df[df['Country'] == 'United Kingdom']
    df['Month'] = df['InvoiceDate'].dt.to_period('M')
    return df

df = load_data()

# --- Sidebar ---
st.sidebar.title("Sales Explorer")
st.sidebar.markdown(
    "Interactive dashboard exploring sales trends\n"
    "using a proxy dataset."
)

min_date = df['InvoiceDate'].min().date()
max_date = df['InvoiceDate'].max().date()
cutoff = st.sidebar.date_input(
    "Through date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

top_products = (
    df.groupby('Description')['Revenue']
      .sum()
      .nlargest(20)
      .index
      .tolist()
)
selected = st.sidebar.multiselect(
    "Products (top 20)", top_products, default=top_products[:5]
)

# --- Filtered Data ---
filtered = df[
    (df['InvoiceDate'].dt.date <= cutoff) &
    (df['Description'].isin(selected))
]

# --- Metrics ---
total_rev = filtered['Revenue'].sum()
avg_order = filtered.groupby('InvoiceNo')['Revenue'].sum().mean()

# --- Tabs Layout ---
tab1, tab2 = st.tabs(["Overview", "Data"])

with tab1:
    st.subheader("Key Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Total Revenue", f"£{total_rev:,.0f}")
    col2.metric("Avg Order Value", f"£{avg_order:,.2f}")

    # Monthly Revenue Trend
    st.subheader("Monthly Revenue Trend")
    monthly = (
        filtered
        .groupby(filtered['InvoiceDate'].dt.to_period('M'))['Revenue']
        .sum()
        .astype(float)
        .reset_index()
    )
    monthly['Month'] = monthly['InvoiceDate'].dt.to_timestamp()
    fig1 = px.line(
        monthly,
        x='Month',
        y='Revenue',
        title="Monthly Revenue Trend",
        labels={'Revenue': 'Revenue (£)'}
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Top 10 Products
    st.subheader("Top 10 Products by Revenue")
    top10 = (
        filtered
        .groupby('Description')['Revenue']
        .sum()
        .nlargest(10)
        .reset_index()
    )
    fig2 = px.bar(
        top10,
        x='Revenue',
        y='Description',
        orientation='h',
        title="Top 10 Products",
        labels={'Revenue': 'Revenue (£)', 'Description': ''}
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Sample of Cleaned Data")
    st.dataframe(
        filtered[['InvoiceDate','Description','Quantity','UnitPrice','Revenue']]
        .head(20),
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown("**Source:** UCI Online Retail dataset as proxy for sales.")
