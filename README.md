# 🚀 LTA Bus Arrival Real-Time Streaming Pipeline

## 📌 Overview

This project builds a real-time data engineering pipeline that ingests live bus arrival data from Singapore’s LTA API, streams it via Kafka, processes events instantly, and generates alerts.

It detects issues like long waits, missing tracking, and crowded buses, simulating a real-world intelligent transport system.

---

## 🎯 Problem Statement

Bus arrival predictions change dynamically, but there is no structured system to monitor:

* Long waiting times
* Missing or untracked buses
* Overcrowded services

This project solves the problem by building a real-time streaming pipeline that processes events and detects anomalies instantly.

---

## 🏗️ Architecture Overview

LTA API → Kafka Producer → Kafka Topic → Kafka Consumer → CSV Outputs

---

## 📌 Key Features

* Real-time data ingestion from LTA API
* Kafka-based streaming pipeline
* ETA calculation and anomaly detection
* Tracking status identification
* CSV-based data persistence

---

## ⚙️ Tech Stack

* Python
* Apache Kafka
* Requests (API ingestion)
* CSV (data storage)

---

## 🔄 Pipeline Flow

### 1. Producer (Data Ingestion)

* Polls LTA Bus Arrival API every 10 seconds
* Extracts:

  * Service number
  * Estimated arrival time
  * Passenger load
  * Latitude & Longitude
  * Tracking status
* Sends structured JSON events to Kafka

---

### 2. Kafka (Streaming Layer)

* Topic: `lta_bus_arrivals`
* Handles real-time event streaming

---

### 3. Consumer (Real-Time Processing)

* Reads streaming data from Kafka
* Calculates ETA in minutes
* Applies business logic to detect anomalies

#### Alerts Generated:

* LONG_WAIT → ETA > 15 minutes
* ARRIVING_OR_PASSED → ETA < 0
* HIGH_LOAD → crowded buses
* NORMAL → no issues

#### Tracking Status:

* TRACKED → valid GPS data
* NOT_TRACKED → missing/invalid GPS

---

### 4. Output Layer

* processed_events.csv → all processed records
* alerts.csv → only anomaly events

---

## 📊 Example Output

Service 12 | ETA: 18 min | Tracking: NOT_TRACKED | Alert: LONG_WAIT
Service 79 | ETA: 9 min  | Tracking: TRACKED     | Alert: NORMAL
Service 198 | ETA: -1 min | Tracking: NOT_TRACKED | Alert: ARRIVING_OR_PASSED

---

## 📂 Project Structure

```
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
```

---

## 🚀 How to Run

### 1. Start Kafka Services

zookeeper-server-start.bat config/zookeeper.properties
kafka-server-start.bat config/server.properties

### 2. Create Kafka Topic

kafka-topics.bat --create --topic lta_bus_arrivals --bootstrap-server localhost:9092

### 3. Run Producer

python producer.py

### 4. Run Consumer

python consumer.py

---

## 💡 Key Learnings

* Built real-time streaming pipelines using Kafka
* Implemented producer–consumer architecture
* Processed live API data
* Designed anomaly detection logic
* Worked with event-driven systems.
