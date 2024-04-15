# localtelemetry
Designed to be a self hosted telemetry server running on any architecture. Current solution works fine on both AMD64 and ARM64 architectures.

This solution uses docker to run the applications together in a **single** compose document.

This has been tested on a windows 11 machine using docker desktop 

# Where to begin?

There are two folders marked

- Pywebhook
- RabbitListener

### 1) Build initial apps to your own hub

You will need to build these apps giving them an appropriate name with your docker username beforehand using the following command:

```
docker buildx build --platform linux/arm64,linux/amd64 --push --tag YOUR_DOCKER_USERNAME/APP_NAME:multi .
```

### Example:
```
docker buildx build --platform linux/arm64,linux/amd64 --push --tag myuser123/pywebhook:multi .
```

This command will build the app for both architectures and host it to your users docker hub publically. You may want to tweak this if you want private.


### 2) Edit Compose

Next you will need to edit the compose document labeled compose.yaml inside cleobury-cactuar-mini

The services that need renaming are as follows again:

- webhook
- rabbitlistener

```
  webhook:
      image: cleobury/pywebhook:multi
      restart: unless-stopped
      ports:
        - 5000:5000
      environment:
        - RABBITMQ_HOST=host.docker.internal
      depends_on:
        - rabbitmq
```

Now needs to be:

```
  webhook:
      image: YOUR_DOCKER_USERNAME/pywebhook:multi
      restart: unless-stopped
      ports:
        - 5000:5000
      environment:
        - RABBITMQ_HOST=host.docker.internal
      depends_on:
        - rabbitmq
```

Complete this for both apps and were nearly there!

### 3) Initial build on system

Copy your compose.yaml file and parent folder to the system you would like to run this on.

> [!IMPORTANT]  
> Your given machine must have docker installed on it for this to work. Please go off and install that before continuing. 

Open terminal to the given directory of the compose:

```
cd ./cleobury-cactuar-multi
```

Run docker compose:

```
docker compose up --build
```

This will download and run the solution initialising all of its components and allowing us to get keys for some of the next sequence.

### 4) Filling in the keys to the kingdom

The following apps will need tokens filled in to finish the setup:

- influxdb
- ngrok


> [!IMPORTANT]  
> You will need a personal ngrok account to get a key for that as well as setting up a static address
>
> More information can be found at: https://ngrok.com/

As for influx db you will now need to open a browser and go to your influx db portal:

```
your_ip:8086
```

As it is your first time influx will prompt you to create an admin account as well as creating an org and bucket.

To make things a bit easier name your org SB and your bucket telemetry. If you would like to change these please alter and rebuild the rabbit listener app.

Once you have set these up influx db will give you an api key ready to put into your compose file:

```
  rabbitlistener:
    image: cleobury/rabbitlistener:multi
    restart: unless-stopped
    environment:
      - INFLUXDB_TOKEN=TOKEN_HERE
      - RABBITMQ_HOST=host.docker.internal
      - INFLUXDB_URL=host.docker.internal:8086
    depends_on:
      - rabbitmq
```

Will now be:

```
  rabbitlistener:
    image: cleobury/rabbitlistener:multi
    restart: unless-stopped
    environment:
      - INFLUXDB_TOKEN=dfdsfsfs0d98t7s70vdsdewr65e4ter==
      - RABBITMQ_HOST=host.docker.internal
      - INFLUXDB_URL=host.docker.internal:8086
    depends_on:
      - rabbitmq
```

> [!WARNING]
> You might need to change the environmental variables marked "host.docker.internal" if your project is running not functioning correctly. Just change it to the IP address of the system in use.


### 5) Run

send a json payload to your ngrok address with the suffix /webhook and you can then start viewing data in your influxdb on port 8086 on the devices local ip 🙂

