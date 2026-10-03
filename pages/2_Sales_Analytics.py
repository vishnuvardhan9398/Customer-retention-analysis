import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    load_data,
    sidebar_filters,
    currency,
    number
)

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Sales Analytics",
    page_icon="📈",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

df = load_data()
df = sidebar_filters(df)

# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("📈 Sales Analytics Dashboard")

st.caption(
    "Analyze customer purchasing behaviour, products and country performance."
)

st.divider()

# -------------------------------------------------
# CUSTOMER METRICS
# -------------------------------------------------

customer_summary = (
    df.groupby("customer_id")
    .agg(
        Orders=("invoice", "nunique"),
        Revenue=("total_price", "sum"),
        Quantity=("quantity", "sum")
    )
    .reset_index()
)

customer_summary["Average Spend"] = (
    customer_summary["Revenue"] /
    customer_summary["Orders"]
)

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "👥 Customers",
        number(customer_summary.shape[0])
    )

with c2:
    st.metric(
        "💰 Avg Customer Spend",
        currency(customer_summary["Revenue"].mean())
    )

with c3:
    st.metric(
        "🧾 Avg Orders",
        round(customer_summary["Orders"].mean(), 2)
    )

with c4:
    st.metric(
        "🛒 Avg Quantity",
        round(customer_summary["Quantity"].mean(), 2)
    )

st.divider()

# -------------------------------------------------
# CUSTOMER SPENDING
# -------------------------------------------------

# -------------------------------------------------
# CUSTOMER SEGMENT
# -------------------------------------------------

customer_summary["Customer Segment"] = pd.cut(
    customer_summary["Revenue"],
    bins=[0, 500, 2000, float("inf")],
    labels=[
        "Small Customers",
        "Medium Customers",
        "Loyal Customers"
    ]
)

left, right = st.columns(2)

# =================================================
# TOP 10 SPENDING CUSTOMERS
# =================================================

with left:

    top_customer = (
        customer_summary
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_customer,
        x="Revenue",
        y=top_customer["customer_id"].astype(str),
        orientation="h",
        color="Revenue",
        color_continuous_scale="Blues",
        text="Revenue",
        title="🏆 Top 10 Spending Customers"
    )

    fig.update_traces(
        texttemplate="£%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_white",
        height=500,
        yaxis_title="Customer ID",
        xaxis_title="Revenue (£)",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =================================================
# CUSTOMER SEGMENT PIE CHART
# =================================================

with right:

    segment = (
        customer_summary
        .groupby("Customer Segment")
        .size()
        .reset_index(name="Customers")
    )

    fig = px.pie(
        segment,
        names="Customer Segment",
        values="Customers",
        hole=0.50,
        title="👥 Customer Segmentation"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>"
                      "Customers: %{value}<br>"
                      "Share: %{percent}<extra></extra>"
    )

    fig.update_layout(
        template="plotly_white",
        height=500,
        legend_title="Segments"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()
# -------------------------------------------------
# PRODUCT ANALYSIS
# -------------------------------------------------

st.subheader("📦 Product Analysis")

left, right = st.columns(2)

with left:

    product_sales = (
        df.groupby("description")
        .agg(
            Revenue=("total_price", "sum"),
            Quantity=("quantity", "sum")
        )
        .sort_values("Revenue", ascending=False)
        .head(15)
        .reset_index()
    )

    fig_product = px.bar(
        product_sales,
        x="Revenue",
        y="description",
        orientation="h",
        color="Revenue",
        color_continuous_scale="Viridis",
        title="Top 15 Products by Revenue"
    )

    fig_product.update_layout(
        template="plotly_white",
        height=500,
        yaxis_title="",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_product,
        use_container_width=True
    )

with right:

    fig_quantity = px.bar(
        product_sales,
        x="Quantity",
        y="description",
        orientation="h",
        color="Quantity",
        color_continuous_scale="Oranges",
        title="Top 15 Products by Quantity"
    )

    fig_quantity.update_layout(
        template="plotly_white",
        height=500,
        yaxis_title="",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_quantity,
        use_container_width=True
    )

st.divider()

# -------------------------------------------------
# COUNTRY ANALYSIS
# -------------------------------------------------

st.subheader("🌍 Country Analysis")

col1, col2 = st.columns(2)

country_summary = (
    df.groupby("country")
    .agg(
        Revenue=("total_price", "sum"),
        Customers=("customer_id", "nunique"),
        Orders=("invoice", "nunique")
    )
    .reset_index()
)

with col1:

    fig_country = px.treemap(
        country_summary,
        path=["country"],
        values="Revenue",
        color="Revenue",
        color_continuous_scale="Blues",
        title="Revenue Treemap"
    )

    fig_country.update_layout(
        height=550
    )

    st.plotly_chart(
        fig_country,
        use_container_width=True
    )

with col2:

    top10 = country_summary.sort_values(
        "Revenue",
        ascending=False
    ).head(10)

    fig_country_bar = px.bar(
        top10,
        x="country",
        y="Revenue",
        color="Revenue",
        color_continuous_scale="Greens",
        title="Top 10 Countries"
    )

    fig_country_bar.update_layout(
        template="plotly_white",
        height=550,
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_country_bar,
        use_container_width=True
    )

st.divider()

# -------------------------------------------------
# COUNTRY SHARE
# -------------------------------------------------

country_share = (
    country_summary
    .sort_values("Revenue", ascending=False)
    .head(8)
)

fig_pie = px.pie(
    country_share,
    names="country",
    values="Revenue",
    hole=0.45,
    title="Country Revenue Share"
)

fig_pie.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig_pie.update_layout(
    height=500
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)

st.divider()
import plotly.graph_objects as go

# -------------------------------------------------
# PARETO ANALYSIS
# -------------------------------------------------

st.subheader("📊 Pareto Analysis (80/20 Rule)")

pareto = (
    customer_summary
    .sort_values("Revenue", ascending=False)
    .reset_index(drop=True)
)

pareto["Cumulative Revenue"] = pareto["Revenue"].cumsum()
pareto["Cumulative %"] = (
    pareto["Cumulative Revenue"]
    / pareto["Revenue"].sum()
) * 100

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=pareto.index + 1,
        y=pareto["Revenue"],
        name="Revenue"
    )
)

fig.add_trace(
    go.Scatter(
        x=pareto.index + 1,
        y=pareto["Cumulative %"],
        yaxis="y2",
        mode="lines",
        name="Cumulative %",
        line=dict(width=3)
    )
)

fig.update_layout(
    template="plotly_white",
    height=500,
    xaxis_title="Customers",
    yaxis_title="Revenue",
    yaxis2=dict(
        overlaying="y",
        side="right",
        title="Cumulative %",
        range=[0,100]
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------
# REVENUE VS ORDERS
# -------------------------------------------------

# st.subheader("📈 Customer Revenue vs Orders")

# fig = px.scatter(
#     customer_summary,
#     x="Orders",
#     y="Revenue",
#     size="Quantity",
#     color="Average Spend",
#     hover_data=["customer_id"],
#     title="Customer Behaviour"
# )

# fig.update_layout(
#     template="plotly_white",
#     height=500
# )

# st.plotly_chart(
#     fig,
#     use_container_width=True
# )

# st.divider()

# # -------------------------------------------------
# # BOX PLOT
# # -------------------------------------------------

# left, right = st.columns(2)

# with left:

#     fig = px.box(
#         customer_summary,
#         y="Revenue",
#         title="Revenue Distribution"
#     )

#     fig.update_layout(
#         template="plotly_white",
#         height=420
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

# with right:

#     fig = px.box(
#         customer_summary,
#         y="Orders",
#         title="Orders Distribution"
#     )

#     fig.update_layout(
#         template="plotly_white",
#         height=420
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

# st.divider()

# -------------------------------------------------
# DOWNLOAD FILTERED DATA
# -------------------------------------------------

st.subheader("📥 Export Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Dataset",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.divider()

# -------------------------------------------------
# BUSINESS INSIGHTS
# -------------------------------------------------

st.subheader("💡 Key Business Insights")

highest_customer = customer_summary.loc[
    customer_summary["Revenue"].idxmax()
]

highest_country = country_summary.loc[
    country_summary["Revenue"].idxmax()
]

highest_product = product_sales.iloc[0]

st.success(
    f"👑 Highest Revenue Customer: {highest_customer['customer_id']} "
    f"({currency(highest_customer['Revenue'])})"
)

st.success(
    f"🌍 Best Performing Country: {highest_country['country']} "
    f"({currency(highest_country['Revenue'])})"
)

st.success(
    f"📦 Best Selling Product: {highest_product['description']}"
)

st.success(
    f"💰 Average Customer Spend: {currency(customer_summary['Revenue'].mean())}"
)

st.info(
    "📊 Insight: A small percentage of customers generate a large percentage of total revenue. "
    "Use this information to design customer retention and loyalty programs."
)

st.divider()

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.markdown(
    """
---
<div style="text-align:center;color:gray;">
📈 Sales Analytics Dashboard<br>
Built using Streamlit • Plotly • Pandas
</div>
""",
    unsafe_allow_html=True
)