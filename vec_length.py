# vec_length.py
# -*- coding: utf-8 -*-
import globals
def vec_length(vec):
    return globals.math.sqrt(sum([x*x for x in vec]))