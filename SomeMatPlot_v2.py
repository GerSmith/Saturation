#! python
# -*- coding: utf-8 -*-

# Скрипт формирует график работы защиты по острому пару ПТ
# Версия 2

import pylab
from Tsaturation import Tsaturation, Tprotection
# Импортируем класс слайдера
from matplotlib.widgets import Slider

# print(plt.isinteractive()) # состояние интерактивного режима

# формируем списки давлений
P = range(100, 10100, 10)  	# Давление, кПа
Pa = 101.325  				# атмосферное давление, кПа
Pi = []  					# избыточное давление
# Пересчёт на показания датчиков
for a in P:
    Pi.append(a - Pa)

# формируем пустые списки температур
Ts = []			# для Т насщения
Ts_aux = []  	# для T запаса
Tz = []			# для уставки защиты

# константы для расчёта
dt = 50			# запас 50 °С

# наполняем списки значениями от функций
for i in Pi:
    Ts.append(Tsaturation(i * 0.001))
    Tz.append(Tprotection(i * 0.001))

for j in range(len(Ts)):
    Ts_aux.append(Ts[j] + dt)


def updateGraph():
    '''!!! Функция для обновления графика'''
    # Будем использовать sigma и mu, установленные с помощью слайдеров
    global slider_P
    global slider_T
    global graph_axes

    # Используем атрибут val, чтобы получить значение слайдеров
    P = slider_P.val
    T = slider_T.val

    # graph_axes.clear()
    graph_axes.scatter(P, T)
    pylab.draw()


def onChangeValue(value):
    '''!!! Обработчик события изменения значений слайдеров'''
    updateGraph()


# Создадим окно с графиком
fig, graph_axes = pylab.subplots()
graph_axes.grid()

# Оставим снизу от графика место для виджетов
fig.subplots_adjust(left=0.06, right=0.95, top=0.95, bottom=0.2)

# Создание слайдера для задания sigma
axes_slider_P = pylab.axes([0.05, 0.1, 0.88, 0.04])
slider_P = Slider(axes_slider_P,
                  label='P',
                  valmin=0,
                  valmax=9999,
                  valinit=2000,
                  valfmt='%4.0f')

# !!! Подпишемся на событие при изменении значения слайдера.
slider_P.on_changed(onChangeValue)

# Создание слайдера для задания mu
axes_slider_T = pylab.axes([0.05, 0.05, 0.88, 0.04])
slider_T = Slider(axes_slider_T,
                  label='T',
                  valmin=150,
                  valmax=450,
                  valinit=300,
                  valfmt='%3.0f')

# !!! Подпишемся на событие при изменении значения слайдера.
slider_T.on_changed(onChangeValue)

# формирование линий
graph_axes.plot(P, Ts, 'r', linestyle='solid')				# линия насыщения
graph_axes.plot(P, Ts_aux, 'g', linestyle='solid')			# линия с запасом
graph_axes.plot(P, Tz, 'b', linestyle='solid')				# линия защиты

# закраска
graph_axes.fill_between(P, 0, Ts, facecolor='#ffb19a')
graph_axes.fill_between(P, Ts, Ts_aux, facecolor='#aaf0d1')
graph_axes.fill_between(P, Ts_aux, Tz, facecolor='#9ab4ff')

# определение надписей
graph_axes.set(xlabel='Давление (кПа)', ylabel='Температура (°С)',
               title='Работа защиты по острому пару для SST-400')

# Вывод легенды
lgnd = graph_axes.legend(['T насыщения', 'Требуемый запас', 'Уставка защиты'],
                         loc='upper left', shadow=True)
lgnd.get_frame().set_facecolor('#ffb19a')

# fig.savefig("test.png")			# сохраняем изображение
updateGraph()
mng = pylab.get_current_fig_manager()
mng.full_screen_toggle()
pylab.show()					# команда построить график
