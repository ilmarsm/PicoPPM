import time
from machine import Pin, ADC
from ppm import Servo


led = Pin(25, Pin.OUT)

print("Hello world")

angle = 0
angle_add = 2
servo = Servo(0, angle)

hall = ADC(26)
hall_min = 16200
hall_max = 51000

i = 0
while True:
    i += 1
    # LED light on board
    # led.low()
    # time.sleep(0.1)
    # led.high()
    # time.sleep(0.01)
    # HALL read
    hall_value = hall.read_u16()
    if i % 1000 == 0:
        print("hall_value: %d", hall_value)
    if hall_value > hall_max:
        hall_value = hall_max
    if hall_value < hall_min:
        hall_value = hall_min

    hall_fraction = (hall_value - hall_min) / (hall_max - hall_min)
    angle = hall_fraction * 180
    # PPM output
    # angle += angle_add
    # if angle >= 180:
    #     angle_add = 0 - angle_add
    # if angle <= 0:
    #     angle_add = 0 - angle_add
    servo.move(angle)
