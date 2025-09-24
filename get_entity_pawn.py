# get_entity_pawn.py
# -*- coding: utf-8 -*-
import globals
def get_entity_pawn(pm, client, i):
    try:
        entity_list = pm.read_longlong(client + globals.dwEntityList)
        if not entity_list:
            return 0, 0
        list_entry = pm.read_longlong(entity_list + ((8 * (i & 0x7FFF) >> 9) + 16))
        if not list_entry:
            return 0, 0
        entity_controller = pm.read_longlong(list_entry + 120 * (i & 0x1FF))
        if not entity_controller:
            return 0, 0
        entity_controller_pawn = pm.read_longlong(entity_controller + globals.m_hPlayerPawn)
        if not entity_controller_pawn:
            return 0, 0
        list_entry2 = pm.read_longlong(entity_list + (0x8 * ((entity_controller_pawn & 0x7FFF) >> 9) + 16))
        if not list_entry2:
            return 0, 0
        pawn = pm.read_longlong(list_entry2 + 120 * (entity_controller_pawn & 0x1FF))
        return pawn, entity_controller
    except Exception:
        return 0, 0