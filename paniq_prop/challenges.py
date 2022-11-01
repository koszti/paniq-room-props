from machine import Pin


from paniq_prop.logger import Logger
from paniq_prop.mqtt import Mqtt

logger = Logger(__name__)


def three_pin_is_on(
    pin1: int = 20,
    pin2: int = 21,
    pin3: int = 22,
):
    challenge_name = "three_pin_is_on"
    challenge_is_completed = False
    
    logger.info(f"Checking if [{challenge_name}] challenge completed...")

    p1 = Pin(pin1, Pin.IN, None)
    p2 = Pin(pin2, Pin.IN, None)
    p3 = Pin(pin3, Pin.IN, None)

    p1.init(p1.IN, p1.PULL_DOWN)
    p2.init(p1.IN, p2.PULL_DOWN)
    p3.init(p1.IN, p3.PULL_DOWN)

    logger.info(f"pin1 is {p1.value()}")
    logger.info(f"pin2 is {p2.value()}")
    logger.info(f"pin3 is {p3.value()}")

    if p1.value() == 0 and p2.value() == 0 and p3.value() == 0:
        logger.info(f"[{challenge_name}] challenge is completed")
        challenge_is_completed = True

    return challenge_is_completed
