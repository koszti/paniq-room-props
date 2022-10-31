from machine import Timer
from umqtt.simple import MQTTClient

from paniq_prop.status_leds import StatusLed

class Mqtt():
    STAT_NOT_CONNECTED = 0
    STAT_CONNECTED = 1
    STAT_CONNECTING = 2

    def __init__(
        self, 
        statusLed: StatusLed,

        client_id: str,
        server: str,
        port: int,
        topics,
        topic_to_publish: str,
        keepalive: int = 60,
        connection_check_period: int = 5000,
        on_message = None,
    ):
        self.statusLed = statusLed

        self.client_id = client_id
        self.server = server
        self.port = port
        self.topics = topics
        self.topic_to_publish = topic_to_publish
        self.keepalive = keepalive
        self.connection_check_period = connection_check_period

        self.status = self.STAT_NOT_CONNECTED
        self._client = MQTTClient(
            self.client_id,
            self.server,
            self.port,
            keepalive=self.keepalive,
        )
        if on_message:
            self.on_message = on_message
        else:
            self.on_message = self._default_on_message

        self.init_auto_reconnect_timer()
        self.connect()


    def init_auto_reconnect_timer(self):
        reconnect_timer = Timer()
        reconnect_timer.init(
            mode=Timer.PERIODIC,
            period=self.connection_check_period,
            callback=lambda t: self.connect()
        )

    def connect(self):
        if self.status == self.STAT_NOT_CONNECTED:
            print(f"Connecting to mqtt broker at {self.server}:{self.port}...")
            try:
                self.status = self.STAT_CONNECTING

                if self.statusLed:
                    self.statusLed.blink()

                self._client.connect()
                self._client.set_callback(self.on_message)

                for topic in self.topics:
                    print(f"Subscribing to topic: {topic}")
                    self._client.subscribe(topic)

                self.status = self.STAT_CONNECTED
                self.publish(f"CONNECTED client_id={self.client_id}")

                print("Mqtt connection established")
                if self.statusLed:
                    self.statusLed.on()
            except OSError as e:
                print(f"Failed to connect to MQTT broker. {e}")
                self.status = self.STAT_NOT_CONNECTED
                if self.statusLed:
                    self.statusLed.off()
        elif self.status == self.STAT_CONNECTED:
            print("Mqtt connected")
            if self.statusLed:
                self.statusLed.on()


    def disconnect(self):
        if self._client:
            self._client.disconnect()
            self.status = self.STAT_NOT_CONNECTED

            if self.statusLed:
                self.statusLed.off()

    def isconnected(self):
        return self.status == self.STAT_CONNECTED
    
    def check_msg(self):
        if self.isconnected():
            self._client.check_msg()

    def _default_on_message(self, b_topic: str, b_msg: str, retained: bool, dup: bool):
        topic = b_topic.decode('utf-8')
        msg = b_msg.decode('utf-8')
        print(f"Message received from {topic} (retained: {retained}) (dup: {dup}): {msg}")

    def publish(self, msg: str):
        if self.isconnected():
            self._client.publish(self.topic_to_publish, msg)
