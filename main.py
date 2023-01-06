import config
import network_config
import time

from micropython_ota import micropython_ota

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
    wifi_ssid=network_config.WIFI_SSID,
    wifi_password=network_config.WIFI_PASSWORD,
    wifi_connection_check_period=network_config.WIFI_CONNECTION_CHECK_PERIOD,

    # For Ethernet adapter
    eth_dhcp=network_config.ETH_DHCP,
    eth_ip=network_config.ETH_IP,
    eth_subnet=network_config.ETH_SUBNET,
    eth_gateway=network_config.ETH_GATEWAY,
    eth_dns=network_config.ETH_DNS,
    eth_connection_check_period=network_config.ETH_CONNECTION_CHECK_PERIOD,
)

# Update to latest version from remote server
micropython_ota.ota_update(
    network_config.OTA_HOST,
    config.OTA_PROJECT_NAME,
    config.OTA_FILENAMES,
    use_version_prefix=False,
    hard_reset_device=True,
    soft_reset_device=False,
    timeout=5
)

mqtt = Mqtt(
    statusLed=statusLeds.mqtt,

    # MQTT broker details
    client_id=config.MQTT_CLIENT_ID,
    server=network_config.MQTT_SERVER_HOST,
    port=network_config.MQTT_SERVER_PORT,
    topics=config.MQTT_TOPICS_TO_SUBSCRIBE,
    topic_to_publish=config.MQTT_TOPIC_TO_PUBLISH,
    keepalive=network_config.MQTT_SERVER_KEEPALIVE,
    connection_check_period=network_config.MQTT_CONNECTION_CHECK_PERIOD,

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
    state = dict()
    
    while True:
        # Calculate how long the prop is running
        prop_runtime_secs = main_loop_period_counter * MAIN_PERIOD_SLEEP_SECONDS

        # Check sensor statuses, send custom MQTT messages depending on states
        state = config.check_sensors(prop_runtime_secs, mqtt, state)

        # Check and process incoming MQTT messages
        mqtt.check_msg()

        # Wait
        time.sleep(MAIN_PERIOD_SLEEP_SECONDS)
        main_loop_period_counter += 1


if __name__ == "__main__":
    main_loop()

