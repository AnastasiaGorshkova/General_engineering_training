import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import numpy


with open('settings.txt') as file:
    settings=[float(i) for i in file.read().split('\n')]

# считывание из документа показаний компаратора и перевод их через шаг в вольты
data=numpy.loadtxt('data.txt', dtype=int) * settings[1]

# массив времен (создан через количество измерений и известный шаг по времени)
data_time=numpy.array([i*1/settings[0] for i in range(data.size)])

# параметры фигуры
fig, ax=pyplot.subplots(figsize=(16, 10), dpi=500)

# минимальные и максимальные значения для осей графика
ax.axis([data.min(), data_time.max()+1, data.min(), data.max()+0.2])

# интервал основных делений на оси "x":
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))

# интервал вспомогательных делений на оси "x":
ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))

# интервал основных делений и вспомогательных делений на оси "y":
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

# название графика с условием для переноса строки и центрированием
ax.set_title('Процесс заряда и разряда конденсатора в RC цепи')

# главная и дополнительная сетки
ax.grid(which='major', color = 'k')
ax.minorticks_on()
ax.grid(which='minor', color = 'gray', linestyle = ':')

# подпись осей "x" и "y"
ax.set_ylabel("Напряжение, В")
ax.set_xlabel("Время, с")

# линия с легендой
ax.plot(data_time, data, c='black', linewidth=1, label = 'V(t)')
ax.scatter(data_time[0:data.size:100], data[0:data.size:100], marker = 's', c = 'green', s=10)
ax.legend(shadow = False, loc = 'right', fontsize = 30)

#сохранение
fig.savefig('graphic.png')
fig.savefig('graphic.svg')
