import os
import pika
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# RabbitMQ configurations
RABBITMQ_HOST = 'host.docker.internal'
RABBITMQ_QUEUE = 'webhook_q'

# InfluxDB configurations
INFLUXDB_URL = os.getenv('INFLUXDB_URL', 'http://127.0.0.1:8086')
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN', 'TOKEN_HERE')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG', 'SB')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET', 'telemetry')

def flatten_json(json_obj, parent_key='', sep='_'):
    items = {}
    for key, value in json_obj.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, dict):
            items.update(flatten_json(value, new_key, sep=sep))
        else:
            # Check if the value is an integer, if so, convert it to float
            if isinstance(value, int):
                value = float(value)
            items[new_key] = value
    return items

def callback(ch, method, properties, body):
    # Assuming body contains data in a specific format, adjust this part according to your data format
    json_data = body.decode('utf-8')
    print("Received data:", json_data)

    json_obj = json.loads(json_data)
    flattened_data = flatten_json(json_obj)
    
    for key, value in flattened_data.items():
        print(f"{key}: {value}")
        # Write data to InfluxDB
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
        point = Point(key).field("value", value)
        write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, point)
    
    print("Data sent")

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

# Connect to InfluxDB
influxdb_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN)

# Set up callback to handle incoming messages
channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
