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

# OTA
OTA_HOST="http://192.168.1.106:8080"

# MQTT broker credentials
MQTT_CONNECTION_CHECK_PERIOD = 5000
# IP of your MQTT broker
MQTT_SERVER_HOST = "192.168.1.106"
MQTT_SERVER_PORT = 1883
MQTT_SERVER_KEEPALIVE = 60
