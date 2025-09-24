# w2s.py
# -*- coding: utf-8 -*-
def w2s(mtx, posx, posy, posz, game_width, game_height, screen_width, screen_height):
    try:
        screenW = mtx[12]*posx + mtx[13]*posy + mtx[14]*posz + mtx[15]
        if screenW > 0.001:
            screenX = mtx[0]*posx + mtx[1]*posy + mtx[2]*posz + mtx[3]
            screenY = mtx[4]*posx + mtx[5]*posy + mtx[6]*posz + mtx[7]
            camX = game_width / 2
            camY = game_height / 2
            x = camX + (camX * screenX / screenW)
            y = camY - (camY * screenY / screenW)
            x = (x / game_width) * screen_width
            y = (y / game_height) * screen_height
            return [x, y]
    except Exception:
        pass
    return [-999, -999]