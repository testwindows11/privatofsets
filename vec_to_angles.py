# vec_to_angles.py
# -*- coding: utf-8 -*-
import globals
def vec_to_angles(vec):
    x, y, z = vec
    hyp = globals.math.sqrt(x*x + y*y)
    pitch = globals.math.degrees(globals.math.atan2(-z, hyp))
    yaw = globals.math.degrees(globals.math.atan2(y, x))
    return pitch, yaw