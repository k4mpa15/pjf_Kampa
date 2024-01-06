import json

import customtkinter as ctk

from options.equations_history import EquationHistory
from options.translator import Translator

with open("gui/colors.json") as f:
    colors_data = json.load(f)

COLORS = colors_data.get("COLORS", {})
FONT = "Century Gothic"


class TopLevelHistory(ctk.CTkToplevel):
    def __init__(self, language_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x500")
        self.language_manager = language_manager
        self.translator = Translator(self.language_manager)
        self.equation_history = EquationHistory(self.language_manager)
        self.create_widgets()
        self.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.title("Historia")
        self.resizable(False, True)
        self.grab_set()

    def clear_history(self):
        with open("eq_history.txt", "w"):
            pass
        self.create_widgets()

    def create_widgets(self):
        text = "history"
        translated_text = self.translator.translate(text)
        label = ctk.CTkLabel(
            self,
            text=translated_text,
            bg_color=COLORS["BACKGROUND_COLOR"],
            fg_color=COLORS["BACKGROUND_COLOR"],
            corner_radius=10,
            text_color=COLORS["MAIN_BUTTONS_COLOR"],
            font=(FONT, 20),
        )
        label.place(relx=0.42, rely=0.1)

        history_text = self.equation_history.get_history()
        scrollable_frame = ctk.CTkScrollableFrame(
            master=self,
            width=500,
            height=300,
            bg_color=COLORS["LIGHT_ENTRY_COLOR"],
            fg_color=COLORS["LIGHT_ENTRY_COLOR"],
        )
        scrollable_frame.place(relx=0.06, rely=0.23)

        ctk.CTkLabel(
            scrollable_frame,
            text=history_text,
            bg_color=COLORS["LIGHT_ENTRY_COLOR"],
            fg_color=COLORS["LIGHT_ENTRY_COLOR"],
            corner_radius=10,
            text_color=COLORS["BLACK"],
            font=(FONT, 14),
            width=600,
            height=300,
            anchor=ctk.W,
        ).pack(pady=10)
        text = "erase"
        translated_text = self.translator.translate(text)
        ctk.CTkButton(
            master=self,
            command=lambda: self.clear_history(),
            fg_color=COLORS["MAIN_BUTTONS_COLOR"],
            bg_color=COLORS["BACKGROUND_COLOR"],
            corner_radius=10,
            text=translated_text,
            width=50,
            font=(FONT, 14),
            height=25,
            text_color=COLORS["WHITE"],
            hover_color=COLORS["MAIN_BUTTONS_HOVER_COLOR"],
        ).place(relx=0.8, rely=0.01)
