# Import Pin class
import time
from RPI.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.out)

print("LED test begin")
for i in range(10):
  GPIO.output(27, GPIO.LOW)
  time.sleep(1)
  GPIO.output(27, GPIO.HIGH)
  time.sleep(1)
#GPIO.cleanup()
print("LED test end")
