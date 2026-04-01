🚀 LTA Bus Arrival Real-Time Streaming Pipeline
📌 Overview

This project builds a real-time data engineering pipeline that ingests live bus arrival data from Singapore’s LTA API, streams it via Kafka, processes events instantly, and generates alerts.

It detects issues like long waits, missing tracking, and crowded buses, simulating a real-world intelligent transport system.

🎯 Problem Statement

Bus arrival predictions change dynamically, but there is no structured system to monitor:

Long waiting times
Missing or untracked buses
Overcrowded services

This project solves the problem by building a real-time streaming pipeline that processes events and detects anomalies instantly.

🏗️ Architecture Overview
LTA API → Kafka Producer → Kafka Topic → Kafka Consumer → CSV Outputs
⚙️ Tech Stack
Python
Apache Kafka
Requests (API ingestion)
CSV (data storage)
🔄 Pipeline Flow

1. Producer (Data Ingestion)
Polls LTA Bus Arrival API every 10 seconds
Extracts:
Service number
Estimated arrival time
Passenger load
Latitude & Longitude
Tracking status
Sends structured JSON events to Kafka

3. Kafka (Streaming Layer)
Topic: lta_bus_arrivals
Handles real-time event streaming

5. Consumer (Real-Time Processing)
Reads streaming data from Kafka
Calculates ETA in minutes
Applies business logic to detect anomalies
Alerts Generated:
LONG_WAIT → ETA > 15 minutes
ARRIVING_OR_PASSED → ETA < 0
HIGH_LOAD → crowded buses
NORMAL → no issues
Tracking Status:
TRACKED → valid GPS data
NOT_TRACKED → missing/invalid GPS

7. Output Layer
processed_events.csv → all processed records
alerts.csv → only anomaly events
📊 Example Output
Service 12 | ETA: 18 min | Tracking: NOT_TRACKED | Alert: LONG_WAIT
Service 79 | ETA: 9 min  | Tracking: TRACKED     | Alert: NORMAL
Service 198 | ETA: -1 min | Tracking: NOT_TRACKED | Alert: ARRIVING_OR_PASSED
📂 Project Structure
lta_kafka_streaming/
├── producer/
│   └── producer.py
├── consumer/
│   └── consumer.py
├── output/
│   ├── processed_events.csv
│   └── alerts.csv
├── requirements.txt
└── README.md

🚀 How to Run
1. Start Kafka Services
zookeeper-server-start.bat config/zookeeper.properties
kafka-server-start.bat config/server.properties

3. Create Kafka Topic
kafka-topics.bat --create --topic lta_bus_arrivals --bootstrap-server localhost:9092

5. Run Producer
python producer.py

7. Run Consumer
python consumer.py
