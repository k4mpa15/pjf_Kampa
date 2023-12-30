import customtkinter as ctk
import json
from PIL import Image

with open("gui/colors.json") as f:
    colors_data = json.load(f)

COLORS = colors_data.get("COLORS", {})


class TopLevelInstructions(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x500")
        self.create_widgets()
        self.resizable(True, True)
        self.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.title("Instrukcje")

    def on_close(self):
        self.destroy()

    def create_widgets(self):
        my_image = ctk.CTkImage(
            light_image=Image.open("gui\instructions.png"),
            dark_image=None,
            size=(600, 500),
        )

        image_label = ctk.CTkLabel(self, image=my_image, text="").place(
            relx=0.0, rely=0.0
        )
