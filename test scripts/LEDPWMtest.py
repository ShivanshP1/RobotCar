# Import PWM class
from robot_hat import PWM

# Create PWM object with numeric pin numbering and default input pullup enabled
p4 = PWM(4)
p5 = PWM(5)

# Create PWM object with named pin numbering
#p1 = PWM('P1')

# Set frequency will automatically set prescaller and period
# This is easy for device like Buzzer or LED, which you care
# about the frequency and pulse width percentage.
# this usually use with pulse_width_percent function.
# Set frequency to 1000Hz

###################### pin 4
p4.freq(1000)
print(f"Frequence: {p4.freq()} Hz")
print(f"Prescaler: {p4.prescaler()}")
print(f"Period: {p4.period()}")
p4.pulse_width_percent(100)
##################### pin 5
p5.freq(1000)
print(f"Frequence: {p5.freq()} Hz")
print(f"Prescaler: {p5.prescaler()}")
print(f"Period: {p5.period()}")
p5.pulse_width_percent(200)


