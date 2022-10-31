# Make changes in this file to fit to your prop
# Never commit secrets in this file

# Prop name to identify your tap.
# MQTT topic names to publish and receive messages will be deri this name
PROP_NAME = "Prop1"

# Logfile name. Set an empty string to disable logging to file
# Log file max size is 1kb. Old logs are deleted automatically
LOG_FILE = ""

# Status leds
NETWORK_STATUS_PIN = 4
MQTT_STATUS_PIN = 5

# WIFI details for Raspberry PI Pico W
WIFI_CONNECTION_CHECK_PERIOD = 5000
WIFI_SSID = "<secret>"
WIFI_PASSWORD = "<secret>"

# Ethernet details for Wiznet W5100S-EVB-Pico
# There is no DHCP client in the etnernet driver so you need to specify all interface details
ETH_IP = "192.168.1.20"
ETH_SUBNET = "255.255.255.0"
ETH_GATEWAY = "192.168.0.1"
ETH_DNS = "8.8.8.8"

# MQTT broker credentials
MQTT_CONNECTION_CHECK_PERIOD = 5000
# IP of your MQTT broker
MQTT_SERVER_HOST = "<mqtt-broker-ip>"
MQTT_SERVER_PORT = 1883
MQTT_SERVER_KEEPALIVE = 60
# Make the MQTT client ID unique across all the props
MQTT_CLIENT_ID = "Wiznet W5100S-EVB-Pico ETH 1"

# Topics to receive messages from
MQTT_TOPIC_PREFIX = "Room/TestRoom"
MQTT_TOPICS_TO_SUBSCRIBE = [
    # Subscribe to topics with room server control messages
    f"{MQTT_TOPIC_PREFIX}/Control/game:players",
    f"{MQTT_TOPIC_PREFIX}/Control/game:scenario",
    f"{MQTT_TOPIC_PREFIX}/Control/game:countdown:seconds",

    # Subscribe to the topic with messages sent to this prop from other ones
    f"{MQTT_TOPIC_PREFIX}/Props/{PROP_NAME}/inbox",
]

# Topics to send messages to. Make it unique across all the props
MQTT_TOPIC_TO_PUBLISH = f"{MQTT_TOPIC_PREFIX}/Props/{PROP_NAME}/outbox"
