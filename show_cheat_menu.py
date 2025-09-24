# show_cheat_menu.py
# -*- coding: utf-8 -*-
import imgui
from imgui_color_edit4_compat import imgui_color_edit4_compat

def show_cheat_menu(
    esp_enabled,
    esp_skeleton_enabled,
    esp_hp_enabled,
    esp_names_enabled,
    esp_hitbox_enabled,
    esp_head_circle_enabled,
    display_allies,
    anti_flash,
    menu_key,
    show_menu,
    waiting_for_menu_key,
    enemy_skeleton_color,
    teammate_skeleton_color,
    enemy_head_color,
    teammate_head_color,
    enemy_name_color,
    teammate_name_color,
    enemy_hp_color,
    teammate_hp_color,
    enemy_hitbox_color,
    teammate_hitbox_color,
    name_font_size,
    hp_font_size,
    aimbot_enabled,
    ignore_team,
    use_fov_circle,
    FOV_RADIUS,
    aimbot_key,
    waiting_for_aimbot_key
):
    _, show_menu = imgui.begin("Меню чита", show_menu, flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_COLLAPSE)
    _, esp_enabled = imgui.checkbox("ESP (загальний)", esp_enabled)
    _, esp_skeleton_enabled = imgui.checkbox("Кістки гравців", esp_skeleton_enabled)
    if esp_skeleton_enabled:
        imgui.text("Колір скелету ворогів:")
        changed, new_enemy = imgui_color_edit4_compat("##enemy_skeleton_color", enemy_skeleton_color)
        if changed:
            enemy_skeleton_color[0:4] = new_enemy[0:4]
        imgui.text("Колір скелету союзників:")
        changed, new_team = imgui_color_edit4_compat("##teammate_skeleton_color", teammate_skeleton_color)
        if changed:
            teammate_skeleton_color[0:4] = new_team[0:4]
    _, esp_head_circle_enabled = imgui.checkbox("Показувати голову", esp_head_circle_enabled)
    if esp_head_circle_enabled:
        imgui.text("Колір голови ворогів:")
        changed, new_enemy_head = imgui_color_edit4_compat("##enemy_head_color", enemy_head_color)
        if changed:
            enemy_head_color[0:4] = new_enemy_head[0:4]
        imgui.text("Колір голови союзників:")
        changed, new_team_head = imgui_color_edit4_compat("##teammate_head_color", teammate_head_color)
        if changed:
            teammate_head_color[0:4] = new_team_head[0:4]
    _, esp_names_enabled = imgui.checkbox("Показувати імена гравців", esp_names_enabled)
    if esp_names_enabled:
        imgui.text("Колір імен ворогів:")
        changed, new_enemy_name = imgui_color_edit4_compat("##enemy_name_color", enemy_name_color)
        if changed:
            enemy_name_color[0:4] = new_enemy_name[0:4]
        imgui.text("Колір імен союзників:")
        changed, new_team_name = imgui_color_edit4_compat("##teammate_name_color", teammate_name_color)
        if changed:
            teammate_name_color[0:4] = new_team_name[0:4]
       
        _, name_font_size = imgui.slider_float("Розмір шрифту імен", name_font_size, 8.0, 30.0)
    _, esp_hp_enabled = imgui.checkbox("Показувати HP", esp_hp_enabled)
    if esp_hp_enabled:
        imgui.text("Колір HP ворогів:")
        changed, new_enemy_hp = imgui_color_edit4_compat("##enemy_hp_color", enemy_hp_color)
        if changed:
            enemy_hp_color[0:4] = new_enemy_hp[0:4]
        imgui.text("Колір HP союзників:")
        changed, new_team_hp = imgui_color_edit4_compat("##teammate_hp_color", teammate_hp_color)
        if changed:
            teammate_hp_color[0:4] = new_team_hp[0:4]
       
        _, hp_font_size = imgui.slider_float("Розмір шрифту HP", hp_font_size, 8.0, 30.0)
    _, esp_hitbox_enabled = imgui.checkbox("Показувати хітбокс", esp_hitbox_enabled)
    if esp_hitbox_enabled:
        imgui.text("Колір хітбоксу ворогів:")
        changed, new_enemy_hitbox = imgui_color_edit4_compat("##enemy_hitbox_color", enemy_hitbox_color)
        if changed:
            enemy_hitbox_color[0:4] = new_enemy_hitbox[0:4]
        imgui.text("Колір хітбоксу союзників:")
        changed, new_team_hitbox = imgui_color_edit4_compat("##teammate_hitbox_color", teammate_hitbox_color)
        if changed:
            teammate_hitbox_color[0:4] = new_team_hitbox[0:4]
    _, display_allies = imgui.checkbox("Відображати союзників", display_allies)
    _, anti_flash = imgui.checkbox("Анти-флеш", anti_flash)
    _, aimbot_enabled = imgui.checkbox("Аімбот", aimbot_enabled)
    if aimbot_enabled:
        _, ignore_team = imgui.checkbox("Аімбот союзників", ignore_team)
        _, use_fov_circle = imgui.checkbox("Включити FOV", use_fov_circle)
        if use_fov_circle:
            _, FOV_RADIUS = imgui.slider_int("FOV радіус", FOV_RADIUS, 50, 500)
        imgui.text(f"Поточна клавіша аімбота: {aimbot_key}")
        if waiting_for_aimbot_key:
            imgui.text("Натисніть будь-яку клавішу для аімбота")
        else:
            if imgui.button("Призначити клавішу аімбота"):
                waiting_for_aimbot_key = True
    imgui.text(f"Поточна клавіша меню: {menu_key}")
    if waiting_for_menu_key:
        imgui.text("Натисніть будь-яку клавішу")
    else:
        if imgui.button("Призначити нову клавішу"):
            waiting_for_menu_key = True
    imgui.end()
    return (
        esp_enabled,
        esp_skeleton_enabled,
        esp_hp_enabled,
        esp_names_enabled,
        esp_hitbox_enabled,
        esp_head_circle_enabled,
        display_allies,
        anti_flash,
        menu_key,
        show_menu,
        waiting_for_menu_key,
        enemy_skeleton_color,
        teammate_skeleton_color,
        enemy_head_color,
        teammate_head_color,
        enemy_name_color,
        teammate_name_color,
        enemy_hp_color,
        teammate_hp_color,
        enemy_hitbox_color,
        teammate_hitbox_color,
        name_font_size,
        hp_font_size,
        aimbot_enabled,
        ignore_team,
        use_fov_circle,
        FOV_RADIUS,
        aimbot_key,
        waiting_for_aimbot_key
    )