#! python
# -*- coding: utf-8 -*-

# Скрипт формирует график работы защиты по острому пару ПТ

import matplotlib.pyplot as plt
from Tsaturation import Tsaturation, Tprotection

# print(plt.isinteractive()) # состояние интерактивного режима

# формируем списки давлений
P = range(100, 10100, 10)  	# Давление, кПа
Pa = 101.325  				# атмосферное давление, кПа
Pi = []  					# избыточное давление

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

# вывод для теста
# for x in range(len(P)):
#     print(round(P[x] * 0.001, 2), round(Ts[x], 2), round(Tz[x], 2))

fig, ax = plt.subplots()

# формирование линий
ax.plot(P, Ts, 'r', linestyle='solid')				# линия насыщения
ax.plot(P, Ts_aux, 'g', linestyle='solid')			# линия насыщения с запасом
ax.plot(P, Tz, 'b', linestyle='solid')				# линия защиты

# закраска
ax.fill_between(P, 0, Ts, facecolor='#ffb19a')
ax.fill_between(P, Ts, Ts_aux, facecolor='#aaf0d1')
ax.fill_between(P, Ts_aux, Tz, facecolor='#9ab4ff')

# определение надписей
ax.set(xlabel='Давление (кПа)', ylabel='Температура (°С)',
       title='Работа защиты по острому пару для SST-400')
ax.grid()

# Вывод легенды
lgnd = ax.legend(['T насыщения', 'Требуемый запас', 'Уставка защиты'],
                 loc='upper center', shadow=True)
lgnd.get_frame().set_facecolor('#ffb19a')

fig.savefig("test.png")		# сохраняем изображение
plt.show()					# команда построить график
