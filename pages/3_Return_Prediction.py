import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Return Prediction",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

try:
    model = joblib.load("model/return_prediction.pkl")
    scaler = joblib.load("model/scaler.pkl")
except Exception as e:
    st.error("Model files not found.")
    st.stop()

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("🤖 Customer Return Prediction")

st.caption(
    "Predict whether a customer is likely to make another purchase."
)

st.divider()

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

left, right = st.columns(2)

with left:

    total_orders = st.number_input(
        "Total Orders",
        min_value=1,
        value=5
    )

    total_revenue = st.number_input(
        "Total Revenue (£)",
        min_value=0.0,
        value=500.0
    )

    total_quantity = st.number_input(
        "Total Quantity",
        min_value=1,
        value=20
    )

    average_order = st.number_input(
        "Average Order Value",
        min_value=0.0,
        value=100.0
    )

with right:

    recency = st.number_input(
        "Recency (Days)",
        min_value=0,
        value=20
    )

    customer_lifetime = st.number_input(
        "Customer Lifetime (Days)",
        min_value=1,
        value=180
    )

    purchase_frequency = st.number_input(
        "Purchase Frequency",
        min_value=0.0,
        value=0.20,
        format="%.4f"
    )

st.divider()


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

if st.button("Predict Customer Return", use_container_width=True):

    input_data = pd.DataFrame({
        "TotalOrders": [total_orders],
        "TotalRevenue": [total_revenue],
        "TotalQuantity": [total_quantity],
        "AverageOrderValue": [average_order],
        "CustomerLifetime": [customer_lifetime],
        "Recency": [recency],
        "PurchaseFrequency": [purchase_frequency]
    })

    # IMPORTANT:
    # If your training data contains one-hot encoded country columns,
    # you must add those columns here with value 0 before prediction.

    try:

        expected_columns = scaler.feature_names_in_

        for col in expected_columns:
            if col not in input_data.columns:
                input_data[col] = 0

        input_data = input_data[expected_columns]

    except AttributeError:
        pass

    scaled = scaler.transform(input_data)

    if model.__class__.__name__ == "LogisticRegression":
        prediction = model.predict(scaled)[0]
        probability = model.predict_proba(scaled)[0][1]
    else:
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

    st.divider()

    st.subheader("Prediction Result")

    st.progress(float(probability))

    st.metric(
        "Return Probability",
        f"{probability*100:.2f}%"
    )

    if probability >= 0.80:
        st.success("🟢 High Chance of Returning")

    elif probability >= 0.50:
        st.warning("🟡 Medium Chance of Returning")

    else:
        st.error("🔴 Low Chance of Returning")

# --------------------------------------------------
# BUSINESS RECOMMENDATION
# --------------------------------------------------

    st.divider()

    st.subheader("Business Recommendation")

    if probability >= 0.80:

        st.success(
            """
✅ Loyal Customer

• Recommend premium products

• Offer exclusive rewards

• Invite to loyalty program
"""
        )

    elif probability >= 0.50:

        st.warning(
            """
⚠ Moderate Customer

• Send discount coupons

• Personalized recommendations

• Email campaigns
"""
        )

    else:

        st.error(
            """
❌ High Risk Customer

• Immediate retention campaign

• Special discounts

• Phone or email follow-up

• Win-back strategy
"""
        )

    st.divider()

    st.subheader("Input Summary")

    summary = pd.DataFrame({

        "Feature":[
            "Orders",
            "Revenue",
            "Quantity",
            "Average Order",
            "Recency",
            "Lifetime",
            "Frequency"
        ],

        "Value":[
            total_orders,
            total_revenue,
            total_quantity,
            average_order,
            recency,
            customer_lifetime,
            purchase_frequency
        ]

    })

    st.dataframe(
        summary,
        use_container_width=True
    )

st.divider()

st.markdown(
"""
<div style="text-align:center;color:gray;">
Customer Return Prediction Module<br>
Built using Streamlit + Scikit-learn
</div>
""",
unsafe_allow_html=True
)

