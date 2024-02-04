import numpy as np
import cv2 as cv

# Variables used in the arena grid
I = 1  # wall
o = 2  # pellet
e = 3  # empty space
O = 4  # powerpoint
n = 5  # untouchable
P = 6  # pacbot
v = 7  # visited
original_matrix = np.rot90([
    [I, I, I, I, I, I, I, I, I, I, I, I, e, e, e, I,
     I, I, e, e, e, I, I, I, I, I, I, I, I, I, I],
    [I, o, o, o, o, I, I, O, o, o, o, I, e, e, e, I,
     v, I, e, e, e, I, o, o, o, o, o, O, o, o, I],
    [I, o, I, I, o, I, I, o, I, I, o, I, e, e, e, I,
     v, I, e, e, e, I, o, I, I, o, I, I, I, o, I],
    [I, o, I, I, o, o, o, o, I, I, o, I, e, e, e, I,
     v, I, e, e, e, I, o, I, I, o, I, I, I, o, I],
    [I, o, I, I, o, I, I, I, I, I, o, I, e, e, e, I,
     v, I, e, e, e, I, o, I, I, o, I, I, I, o, I],
    [I, o, I, I, o, I, I, I, I, I, o, I, I, I, I, I,
     I, I, I, I, I, I, o, I, I, o, I, I, I, o, I],
    [I, o, I, I, o, o, o, o, o, o, o, o, o, o, o, o,
     o, o, o, o, o, o, o, o, o, o, o, o, o, o, I],
    [I, o, I, I, I, I, I, o, I, I, o, I, I, I, I, I,
     v, I, I, I, I, I, I, I, I, o, I, I, I, o, I],
    [I, o, I, I, I, I, I, o, I, I, o, I, I, I, I, I,
     v, I, I, I, I, I, I, I, I, o, I, I, I, o, I],
    [I, o, I, I, o, o, o, o, I, I, o, v, v, v, v, v,
     v, v, v, v, I, I, o, o, o, o, I, I, I, o, I],
    [I, o, I, I, o, I, I, o, I, I, o, I, I, v, I, I,
     I, I, I, v, I, I, o, I, I, o, I, I, I, o, I],
    [I, o, I, I, o, I, I, o, I, I, o, I, I, v, I, n,
     n, n, I, v, I, I, o, I, I, o, I, I, I, o, I],
    [I, o, o, o, o, I, I, o, o, o, o, I, I, v, I, n,
     n, n, I, v, v, v, o, I, I, o, o, o, o, o, I],
    [I, o, I, I, I, I, I, v, I, I, I, I, I, v, I, n,
     n, n, n, v, I, I, I, I, I, o, I, I, I, I, I],
    [I, o, I, I, I, I, I, v, I, I, I, I, I, v, I, n,
     n, n, n, v, I, I, I, I, I, o, I, I, I, I, I],
    [I, o, o, o, o, I, I, o, o, o, o, I, I, v, I, n,
     n, n, I, v, v, v, o, I, I, o, o, o, o, o, I],
    [I, o, I, I, o, I, I, o, I, I, o, I, I, v, I, n,
     n, n, I, v, I, I, o, I, I, o, I, I, I, o, I],
    [I, o, I, I, o, I, I, o, I, I, o, I, I, v, I, I,
     I, I, I, v, I, I, o, I, I, o, I, I, I, o, I],
    [I, o, I, I, o, o, o, o, I, I, o, v, v, v, v, v,
     v, v, v, v, I, I, o, o, o, o, I, I, I, o, I],
    [I, o, I, I, I, I, I, o, I, I, o, I, I, I, I, I,
     v, I, I, I, I, I, I, I, I, o, I, I, I, o, I],
    [I, o, I, I, I, I, I, o, I, I, o, I, I, I, I, I,
     v, I, I, I, I, I, I, I, I, o, I, I, I, o, I],
    [I, o, I, I, o, o, o, o, o, o, o, o, o, o, o, o,
     o, o, o, o, o, o, o, o, o, o, o, o, o, o, I],
    [I, o, I, I, o, I, I, I, I, I, o, I, I, I, I, I,
     I, I, I, I, I, I, o, I, I, o, I, I, I, o, I],
    [I, o, I, I, o, I, I, I, I, I, o, I, e, e, e, I,
     v, I, e, e, e, I, o, I, I, o, I, I, I, o, I],
    [I, o, I, I, o, o, o, o, I, I, o, I, e, e, e, I,
     v, I, e, e, e, I, o, I, I, o, I, I, I, o, I],
    [I, o, I, I, o, I, I, o, I, I, o, I, e, e, e, I,
     v, I, e, e, e, I, o, I, I, o, I, I, I, o, I],
    [I, o, o, o, o, I, I, O, o, o, o, I, e, e, e, I,
     v, I, e, e, e, I, o, o, o, o, o, O, o, o, I],
    [I, I, I, I, I, I, I, I, I, I, I, I, e, e, e, I, I, I, e, e, e, I, I, I, I, I, I, I, I, I, I]], k=2)

cv_matrix = []

print(original_matrix)