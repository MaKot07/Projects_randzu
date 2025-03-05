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



print(len(data))

x = list(range(2,42))

r = max(data[0])

y = [0]*40
c = 0
m = 0
for i in range(40):
    for j in range(len(data)):
        if data[j][i+2] != 0:
            c += 1
            m += data[j][i+2]

    y[i] = m / c if c != 0 else r + np.random.randint(0, 10)
    c = 0
    m = 0



plt.plot(x, y)
plt.show()

