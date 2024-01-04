import json
from tkinter import filedialog

import customtkinter as ctk

from options.translator import Translator

with open("gui/colors.json") as f:
    colors_data = json.load(f)

COLORS = colors_data.get("COLORS", {})
FONT = "Century Gothic"


class ToplevelWindowPicChoser(ctk.CTkToplevel):
    def __init__(self, language_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.language_manager = language_manager
        self.translator = Translator(self.language_manager)
        self.create_widgets()
        self.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.title("Wybór zdjęcia")
        self.grab_set()

    def on_close(self):
        self.destroy()

    def create_widgets(self):
        text = "choose_file"
        translated_text = self.translator.translate(text)
        label = ctk.CTkLabel(
            self,
            text=translated_text,
            bg_color=COLORS["BACKGROUND_COLOR"],
            fg_color=COLORS["BACKGROUND_COLOR"],
            corner_radius=10,
            text_color=COLORS["BLACK"],
            font=(FONT, 20),
        )
        label.place(relx=0.08, rely=0.1)

        text = "load_file"
        translated_text = self.translator.translate(text)
        load_button = ctk.CTkButton(
            self,
            text=translated_text,
            command=self.load_file,
            corner_radius=10,
            bg_color=COLORS["BACKGROUND_COLOR"],
        )
        load_button.place(relx=0.32, rely=0.3)

    def load_file(self):
        text = "load_file"
        translated_text = self.translator.translate(text)
        file_path = filedialog.askopenfilename(
            title=translated_text,
            filetypes=[("Pliki obrazów", "*.png;*.jpg;*.jpeg;")],
        )
        if file_path:
            print(f"Wczytano plik: {file_path}")
