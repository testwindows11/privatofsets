# normalize_angle.py
# -*- coding: utf-8 -*-
def normalize_angle(delta):
    if delta > 180:
        delta -= 360
    elif delta < -180:
        delta += 360
    return delta