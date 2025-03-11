# Import Pin class
import time
from robot_hat import Pin

# Create Pin object with numeric pin numbering and default input pullup enabled
d4 = Pin(2, Pin.OUT)
#d1 = Pin(1, Pin.OUT)
# Create Pin object with named pin numbering
#d1.low()
for i in range(10):
  d4.high()
  time.sleep(1)
  d4.low()
  time.sleep(1)
