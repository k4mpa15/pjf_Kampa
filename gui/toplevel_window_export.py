import customtkinter as ctk
from tkinter import filedialog
import json
from options.file_exporter import FileExporter
import tkinter

with open("gui/colors.json") as f:
    colors_data = json.load(f)

COLORS = colors_data.get("COLORS", {})


class TopLevelExport(ctk.CTkToplevel):
    def __init__(self, result, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.create_widgets()
        self.file_exporter = FileExporter()
        self.resizable(True, True)
        self.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.title("Wybór rozszerzenia pliku")
        self.result = result
        self.selected_option = None

    def on_close(self):
        self.destroy()

    def create_widgets(self):
        label = ctk.CTkLabel(
            self,
            text="Wybierz rozszerzenie pliku",
            bg_color=COLORS["BACKGROUND_COLOR"],
            fg_color=COLORS["BACKGROUND_COLOR"],
            corner_radius=10,
            text_color=COLORS["BLACK"],
        )
        label.place(relx=0.26, rely=0.1)

        load_button = ctk.CTkButton(
            self,
            text="Eksportuj",
            command=self.export,
            corner_radius=10,
            bg_color=COLORS["BACKGROUND_COLOR"],
        )
        load_button.place(relx=0.32, rely=0.7)

        self.radio_var = tkinter.IntVar(value=0)

        self.radiobutton_tex = ctk.CTkRadioButton(
            self,
            text=".tex",
            value=1,
            variable=self.radio_var,
            text_color=COLORS["BLACK"],
        )
        self.radiobutton_tex.place(relx=0.25, rely=0.3)

        self.radiobutton_xlsx = ctk.CTkRadioButton(
            self,
            text=".xlsx",
            value=2,
            variable=self.radio_var,
            text_color=COLORS["BLACK"],
        )
        self.radiobutton_xlsx.place(relx=0.25, rely=0.4)

    def export(self):
        if self.radio_var.get() == 1:
            self.file_exporter.export_to_latex(self.result)
        elif self.radio_var.get() == 2:
            self.file_exporter.export_to_excel(self.result)

        self.show_message()

    def show_message(self):
        self.after(1000, self.show_info)

    def show_info(self):
        tkinter.messagebox.showinfo(
            "Export files", "Eksport do pliku wykonany pomyślnie."
        )
