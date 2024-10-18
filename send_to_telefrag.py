#!/usr/bin/env python3

#test script to insert some dummy data into the stream.

import random
import time
from datetime import datetime
import socket

# Telegraf configuration
#TELEGRAF_HOST = 'localhost'  # Change this to your Telegraf host if different
#TELEGRAF_PORT = 8094  # Default port for Telegraf socket_listener input

TELEGRAF_HOST = '192.168.188.25'  # This should match the service name in docker-compose.yml
TELEGRAF_PORT = 8094  # This matches the port we exposed in docker-compose.yml


# Simulated sensor data
def get_sensor_data():
    temperature = round(random.uniform(20, 30), 2)
    humidity = round(random.uniform(40, 60), 2)
    return temperature, humidity

# Generate InfluxDB line protocol string
def generate_line_protocol(measurement, tags, fields):
    tag_string = ','.join([f"{k}={v}" for k, v in tags.items()])
    field_string = ','.join([f"{k}={v}" for k, v in fields.items()])
    timestamp = int(time.time() * 1e9)  # nanosecond precision
    return f"{measurement},{tag_string} {field_string} {timestamp}"

# Send data to Telegraf
def send_to_telegraf(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((TELEGRAF_HOST, TELEGRAF_PORT))
        sock.sendall(data.encode() + b'\n')  # Add newline to separate multiple metrics
    finally:
        sock.close()

# Main loop
def main():
    while True:
        temperature, humidity = get_sensor_data()

        # Prepare the data
        measurement = "room_conditions"
        tags = {
            "location": "living_room",
            "sensor_id": "THSensor001"
        }
        fields = {
            "temperature": temperature,
            "humidity": humidity
        }

        # Generate line protocol
        line_protocol = generate_line_protocol(measurement, tags, fields)

        # Send to Telegraf
        send_to_telegraf(line_protocol)

        print(f"Sent: {line_protocol}")

        # Wait for 5 seconds before sending the next data point
        time.sleep(5)

if __name__ == "__main__":
    main()

