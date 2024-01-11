import json
import tkinter

import customtkinter as ctk

from options.translator import Translator

with open("gui/colors.json") as f:
    colors_data = json.load(f)

COLORS = colors_data.get("COLORS", {})
FONT = "Century Gothic"


class TopLevelSolidType(ctk.CTkToplevel):
    def __init__(self, language_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("210x220")
        self.language_manager = language_manager
        self.translator = Translator(self.language_manager)
        self.create_widgets()
        self.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.title("Wybór typu btyły")
        self.selected_option = None
        self.grab_set()
        self.selected_option = None

    def on_close(self):
        self.destroy()

    def create_radio_button(self, text, value, x, y):
        radio_button = ctk.CTkRadioButton(
            self,
            text=text,
            value=value,
            variable=self.radio_var,
            text_color=COLORS["BLACK"],
        )
        radio_button.place(relx=x, rely=y)
        return radio_button

    def create_widgets(self):
        self.radio_var = tkinter.IntVar(value=0)
        text = "walec"
        translated_text = self.translator.translate(text)
        self.create_radio_button(translated_text, 1, 0.27, 0.20)

        text = "stozek"
        translated_text = self.translator.translate(text)
        self.create_radio_button(translated_text, 2, 0.27, 0.33)

        text = "prostopadloscian"
        translated_text = self.translator.translate(text)
        self.create_radio_button(translated_text, 3, 0.27, 0.46)

        text = "pierscien"
        translated_text = self.translator.translate(text)
        self.create_radio_button(translated_text, 4, 0.27, 0.59)

        load_button = ctk.CTkButton(
            self,
            text=">>>",
            command=self.set_value,
            corner_radius=10,
            bg_color=COLORS["BACKGROUND_COLOR"],
            fg_color=COLORS["MAIN_BUTTONS_COLOR"],
            width=100,
        )
        load_button.place(relx=0.60, rely=0.8)

    def set_value(self):
        self.selected_option = self.radio_var.get()
        self.destroy()

    def get_type(self):
        return self.selected_option
