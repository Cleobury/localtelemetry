# Use the official Python image as a base
FROM python:3.11.4-slim

# Set environment variables
ENV RABBITMQ_HOST=localhost \
    RABBITMQ_QUEUE=telemetry_q \
    INFLUXDB_URL=http://host.docker.internal:8086 \
    INFLUXDB_TOKEN=TOKEN_HERE \
    INFLUXDB_ORG=SB \
    INFLUXDB_BUCKET=telemetry

# Install dependencies
RUN pip install pika influxdb-client

# Expose ports
EXPOSE 5672 8086 15672 1883

# Copy the Python script into the container
COPY con_webhook_q.py /app/con_webhook_q.py

# Set the working directory
WORKDIR /app

# Run the Python script
CMD ["python", "con_webhook_q.py"]
