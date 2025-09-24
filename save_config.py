# save_config.py
# -*- coding: utf-8 -*-
import json
import globals

def save_config(esp_enabled, esp_skeleton_enabled, esp_hp_enabled, esp_names_enabled,
                esp_hitbox_enabled, esp_head_circle_enabled, display_allies, anti_flash_val,
                menu_key, enemy_skeleton_color, teammate_skeleton_color,
                enemy_head_color, teammate_head_color, enemy_name_color,
                teammate_name_color, enemy_hp_color, teammate_hp_color,
                enemy_hitbox_color, teammate_hitbox_color, name_font_size, hp_font_size,
                aimbot_enabled, ignore_team, use_fov_circle, FOV_RADIUS, aimbot_key):
    config = {
        "esp_enabled": esp_enabled,
        "esp_skeleton_enabled": esp_skeleton_enabled,
        "esp_hp_enabled": esp_hp_enabled,
        "esp_names_enabled": esp_names_enabled,
        "esp_hitbox_enabled": esp_hitbox_enabled,
        "esp_head_circle_enabled": esp_head_circle_enabled,
        "display_allies": display_allies,
        "anti_flash": anti_flash_val,
        "menu_key": menu_key,
        "enemy_skeleton_color": list(enemy_skeleton_color),
        "teammate_skeleton_color": list(teammate_skeleton_color),
        "enemy_head_color": list(enemy_head_color),
        "teammate_head_color": list(teammate_head_color),
        "enemy_name_color": list(enemy_name_color),
        "teammate_name_color": list(teammate_name_color),
        "enemy_hp_color": list(enemy_hp_color),
        "teammate_hp_color": list(teammate_hp_color),
        "enemy_hitbox_color": list(enemy_hitbox_color),
        "teammate_hitbox_color": list(teammate_hitbox_color),
        "name_font_size": name_font_size,
        "hp_font_size": hp_font_size,
        "aimbot_enabled": aimbot_enabled,
        "ignore_team": ignore_team,
        "use_fov_circle": use_fov_circle,
        "fov_radius": FOV_RADIUS,
        "aimbot_key": aimbot_key
    }
    try:
        with open(globals.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except PermissionError:
        print(f"[!] Немає доступу для запису {globals.CONFIG_FILE}. "
              f"Спробуй запустити від адміністратора")