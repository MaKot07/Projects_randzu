#CONST COLORS
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
import numba

spec = [
    ('a', int32[:]),
    ('n', int32)
]

@jitclass(spec)
class A:
    #a: List[List[int64]]
    #n: numba.as_numba_type(SomeOtherType)
    #n: int32
    def __init__(self,a, n):
        self.a = a
        self.n = n

    def pr(self):
        print(self.a)

    def gh(self):
        print(self.n)

    def ad(self):
        #g = NumbaList([1,2,8])
        #g.append(self.a)
        #g = typed.List()
        #print(1)
        self.a = np.append(self.a, [1])
        #self.a.append(g)

c = np.array([1])
print("#@",c)
c = np.append(c, [1])
print("#@",c)
b = A(c,4)
b.pr()
#b.gh()
b.ad()
b.pr()

#d = typed.List()
#print(d)
#d.append(1)
#d.append(2)
#print(d)
#print(typeof(d))

