# anti_flash_logic.py
# -*- coding: utf-8 -*-
import globals
from is_process_running import is_process_running

def anti_flash_logic(pm, client, anti_flash_enabled):
    if not is_process_running(pm, "cs2.exe"):
        return False
    try:
        local_player = pm.read_longlong(client + globals.dwLocalPlayerPawn)
        if local_player:
            pm.write_float(local_player + globals.m_flFlashMaxAlpha, 0.0 if anti_flash_enabled else 255.0)
    except Exception:
        return False
    return True