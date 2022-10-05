import RPi.GPIO as GPIO
import time
def decimal2binary(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc(comp, dac):
    value = 0
    d = 0
    for i in range(8):
        d = value + 2 ** (7 - i)
        if d < 256:
            signal = decimal2binary(d)
            GPIO.output(dac, signal)
            time.sleep(0.05)
            comparatorvalue = GPIO.input(comp)
            if comparatorvalue == 1:
                value = d
    return value

GPIO.setmode(GPIO.BCM)
dac= [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17
leds = [21, 20, 16, 12, 7, 8, 25, 24]
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = 1)
GPIO.setup(comp, GPIO.IN)

try:
    while True:
        a = (adc(comp, dac))
        a1 = a
        k = 250 / 8
        for t in leds:
            if a1 > k:
                GPIO.output(t, 1)
                a1 -= k
            else:
                GPIO.output(t, 0)
        print("цифровое-", a, "напряжение", end = " ")
        print("{:.3f}".format(a * 3.3 / 2 ** 8))
finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()