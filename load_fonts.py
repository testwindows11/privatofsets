# load_fonts.py
# -*- coding: utf-8 -*-
import globals
def load_fonts(io, impl, name_font_size, hp_font_size):
    font_path = "C:\\Windows\\Fonts\\arial.ttf"
    io.fonts.clear()
    try:
        globals.default_font = io.fonts.add_font_from_file_ttf(font_path, 13.0, glyph_ranges=io.fonts.get_glyph_ranges_cyrillic())
        globals.name_font = io.fonts.add_font_from_file_ttf(font_path, name_font_size, glyph_ranges=io.fonts.get_glyph_ranges_cyrillic())
        globals.hp_font = io.fonts.add_font_from_file_ttf(font_path, hp_font_size, glyph_ranges=io.fonts.get_glyph_ranges_cyrillic())
    except Exception:
        globals.default_font = None
        globals.name_font = None
        globals.hp_font = None
    impl.refresh_font_texture()