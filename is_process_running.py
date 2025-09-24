# is_process_running.py
# -*- coding: utf-8 -*-
def is_process_running(pm, process_name):
    try:
        _ = pm.process_handle
        return True
    except Exception:
        return False