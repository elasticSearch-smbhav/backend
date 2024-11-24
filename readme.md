# Design of the Backend

## Techonologies Used

1. Language - Python is used

2. Database Technologies - For this demo we have used Mongo DB as the primary database

3. Message Queue - AWS SQS ( Simple Queueing Service ) is used due to easy of setup and usage.

4. Backend Server - Python Flask is used to build the server to communicate with the dashboard.

5. Event Driven Processing - We have used AWS Lambda for handling events to SQS queue.

## High level design of the system

<img src="https://drive.google.com/uc?export=view&id=1l_GoIILAbVSXnVF9dgJhgIHWpTSC4n2L" alt="High Level Design" width="90%" height="500">

We have shown the High Level Design of the System

### Description of the Flow

1. We use MCF API for implemeting things like placing of orders/updating listings and SLA checks

2. For Realtime notifications we use the MCF Notifications API, we subscribe to events using AWS Lambda Functions and perform realtime updates from these functions

3. We use the inbound API to perform demand forecasting, when inventory gets too low, we trigger the ML demand predictions workflow to preemtively have inventory

4. We push order data to a queue for multiple consumers like Demand Prediction and Analytics

5. We provide a custom analytics dashboard providing information like order value / count in a set date range

## Running the app

```bash
pip3 install -r requirements.txt
python3 main.py
```