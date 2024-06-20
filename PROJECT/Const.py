#CONST COLORS
import copy

WHITE = (255, 255, 255)
RED = (225, 0, 50)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)
BLACK = (10, 10, 10)
GRAY = (92, 87, 87)
black = 0
white = 1

#CONST PARAMETRE BOARD
cell_qty = 14
cell_size = 40
cell_size_ramka = 42
colors = (234, 237, 204)
board_shift = 30



from numba.experimental import jitclass
from typing import List
from numba.typed import List as NumbaList
from numba import typed, typeof
from numba import int32, float32, int64, int8
import numpy as np
from numba import njit,jit
from numba import types, typed

#spec = [
    #('a', int64(:,:)),
    #('n', int32)
#]

#@jitclass
##class A:
    #a: List[int64]
    #def __init__(self, n):
        #self.a = a
        #self.n = n

    #def pr(self):
        #print(self.a)

    #def gh(self):
        #self.n += 32
        #print(self.n)

    #def ad(self):
        #g = NumbaList([1,2,8])
        #g.append(self.a)
        #g = typed.List()
        #print(1)
        #self.a = np.append(self.a, [[1],[2]])
        #self.a.append([21])
        #print(1)

#c = np.array([[4,2]], 'int64')
#print("#@",c)
#c = np.append(c, [[1,2],[3,4,5]])
#print("#@",c)
#b = A(c,4)
#b.pr()
#b.gh()
#b.ad()
#b.pr()


#b = A( NumbaList([[1,2]]),4)
#b.ad()
#b.pr()


#t = typed.List()
#t.append(1)
#r.append(copy.copy(t))
#t.append(2)

#o = np.array([[1,2],[3,4]])
#print("1!",o)
#n = np.array([[5],[6]])
#o = np.vstack((o,[[5,6]]))
#print("2!",o, len(o[0]))

#r = np.array([[3,4]])
#print(np.concatenate([r, k]))
#print( r > k)
#print(np.where (o == [1,2] )[0][0])
#@njit
#3def pr():
#   a = (False,0)
#    f = np.array([1,2])
#    print(f[1])
#    return f
#3d = pr()
#print(type(d))

#v = np.array([[1,2]])
#rint(np.stack((r, k, v)))
#e = np.array(v)
#print("#@#$",e)

a = np.array([1,2,3,4,5])
print(len(np.where(a == [8])[0]))
