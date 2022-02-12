# commandline 'sudo pigpiod' before starting
import MongoModule as MM
from gpiozero import Servo
from time import sleep
import math
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

client = MM.get_database()
database = client['RaspPiMotor']
collection = database['Motor']

thumb = 17
index = 27
middle = 22
ring = 23
pinky = 24

thumbServo = Servo(thumb, min_pulse_width=0.5/1000,
                   max_pulse_width=2.5/1000, pin_factory=factory)
indexServo = Servo(index, min_pulse_width=0.5/1000,
                   max_pulse_width=2.5/1000, pin_factory=factory)
middleServo = Servo(middle, min_pulse_width=0.5/1000,
                    max_pulse_width=2.5/1000, pin_factory=factory)
ringServo = Servo(ring, min_pulse_width=0.5/1000,
                  max_pulse_width=2.5/1000, pin_factory=factory)
pinkyServo = Servo(pinky, min_pulse_width=0.5/1000,
                   max_pulse_width=2.5/1000, pin_factory=factory)


def MotorValue(degrees):
    rad = degrees * (math.pi/360)
    val = math.sin(rad)
    return val


while True:
    handValues = collection.find_one({"_id": "right"}, {})
    handList = list(handValues.items())
    thumbServo.value = MotorValue(handList[1][1])
    indexServo.value = MotorValue(handList[2][1])
    middleServo.value = MotorValue(handList[3][1])
    ringServo.value = MotorValue(handList[4][1])
    pinkyServo.value = MotorValue(handList[5][1])
