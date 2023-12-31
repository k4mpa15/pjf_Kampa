import customtkinter as ctk
import json
from options.equations_history import EquationHistory

with open("gui/colors.json") as f:
    colors_data = json.load(f)

COLORS = colors_data.get("COLORS", {})
FONT = "Century Gothic"


class TopLevelHistory(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x500")
        self.equation_history = EquationHistory()
        self.create_widgets()
        self.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.title("Historia")
        self.resizable(False, True)

    def create_widgets(self):
        label = ctk.CTkLabel(
            self,
            text="Historia",
            bg_color=COLORS["BACKGROUND_COLOR"],
            fg_color=COLORS["BACKGROUND_COLOR"],
            corner_radius=10,
            text_color=COLORS["MAIN_BUTTONS_COLOR"],font=(FONT, 20)
        )
        label.place(relx=0.42, rely=0.1)

        history_text = self.equation_history.get_history()
        label_content = ctk.CTkLabel(
            self,
            text=history_text,
            bg_color=COLORS["BACKGROUND_COLOR"],
            fg_color=COLORS["BACKGROUND_COLOR"],
            corner_radius=10,
            text_color=COLORS["BLACK"],
            font=(FONT, 14),
            width= 600,
            height=300
        )
        label_content.place(relx=0.014, rely=0.23)