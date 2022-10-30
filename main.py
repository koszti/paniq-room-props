import config
import time

from paniq_prop.mqtt import Mqtt
from paniq_prop.status_leds import StatusLeds
from paniq_prop.network import Network

# Init components
statusLeds = StatusLeds(
    network_status_pin=config.NETWORK_STATUS_PIN,
    mqtt_status_pin=config.MQTT_STATUS_PIN
)

# Network init detects WIFI and ETH adapters automatically
Network(
    statusLed=statusLeds.network,

    # For WIFI adapter
    wifi_ssid=config.WIFI_SSID,
    wifi_password=config.WIFI_PASSWORD,
    wifi_connection_check_period=config.WIFI_CONNECTION_CHECK_PERIOD,

    # For Ethernet adapter
    eth_ip=config.ETH_IP,
    eth_subnet=config.ETH_SUBNET,
    eth_gateway=config.ETH_GATEWAY,
    eth_dns=config.ETH_DNS,
)

# Custom function to override default mqtt on_message function
# def on_mqtt_message(b_topic: str, b_msg: str, retained: bool, dup: bool):
#     print(f"Custom message receiver: {b_topic} - {b_msg}")

mqtt = Mqtt(
    config.MQTT_CLIENT_ID,
    config.MQTT_SERVER_HOST,
    config.MQTT_SERVER_PORT,
    config.MQTT_TOPICS_TO_SUBSCRIBE,
    config.MQTT_TOPIC_TO_PUBLISH,
    statusLeds.mqtt,
    config.MQTT_SERVER_KEEPALIVE,
    config.MQTT_CONNECTION_CHECK_PERIOD,

    # Set on_message if custom message receiver needed
    # on_message=on_mqtt_message,
)

# Main loop
cnt = 0
while True:
    print("..")

    # Get messages from mqtt topics
    if mqtt.isconnected():
        mqtt.check_msg()

    # Send test messages periodically to mqtt topic
    cnt += 1
    if cnt == 10:
        if mqtt.isconnected():
            mqtt.publish(f"Counter {cnt}")
        cnt = 0

    # Wait
    time.sleep(1)