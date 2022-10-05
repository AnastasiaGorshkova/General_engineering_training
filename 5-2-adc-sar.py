import RPi.GPIO as GPIO
import time
GPIO.setmode (GPIO.BCM)
dac=[26, 19, 13, 6, 5, 11, 9, 10]
comp=4
troyka=17
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
bits=len(dac)
levels=2**bits

def binary(a):
    return [int(d) for d in bin(a)[2::].zfill(8)]

def abc():
    for i in range(255):
        signal=binary(i)
        GPIO.output(dac, signal)
        time.sleep(0.007)
        compvalue=GPIO.input(comp)
        if compvalue==0:
            return i

try:
    while True:
        value=abc()
        if value!=0:
            print(value, "{:.2f}v".format(value*3.3/256))

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()