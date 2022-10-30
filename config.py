# Make changes in this file to fit to your prop
# Never commit secrets in this file


# WIFI details
WIFI_STATUS_PIN = 4
WIFI_CONNECTION_CHECK_PERIOD = 5000
WIFI_SSID = "<secret>"
WIFI_PASSWORD = "<secret>"

# MQTT broker credentials
MQTT_STATUS_PIN = 5
MQTT_CONNECTION_CHECK_PERIOD = 5000
MQTT_SERVER_HOST="<mqtt-broker-ip>"
MQTT_SERVER_PORT=1883
MQTT_SERVER_KEEPALIVE=60
MQTT_CLIENT_ID="Raspberry PI Pico W 1"

# Topics to receive messages from
MQTT_TOPICS_TO_SUBSCRIBE = [
    "Room/TestRoom/Control/game:players",
    "Room/TestRoom/Control/game:scenario",
    "Room/TestRoom/Control/game:countdown:seconds",
    "Room/TestRoom/Props/RandomNumber/inbox",
]

# Topics to send messages to
MQTT_TOPIC_TO_PUBLISH = "Room/TestRoom/Props/WifiProp1/outbox"
