import config
import sys
import time

from paniq_prop.mqtt import Mqtt
from paniq_prop.status_leds import StatusLeds
from paniq_prop.wifi import Wifi

# Init components
statusLeds = StatusLeds(wifi_status_pin=config.WIFI_STATUS_PIN, mqtt_status_pin=config.MQTT_STATUS_PIN)
wifi = Wifi(
    config.WIFI_SSID,
    config.WIFI_PASSWORD,
    statusLeds.wifi,
    config.WIFI_CONNECTION_CHECK_PERIOD,
)

# Custom function to override default mqtt on_message function
# def on_mqtt_message(b_topic: str, b_msg: str):
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
    mqtt.check_msg()

    # Send test messages periodically to mqtt topic
    cnt += 1
    if cnt == 10:
        mqtt.publish(f"Counter {cnt}")
        cnt = 0

    # Wait
    time.sleep(1)
