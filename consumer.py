from kafka import KafkaConsumer
import json
from datetime import datetime
import csv
import os

consumer = KafkaConsumer(
    'lta_bus_arrivals',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Smart consumer started...")

BASE_DIR = r"C:\projects\lta_kafka_streaming"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

processed_file = os.path.join(OUTPUT_DIR, "processed_events.csv")
alerts_file = os.path.join(OUTPUT_DIR, "alerts.csv")

processed_headers = [
    "query_time",
    "bus_stop_code",
    "service_no",
    "estimated_arrival",
    "eta_minutes",
    "load",
    "feature",
    "bus_type",
    "visit_number",
    "latitude",
    "longitude",
    "monitored",
    "tracking_status",
    "alert"
]

alert_headers = [
    "query_time",
    "bus_stop_code",
    "service_no",
    "eta_minutes",
    "tracking_status",
    "alert"
]

def ensure_csv(file_path, headers):
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

def calculate_eta_minutes(estimated_arrival):
    try:
        arrival_time = datetime.fromisoformat(estimated_arrival.replace("Z", "+00:00"))
        now = datetime.now(arrival_time.tzinfo)
        return int((arrival_time - now).total_seconds() / 60)
    except:
        return None

ensure_csv(processed_file, processed_headers)
ensure_csv(alerts_file, alert_headers)

for message in consumer:
    data = message.value
    eta = calculate_eta_minutes(data["estimated_arrival"])

    tracking_status = "TRACKED"
    if str(data.get("latitude")) == "0.0" or data.get("monitored") == 0:
        tracking_status = "NOT_TRACKED"

    alerts = []

    if eta is not None and eta > 15:
        alerts.append("LONG_WAIT")

    if eta is not None and eta < 0:
        alerts.append("ARRIVING_OR_PASSED")

    if data.get("load") == "LSD":
        alerts.append("HIGH_LOAD")

    if not alerts:
        alerts.append("NORMAL")

    alert_text = ", ".join(alerts)

    print(
        f"Service {data['service_no']} | "
        f"ETA: {eta} min | "
        f"Tracking: {tracking_status} | "
        f"Alert: {alert_text}"
    )

    with open(processed_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            data.get("query_time"),
            data.get("bus_stop_code"),
            data.get("service_no"),
            data.get("estimated_arrival"),
            eta,
            data.get("load"),
            data.get("feature"),
            data.get("bus_type"),
            data.get("visit_number"),
            data.get("latitude"),
            data.get("longitude"),
            data.get("monitored"),
            tracking_status,
            alert_text
        ])

    if alert_text != "NORMAL":
        with open(alerts_file, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                data.get("query_time"),
                data.get("bus_stop_code"),
                data.get("service_no"),
                eta,
                tracking_status,
                alert_text
            ])