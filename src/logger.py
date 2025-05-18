import csv
import os
from datetime import datetime

LOG_FILE = "logs/query_log.csv"

def log_interaction(user_name, topic, weak_topic_flag):
    os.makedirs("logs", exist_ok=True)
    write_header = not os.path.exists(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["Timestamp", "User", "Topic", "Weak Topic"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_name,
            topic,
            "Yes" if weak_topic_flag else "No"
        ])
