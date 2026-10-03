import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    load_data,
    sidebar_filters,
    calculate_kpis,
    currency,
    number,
    business_insights
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Home Dashboard",
    page_icon="🏠",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

div[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    padding:18px;
    border-left:6px solid #2563eb;
    box-shadow:0px 3px 12px rgba(0,0,0,.08);
}

h1,h2,h3{
    color:#1f2937;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = load_data()

df = sidebar_filters(df)

kpi = calculate_kpis(df)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📊 Customer Retention & Sales Analytics Dashboard")

st.caption(
    "Interactive dashboard for customer behaviour, sales trends and business insights."
)

st.divider()

# --------------------------------------------------
# KPI ROW 1
# --------------------------------------------------

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "💰 Revenue",
        currency(kpi["Revenue"])
    )

with c2:
    st.metric(
        "👥 Customers",
        number(kpi["Customers"])
    )

with c3:
    st.metric(
        "🧾 Orders",
        number(kpi["Orders"])
    )

with c4:
    st.metric(
        "📦 Products",
        number(kpi["Products"])
    )

# --------------------------------------------------
# KPI ROW 2
# --------------------------------------------------

c5,c6,c7,c8 = st.columns(4)

with c5:
    st.metric(
        "🛒 Quantity",
        number(kpi["Quantity"])
    )

with c6:
    st.metric(
        "💳 Avg Order",
        currency(kpi["AverageOrder"])
    )

with c7:
    st.metric(
        "🌍 Countries",
        number(kpi["Countries"])
    )

with c8:
    st.metric(
        "🔁 Repeat Rate",
        f"{kpi['RepeatRate']:.2f}%"
    )

st.divider()

# --------------------------------------------------
# MONTHLY REVENUE
# --------------------------------------------------

monthly = (
    df.groupby(["Year", "Month_Num"])["total_price"]
      .sum()
      .reset_index()
)

month_order = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

monthly["Month"] = pd.to_datetime(
    monthly["Month_Num"],
    format="%m"
).dt.strftime("%b")

fig_month = px.line(
    monthly,
    x="Month",
    y="total_price",
    color=monthly["Year"].astype(str),   # Separate line for each year
    markers=True,
    category_orders={"Month": month_order},
    title="Monthly Revenue Trend"
)

fig_month.update_layout(
    template="plotly_white",
    height=450,
    title_x=0.02,
    xaxis_title="Month",
    yaxis_title="Revenue",
    legend_title="Year"
)

st.plotly_chart(fig_month, use_container_width=True)

# --------------------------------------------------
# REVENUE BY COUNTRY & TOP CUSTOMERS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    country_sales = (
        df.groupby("country")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_country = px.bar(
        country_sales,
        x="total_price",
        y="country",
        orientation="h",
        color="total_price",
        color_continuous_scale="Blues",
        title="🌍 Top 10 Countries by Revenue"
    )

    fig_country.update_layout(
        template="plotly_white",
        height=450,
        yaxis_title="",
        xaxis_title="Revenue",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_country, use_container_width=True)

with col2:

    top_customers = (
        df.groupby("customer_id")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    top_customers["customer_id"] = top_customers["customer_id"].astype(str)

    fig_customer = px.bar(
        top_customers,
        x="total_price",
        y="customer_id",
        orientation="h",
        color="total_price",
        color_continuous_scale="Greens",
        title="👥 Top 10 Customers"
    )

    fig_customer.update_layout(
        template="plotly_white",
        height=450,
        yaxis_title="Customer ID",
        xaxis_title="Revenue",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_customer, use_container_width=True)

st.divider()

# --------------------------------------------------
# TOP PRODUCTS & MONTHLY ORDERS
# --------------------------------------------------

col3, col4 = st.columns(2)

with col3:

    top_products = (
        df.groupby("description")["quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_products = px.bar(
        top_products,
        x="quantity",
        y="description",
        orientation="h",
        color="quantity",
        color_continuous_scale="Oranges",
        title="📦 Top 10 Best Selling Products"
    )

    fig_products.update_layout(
        template="plotly_white",
        height=450,
        yaxis_title="",
        xaxis_title="Quantity Sold",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_products, use_container_width=True)

with col4:

    monthly_orders = (
        df.groupby(["Year", "Month_Num"])["invoice"]
        .nunique()
        .reset_index(name="Orders")
    )

    monthly_orders["Month"] = pd.to_datetime(
        monthly_orders["Month_Num"],
        format="%m"
    ).dt.strftime("%b")

    monthly_orders = monthly_orders.sort_values(
        ["Year", "Month_Num"]
    )

    fig_orders = px.bar(
        monthly_orders,
        x="Month",
        y="Orders",
        color="Year",
        barmode="group",
        title="🧾 Monthly Orders"
    )

    fig_orders.update_layout(
        template="plotly_white",
        height=450,
        xaxis_title="Month",
        yaxis_title="Orders"
    )

    st.plotly_chart(fig_orders, use_container_width=True)

st.divider()

# --------------------------------------------------
# WEEKDAY SALES & HOURLY SALES
# --------------------------------------------------

col5, col6 = st.columns(2)

with col5:

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    weekday_sales = (
        df.groupby("Weekday")["total_price"]
        .sum()
        .reindex(weekday_order)
        .reset_index()
    )

    fig_weekday = px.bar(
        weekday_sales,
        x="Weekday",
        y="total_price",
        color="total_price",
        color_continuous_scale="Teal",
        title="📅 Revenue by Weekday"
    )

    fig_weekday.update_layout(
        template="plotly_white",
        height=420,
        coloraxis_showscale=False,
        xaxis_title="",
        yaxis_title="Revenue"
    )

    st.plotly_chart(fig_weekday, use_container_width=True)


with col6:

    hourly_sales = (
        df.groupby("Hour")["total_price"]
        .sum()
        .reset_index()
    )

    fig_hour = px.line(
        hourly_sales,
        x="Hour",
        y="total_price",
        markers=True,
        title="🕒 Revenue by Hour"
    )

    fig_hour.update_layout(
        template="plotly_white",
        height=420,
        xaxis_title="Hour",
        yaxis_title="Revenue"
    )

    st.plotly_chart(fig_hour, use_container_width=True)

st.divider()

# # --------------------------------------------------
# # REVENUE DISTRIBUTION
# # --------------------------------------------------

# fig_hist = px.histogram(
#     df,
#     x="total_price",
#     nbins=50,
#     title="📊 Revenue Distribution",
#     color_discrete_sequence=["#2563eb"]
# )

# fig_hist.update_layout(
#     template="plotly_white",
#     height=420,
#     xaxis_title="Revenue",
#     yaxis_title="Frequency"
# )

# st.plotly_chart(fig_hist, use_container_width=True)

# st.divider()

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.subheader("💡 Business Insights")

insights = business_insights(df)

for insight in insights:
    st.success(insight)

# --------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------

st.subheader("📌 Executive Summary")

left, right = st.columns(2)

with left:

    st.info(
        f"""
**Revenue:** {currency(kpi['Revenue'])}

**Customers:** {number(kpi['Customers'])}

**Orders:** {number(kpi['Orders'])}

**Average Order Value:** {currency(kpi['AverageOrder'])}
"""
    )

with right:

    st.info(
        f"""
**Products Sold:** {number(kpi['Quantity'])}

**Countries:** {number(kpi['Countries'])}

**Repeat Purchase Rate:** {kpi['RepeatRate']:.2f}%

Dashboard updated successfully.
"""
    )

st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
---
<div style='text-align:center;color:gray;'>

Customer Retention & Sales Analytics Dashboard

Built with ❤️ using Streamlit, Plotly, Pandas and Scikit-Learn

</div>
""",
    unsafe_allow_html=True
)