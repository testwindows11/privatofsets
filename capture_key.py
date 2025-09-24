# capture_key.py
# -*- coding: utf-8 -*-
import keyboard
def capture_key():
    try:
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN:
            return event.name
    except Exception:
        pass
    return None