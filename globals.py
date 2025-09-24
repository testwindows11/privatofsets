# globals.py
# -*- coding: utf-8 -*-
import os
import json
import math  # Додано для глобального використання, якщо потрібно; інакше імпортуйте в файлах функцій

if os.name == 'nt':
    os.system('chcp 65001 > nul')

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
GAME_WIDTH = 1440
GAME_HEIGHT = 1080
CONFIG_FILE = "config.json"

# Завантаження офсетів
with open('offsets.json', 'r', encoding='utf-8') as f:
    offsets = json.load(f)
with open('client_dll.json', 'r', encoding='utf-8') as f:
    client_dll = json.load(f)

# Оффсети/поля
try:
    dwEntityList = offsets['client.dll']['dwEntityList']
    dwLocalPlayerPawn = offsets['client.dll']['dwLocalPlayerPawn']
    dwViewMatrix = offsets['client.dll']['dwViewMatrix']
    m_iTeamNum = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_iTeamNum']
    m_lifeState = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_lifeState']
    m_pGameSceneNode = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_pGameSceneNode']
    m_modelState = client_dll['client.dll']['classes']['CSkeletonInstance']['fields']['m_modelState']
    m_hPlayerPawn = client_dll['client.dll']['classes']['CCSPlayerController']['fields']['m_hPlayerPawn']
    m_iHealth = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_iHealth']
    m_flFlashMaxAlpha = client_dll['client.dll']['classes']['C_CSPlayerPawnBase']['fields']['m_flFlashMaxAlpha']
    m_sSanitizedPlayerName = client_dll['client.dll']['classes']['CCSPlayerController']['fields']['m_sSanitizedPlayerName']
    dwViewAngles = offsets['client.dll']['dwViewAngles'] if 'dwViewAngles' in offsets['client.dll'] else 0x1A78650
    m_vecViewOffset = client_dll['client.dll']['classes']['C_BaseModelEntity']['fields']['m_vecViewOffset']
    vec_abs_origin = 0xD0  # Офсет для позиції
except Exception as e:
    print("Помилка завантаження offsets/client_dll:", e)
    raise

pm = None
client = None
anti_flash = True
default_font = None
name_font = None
hp_font = None
aimbot_enabled = False
ignore_team = True
use_fov_circle = True
FOV_RADIUS = 150
aimbot_key = 'alt'