import time
import random
import csv
from datetime import datetime
import os

file_name = "logs.csv"

users = ["john", "alice", "bob", "admin"]
ips = ["192.168.1.1", "10.0.0.1", "172.16.0.5"]
status = ["success", "failed"]

# Create file with header if not exists
if not os.path.exists(file_name):
    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user", "ip", "time", "status"])

print("🚀 Generating live logs...")

while True:
    log = [
        random.choice(users),
        random.choice(ips),
        datetime.now().strftime("%H:%M:%S"),
        random.choice(status)
    ]

    with open(file_name, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(log)

    print("New log:", log)

    time.sleep(2)