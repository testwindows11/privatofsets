# write_view_angles.py
# -*- coding: utf-8 -*-
import globals
def write_view_angles(pm, client, pitch, yaw):
    if globals.dwViewAngles == 0:
        return
    try:
        pm.write_float(client + globals.dwViewAngles, pitch)
        pm.write_float(client + globals.dwViewAngles + 0x4, yaw)
    except Exception:
        pass