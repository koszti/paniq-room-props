# Make changes in this file to fit to your prop
# Never commit secrets in this file

# Status leds
NETWORK_STATUS_PIN = 4
MQTT_STATUS_PIN = 5

# WIFI details for Pico W boards
WIFI_CONNECTION_CHECK_PERIOD = 5000
WIFI_SSID = "<secret>"
WIFI_PASSWORD = "<secret>"

# Ethernet details for 2040 boards with ethernet
# There is no DHCP client in the etnernet driver so you need to specify all interface details
ETH_IP="192.168.1.20"
ETH_SUBNET="255.255.255.0"
ETH_GATEWAY="192.168.0.1"
ETH_DNS="8.8.8.8"

# MQTT broker credentials
MQTT_CONNECTION_CHECK_PERIOD = 5000
MQTT_SERVER_HOST="<mqtt-broker-ip>"
MQTT_SERVER_PORT=1883
MQTT_SERVER_KEEPALIVE=60
MQTT_CLIENT_ID="Raspberry PI Pico W/ETH 1"

# Topics to receive messages from
MQTT_TOPICS_TO_SUBSCRIBE = [
    "Room/TestRoom/Control/game:players",
    "Room/TestRoom/Control/game:scenario",
    "Room/TestRoom/Control/game:countdown:seconds",
    "Room/TestRoom/Props/RandomNumber/inbox",
]

# Topics to send messages to
MQTT_TOPIC_TO_PUBLISH = "Room/TestRoom/Props/W-EthProp1/outbox"
