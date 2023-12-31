import time
from machine import Pin, ADC
from ppm import Servo


def collect_hall_neutral(hall: ADC):
    collection_time = 0.5  # seconds
    steps = 50
    neutral = 0
    min_v = 999999
    max_v = 0
    for _ in range(steps):
        time.sleep(collection_time/steps)
        value = hall.read_u16()
        neutral += value / steps
        min_v = min(min_v, value)
        max_v = max(max_v, value)

    return neutral, min_v, max_v


def exponential(x, e=3.0):
    return x / (1 + (1/e) - x)/e


led = Pin(25, Pin.OUT)

print("Hello world")

angle = 0
angle_add = 2
servo = Servo(0, angle)

hall = ADC(26)
hall_min = 16200
hall_max = 51000
hall_neutral, hall_neutral_min, hall_neutral_max = collect_hall_neutral(hall)

i = 0
while True:
    i += 1
    # LED light on board
    # led.low()
    # time.sleep(0.1)
    # led.high()
    time.sleep(0.01)
    # HALL read
    hall_value = hall.read_u16()
    if hall_value > hall_max:
        hall_value = hall_max
    if hall_value < hall_min:
        hall_value = hall_min

    if hall_value > hall_neutral_max:
        # Forward
        hall_fraction = (hall_value - hall_neutral_max) / (hall_max - hall_neutral_max)
        hall_fraction = exponential(hall_fraction, 5)
        angle = 90 + (hall_fraction * 45)
    else:
        # Backward
        hall_fraction = (hall_neutral_min - hall_value) / (hall_neutral_min - hall_min)
        hall_fraction = exponential(hall_fraction, 5)
        angle = 90 - (hall_fraction * 45)

    if i % 100 == 0:
        led.toggle()
        print("neutral: (%d,%d,%d) hall_value: %d angle: %f" % (hall_neutral, hall_neutral_min, hall_neutral_max, hall_value, angle))

    # PPM output
    # angle += angle_add
    # if angle >= 180:
    #     angle_add = 0 - angle_add
    # if angle <= 0:
    #     angle_add = 0 - angle_add
    servo.move(angle)


