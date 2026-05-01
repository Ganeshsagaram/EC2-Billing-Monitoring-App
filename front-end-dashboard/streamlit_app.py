import streamlit as st
import requests
import pandas as pd

# 🔗 Backend base URL
BASE_URL = "https://scaling-fortnight-5wgvj9gqrgv27rg4-8000.app.github.dev/"

def get_headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }

# -------------------------------
# 🔐 Login Section
# -------------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token is None:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(
            f"{BASE_URL}/auth/login",
            params={"username": username, "password": password}
        )

        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()  # stop execution if not logged in


if st.session_state.token is not None:
    # Top bar
    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.token = None
            st.rerun()
st.set_page_config(page_title="AWS Dashboard", layout="wide")

st.title("☁️ AWS Monitoring Dashboard")

# -------------------------------
# 🔽 Region Selection
# -------------------------------
region = st.selectbox(
    "Select Region",
    ["eu-north-1", "us-east-1"]
)

# -------------------------------
# 📦 Fetch EC2 Instances
# -------------------------------
st.subheader("EC2 Instances")

try:
    ec2_response = requests.get(f"{BASE_URL}/ec2/instances", params={"region": region},headers=get_headers())
    ec2_data = ec2_response.json()

    instances = ec2_data.get("instances", [])

    if not instances:
        st.warning("No EC2 instances found.")
        instance_ids = []
    else:
        df = pd.DataFrame(instances)
        st.dataframe(df)

        instance_ids = df["instance_id"].tolist()

except Exception as e:
    st.error(f"Error fetching EC2 data: {e}")
    instance_ids = []

# -------------------------------
# 📊 CPU Metrics
# -------------------------------
st.subheader("CPU Utilization")

if instance_ids:
    selected_instance = st.selectbox("Select Instance", instance_ids)

    try:
        metrics_response = requests.get(
            f"{BASE_URL}/metrics/cpu/{selected_instance}",
            params={"region": region},
            headers=get_headers()
        )

        metrics_data = metrics_response.json()
        data = metrics_data.get("data", [])

        if not data:
            st.info("No CPU data available.")
        else:
            df_metrics = pd.DataFrame(data)
            df_metrics["timestamp"] = pd.to_datetime(df_metrics["timestamp"])
            df_metrics.set_index("timestamp", inplace=True)

            st.line_chart(df_metrics["value"])

    except Exception as e:
        st.error(f"Error fetching metrics: {e}")

# -------------------------------
# 💰 Billing Section
# -------------------------------
st.subheader("Monthly Cost")

try:
    billing_response = requests.get(
        f"{BASE_URL}/ec2_billing/monthly",
        params={"region": region},
        headers=get_headers()
    )

    billing_data = billing_response.json()
    if billing_data.get("details")=="Not Found":
        st.warning("Billing data not found for the selected region.")
    st.metric(
        label="EC2 Monthly Cost",
        value=f'{billing_data.get("total_cost", 0)} {billing_data.get("currency", "USD")}'
    )

    st.caption(f"{billing_data.get('start_date')} → {billing_data.get('end_date')}")

except Exception as e:
    st.error(f"Error fetching billing data: {e}")

