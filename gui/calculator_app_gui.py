import customtkinter as ctk
import os
import webbrowser
from tkinter import *
from eq_solvers.common_eq_solv import EquationSolver
from gui.toplevel_window_pic_choser import ToplevelWindowPicChoser
from gui.toplevel_window_export import TopLevelExport
import json
from PIL import Image
from gui.toplevel_window_instructions import TopLevelInstructions

with open("gui/colors.json") as f:
    colors_data = json.load(f)

COLORS = colors_data.get("COLORS", {})
FONT = "Century Gothic"


class CalculatorApp(ctk.CTk):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Kalkulator równań")
        self.master.geometry("1000x600")
        self.master.resizable(True, True)
        self.master.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.toplevel_window_pic_choser = None
        self.toplevel_window_export = None
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.eq_entry = None
        self.equation_solver = EquationSolver()
        self.create_widgets()
        self.solution = None
        self.eq_type = None
        self.toplevel_window_instructions = None

    def on_close(self):
        if (
            self.toplevel_window_pic_choser is None
            or not self.toplevel_window_pic_choser.winfo_exists()
        ):
            pass
        else:
            self.toplevel_window_pic_choser.destroy()

        self.master.destroy()
        self.master.quit()

    def create_widgets(self):
        self.create_option_button(
            "Jak poprawnie wpisywać równania?",
            0.084,
            0.29,
            150,
            COLORS["BACKGROUND_COLOR"],
            COLORS["BACKGROUND_COLOR"],
            COLORS["BLACK"],
            COLORS["OPTION_BUTTON_HOVER_COLOR"],
            lambda: self.show_instrcutions(),
        )

        self.create_label(
            "Kalkulator równań",
            0.0,
            0.0,
            1000,
            90,
            (FONT, 28),
            COLORS["WHITE"],
            COLORS["BACKGROUND_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            5000,
            "w",
        )

        self.create_option_button(
            "PL EN",
            0.87,
            0.0,
            50,
            COLORS["MAIN_BUTTONS_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            COLORS["WHITE"],
            COLORS["OPTION_BUTTON_HOVER_COLOR"],
            None,
        )

        eq_types = [
            "Wybierz typ",
            "równanie liniowe",
            "układ równań liniowych",
            "równanie kwadratowe",
            "równanie nieliniowe"
        ]
        self.create_combobox(
            eq_types,
            250,
            COLORS["BACKGROUND_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            (FONT, 14),
            0.084,
            0.2,
            (FONT, 14),
            COLORS["MAIN_BUTTONS_COLOR"],
        )

        self.create_entry(0.084, 0.33, 600, 100)

        self.solve_button = self.create_main_button(
            "Rozwiąż", 0.15, 0.6, 120, 32, ctk.CENTER, lambda: self.solve_choosen_type()
        )

        self.create_main_button(
            "Rozwiąż krok po kroku", 0.385, 0.6, 250, 32, ctk.CENTER, None
        )
        self.create_main_button(
            "Pokaż graficzne przedstawienie", 0.7, 0.6, 260, 32, ctk.CENTER, None
        )

        self.result_label = self.create_label(
            "Rozwiązanie równania... ",
            0.085,
            0.7,
            500,
            100,
            (FONT, 14),
            COLORS["TEXT_GREY_COLOR"],
            COLORS["BACKGROUND_COLOR"],
            COLORS["LIGHT_ENTRY_COLOR"],
            10,
            None,
        )

        self.create_image_buttons()

        self.create_option_button(
            "Materiały pomocnicze",
            0.085,
            0.9,
            180,
            COLORS["BACKGROUND_COLOR"],
            COLORS["BACKGROUND_COLOR"],
            COLORS["BLACK"],
            COLORS["OPTION_BUTTON_HOVER_COLOR"],
            lambda: self.open_help(),
        )

        self.create_label(
            "app version 1.0",
            0.43,
            0.95,
            120,
            20,
            None,
            COLORS["TEXT_GREY_COLOR"],
            COLORS["BACKGROUND_COLOR"],
            COLORS["BACKGROUND_COLOR"],
            0,
            None,
        )

    def create_image_buttons(self):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")

        img_h = ctk.CTkImage(Image.open(os.path.join(image_path, "history_icon.png")))
        history_button = ctk.CTkButton(
            master=self.master,
            image=img_h,
            text="",
            width=14,
            height=14,
            bg_color=COLORS["MAIN_BUTTONS_COLOR"],
            fg_color=COLORS["MAIN_BUTTONS_COLOR"],
            hover_color=COLORS["MAIN_BUTTONS_COLOR"],
        )
        history_button.place(relx=0.92, rely=0.0)
        history_button.configure(compound="top")

        img_c = ctk.CTkImage(Image.open(os.path.join(image_path, "camera_icon.png")))
        camera_button = ctk.CTkButton(
            master=self.master,
            image=img_c,
            command=lambda: self.display_scan_eq_opt(),
            text="",
            width=16,
            height=14,
            bg_color=COLORS["LIGHT_ENTRY_COLOR"],
            fg_color=COLORS["LIGHT_ENTRY_COLOR"],
            hover_color=COLORS["OPTION_BUTTON_HOVER_COLOR"],
        )
        camera_button.place(relx=0.64, rely=0.34)
        camera_button.configure(compound="top")

        img_e = ctk.CTkImage(Image.open(os.path.join(image_path, "export_icon.jpg")))
        export_button = ctk.CTkButton(
            master=self.master,
            image=img_e,
            command=lambda: self.export_to_file(),
            text="",
            width=14,
            height=14,
            bg_color=COLORS["LIGHT_ENTRY_COLOR"],
            fg_color=COLORS["LIGHT_ENTRY_COLOR"],
            hover_color=COLORS["OPTION_BUTTON_HOVER_COLOR"],
            corner_radius=8,
        )
        export_button.place(relx=0.542, rely=0.71)
        export_button.configure(compound="top")

    def show_instrcutions(self):
        if (
            self.toplevel_window_instructions is None
            or not self.toplevel_window_instructions.winfo_exists()
        ):
            self.toplevel_window_instructions = TopLevelInstructions()

    def export_to_file(self):
        result = self.solution
        if (
            self.toplevel_window_export is None
            or not self.toplevel_window_export.winfo_exists()
        ):
            self.toplevel_window_export = TopLevelExport(result)

    def display_scan_eq_opt(self):
        if (
            self.toplevel_window_pic_choser is None
            or not self.toplevel_window_pic_choser.winfo_exists()
        ):
            self.toplevel_window_pic_choser = ToplevelWindowPicChoser()

    def create_option_button(
        self, text, x, y, wid, bg_color, fg_color, text_color, hover_color, command
    ):
        opt_button = ctk.CTkButton(
            master=self.master,
            text=text,
            width=wid,
            border_color=COLORS["WHITE"],
            bg_color=bg_color,
            fg_color=fg_color,
            hover_color=hover_color,
            font=(FONT, 13),
            text_color=text_color,
            command=command,
        )
        opt_button.place(relx=x, rely=y)
        return opt_button

    def create_main_button(self, text, x, y, wid, hei, anchor, command):
        button = ctk.CTkButton(
            fg_color=COLORS["MAIN_BUTTONS_COLOR"],
            bg_color=COLORS["BACKGROUND_COLOR"],
            master=self.master,
            text=text,
            corner_radius=10,
            width=wid,
            font=(FONT, 14),
            height=hei,
            text_color=COLORS["WHITE"],
            hover_color=COLORS["MAIN_BUTTONS_HOVER_COLOR"],
            command=command,
        )
        button.place(relx=x, rely=y, anchor=anchor)
        return button

    def create_label(
        self,
        text,
        x,
        y,
        wid,
        hei,
        text_font,
        text_color,
        bg_color,
        fg_color,
        corner_radius,
        anchor,
    ):
        label = ctk.CTkLabel(
            master=self.master,
            text=text,
            width=wid,
            height=hei,
            corner_radius=corner_radius,
            font=text_font,
            bg_color=bg_color,
            text_color=text_color,
            fg_color=fg_color,
            anchor=anchor,
        )
        label.place(relx=x, rely=y)
        return label

    def create_entry(self, x, y, wid, hei):
        self.eq_entry = ctk.CTkEntry(
            master=self.master,
            width=wid,
            height=hei,
            font=(FONT, 14),
            corner_radius=10,
            fg_color=COLORS["LIGHT_ENTRY_COLOR"],
            bg_color=COLORS["BACKGROUND_COLOR"],
            placeholder_text="Wpisz równanie",
            placeholder_text_color=COLORS["TEXT_GREY_COLOR"],
            text_color=COLORS["BLACK"],
        )
        self.eq_entry.place(relx=x, rely=y)

        return self.eq_entry

    def get_entry_content(self):
        return self.eq_entry.get()

    def create_combobox(
        self,
        values,
        wid,
        bg_color,
        fg_color,
        border_color,
        font,
        x,
        y,
        dropdown_font,
        button_color,
    ):
        self.combobox = ctk.CTkComboBox(
            master=self.master,
            values=values,
            width=wid,
            corner_radius=10,
            bg_color=bg_color,
            fg_color=fg_color,
            border_color=border_color,
            font=font,
            dropdown_font=dropdown_font,
            button_color=button_color,
            command=self.get_type_content,
        )
        self.combobox.place(relx=x, rely=y)

    def open_help(self):
        url_to_help = {
            "równanie liniowe": "https://pl.wikipedia.org/wiki/Równanie_liniowe",
            "równanie kwadratowe": "https://pl.wikipedia.org/wiki/Równanie_kwadratowe",
            "układ równań liniowych": "https://pl.wikipedia.org/wiki/Układ_równań_liniowych",
            "równanie nieliniowe": "https://www.cce.pk.edu.pl/~mj/lib/exe/fetch.php?media=pl:dydaktyka:konspektrniel.pdf"
        }
        url = url_to_help.get(self.eq_type)
        webbrowser.open(url, new=0, autoraise=True)

    def get_type_content(self, choice):
        self.eq_type = choice

    def solve_equation(self):
        equation_content = self.get_entry_content()
        result = self.equation_solver.solve_linear_equation(equation_content)
        self.update_label(result)

    def solve_quadratic_equation(self):
        equation_content = self.get_entry_content()
        result = self.equation_solver.solve_quadratic_equation(equation_content)
        self.update_label(result)

    def solve_system_of_equations(self):
        equation_content = self.get_entry_content()
        result = self.equation_solver.solve_system_of_equation(equation_content)
        self.update_label(result)
        
    def solve_non_linear_equation(self):
        equation_content = self.get_entry_content()
        result = self.equation_solver.solve_non_linear_equation(equation_content)
        self.update_label(result)
        
    def update_label(self, result):
        if result is not None:
            self.solution = result
            self.result_label.configure(text=result, text_color=COLORS["BLACK"])
        else:
            self.solution = "Nie udało się rozwiązać równania."
            self.result_label.configure(
                text="Nie udało się rozwiązać równania.", text_color=COLORS["BLACK"]
            )

    def solve_choosen_type(self):
        eq_type_to_func = {
            "równanie liniowe": self.solve_equation,
            "równanie kwadratowe": self.solve_quadratic_equation,
            "układ równań liniowych": self.solve_system_of_equations,
            "równanie nieliniowe": self.solve_non_linear_equation
        }
        selected_func = eq_type_to_func.get(self.eq_type)
        if selected_func:
            selected_func()
