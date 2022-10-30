import network
from machine import Timer

from paniq_prop.status_leds import StatusLed

class WifiNetworkAdapter():
    def __init__(
        self,
        statusLed: StatusLed,
        ssid: str,
        password: str,
        connection_check_period: int = 5000,
    ):
        self.ssid = ssid
        self.password = password
        self.statusLed = statusLed
        self.connection_check_period = connection_check_period

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        
        self.init_auto_reconnect_timer()


    def init_auto_reconnect_timer(self):
        reconnect_timer = Timer()
        reconnect_timer.init(
            mode=Timer.PERIODIC,
            period=self.connection_check_period,
            callback=lambda t: self.connect()
        )

    def connect(self):
        if not self.wlan.isconnected():
            if self.wlan.status() != network.STAT_CONNECTING:
                print("Connecting to wifi...")
                if self.statusLed:
                    self.statusLed.blink()

                self.wlan.connect(self.ssid, self.password)
        else:
            print("Wifi connected")
            if self.statusLed:
                self.statusLed.on()

    def disconnect(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()

            if self.statusLed:
                self.statusLed.off()

    def isconnected(self):
        return self.wlan.isconnected()
