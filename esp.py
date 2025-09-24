# esp.py
# -*- coding: utf-8 -*-
import imgui
import globals
from w2s import w2s
from get_entity_pawn import get_entity_pawn
from is_process_running import is_process_running

def esp(draw_list, display_allies, pm, client, esp_enabled, esp_skeleton_enabled, esp_hp_enabled, esp_names_enabled, esp_hitbox_enabled, esp_head_circle_enabled, enemy_skeleton_color, teammate_skeleton_color, enemy_head_color, teammate_head_color, enemy_name_color, teammate_name_color, enemy_hp_color, teammate_hp_color, enemy_hitbox_color, teammate_hitbox_color):
    if not esp_enabled:
        return True
    if not is_process_running(pm, "cs2.exe"):
        return False
    try:
        view_matrix = [pm.read_float(client + globals.dwViewMatrix + i * 4) for i in range(16)]
    except Exception:
        return False
    local_player = pm.read_longlong(client + globals.dwLocalPlayerPawn)
    if not local_player:
        return True
    try:
        local_team = pm.read_int(local_player + globals.m_iTeamNum)
    except Exception:
        return True
    for i in range(1, 64):
        entity, entity_controller = get_entity_pawn(pm, client, i)
        if not entity or entity == local_player:
            continue
        try:
            if pm.read_int(entity + globals.m_lifeState) != 256:
                continue
            if pm.read_int(entity + globals.m_iHealth) <= 0:
                continue
        except Exception:
            continue
        try:
            entity_team = pm.read_int(entity + globals.m_iTeamNum)
        except Exception:
            continue
        if not display_allies and entity_team == local_team:
            continue
        # Вибір кольору по команді
        if entity_team == local_team:
            skeleton_color_u32 = imgui.get_color_u32_rgba(*teammate_skeleton_color)
            head_color_u32 = imgui.get_color_u32_rgba(*teammate_head_color)
            name_color = imgui.get_color_u32_rgba(*teammate_name_color)
            hp_color = imgui.get_color_u32_rgba(*teammate_hp_color)
            line_color = imgui.get_color_u32_rgba(*teammate_hitbox_color)
        else:
            skeleton_color_u32 = imgui.get_color_u32_rgba(*enemy_skeleton_color)
            head_color_u32 = imgui.get_color_u32_rgba(*enemy_head_color)
            name_color = imgui.get_color_u32_rgba(*enemy_name_color)
            hp_color = imgui.get_color_u32_rgba(*enemy_hp_color)
            line_color = imgui.get_color_u32_rgba(*enemy_hitbox_color)
        try:
            game_scene = pm.read_longlong(entity + globals.m_pGameSceneNode)
            bone_matrix = pm.read_longlong(game_scene + globals.m_modelState + 0x80)
        except Exception:
            continue
        try:
            bone_indices = {
                'head': 6, 'neck': 5, 'spine_3': 4, 'spine_2': 3, 'spine_1': 2, 'spine_0': 1, 'pelvis': 0,
                'left_clavicle': 7, 'left_upper_arm': 8, 'left_lower_arm': 9, 'left_hand': 10,
                'right_clavicle': 12, 'right_upper_arm': 13, 'right_lower_arm': 14, 'right_hand': 15,
                'left_upper_leg': 22, 'left_lower_leg': 23, 'left_foot': 24,
                'right_upper_leg': 25, 'right_lower_leg': 26, 'right_foot': 27
            }
            bone_positions = {}
            for bone_name, bone_id in bone_indices.items():
                try:
                    x = pm.read_float(bone_matrix + bone_id * 0x20)
                    y = pm.read_float(bone_matrix + bone_id * 0x20 + 0x4)
                    z = pm.read_float(bone_matrix + bone_id * 0x20 + 0x8)
                    screen_pos = w2s(view_matrix, x, y, z, globals.GAME_WIDTH, globals.GAME_HEIGHT, globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT)
                    bone_positions[bone_name] = None if screen_pos[0] < 0 or screen_pos[1] < 0 else screen_pos
                except Exception:
                    bone_positions[bone_name] = None
            head_pos = bone_positions.get('head')
            if head_pos:
                leg_pos = bone_positions.get('left_foot') or bone_positions.get('right_foot') or bone_positions.get('pelvis')
                if leg_pos:
                    head_topZ = pm.read_float(bone_matrix + 6 * 0x20 + 0x8) + 8.0
                    headX = pm.read_float(bone_matrix + 6 * 0x20)
                    headY = pm.read_float(bone_matrix + 6 * 0x20 + 0x4)
                    top_pos = w2s(view_matrix, headX, headY, head_topZ, globals.GAME_WIDTH, globals.GAME_HEIGHT, globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT)
                    if top_pos[0] > 0 and top_pos[1] > 0 and leg_pos[0] > 0 and leg_pos[1] > 0:
                        delta = abs(top_pos[1] - leg_pos[1])
                        if delta > 10:
                            leftX = top_pos[0] - delta // 3
                            rightX = top_pos[0] + delta // 3
                            center_x = (leftX + rightX) / 2
                            y_offset = top_pos[1] - 10
                            if esp_names_enabled:
                                try:
                                    entity_name_address = pm.read_longlong(entity_controller + globals.m_sSanitizedPlayerName)
                                    if entity_name_address:
                                        entity_name = pm.read_string(entity_name_address, 64)
                                        sanitized_name = ''.join(c for c in entity_name if c.isprintable())
                                        if sanitized_name:
                                            if globals.name_font:
                                                imgui.push_font(globals.name_font)
                                            name_size = imgui.calc_text_size(sanitized_name)
                                            x = center_x - name_size.x / 2
                                            y = y_offset - name_size.y
                                            draw_list.add_text(x, y, name_color, sanitized_name)
                                            if globals.name_font:
                                                imgui.pop_font()
                                            y_offset = y
                                except Exception:
                                    pass
                            if esp_hp_enabled:
                                try:
                                    entity_hp = pm.read_int(entity + globals.m_iHealth)
                                    hp_str = str(entity_hp)
                                    if globals.hp_font:
                                        imgui.push_font(globals.hp_font)
                                    hp_size = imgui.calc_text_size(hp_str)
                                    x = center_x - hp_size.x / 2
                                    y = y_offset - hp_size.y
                                    draw_list.add_text(x, y, hp_color, hp_str)
                                    if globals.hp_font:
                                        imgui.pop_font()
                                except Exception:
                                    pass
                if esp_head_circle_enabled:
                    try:
                        leg_pos = bone_positions.get('left_foot') or bone_positions.get('right_foot') or bone_positions.get('pelvis')
                        if leg_pos:
                            delta = abs(head_pos[1] - leg_pos[1])
                            radius = max(4.0, delta * 0.1)
                            try:
                                draw_list.add_circle_filled(head_pos[0], head_pos[1], radius, head_color_u32)
                            except Exception:
                                draw_list.add_circle(head_pos[0], head_pos[1], radius, head_color_u32, thickness=2.0)
                    except Exception:
                        pass
                    leg_pos = bone_positions.get('left_foot') or bone_positions.get('right_foot') or bone_positions.get('pelvis')
                    if leg_pos:
                        delta = abs(head_pos[1] - leg_pos[1])
                        radius = delta * 0.1
                        draw_list.add_circle(head_pos[0], head_pos[1], radius, skeleton_color_u32, thickness=2.0)
                if esp_hitbox_enabled:
                    leg_pos = bone_positions.get('left_foot') or bone_positions.get('right_foot') or bone_positions.get('pelvis')
                    if leg_pos:
                        head_topZ = pm.read_float(bone_matrix + 6 * 0x20 + 0x8) + 8.0
                        headX = pm.read_float(bone_matrix + 6 * 0x20)
                        headY = pm.read_float(bone_matrix + 6 * 0x20 + 0x4)
                        top_pos = w2s(view_matrix, headX, headY, head_topZ, globals.GAME_WIDTH, globals.GAME_HEIGHT, globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT)
                        if leg_pos and top_pos[0] > 0 and top_pos[1] > 0 and leg_pos[0] > 0 and leg_pos[1] > 0:
                            delta = abs(top_pos[1] - leg_pos[1])
                            if delta > 10:
                                leftX = top_pos[0] - delta // 3
                                rightX = top_pos[0] + delta // 3
                                draw_list.add_line(leftX, leg_pos[1], rightX, leg_pos[1], line_color, 2.0)
                                draw_list.add_line(leftX, leg_pos[1], leftX, top_pos[1], line_color, 2.0)
                                draw_list.add_line(rightX, leg_pos[1], rightX, top_pos[1], line_color, 2.0)
                                draw_list.add_line(leftX, top_pos[1], rightX, top_pos[1], line_color, 2.0)
                if esp_skeleton_enabled:
                    connections = [
                        ('head', 'neck'), ('neck', 'spine_3'), ('spine_3', 'spine_2'), ('spine_2', 'spine_1'),
                        ('spine_1', 'spine_0'), ('spine_0', 'pelvis'), ('neck', 'left_clavicle'),
                        ('left_clavicle', 'left_upper_arm'), ('left_upper_arm', 'left_lower_arm'),
                        ('left_lower_arm', 'left_hand'), ('neck', 'right_clavicle'), ('right_clavicle', 'right_upper_arm'),
                        ('right_upper_arm', 'right_lower_arm'), ('right_lower_arm', 'right_hand'),
                        ('pelvis', 'left_upper_leg'), ('left_upper_leg', 'left_lower_leg'), ('left_lower_leg', 'left_foot'),
                        ('pelvis', 'right_upper_leg'), ('right_upper_leg', 'right_lower_leg'), ('right_lower_leg', 'right_foot')
                    ]
                    for start_bone, end_bone in connections:
                        start_pos = bone_positions.get(start_bone)
                        end_pos = bone_positions.get(end_bone)
                        if start_pos and end_pos:
                            draw_list.add_line(start_pos[0], start_pos[1], end_pos[0], end_pos[1], skeleton_color_u32, 2.0)
        except Exception:
            continue
    return True