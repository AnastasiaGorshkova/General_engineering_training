import RPi.GPIO as GPIO
import sys
import time
import matplotlib.pyplot as pyplot
dac=[26, 19, 13, 6, 5, 11, 9, 10]
leds=[21, 20, 16, 12, 7, 8, 25, 24]
comp=4
troyka=17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(leds,GPIO.OUT)
GPIO.setup(troyka,GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp,GPIO.IN)


def abc():
    k=0
    for i in range(7,-1,-1):
        k+=2**i
        GPIO.output(dac, binary(k))
        time.sleep(0.0007)
        if GPIO.input(comp)==0:
            k-=2**i
    return k

# перевод в двоичную
def binary(a):
    return [int(d) for d in bin(a)[2::].zfill(8)]

try:
    volt=0
    count=0
    result_value = []
    time_start= time.time()

    # зарядка конденсатора
    while volt<256*0.97:
        volt = abc()
        result_value.append(volt)
        count+=1
        GPIO.output(leds, binary(volt))

    GPIO.setup(troyka, GPIO.OUT,initial=GPIO.LOW)

    # разрядка конденсатора
    while volt>256*0.02:
        volt= abc()
        result_value.append(volt)
        count+=1
        GPIO.output(leds, binary(volt))

    time_measure = time.time() - time_start

    # создание файлов с полученными данными измерений
    with open ("data.txt","w") as s:
        for i in result_value:
            s.write(str(i)+'\n')
    with open ("settings.txt","w") as s:
        s.write(str(1/time_measure/count)+'\n')
        s.write('0.01289')
    print('общая продолжительность эксперимента {}, период одного измерения {}, средняя частота дискретизации проведённых измерений {}, шаг квантования АЦП {}'.format(time_measure, time_measure/count, 1/time_measure/count,3.3/256 ))
    
    # построение графика
    y=[i/256*3.3 for i in result_value]
    x=[i*time_measure/count for i in range(len(result_value))]
    pyplot.plot (x,y)
    pyplot.xlabel('время')
    pyplot.ylabel('напряжение')
    pyplot.show()

finally:
    GPIO.output(dac, 0)
    GPIO.output(leds, 0)
    GPIO.cleanup()
