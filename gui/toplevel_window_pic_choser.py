import customtkinter as ctk
from tkinter import filedialog
import json

with open("gui/colors.json") as f:
    colors_data = json.load(f)

COLORS = colors_data.get("COLORS", {})
FONT = "Century Gothic"

class ToplevelWindowPicChoser(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.create_widgets()
        self.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.title("Wybór zdjęcia")

    def on_close(self):
        self.destroy()

    def create_widgets(self):
        label = ctk.CTkLabel(
            self,
            text="Wybierz plik ze zdjęciem równania",
            bg_color=COLORS["BACKGROUND_COLOR"],
            fg_color=COLORS["BACKGROUND_COLOR"],
            corner_radius=10,
            text_color=COLORS["BLACK"],
            font=(FONT, 20)
        )
        label.place(relx=0.22, rely=0.1)

        load_button = ctk.CTkButton(
            self,
            text="Wczytaj plik",
            command=self.load_file,
            corner_radius=10,
            bg_color=COLORS["BACKGROUND_COLOR"],
        )
        load_button.place(relx=0.32, rely=0.3)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Wybierz plik",
            filetypes=[("Pliki obrazów", "*.png;*.jpg;*.jpeg;")],
        )
        if file_path:
            print(f"Wczytano plik: {file_path}")
