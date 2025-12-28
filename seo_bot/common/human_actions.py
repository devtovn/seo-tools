import random
import time
from config import MIN_KEY_DELAY, MAX_KEY_DELAY, HUMAN_DELAY_MIN_S, HUMAN_DELAY_MAX_S


def human_typing(element, text, min_delay=None, max_delay=None):
    if min_delay is None:
        min_delay = MIN_KEY_DELAY
    if max_delay is None:
        max_delay = MAX_KEY_DELAY

    for ch in text:
        element.send_keys(ch)
        time.sleep(random.uniform(min_delay, max_delay))


def human_delay(min_s=None, max_s=None):
    if min_s is None:
        min_s = HUMAN_DELAY_MIN_S
    if max_s is None:
        max_s = HUMAN_DELAY_MAX_S
    time.sleep(random.uniform(min_s, max_s))
