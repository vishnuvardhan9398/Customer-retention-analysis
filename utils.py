import pandas as pd
import streamlit as st

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/clean_data.csv")

    # Convert invoice date
    df["invoicedate"] = pd.to_datetime(df["invoicedate"])

    # Extra Date Columns
    df["Year"] = df["invoicedate"].dt.year
    df["Month"] = df["invoicedate"].dt.month_name()
    df["Month_Num"] = df["invoicedate"].dt.month
    df["Weekday"] = df["invoicedate"].dt.day_name()
    df["Hour"] = df["invoicedate"].dt.hour

    return df


# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
def sidebar_filters(df):
    st.sidebar.header("🔎 Filters")

    years = ["All"] + sorted(df["Year"].unique().tolist())
    selected_year = st.sidebar.selectbox(
        "Select Year",
        years
    )

    countries = ["All"] + sorted(df["country"].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox(
        "Select Country",
        countries
    )

    customers = ["All"] + sorted(df["customer_id"].dropna().astype(str).unique().tolist())
    selected_customer = st.sidebar.selectbox(
        "Select Customer",
        customers
    )

    filtered_df = df.copy()

    if selected_year != "All":
        filtered_df = filtered_df[
            filtered_df["Year"] == selected_year
        ]

    if selected_country != "All":
        filtered_df = filtered_df[
            filtered_df["country"] == selected_country
        ]

    if selected_customer != "All":
        filtered_df = filtered_df[
            filtered_df["customer_id"].astype(str) == selected_customer
        ]

    return filtered_df


# -------------------------------------------------
# KPI Calculations
# -------------------------------------------------
def calculate_kpis(df):

    total_revenue = df["total_price"].sum()

    total_customers = df["customer_id"].nunique()

    total_orders = df["invoice"].nunique()

    total_products = df["stockcode"].nunique()

    total_quantity = df["quantity"].sum()

    avg_order_value = (
        total_revenue / total_orders
        if total_orders > 0 else 0
    )

    repeat_customers = (
        df.groupby("customer_id")["invoice"]
        .nunique()
        .gt(1)
        .sum()
    )

    repeat_rate = (
        repeat_customers / total_customers * 100
        if total_customers > 0 else 0
    )

    countries = df["country"].nunique()

    return {
        "Revenue": total_revenue,
        "Customers": total_customers,
        "Orders": total_orders,
        "Products": total_products,
        "Quantity": total_quantity,
        "AverageOrder": avg_order_value,
        "RepeatRate": repeat_rate,
        "Countries": countries
    }


# -------------------------------------------------
# Currency Format
# -------------------------------------------------
def currency(value):
    return f"£{value:,.2f}"


# -------------------------------------------------
# Number Format
# -------------------------------------------------
def number(value):
    return f"{value:,.0f}"


# -------------------------------------------------
# Business Insights
# -------------------------------------------------
def business_insights(df):

    top_country = (
        df.groupby("country")["total_price"]
        .sum()
        .idxmax()
    )

    top_product = (
        df.groupby("description")["quantity"]
        .sum()
        .idxmax()
    )

    top_customer = (
        df.groupby("customer_id")["total_price"]
        .sum()
        .idxmax()
    )

    best_month = (
        df.groupby("Month")["total_price"]
        .sum()
        .idxmax()
    )

    insights = [
        f"🌍 Highest revenue country: **{top_country}**",
        f"📦 Best-selling product: **{top_product}**",
        f"👑 Highest spending customer: **{top_customer}**",
        f"📈 Highest revenue month: **{best_month}**"
    ]

    return insights