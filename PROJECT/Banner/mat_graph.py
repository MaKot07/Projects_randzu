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


data = np.loadtxt(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\Banner\data1',
                        delimiter=',',
                        dtype=float)





# x = list(range(30))
#
# y = [0]*30
# c = 0
# m = 0
# for i in range(30):
#     for j in range(len(data)):
#         if data[j][i] != 0:
#             c += 1
#             m += data[j][i]
#     y[i] = m / c if c != 0 else 0
#     c = 0
#     m = 0
#
# plt.plot(x, y)
# plt.show()

