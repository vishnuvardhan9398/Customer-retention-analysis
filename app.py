import streamlit as st

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Customer Retention Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Home Page
# ---------------------------
st.title("📊 Customer Retention & Sales Analytics Dashboard")

st.markdown("""
Welcome to the **Customer Retention Dashboard**.

Use the **sidebar** to navigate between pages.

### Available Pages

- 🏠 Home
- 📈 Sales Analytics
- 🤖 Customer Return Prediction

# This project provides interactive business insights, customer analytics, sales trends, and machine learning predictions using the Online Retail dataset.
# """)

# st.info("👈 Select a page from the sidebar to begin exploring the dashboard.")

# st.markdown("---")

# col1, col2, col3 = st.columns(3)

# with col1:
#     st.metric("Dashboard", "Ready")

# with col2:
#     st.metric("Dataset", "Loaded")

# with col3:
#     st.metric("ML Model", "Coming Soon 🚀")

# st.markdown("---")

# st.caption("Developed using Streamlit • Plotly • Pandas • Scikit-learn")