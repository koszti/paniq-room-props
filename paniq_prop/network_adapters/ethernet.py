import network
import time

from machine import Pin
from machine import SPI
from machine import Timer

from paniq_prop.status_leds import StatusLed

class EthernetNetworkAdapter():
    STAT_NOT_CONNECTED = 0
    STAT_CONNECTED = 1
    STAT_CONNECTING = 2

    def __init__(
        self,
        statusLed: StatusLed,
        ip: str,
        subnet: str,
        gateway: str,
        dns: str,
        connection_check_period: int = 5000,
    ):
        self.statusLed = statusLed
        self.ip = ip
        self.subnet = subnet
        self.gateway = gateway
        self.dns = dns
        self.connection_check_period = connection_check_period

        self.status = self.STAT_NOT_CONNECTED

        self.nic = network.WIZNET5K(
            SPI(0, 2_000_000, mosi=Pin(19), miso=Pin(16), sck=Pin(18)),
            Pin(17),
            Pin(20),
        )
        
        self.init_auto_reconnect_timer()


    def init_auto_reconnect_timer(self):
        reconnect_timer = Timer()
        reconnect_timer.init(
            mode=Timer.PERIODIC,
            period=self.connection_check_period,
            callback=lambda t: self.connect()
        )

    def connect(self):
        if not self.isconnected():
            if self.status != self.STAT_CONNECTING:
                print("Connecting to Ethernet LAN...")
                self.status = self.STAT_CONNECTING

                if self.statusLed:
                    self.statusLed.blink()
                
                self.nic.ifconfig((self.ip, self.subnet, self.gateway, self.dns))
        else:
            print(f"Ethernet connected: {self.nic.ifconfig()}")
            self.status = self.STAT_CONNECTED
            if self.statusLed:
                self.statusLed.on()

    def disconnect(self):
        print("Disconnect ETH WIZNET5K not implemented")

    def isconnected(self):
        return self.nic.isconnected()
