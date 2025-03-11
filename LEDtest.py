import RPi.GPIO as GPIO
import time
# Use BCM numbering for the GPIO pins
GPIO.setmode(GPIO.BCM)
# Setup GPIO pin 18 as an output
#GPIO.setup(26, GPIO.OUT) for onboard LED
GPIO.setup(17, GPIO.OUT)
print("ass")
try:
    while True:
        print("fuck")
        GPIO.output(17, GPIO.HIGH) # Turn LED on
        time.sleep(1)              # Wait 1 second
        GPIO.output(17, GPIO.LOW)  # Turn LED off
        time.sleep(1)              # Wait 1 second
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()   
