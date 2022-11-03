#####
# Example configuration for a prop on [Raspberry PI Pico W] board
# connected to three disks (darts boards).
#
# Functions:
#   on_mqtt_message: Do nothing on incoming MQTT messages
#   check_sensors  : Checking if three pins are all ON at the same time where
#                    the pins are wired to magnetice sensors in three darts
#                    boards.
#
#                    If the three darts boards are positioned correctly then
#                    the three pins turn all ON and it sends the
#                    "Darts at right positions" challenge completed message
#                    (DONE) to the room server.
#####

# Make changes in this file to fit to your prop
# Never commit secrets in this file

# Prop name to identify your tap.
# MQTT topic names to publish and receive messages will be deri this name
PROP_NAME = "WifiProp1"

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
# There is no DHCP client in the etnernet driver so you need to specify all interface details
ETH_IP = "192.168.1.20"
ETH_SUBNET = "255.255.255.0"
ETH_GATEWAY = "192.168.0.1"
ETH_DNS = "8.8.8.8"

# MQTT broker credentials
MQTT_CONNECTION_CHECK_PERIOD = 5000
# IP of your MQTT broker
MQTT_SERVER_HOST = "192.168.1.66"
MQTT_SERVER_PORT = 1883
MQTT_SERVER_KEEPALIVE = 60
# Make the MQTT client ID unique across all the props
MQTT_CLIENT_ID = "Raspberry PI Pico W 1"

# Common topics
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
def on_mqtt_message(topic: str, msg: str):
    """Do nothing on incoming MQTT messages"""
    pass


# Modify this function to do something specific in the main loop
# Typically checking sensors, setting pin values and sending MQTT messages
from paniq_prop.mqtt import Mqtt
def check_sensors(prop_runtime_secs: int, mqtt: Mqtt):
    """Check if three pins are all ON at the same time"""
    import time
    from machine import Pin

    p1 = Pin(20, Pin.IN, Pin.PULL_UP)
    p2 = Pin(21, Pin.IN, Pin.PULL_UP)
    p3 = Pin(22, Pin.IN, Pin.PULL_UP)

    # Send Challenge completed message (OVER) to Room server if all three pins are on
    # Three pins are on if darts positioned at the right positions
    if p1.value() == 0 and p2.value() == 0 and p3.value() == 0:
        mqtt.publish(f"OVER Darts")
