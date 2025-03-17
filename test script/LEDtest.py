from robot_hat import Pin
import time

# Create Pin object with gpio pin numbering and configured for output 
d0 = Pin(17, Pin.OUT) #Digital 0  = GPIO 17

for i in range(10):
    d0.high()
    time.sleep(1)
    d0.low()
    time.sleep(1)
