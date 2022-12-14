# Make changes in this file to fit to your prop
# Never commit secrets in this file

# Prop name to identify your prop.
# MQTT topic names will be derived from the prop name. Make it unique acress all props
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
ETH_CONNECTION_CHECK_PERIOD = 5000
ETH_DHCP = False

# If not using DHCP then specify all interface details
ETH_IP = "192.168.1.20"
ETH_SUBNET = "255.255.255.0"
ETH_GATEWAY = "192.168.1.1"
ETH_DNS = "8.8.8.8"

# MQTT broker credentials
MQTT_CONNECTION_CHECK_PERIOD = 5000
# IP of your MQTT broker
MQTT_SERVER_HOST = "<mqtt-broker-ip>"
MQTT_SERVER_PORT = 1883
MQTT_SERVER_KEEPALIVE = 60
# Make the MQTT client ID unique across all the props
MQTT_CLIENT_ID = "Wiznet W5100S-EVB-Pico ETH 1"

# Topic patters need be in sync with your room server settings
MQTT_TOPIC_PREFIX = "Room/TestRoom"
MQTT_TOPIC_PROP_INBOX = f"{MQTT_TOPIC_PREFIX}/Props/{PROP_NAME}/inbox"

# Topics to receive messages from
MQTT_TOPICS_TO_SUBSCRIBE = [
    # Subscribe to topics with room server control messages
    f"{MQTT_TOPIC_PREFIX}/Control/game:players",
    f"{MQTT_TOPIC_PREFIX}/Control/game:scenario",

    # Subscribe to the prop's own inbox topic
    MQTT_TOPIC_PROP_INBOX,
]

# Topics to send messages to. Make it unique across all the props
MQTT_TOPIC_TO_PUBLISH = f"{MQTT_TOPIC_PREFIX}/Props/{PROP_NAME}/outbox"


# Modify this function to do something specific on incoming MQTT messages
def on_mqtt_message(topic: str, msg: str, state: dict) -> dict:
    print(f"Custom Message received from {topic}: {msg}")
    return state


# Modify this function to do something specific in the main loop
# Typically checking sensors, setting pin values and sending MQTT messages
from paniq_prop.mqtt import Mqtt
def check_sensors(prop_runtime_secs: int, mqtt: Mqtt, state: dict) -> dict:
    import time

    # Example code to publish MQTT message every 5 seconds
    if not prop_runtime_secs % 5:
        mqtt.publish(f"DATA client_id={MQTT_CLIENT_ID} prop_runtime_secs={prop_runtime_secs} time={time.time()}")

    return state
