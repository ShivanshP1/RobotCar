# Import Pin class
# 
# import time
# import RPi.GPIO as GPIO
# 
# 
# GPIO.setmode(GPIO.BCM)
# 
# GPIO.setup(27, GPIO.out)
# 
# print("LED test begin")
# for i in range(10):
#   GPIO.output(27, GPIO.LOW)
#   time.sleep(1)
#   GPIO.output(27, GPIO.HIGH)
#   time.sleep(1)
# #GPIO.cleanup()
# print("LED test end")
###########################################
from robot_hat import Pin
import time

# Create Pin object with numeric pin numbering and default input pullup enabled
d2 = Pin(27, Pin.OUT)
#d1 = Pin(1, Pin.OUT)
# d1 = Pin(1, Pin.OUT)
# Create Pin object with named pin numbering
#d1.low()
# d1.low()
for i in range(10):
    d2.high()
    time.sleep(1)
    d2.low()
    time.sleep(1)
