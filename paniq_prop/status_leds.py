import time

from machine import Pin
from machine import Timer


class StatusLed():
    STAT_OFF = 0
    STAT_ON = 1
    STAT_BLINKING = 2
    BLINK_PERIOD = 500

    def __init__(self, pin: Pin):
        self.pin = pin
        self.timer = None
        self.status = self.STAT_OFF

    def _toggle(self):
        self.pin.toggle()

    def _timer_deinit(self):
        if self.timer:
            self.timer.deinit()

    def on(self):
        self._timer_deinit()
        self.pin.high()
        self.status = self.STAT_ON

    def off(self):
        self._timer_deinit()
        self.pin.low()
        self.status = self.STAT_OFF

    def blink(self):
        if self.status != self.STAT_BLINKING:
            self.timer = Timer()
            self.timer.init(
                mode=Timer.PERIODIC,
                period=self.BLINK_PERIOD,
                callback=lambda t: self._toggle(),
            )

        self.status = self.STAT_BLINKING

class StatusLeds():

    def __init__(
        self,
        network_status_pin: int = 0,
        mqtt_status_pin: int = 1,
    ):
        self.network = StatusLed(Pin(network_status_pin, Pin.OUT))
        self.mqtt = StatusLed(Pin(mqtt_status_pin, Pin.OUT))
        self.reset()

    def reset(self):
        self.network.on()
        self.mqtt.on()

        time.sleep(1)

        self.network.off()
        self.mqtt.off()
