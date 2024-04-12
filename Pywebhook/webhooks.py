from flask import Flask, request, jsonify
import logging
import pika
import json
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    logging.info('Python HTTP trigger function processed a request.')

    ok = True

    # Connection parameters
    rabbitmq_host = os.environ.get('RABBITMQ_HOST', "host.docker.internal")
    rabbitmq_port = 5672
    queue_name = "webhook_q"

    # Establishing connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    try:
        # Get the request body
        data = request.get_json()
        if not data:
            raise ValueError("No json body passed in the request.")
        
        # Convert data to JSON
        json_data = json.dumps(data)
        
        # Publish the message to the queue
        channel.basic_publish(exchange='', routing_key=queue_name, body=json_data)
        print(f"Sent '{json_data}' to {queue_name}")
    except Exception as e:
        ok = False
        # report error
        print("An error occurred:", e)
        pass

    if ok:
        return jsonify({"message":"Request processed successfully."}), 200
    else:
        return jsonify({"message":"An error occurred while processing the request."}), 402


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
