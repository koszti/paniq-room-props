# paniq-room-props

`paniq-room-props` is a [MicroPython](https://micropython.org/) library to program escape room props by microcontrollers with internet capabilites.
The library detects and sets up the networking capabilites of the board (Wifi or Ethernet), makes it to operate as an MQTT client and gives standard programmable endpoints to customise the prop to behieve uniquely on certain MQTT and sensor events.

Supported devices:
* [Raspberry PI Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
* [Wiznet W5100S-EVB-Pico](https://www.wiznet.io/product-item/w5100s-evb-pico/)

## Installation

### 1. Install the correct MicroPython firmware

Different boards require different MicroPython firmwares:
* **Raspberry PI Pico W**: https://micropython.org/download/rp2-pico-w/
* **Wiznet W5100S-EVB-Pico**: https://github.com/Wiznet/RP2040-HAT-MicroPython/releases

Download the correct UF2 file from the list above and install it onto the board:
* Push and hold the `BOOTSEL` button and plug your board into the USB port of other computer. Release the `BOOTSEL` button after your Pico is connected. It will mount as a Mass Storage Device called RPI-RP2.
* Drag and drop the MicroPython UF2 file onto the RPI-RP2 volume. Your Pico will reboot. You are now running MicroPython.

### 2. Transfer the project files to your board

Transfer the following files and directories to your device with [the Thonny IDE](https://www.freva.com/transfer-files-between-computer-and-raspberry-pi-pico/)
or [without Thonny](https://mikeesto.medium.com/uploading-to-the-raspberry-pi-pico-without-thonny-53de1a10da30).

```
|- lib (dir)
|- paniq_prop (dir)
|- config.py
`- main.py
```

**IMPORTANT**: At the next restart the board will connect to the network and will start operating as an MQTT client
but **the prop is not expected to be working at this stage**. You need to provide unique configuration to each props
by following the next step.

### 3. Edit config

The configuration is unique across all props. It details the board type, the network connections and the
**unique behaviour what to do in the game**. You need to configure all prop differently according to what you want
to use them in the game. You can find example configurations in the [example-configs](./example-configs) directory.

Open the `config.py` **on the board by Thonny** and edit it directly. You will need change at least
the following properties to fit to your environment:

```
# MQTT topic names will be derived from the prop name. Make it unique acress all props
PROP_NAME = "Prop1"

# WIFI details for Raspberry PI Pico W
WIFI_SSID = "your-ssid"
WIFI_PASSWORD = "your-secret"

# Ethernet details for Wiznet W5100S-EVB-Pico
# There is no DHCP client in the etnernet driver so you need to specify all interface details
ETH_IP="192.168.1.20"

# IP of your MQTT broker
MQTT_SERVER_HOST="192.168.1.66"
# Make the MQTT client ID unique across all the props
MQTT_CLIENT_ID="Wiznet W5100S-EVB-Pico ETH 1"

# Topic patters need be in sync with your room server settings
MQTT_TOPIC_PREFIX = "Room/TestRoom"

# Topics to receive messages from
MQTT_TOPICS_TO_SUBSCRIBE = [
    # Subscribe to topics with room server control messages
    f"{MQTT_TOPIC_PREFIX}/Control/game:players",
    f"{MQTT_TOPIC_PREFIX}/Control/game:scenario",

    # Subscribe to the prop's own inbox topic
    MQTT_TOPIC_PROP_INBOX,
]


# Modify this function to do something specific on incoming MQTT messages
def on_mqtt_message(topic: str, msg: str):
    ...

# Modify this function to do something specific in the main loop
# Typically checking sensors, setting pin values and sending MQTT messages
from paniq_prop.mqtt import Mqtt
def check_sensors(prop_runtime_secs: int, mqtt: Mqtt):
    ...
```

If required set other details in the `config.py`.

## In Action

paniq-room-props are compatible with [xcape.io](https://xcape.io/) Room Server.

![Xcape.io](xcape-frontend.png)
