import csv
import os
from datetime import datetime

def log_query(user_name, question, matched_topic, is_weak):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    file_path = os.path.join(log_dir, "query_log.csv")
    
    with open(file_path, mode="a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Timestamp", "User Name", "Question", "Matched Topic", "Is Weak Topic"])
        writer.writerow([datetime.now(), user_name, question, matched_topic, is_weak])
    print(f"Logged query for {user_name}: {question} on topic {matched_topic}. Weak topic: {is_weak}")