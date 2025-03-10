import matplotlib.pyplot as plt
import pickle
import numpy as np
from numba import njit, int8


# with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\Banner\data',
#           'rb') as file:
#     while True:
#         try:
#             data = pickle.load(file)
#         except EOFError:
#             break
#
#
#
#
# x = list(range(100))
#
# y = [sum(i) / len(i) if sum(i) != 0 else 0 for i in data]
#
#
# plt.plot(x, y)
# plt.show()


data = np.loadtxt(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\Banner\data3',
                        delimiter=',',
                        dtype=float)



print(data)

x = list(range(40))

r = max(data[0][2:])
print(r)

y = [0]*40
c = 0
m = 0
for i in range(1,40):
    for j in range(len(data)):
        if data[j][i] != 0:
            c += 1
            m += data[j][i]

    y[i] = m / c if c != 0 else 0 #r + np.random.randint(0,5)
    c = 0
    m = 0



# plt.plot(x, y)
#
# plt.xlabel('Ось х') #Подпись для оси х
# plt.ylabel('Ось y') #Подпись для оси y
# plt.title('Первый график') #Название
#
# plt.show()



plt.bar(x, y, label='Среднее время обдумывания') #Параметр label позволяет задать название величины для легенды
plt.xlabel('Количество ходов')
plt.ylabel('Время, сек')
plt.title('Зависимость времени обдумывания хода от количества сделанных ходов')
plt.legend()
plt.show()