# main.py
# -*- coding: utf-8 -*-
import pymem
import win32gui, win32con
import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
import OpenGL.GL as gl
import keyboard
import time
import threading
import sys
import ctypes
import os
import multiprocessing

import globals
from load_config import load_config
from save_config import save_config
from load_fonts import load_fonts
from show_cheat_menu import show_cheat_menu
from capture_key import capture_key
from esp import esp
from anti_flash_logic import anti_flash_logic
from multiprocessing import freeze_support
freeze_support()

def main():
    # Підключення до процесу
    while True:
        try:
            globals.pm = pymem.Pymem("cs2.exe")
            globals.client = pymem.process.module_from_name(globals.pm.process_handle, "client.dll").lpBaseOfDll
            print("CS2.exe запущено")
            break
        except Exception:
            print("Запускай понос2  40rt  8===∍▄█▀█●")
            time.sleep(5)
    time.sleep(1)
    # Ховаємо консоль тільки після підключення
    if os.name == 'nt':
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    # Ініціалізація вікна/ImGui
    if not glfw.init():
        print("glfw піздейшн")
        return
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, glfw.TRUE)
    window = glfw.create_window(globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT, "overlay", None, None)
    if not window:
        print("glfw пізда")
        return
    hwnd = glfw.get_win32_window(window)
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    style &= ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME)
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
    ex_style = win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, -2, -2, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
    glfw.make_context_current(window)
    imgui.create_context()
    io = imgui.get_io()
    impl = GlfwRenderer(window)
    # Завантаження конфігів
    config = load_config()
    if config:
        display_allies = config.get("display_allies", False)
        globals.anti_flash = config.get("anti_flash", True)
        esp_enabled = config.get("esp_enabled", True)
        esp_skeleton_enabled = config.get("esp_skeleton_enabled", True)
        esp_hp_enabled = config.get("esp_hp_enabled", True)
        esp_names_enabled = config.get("esp_names_enabled", True)
        esp_hitbox_enabled = config.get("esp_hitbox_enabled", True)
        esp_head_circle_enabled = config.get("esp_head_circle_enabled", True)
        menu_key = config.get("menu_key", "f1")
        enemy_skeleton_color = config.get("enemy_skeleton_color", [1.0, 1.0, 1.0, 1.0])
        teammate_skeleton_color = config.get("teammate_skeleton_color", [1.0, 1.0, 1.0, 1.0])
        enemy_head_color = config.get("enemy_head_color", [1.0, 1.0, 1.0, 1.0])
        teammate_head_color = config.get("teammate_head_color", [1.0, 1.0, 1.0, 1.0])
        enemy_name_color = config.get("enemy_name_color", [1.0, 1.0, 1.0, 1.0])
        teammate_name_color = config.get("teammate_name_color", [1.0, 1.0, 1.0, 1.0])
        enemy_hp_color = config.get("enemy_hp_color", [1.0, 1.0, 1.0, 1.0])
        teammate_hp_color = config.get("teammate_hp_color", [1.0, 1.0, 1.0, 1.0])
        enemy_hitbox_color = config.get("enemy_hitbox_color", [1.0, 1.0, 1.0, 1.0])
        teammate_hitbox_color = config.get("teammate_hitbox_color", [1.0, 1.0, 1.0, 1.0])
        name_font_size = config.get("name_font_size", 13.0)
        hp_font_size = config.get("hp_font_size", 14.0)
        globals.aimbot_enabled = config.get("aimbot_enabled", False)
        globals.ignore_team = config.get("ignore_team", True)
        globals.use_fov_circle = config.get("use_fov_circle", True)
        globals.FOV_RADIUS = config.get("fov_radius", 150)
        globals.aimbot_key = config.get("aimbot_key", "alt")
    else:
        display_allies = False
        globals.anti_flash = True
        esp_enabled = True
        esp_skeleton_enabled = True
        esp_hp_enabled = True
        esp_names_enabled = True
        esp_hitbox_enabled = True
        esp_head_circle_enabled = True
        menu_key = "f1"
        enemy_skeleton_color = [1.0, 1.0, 1.0, 1.0]
        teammate_skeleton_color = [1.0, 1.0, 1.0, 1.0]
        enemy_head_color = [1.0, 1.0, 1.0, 1.0]
        teammate_head_color = [1.0, 1.0, 1.0, 1.0]
        enemy_name_color = [1.0, 1.0, 1.0, 1.0]
        teammate_name_color = [1.0, 1.0, 1.0, 1.0]
        enemy_hp_color = [1.0, 1.0, 1.0, 1.0]
        teammate_hp_color = [1.0, 1.0, 1.0, 1.0]
        enemy_hitbox_color = [1.0, 1.0, 1.0, 1.0]
        teammate_hitbox_color = [1.0, 1.0, 1.0, 1.0]
        name_font_size = 13.0
        hp_font_size = 14.0
        globals.aimbot_enabled = False
        globals.ignore_team = True
        globals.use_fov_circle = True
        globals.FOV_RADIUS = 150
        globals.aimbot_key = "alt"
    load_fonts(io, impl, name_font_size, hp_font_size)
    show_menu = False
    waiting_for_menu_key = False
    waiting_for_aimbot_key = False
    last_ins_state = False
    need_font_reload = False
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()
    shared_dict['aimbot_enabled'] = globals.aimbot_enabled
    shared_dict['ignore_team'] = globals.ignore_team
    shared_dict['use_fov_circle'] = globals.use_fov_circle
    shared_dict['FOV_RADIUS'] = globals.FOV_RADIUS
    shared_dict['aimbot_key'] = globals.aimbot_key
    from aimbot import aimbot_process
    p = multiprocessing.Process(target=aimbot_process, args=(shared_dict,))
    p.daemon = True
    p.start()
    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()
        anti_flash_logic(globals.pm, globals.client, globals.anti_flash)
        imgui.new_frame()
        # Обробка переназначення клавіші меню
        if waiting_for_menu_key:
            new_key = capture_key()
            if new_key:
                menu_key = new_key
                waiting_for_menu_key = False
                save_config(esp_enabled, esp_skeleton_enabled, esp_hp_enabled, esp_names_enabled, esp_hitbox_enabled, esp_head_circle_enabled, display_allies, globals.anti_flash, menu_key, enemy_skeleton_color, teammate_skeleton_color, enemy_head_color, teammate_head_color, enemy_name_color, teammate_name_color, enemy_hp_color, teammate_hp_color, enemy_hitbox_color, teammate_hitbox_color, name_font_size, hp_font_size, globals.aimbot_enabled, globals.ignore_team, globals.use_fov_circle, globals.FOV_RADIUS, globals.aimbot_key)
        # Обробка переназначення клавіші аімбота
        if waiting_for_aimbot_key:
            new_key = capture_key()
            if new_key:
                globals.aimbot_key = new_key
                shared_dict['aimbot_key'] = globals.aimbot_key
                waiting_for_aimbot_key = False
                save_config(esp_enabled, esp_skeleton_enabled, esp_hp_enabled, esp_names_enabled, esp_hitbox_enabled, esp_head_circle_enabled, display_allies, globals.anti_flash, menu_key, enemy_skeleton_color, teammate_skeleton_color, enemy_head_color, teammate_head_color, enemy_name_color, teammate_name_color, enemy_hp_color, teammate_hp_color, enemy_hitbox_color, teammate_hitbox_color, name_font_size, hp_font_size, globals.aimbot_enabled, globals.ignore_team, globals.use_fov_circle, globals.FOV_RADIUS, globals.aimbot_key)
        try:
            current_ins = keyboard.is_pressed(menu_key)
        except Exception:
            current_ins = False
        if current_ins and not last_ins_state and not waiting_for_menu_key and not waiting_for_aimbot_key:
            show_menu = not show_menu
        last_ins_state = current_ins
        # Динамічне перемикання прозорості вікна
        try:
            current_ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            if show_menu:
                new_ex_style = current_ex_style & ~win32con.WS_EX_TRANSPARENT
            else:
                new_ex_style = current_ex_style | win32con.WS_EX_TRANSPARENT
            if new_ex_style != current_ex_style:
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_ex_style)
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, -2, -2, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_SHOWWINDOW)
        except Exception:
            pass
        prev_name_font_size = name_font_size
        prev_hp_font_size = hp_font_size
        # Якщо меню показане — відобразити елементи управління
        if show_menu:
            (esp_enabled, esp_skeleton_enabled, esp_hp_enabled, esp_names_enabled, esp_hitbox_enabled, esp_head_circle_enabled, display_allies, globals.anti_flash, menu_key, show_menu, waiting_for_menu_key, enemy_skeleton_color, teammate_skeleton_color, enemy_head_color, teammate_head_color, enemy_name_color, teammate_name_color, enemy_hp_color, teammate_hp_color, enemy_hitbox_color, teammate_hitbox_color, name_font_size, hp_font_size, globals.aimbot_enabled, globals.ignore_team, globals.use_fov_circle, globals.FOV_RADIUS, globals.aimbot_key, waiting_for_aimbot_key) = show_cheat_menu(
                esp_enabled, esp_skeleton_enabled, esp_hp_enabled, esp_names_enabled, esp_hitbox_enabled, esp_head_circle_enabled, display_allies, globals.anti_flash, menu_key, show_menu, waiting_for_menu_key, enemy_skeleton_color, teammate_skeleton_color, enemy_head_color, teammate_head_color, enemy_name_color, teammate_name_color, enemy_hp_color, teammate_hp_color, enemy_hitbox_color, teammate_hitbox_color, name_font_size, hp_font_size, globals.aimbot_enabled, globals.ignore_team, globals.use_fov_circle, globals.FOV_RADIUS, globals.aimbot_key, waiting_for_aimbot_key
            )
            shared_dict['aimbot_enabled'] = globals.aimbot_enabled
            shared_dict['ignore_team'] = globals.ignore_team
            shared_dict['use_fov_circle'] = globals.use_fov_circle
            shared_dict['FOV_RADIUS'] = globals.FOV_RADIUS
            shared_dict['aimbot_key'] = globals.aimbot_key
            save_config(esp_enabled, esp_skeleton_enabled, esp_hp_enabled, esp_names_enabled, esp_hitbox_enabled, esp_head_circle_enabled, display_allies, globals.anti_flash, menu_key, enemy_skeleton_color, teammate_skeleton_color, enemy_head_color, teammate_head_color, enemy_name_color, teammate_name_color, enemy_hp_color, teammate_hp_color, enemy_hitbox_color, teammate_hitbox_color, name_font_size, hp_font_size, globals.aimbot_enabled, globals.ignore_team, globals.use_fov_circle, globals.FOV_RADIUS, globals.aimbot_key)
        if name_font_size != prev_name_font_size or hp_font_size != prev_hp_font_size:
            need_font_reload = True
        imgui.set_next_window_size(globals.WINDOW_WIDTH, globals.WINDOW_HEIGHT)
        imgui.set_next_window_position(0, 0)
        imgui.begin("overlay", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_BACKGROUND)
        draw_list = imgui.get_window_draw_list()
        if not esp(draw_list, display_allies, globals.pm, globals.client, esp_enabled, esp_skeleton_enabled, esp_hp_enabled, esp_names_enabled, esp_hitbox_enabled, esp_head_circle_enabled, enemy_skeleton_color, teammate_skeleton_color, enemy_head_color, teammate_head_color, enemy_name_color, teammate_name_color, enemy_hp_color, teammate_hp_color, enemy_hitbox_color, teammate_hitbox_color):
            break
        if globals.aimbot_enabled and globals.use_fov_circle:
            center_x = globals.WINDOW_WIDTH / 2
            center_y = globals.WINDOW_HEIGHT / 2
            fov_color = imgui.get_color_u32_rgba(1.0, 1.0, 1.0, 0.5) # Білий напівпрозорий
            draw_list.add_circle(center_x, center_y, globals.FOV_RADIUS, fov_color, thickness=1.0)
        imgui.end()
        imgui.end_frame()
        gl.glClearColor(0, 0, 0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)
        if need_font_reload:
            load_fonts(io, impl, name_font_size, hp_font_size)
            need_font_reload = False
    save_config(esp_enabled, esp_skeleton_enabled, esp_hp_enabled, esp_names_enabled, esp_hitbox_enabled, esp_head_circle_enabled, display_allies, globals.anti_flash, menu_key, enemy_skeleton_color, teammate_skeleton_color, enemy_head_color, teammate_head_color, enemy_name_color, teammate_name_color, enemy_hp_color, teammate_hp_color, enemy_hitbox_color, teammate_hitbox_color, name_font_size, hp_font_size, globals.aimbot_enabled, globals.ignore_team, globals.use_fov_circle, globals.FOV_RADIUS, globals.aimbot_key)
    impl.shutdown()
    glfw.terminate()
    p.terminate()
    sys.exit(0)

if __name__ == '__main__':
    main()
