# aim_w2s.py
# -*- coding: utf-8 -*-
def aim_w2s(mtx, posx, posy, posz, width, height):
    screenW = mtx[12]*posx + mtx[13]*posy + mtx[14]*posz + mtx[15]
    if screenW > 0.001:
        screenX = mtx[0]*posx + mtx[1]*posy + mtx[2]*posz + mtx[3]
        screenY = mtx[4]*posx + mtx[5]*posy + mtx[6]*posz + mtx[7]
        camX = width / 2
        camY = height / 2
        x = camX + (camX * screenX / screenW)
        y = camY - (camY * screenY / screenW)
        return [x, y]
    return [-999, -999]