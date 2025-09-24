# imgui_color_edit4_compat.py
# -*- coding: utf-8 -*-
import imgui
def imgui_color_edit4_compat(label, color_list):
    try:
        res = imgui.color_edit4(label, *color_list, flags=imgui.COLOR_EDIT_ALPHA_BAR | imgui.COLOR_EDIT_ALPHA_PREVIEW)
        if isinstance(res, tuple):
            if len(res) == 2:
                changed, new = res
                if isinstance(new, (list, tuple)) and len(new) >= 4:
                    return bool(changed), [float(new[0]), float(new[1]), float(new[2]), float(new[3])]
            elif len(res) >= 5:
                changed = res[0]
                return bool(changed), [float(res[1]), float(res[2]), float(res[3]), float(res[4])]
    except Exception:
        pass
    return False, list(color_list)