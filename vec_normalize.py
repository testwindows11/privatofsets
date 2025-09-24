# vec_normalize.py
# -*- coding: utf-8 -*-
from vec_length import vec_length
def vec_normalize(vec):
    length = vec_length(vec)
    if length == 0:
        return [0,0,0]
    return [x / length for x in vec]