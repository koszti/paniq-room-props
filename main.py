import config
import time

from machine import Pin

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
    eth_connection_check_period=config.ETH_CONNECTION_CHECK_PERIOD,
)

mqtt = Mqtt(
    statusLed=statusLeds.mqtt,

    # MQTT broker details
    client_id=config.MQTT_CLIENT_ID,
    server=config.MQTT_SERVER_HOST,
    port=config.MQTT_SERVER_PORT,
    topics=config.MQTT_TOPICS_TO_SUBSCRIBE,
    topic_to_publish=config.MQTT_TOPIC_TO_PUBLISH,
    keepalive=config.MQTT_SERVER_KEEPALIVE,
    connection_check_period=config.MQTT_CONNECTION_CHECK_PERIOD,

    inbox_topic=config.MQTT_TOPIC_PROP_INBOX,
    on_message=config.on_mqtt_message,
)

def main_loop():
    """Main loop is doing two things
    1. Checking onboard sensors and sending MQTT messages (config.on_mqtt_message)
    2. Listening to income MQTT messages and processing them (config.check_sensors)

    Both configured in config.py and define uniqe behaviour for the prop
    """
    main_loop_period_counter = 0
    MAIN_PERIOD_SLEEP_SECONDS = 0.5

    while True:
        # Calculate how long the prop is running
        prop_runtime_secs = main_loop_period_counter * MAIN_PERIOD_SLEEP_SECONDS

        # Check sensor statuses, send custom MQTT messages depending on states
        config.check_sensors(prop_runtime_secs, mqtt)

        # Turn battery pin high periodically if BATTERY_CHECK_PERIOD_SECONDS in config is greater than 0 seconds
        if config.BATTERY_CHECK_PERIOD_SECONDS > 0 and prop_runtime_secs % config.BATTERY_CHECK_PERIOD_SECONDS == 0:
            battery_pin = Pin(config.BATTERY_PIN, Pin.OUT)

            battery_pin.high()
            wait(config.BATTERY_CHECK_DURATION_SECONDS)
            battery_pin.low()

        # Check and process incoming MQTT messages
        mqtt.check_msg()

        # Wait
        time.sleep(MAIN_PERIOD_SLEEP_SECONDS)
        main_loop_period_counter += 1


if __name__ == "__main__":
    main_loop()
