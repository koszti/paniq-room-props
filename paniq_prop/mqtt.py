from machine import Timer
from umqtt.simple import MQTTClient

from paniq_prop.logger import Logger
from paniq_prop.status_leds import StatusLed

logger = Logger(__name__)


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

        inbox_topic: str = None,
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

        self.inbox_topic = inbox_topic
        self.on_message = on_message

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
            logger.info(f"Connecting to mqtt broker at {self.server}:{self.port}...")
            try:
                self.status = self.STAT_CONNECTING

                if self.statusLed:
                    self.statusLed.blink()

                self._client.connect()
                self._client.set_callback(self._default_on_message)

                for topic in self.topics:
                    logger.info(f"Subscribing to topic: {topic}")
                    self._client.subscribe(topic)

                self.status = self.STAT_CONNECTED
                self.publish(f"CONNECTED client_id={self.client_id}")

                logger.info("Mqtt connection established")
                if self.statusLed:
                    self.statusLed.on()
            except OSError as e:
                logger.error(f"Failed to connect to MQTT broker. {e}")
                self.status = self.STAT_NOT_CONNECTED
                if self.statusLed:
                    self.statusLed.off()
        elif self.status == self.STAT_CONNECTED:
            logger.info("Mqtt connected")
            if self.statusLed:
                self.statusLed.on()


    def disconnect(self):
        if self._client:
            try:
                self._client.disconnect()
            except OSError:
                pass

            self.status = self.STAT_NOT_CONNECTED

            if self.statusLed:
                self.statusLed.off()

    def isconnected(self):
        return self.status == self.STAT_CONNECTED
    
    def check_msg(self):
        if self.isconnected():
            try:
                self._client.check_msg()
            except OSError as e:
                logger.error(f"Lost connection to MQTT server on checking message. {e}")
                self.disconnect()

    def _default_on_message(self, b_topic: str, b_msg: str, retained: bool, dup: bool):
        topic = b_topic.decode('utf-8')
        msg = b_msg.decode('utf-8')

        if msg:
            logger.info(f"Message received from {topic} (retained: {retained}) (dup: {dup}): {msg}")

            # Send PONG to Room server PING to measure connection speed
            if topic == self.inbox_topic and msg == "@PING":
                self.publish("PONG")

            # Run custom message handler
            elif self.on_message:
                self.on_message(topic, msg)


    def publish(self, msg: str):
        if self.isconnected():
            try:
                self._client.publish(self.topic_to_publish, msg)
            except OSError as e:
                logger.error(f"Lost connection to MQTT server on publish. {e}")
                self.disconnect()
