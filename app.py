import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="AI Threat Detector", layout="wide")

st.title("🔐 AI Cloud Threat Detection Dashboard")

# Upload file
uploaded_file = st.file_uploader("Upload Log File", type=["csv"])

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)

        st.subheader("📊 Raw Logs")
        st.dataframe(data)

        # 🚨 Rule-based detection
        failed_logins = data[data['status'] == 'failed']
        failed_count = failed_logins.groupby(['user', 'ip']).size().reset_index(name='fail_count')
        suspicious_users = failed_count[failed_count['fail_count'] > 3]

        st.subheader("🚨 Suspicious Users (Brute Force)")
        st.dataframe(suspicious_users)

        # 🌐 Suspicious IPs
        ip_activity = data.groupby('ip').size().reset_index(name='request_count')
        suspicious_ips = ip_activity[ip_activity['request_count'] > 5]

        st.subheader("🌐 Suspicious IPs")
        st.dataframe(suspicious_ips)

        # 🤖 AI Detection (SAFE)
        st.subheader("🤖 AI Detected Anomalies")

        data_encoded = data.copy()

        # Safe conversions
        data_encoded['status'] = data_encoded['status'].map({'success': 0, 'failed': 1}).fillna(0)

        data_encoded['ip'] = data_encoded['ip'].astype(str).apply(
            lambda x: sum([int(i) for i in x.split('.') if i.isdigit()])
        )

        data_encoded['time'] = data_encoded['time'].astype(str).str.replace(":", "", regex=False)
        data_encoded['time'] = pd.to_numeric(data_encoded['time'], errors='coerce').fillna(0)

        # Model
        model = IsolationForest(contamination=0.2, random_state=42)
        data_encoded['anomaly'] = model.fit_predict(
            data_encoded[['ip', 'time', 'status']]
        )

        anomalies = data_encoded[data_encoded['anomaly'] == -1]

        st.dataframe(anomalies)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

else:
    st.info("👆 Upload a CSV file to start analysis")