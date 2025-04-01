import flet as ft
from flet.core.border import Border

from utils.constantes import *

login_style: dict = dict(
    dense=True, height=45,
    focused_border_color=MAIN_COLOR,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="PPM", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="PPM"),
    text_style=ft.TextStyle(size=13, font_family="PPM"),
    border_radius=8, border_width=1, cursor_color="black",
    focused_border_width=2,
)

field_style: dict = dict(
    height=45,
    border_color="#f0f0f6", bgcolor="#f0f0f6",
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="PPM", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="PPM"),
    text_style=ft.TextStyle(size=13, font_family="PPM"),
    border_radius=8, border_width=1, cursor_color=SECONDARY_COLOR,
    # capitalization=ft.TextCapitalization.CHARACTERS
)
drop_style: dict = dict(
    border_radius=8,
    label_style=ft.TextStyle(size=12, font_family="PPM"),
    text_style=ft.TextStyle(size=12, font_family="PPM", color="black"),
    focused_border_color=MAIN_COLOR, border_width=1,
    focused_border_width=2,
)
field_style_2: dict = dict(
    height=45,
    focused_border_color=MAIN_COLOR,
    content_padding=16, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="PPM", color="black87"),
    hint_style=ft.TextStyle(size=12, font_family="PPM"),
    text_style=ft.TextStyle(size=13, font_family="PPM"),
    border_radius=8, border_width=1, cursor_color=SECONDARY_COLOR,
    focused_border_width=2,  # border=ft.InputBorder.UNDERLINE,
#     capitalization=ft.TextCapitalization.CHARACTERS
)
inactive_field_style: dict = dict(
    height=45, disabled=True,
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="PPM", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="PPM"),
    text_style=ft.TextStyle(size=12, font_family="PPM"),
    border_radius=8, border_width=1,
    capitalization=ft.TextCapitalization.CHARACTERS
)
underline_field_style: dict = dict(
    height=45, read_only=True,
    border_color="#f0f0f6", bgcolor="#f0f0f6",
    content_padding=12, cursor_height=24,
    label_style=ft.TextStyle(size=12, font_family="PPM", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="PPM"),
    text_style=ft.TextStyle(size=13, font_family="PPM"),
    border_radius=8, border_width=1, cursor_color=SECONDARY_COLOR,
    capitalization=ft.TextCapitalization.CHARACTERS
)

date_field_style: dict = dict(
    height=45,
    focused_border_width=2, focused_border_color=MAIN_COLOR,
    label_style=ft.TextStyle(size=12, font_family="PPM", color="black"),
    hint_style=ft.TextStyle(size=12, font_family="PPM"),
    text_style=ft.TextStyle(size=13, font_family="PPM"),
    border_radius=8, border_width=1, cursor_color=SECONDARY_COLOR,
    capitalization=ft.TextCapitalization.CHARACTERS
)
radio_style = dict(
    label_style=ft.TextStyle(size=12, font_family="PPM"),
    fill_color=SECONDARY_COLOR
)
text_title_style = dict(
    size=12, font_family="PPI", color="grey"
)