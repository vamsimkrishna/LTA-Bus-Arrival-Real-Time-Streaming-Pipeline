from kafka import KafkaProducer
import requests
import json
import time
from datetime import datetime

API_KEY = "your API key"
BUS_STOP_CODE = "Bus Stop Code"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

topic = "lta_bus_arrivals"

url = f"https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival?BusStopCode={BUS_STOP_CODE}"

headers = {
    "AccountKey": API_KEY,
    "accept": "application/json"
}

print("Starting LTA producer...")

while True:
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"HTTP status: {response.status_code}")

        if response.status_code != 200:
            print("Non-200 response body:")
            print(response.text[:500])
            time.sleep(10)
            continue

        if not response.text.strip():
            print("Empty response received.")
            time.sleep(10)
            continue

        data = response.json()

        query_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        services = data.get("Services", [])
        print(f"Services returned: {len(services)}")

        for service in services:
            for bus in ["NextBus", "NextBus2", "NextBus3"]:
                bus_data = service.get(bus, {})

                if bus_data and bus_data.get("EstimatedArrival"):
                    event = {
                        "query_time": query_time,
                        "bus_stop_code": BUS_STOP_CODE,
                        "service_no": service.get("ServiceNo"),
                        "estimated_arrival": bus_data.get("EstimatedArrival"),
                        "load": bus_data.get("Load"),
                        "feature": bus_data.get("Feature"),
                        "bus_type": bus_data.get("Type"),
                        "visit_number": bus_data.get("VisitNumber"),
                        "latitude": bus_data.get("Latitude"),
                        "longitude": bus_data.get("Longitude"),
                        "monitored": bus_data.get("Monitored")
                    }

                    producer.send(topic, value=event)
                    print(f"Sent: {event}")

        producer.flush()
        time.sleep(10)

    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        time.sleep(10)
    except Exception as e:
        print("Unexpected error:", e)
        time.sleep(10)