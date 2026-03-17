import pandas as pd

# Load data
data = pd.read_csv("logs.csv")

print("==== ALL LOGS ====")
print(data)

# 🚨 1. Detect multiple failed logins (Brute Force)
failed_logins = data[data['status'] == 'failed']

failed_count = failed_logins.groupby(['user', 'ip']).size().reset_index(name='fail_count')

suspicious_users = failed_count[failed_count['fail_count'] > 3]

print("\n🚨 Suspicious Users (Brute Force):")
print(suspicious_users)

# 🚨 2. Detect too many requests from same IP
ip_activity = data.groupby('ip').size().reset_index(name='request_count')

suspicious_ips = ip_activity[ip_activity['request_count'] > 5]

print("\n🚨 Suspicious IPs:")
print(suspicious_ips)


from sklearn.ensemble import IsolationForest

# Convert categorical data to numbers
data_encoded = data.copy()
data_encoded['status'] = data_encoded['status'].map({'success': 0, 'failed': 1})

# Convert IP to numeric (simple trick)
data_encoded['ip'] = data_encoded['ip'].apply(lambda x: sum([int(i) for i in x.split('.')]))

# Convert time to numeric
data_encoded['time'] = data_encoded['time'].str.replace(":", "").astype(int)

# Train model
model = IsolationForest(contamination=0.2)
data_encoded['anomaly'] = model.fit_predict(data_encoded[['ip', 'time', 'status']])

# Extract anomalies
anomalies = data_encoded[data_encoded['anomaly'] == -1]

print("\n🤖 AI Detected Anomalies:")
print(anomalies)