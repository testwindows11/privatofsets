# aimbot.py
# -*- coding: utf-8 -*-
import keyboard
import globals
from aim_w2s import aim_w2s
from vec_sub import vec_sub
from vec_normalize import vec_normalize
from vec_to_angles import vec_to_angles
from normalize_angle import normalize_angle
from write_view_angles import write_view_angles
from get_entity_pawn import get_entity_pawn
import pymem
import time

def aimbot(ignore_team):
    if not keyboard.is_pressed(globals.aimbot_key):
        return
    local_player = globals.pm.read_longlong(globals.client + globals.dwLocalPlayerPawn)
    if not local_player:
        return
    try:
        local_scene = globals.pm.read_longlong(local_player + globals.m_pGameSceneNode)
        local_pos_x = globals.pm.read_float(local_scene + globals.vec_abs_origin)
        local_pos_y = globals.pm.read_float(local_scene + globals.vec_abs_origin + 0x4)
        local_pos_z = globals.pm.read_float(local_scene + globals.vec_abs_origin + 0x8)
        view_offset_x = globals.pm.read_float(local_player + globals.m_vecViewOffset)
        view_offset_y = globals.pm.read_float(local_player + globals.m_vecViewOffset + 0x4)
        view_offset_z = globals.pm.read_float(local_player + globals.m_vecViewOffset + 0x8)
        local_eye = [local_pos_x + view_offset_x, local_pos_y + view_offset_y, local_pos_z + view_offset_z]
    except Exception:
        return
    local_team = globals.pm.read_int(local_player + globals.m_iTeamNum)
    closest_dist = float('inf')
    best_angles = None
    view_matrix = [globals.pm.read_float(globals.client + globals.dwViewMatrix + i * 4) for i in range(16)]
    center_x = globals.WINDOW_WIDTH / 2
    center_y = globals.WINDOW_HEIGHT / 2
    current_yaw = globals.pm.read_float(globals.client + globals.dwViewAngles + 0x4)
    current_pitch = globals.pm.read_float(globals.client + globals.dwViewAngles)
    for i in range(1, 64):
        entity, _ = get_entity_pawn(globals.pm, globals.client, i)
        if not entity:
            continue
        if entity == local_player:
            continue
        if globals.pm.read_int(entity + globals.m_lifeState) != 256:
            continue
        if globals.pm.read_int(entity + globals.m_iHealth) <= 0:
            continue
        if not ignore_team and globals.pm.read_int(entity + globals.m_iTeamNum) == local_team:
            continue
        game_scene = globals.pm.read_longlong(entity + globals.m_pGameSceneNode)
        bone_matrix = globals.pm.read_longlong(game_scene + globals.m_modelState + 0x80)
        try:
            headX = globals.pm.read_float(bone_matrix + 6 * 0x20)
            headY = globals.pm.read_float(bone_matrix + 6 * 0x20 + 0x4)
            headZ = globals.pm.read_float(bone_matrix + 6 * 0x20 + 0x8)
            enemy_head = [headX, headY, headZ]
            delta_vec = vec_sub(enemy_head, local_eye)
            norm_vec = vec_normalize(delta_vec)
            pitch, yaw = vec_to_angles(norm_vec)
            if globals.use_fov_circle:
                head_pos = aim_w2s(view_matrix, headX, headY, headZ, globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT)
                if head_pos[0] == -999 or head_pos[1] == -999:
                    continue
                screen_dist = globals.math.sqrt((head_pos[0] - center_x)**2 + (head_pos[1] - center_y)**2)
                if screen_dist > globals.FOV_RADIUS:
                    continue
            else:
                delta_yaw = normalize_angle(yaw - current_yaw)
                delta_pitch = pitch - current_pitch
                screen_dist = globals.math.sqrt(delta_yaw**2 + delta_pitch**2)
            if screen_dist < closest_dist:
                closest_dist = screen_dist
                best_angles = (pitch, yaw)
        except Exception:
            continue
    if best_angles:
        try:
            pitch, yaw = best_angles
            write_view_angles(globals.pm, globals.client, pitch, yaw)
        except Exception:
            pass

def aimbot_process(shared_dict):
    try:
        pm_local = pymem.Pymem("cs2.exe")
        client_local = pymem.process.module_from_name(pm_local.process_handle, "client.dll").lpBaseOfDll
    except Exception:
        return
    while True:
        if shared_dict.get('aimbot_enabled', False):
            # Use local pm and client for the process
            local_ignore_team = shared_dict.get('ignore_team', True)
            local_aimbot_key = shared_dict.get('aimbot_key', 'alt')
            local_use_fov_circle = shared_dict.get('use_fov_circle', True)
            local_fov_radius = shared_dict.get('FOV_RADIUS', 150)
            # Temporarily set globals for the function call
            original_pm = globals.pm
            original_client = globals.client
            original_ignore_team = globals.ignore_team
            original_aimbot_key = globals.aimbot_key
            original_use_fov_circle = globals.use_fov_circle
            original_FOV_RADIUS = globals.FOV_RADIUS
            globals.pm = pm_local
            globals.client = client_local
            globals.ignore_team = local_ignore_team
            globals.aimbot_key = local_aimbot_key
            globals.use_fov_circle = local_use_fov_circle
            globals.FOV_RADIUS = local_fov_radius
            aimbot(local_ignore_team)
            # Restore originals
            globals.pm = original_pm
            globals.client = original_client
            globals.ignore_team = original_ignore_team
            globals.aimbot_key = original_aimbot_key
            globals.use_fov_circle = original_use_fov_circle
            globals.FOV_RADIUS = original_FOV_RADIUS
        time.sleep(0)