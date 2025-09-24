# load_config.py
# -*- coding: utf-8 -*-
import os
import json
import globals

def load_config():
    if os.path.exists(globals.CONFIG_FILE):
        with open(globals.CONFIG_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return None
    return None