# Make changes in this file to fit to your prop
# Never commit secrets in this file

# Prop name to identify your prop.
# MQTT topic names will be derived from the prop name. Make it unique acress all props
PROP_NAME = "2_UV_BarDoor"

# Logfile name. Set an empty string to disable logging to file
# Log file max size is 1kb. Old logs are deleted automatically
LOG_FILE = ""

# Status leds
NETWORK_STATUS_PIN = 0
MQTT_STATUS_PIN = 1
# Game Hardware Pins
from machine import Pin
UVLIGHT_PIN = Pin(26, Pin.OUT)
DOORSENSOR_PIN = Pin(22, Pin.IN, Pin.PULL_UP)
# DOORSENSOR_PREVIOUS = DOORSENSOR_PIN.value() 

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
MQTT_SERVER_HOST = "192.168.1.66"
MQTT_SERVER_PORT = 1883
MQTT_SERVER_KEEPALIVE = 60
# Make the MQTT client ID unique across all the props
MQTT_CLIENT_ID = "UV_BarDoor_PicoW"

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
def on_mqtt_message(topic: str, msg: str):
    """Turn UV Light on or off by incoming control messages"""
    from machine import Pin

    
    if topic == MQTT_TOPIC_PROP_INBOX and msg == "uvlight:on":
        UVLIGHT_PIN.high()
    elif topic == MQTT_TOPIC_PROP_INBOX and msg == "uvlight:off":
        UVLIGHT_PIN.low()


# Modify this function to do something specific in the main loop
# Typically checking sensors, setting pin values and sending MQTT messages
from paniq_prop.mqtt import Mqtt
def check_sensors(prop_runtime_secs: int, mqtt: Mqtt, state: dict) -> dict:
    """Check if three pins are all ON at the same time"""
    import time

    if not state:
        state = {
            "doorsensor_pin_value": DOORSENSOR_PIN.value(),
        }

    """Send The Door Sensor State"""
    # Send Challenge completed message (OVER) to Room server if door sensor pin on
    # Pin is on if Bar Door is open
    if DOORSENSOR_PIN.value() != state["doorsensor_pin_value"]:
        state["doorsensor_pin_value"] = DOORSENSOR_PIN.value()

        if DOORSENSOR_PIN.value() == 0:
            mqtt.publish(f"OVER Bar Door")
            mqtt.publish(f"tvcontroller:start", topic=f"{MQTT_TOPIC_PREFIX}/Props/3_TVController/inbox")

        if DOORSENSOR_PIN.value() == 1:
            mqtt.publish(f"tvcontroller:stop", topic=f"{MQTT_TOPIC_PREFIX}/Props/3_TVController/inbox")
    
    """Send UV ligth status periodically"""
    # Check the value of the UV light periodically and send it to the Room server
    if not prop_runtime_secs % 1:
        mqtt.publish(f"DATA uvlight_state={UVLIGHT_PIN.value()}")


    return state
