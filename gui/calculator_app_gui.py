import json
import os
import tkinter
import webbrowser
from tkinter import *

import customtkinter as ctk
from PIL import Image

from eq_solvers.common_eq_solv import EquationSolver
from gui.top_level_windows.toplevel_window_export import TopLevelExport
from gui.top_level_windows.toplevel_window_history import TopLevelHistory
from gui.top_level_windows.toplevel_window_instructions import TopLevelInstructions
from gui.top_level_windows.toplevel_window_pic_choser import ToplevelWindowPicChoser
from gui.top_level_windows.toplevel_window_step_by_step import TopLevelWindowStepByStep
from options.equations_history import EquationHistory
from options.translator import Translator

with open("gui/colors.json") as f:
    colors_data = json.load(f)

COLORS = colors_data.get("COLORS", {})
FONT = "Century Gothic"


class CalculatorApp(ctk.CTk):
    def __init__(self, master, language_manager):
        super().__init__()
        self.master = master
        self.language_manager = language_manager
        self.master.title("Kalkulator równań")
        self.master.geometry("1000x600")
        self.master.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.toplevel_window_pic_choser = None
        self.toplevel_window_export = None
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.eq_entry = None
        self.equation_solver = EquationSolver()
        self.translator = Translator(self.language_manager)
        self.create_widgets()
        self.solution = None
        self.eq_type = None
        self.toplevel_window_instructions = None
        self.equation_history = EquationHistory(self.language_manager)
        self.toplevel_window_history = None
        self.create_slider()
        self.toplevel_window_step_by_step = None

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

    def create_image_button(
        self, image, command, bg_color, fg_color, hover_color, wid, hei
    ):
        return ctk.CTkButton(
            master=self.master,
            image=image,
            command=command,
            text="",
            width=wid,
            height=hei,
            bg_color=bg_color,
            fg_color=fg_color,
            hover_color=hover_color,
        )

    def create_image_buttons(self):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")

        img_h = ctk.CTkImage(Image.open(os.path.join(image_path, "history_icon.png")))
        history_button = self.create_image_button(
            img_h,
            lambda: self.show_history(),
            COLORS["MAIN_BUTTONS_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            14,
            14,
        )
        history_button.place(relx=0.917, rely=0.0057)
        history_button.configure(compound="top")

        img_c = ctk.CTkImage(Image.open(os.path.join(image_path, "camera_icon.png")))
        camera_button = self.create_image_button(
            img_c,
            lambda: self.display_scan_eq_opt(),
            COLORS["LIGHT_ENTRY_COLOR"],
            COLORS["LIGHT_ENTRY_COLOR"],
            COLORS["OPTION_BUTTON_HOVER_COLOR"],
            16,
            14,
        )
        camera_button.place(relx=0.64, rely=0.34)
        camera_button.configure(compound="top")

        img_e = ctk.CTkImage(Image.open(os.path.join(image_path, "export_icon.jpg")))
        export_button = self.create_image_button(
            img_e,
            lambda: self.export_to_file(),
            COLORS["LIGHT_ENTRY_COLOR"],
            COLORS["LIGHT_ENTRY_COLOR"],
            COLORS["OPTION_BUTTON_HOVER_COLOR"],
            14,
            14,
        )
        export_button.place(relx=0.542, rely=0.71)
        export_button.configure(compound="top")

    def create_option_button(
        self, text, x, y, wid, bg_color, fg_color, text_color, hover_color, command
    ):
        translated_text = self.translator.translate(text)
        opt_button = ctk.CTkButton(
            master=self.master,
            text=translated_text,
            width=wid,
            border_color=COLORS["WHITE"],
            bg_color=bg_color,
            fg_color=fg_color,
            hover_color=hover_color,
            font=(FONT, 13),
            text_color=text_color,
            command=command,
            anchor="w",
        )
        opt_button.place(relx=x, rely=y)
        return opt_button

    def create_main_button(self, text, x, y, wid, hei, anchor, command):
        translated_text = self.translator.translate(text)
        button = ctk.CTkButton(
            fg_color=COLORS["MAIN_BUTTONS_COLOR"],
            bg_color=COLORS["BACKGROUND_COLOR"],
            master=self.master,
            text=translated_text,
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
        translated_text = self.translator.translate(text)
        label = ctk.CTkLabel(
            master=self.master,
            text=translated_text,
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

    def create_entry(self, x, y, wid, hei, text):
        translated_text = self.translator.translate(text)
        self.eq_entry = ctk.CTkEntry(
            master=self.master,
            width=wid,
            height=hei,
            font=(FONT, 14),
            corner_radius=10,
            fg_color=COLORS["LIGHT_ENTRY_COLOR"],
            bg_color=COLORS["BACKGROUND_COLOR"],
            placeholder_text=translated_text,
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

    def create_slider(self):
        self.slider = ctk.CTkSlider(
            master=self.master,
            from_=1,
            to=1.5,
            command=self.slider_event,
            number_of_steps=2,
            width=40,
            bg_color=COLORS["MAIN_BUTTONS_COLOR"],
            fg_color=COLORS["BACKGROUND_COLOR"],
            progress_color=COLORS["BACKGROUND_COLOR"],
            button_color=COLORS["BACKGROUND_COLOR"],
            button_hover_color=COLORS["BACKGROUND_COLOR"],
        )
        self.slider.set(1.0)
        self.slider.place(relx=0.87, rely=0.03, anchor=tkinter.CENTER)

    def create_widgets(self):
        self.create_option_button(
            "how_to_enter_equations",
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
            "calculator_app",
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
        self.create_label(
            "PL",
            0.821,
            0.00,
            30,
            32,
            (FONT, 14),
            COLORS["WHITE"],
            COLORS["MAIN_BUTTONS_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            10,
            "center",
        )
        self.create_label(
            "EN",
            0.88,
            0.00,
            30,
            32,
            (FONT, 14),
            COLORS["WHITE"],
            COLORS["MAIN_BUTTONS_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            10,
            "center",
        )
        self.eq_types_en = [
            "Choose type",
            "linear equations",
            "system of l. eq.",
            "quadratic eq.",
            "non linear eq., Newton - Raphson method",
            "non linear eq., secant method",
            "non linear eq., bisection method",
            "ODE, first order",
            "ODE, second order",
        ]
        self.eq_types_pl = [
            "Wybierz typ",
            "równanie liniowe",
            "układ równań liniowych",
            "równanie kwadratowe",
            "równanie nieliniowe, metoda Newtona - Raphsona",
            "równanie nieliniowe, metoda siecznych",
            "równanie nieliniowe, metoda bisekcji",
            "równanie różniczkowe zwyczajne, pierwszy stopień",
            "równanie różniczkowe zwyczajne, drugi stopień",
        ]
        if self.translator.language == "pl":
            eq_types = self.eq_types_pl
        else:
            eq_types = self.eq_types_en
        self.create_combobox(
            eq_types,
            500,
            COLORS["BACKGROUND_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            COLORS["MAIN_BUTTONS_COLOR"],
            (FONT, 14),
            0.084,
            0.2,
            (FONT, 14),
            COLORS["MAIN_BUTTONS_COLOR"],
        )
        label = "fill"
        translated_label = self.translator.translate(label)
        self.fill_label = ctk.CTkLabel(
            self.master,
            text=translated_label,
            font=(FONT, 14),
            text_color=COLORS["BLACK"],
        )
        self.fill_label.place(relx=0.72, rely=0.32)

        self.entry_to_placehold = ctk.CTkLabel(
            self.master,
            text=" ",
            font=(FONT, 14),
            text_color=COLORS["BLACK"],
            width=250,
            height=150,
        )
        self.entry_to_placehold.place(relx=0.72, rely=0.32)

        self.create_entry(0.084, 0.33, 600, 100, "solve_eq")

        self.solve_button = self.create_main_button(
            "solve", 0.15, 0.6, 120, 32, ctk.CENTER, lambda: self.solve_choosen_type()
        )
        self.master.bind("<Return>", lambda event: self.solve_choosen_type())

        self.create_main_button(
            "solve_step_by_step",
            0.385,
            0.6,
            250,
            32,
            ctk.CENTER,
            lambda: self.show_step_by_step(),
        )
        self.create_main_button("graph", 0.7, 0.6, 260, 32, ctk.CENTER, None)

        self.result_label = self.create_label(
            "eq_solve__",
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
            "help",
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

    def change_language(self, value):
        if value == 1:
            new_language = "pl"
        if value == 2:
            new_language = "en"
        self.change_language_in_manager(new_language)

    def change_language_in_manager(self, new_language):
        self.language_manager.set_language(new_language)
        self.update_language()

    def update_language(self):
        self.create_widgets()
        self.slider.lift()

    def clear_everything(self):
        if self.language_manager.get_language() == "pl":
            self.combobox.set(self.eq_types_pl[0])
        else:
            self.combobox.set(self.eq_types_en[0])

        if hasattr(self, "x0_entry") and self.x0_entry.winfo_exists():
            self.x0_entry.destroy()

        if hasattr(self, "x1_entry") and self.x1_entry.winfo_exists():
            self.x1_entry.destroy()

        if hasattr(self, "it_entry") and self.it_entry.winfo_exists():
            self.it_entry.destroy()

        if hasattr(self, "fill_label") and self.fill_label.winfo_exists():
            self.fill_label.destroy()

        self.eq_entry.delete(0, len(self.get_entry_content()))

    def slider_event(self, value):
        rounded_value = round(float(value))
        self.slider.set(rounded_value)
        self.change_language(rounded_value)

    def open_help(self):
        url_to_help_pl = {
            "równanie liniowe": "https://pl.wikipedia.org/wiki/Równanie_liniowe",
            "równanie kwadratowe": "https://pl.wikipedia.org/wiki/Równanie_kwadratowe",
            "układ równań liniowych": "https://pl.wikipedia.org/wiki/Układ_równań_liniowych",
            "równanie nieliniowe, metoda Newtona - Raphsona": "https://pl.wikipedia.org/wiki/Metoda_Newtona",
            "równanie nieliniowe, metoda siecznych": "https://pl.wikipedia.org/wiki/Metoda_siecznych",
            "równanie nieliniowe, metoda bisekcji": "https://pl.wikipedia.org/wiki/Metoda_równego_podziału",
            "równanie różniczkowe zwyczajne, pierwszy stopień": "https://pl.wikipedia.org/wiki/Równanie_różniczkowe_zwyczajne",
            "równanie różniczkowe zwyczajne, drugi stopień": "https://pl.wikipedia.org/wiki/Równanie_różniczkowe_zwyczajne",
        }
        url_to_help_en = {
            "linear equations": "https://en.wikipedia.org/wiki/Linear_equation",
            "quadratic eq.": "https://en.wikipedia.org/wiki/Quadratic_equation",
            "system of l. eq.": "https://en.wikipedia.org/wiki/Linear_system",
            "non linear eq., Newton - Raphson method": "https://en.wikipedia.org/wiki/Newton%27s_method",
            "non linear eq., secant method": "https://en.wikipedia.org/wiki/Secant_method",
            "non linear eq., bisection method": "https://en.wikipedia.org/wiki/Bisection_method",
            "ODE, first order": "https://en.wikipedia.org/wiki/Ordinary_differential_equation",
            "ODE, second order": "https://en.wikipedia.org/wiki/Ordinary_differential_equation",
        }
        if self.translator.language == "pl":
            url_to_help = url_to_help_pl
        else:
            url_to_help = url_to_help_en
        url = url_to_help.get(self.eq_type)
        webbrowser.open(url, new=0, autoraise=True)

    def get_type_content(self, choice):
        self.eq_type = choice
        self.create_options_to_solve_eq()

    def solve_equation(self):
        equation_content = self.get_entry_content()
        result = self.equation_solver.solve_linear_equation(equation_content)
        self.update_label_and_history(result)

    def solve_quadratic_equation(self):
        equation_content = self.get_entry_content()
        result = self.equation_solver.solve_quadratic_equation(equation_content)
        self.update_label_and_history(result)

    def solve_system_of_equations(self):
        equation_content = self.get_entry_content()
        result = self.equation_solver.solve_system_of_equation(equation_content)
        self.update_label_and_history(result)

    def solve_non_linear_equation_by_newton_raphson(self):
        num_of_it = self.it_entry.get()
        equation_content = self.get_entry_content()
        result = self.equation_solver.solve_non_linear_equation_by_newton_raphson(
            equation_content, max_iter=int(num_of_it), x0=int(self.x0_entry.get())
        )
        self.update_label_and_history(result)

    def solve_non_linear_equation_by_secant(self):
        equation_content = self.get_entry_content()
        result = self.equation_solver.solve_non_linear_equation_by_secant(
            equation_content,
            max_iter=int(self.it_entry.get()),
            x0=int(self.x0_entry.get()),
            x1=int(self.x1_entry.get()),
        )
        self.update_label_and_history(result)

    def solve_non_linear_equation_by_bisection(self):
        equation_content = self.get_entry_content()
        result = self.equation_solver.solve_non_linear_equation_by_bisection(
            equation_content,
            max_iter=int(self.it_entry.get()),
            a=int(self.x0_entry.get()),
            b=int(self.x1_entry.get()),
        )
        self.update_label_and_history(result)

    def solve_first_ode(self):
        equation_content = self.get_entry_content()
        # equation_content = lambda y, x: -0.1 * y
        a_value = int(self.x0_entry.get()) if self.x0_entry.get() else None
        b_value = int(self.x1_entry.get()) if self.x1_entry.get() else None

        if a_value is None and b_value is not None:
            a_value = b_value
        elif b_value is None and a_value is not None:
            b_value = a_value

        result = self.equation_solver.solve_first_ode(
            equation_content,
            initial_condition=int(self.it_entry.get()),
            a=a_value,
            b=b_value,
        )
        self.update_label_and_history(result)

    def update_label_and_history(self, result):
        self.solution = result
        self.result_label.configure(text=result, text_color=COLORS["BLACK"])
        self.equation_history.add_equation(self.get_entry_content(), result)

    def create_options_to_solve_eq(self):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")

        img_d = ctk.CTkImage(Image.open(os.path.join(image_path, "delete_icon.png")))
        self.delete_button = self.create_image_button(
            img_d,
            lambda: self.clear_everything(),
            COLORS["BACKGROUND_COLOR"],
            COLORS["BACKGROUND_COLOR"],
            COLORS["BACKGROUND_COLOR"],
            14,
            14,
        )
        self.delete_button.place(relx=0.61, rely=0.2)

        acceptable_types = [
            "równanie nieliniowe, metoda Newtona - Raphsona",
            "non linear eq., Newton - Raphson method",
            "równanie nieliniowe, metoda siecznych",
            "non linear eq., secant method",
            "równanie nieliniowe, metoda bisekcji",
            "non linear eq., bisection method",
            "równanie różniczkowe zwyczajne, pierwszy stopień",
            "ODE, first order",
        ]
        if self.eq_type.lower() in map(str.lower, acceptable_types):
            self.entry_to_placehold.destroy()
            self.it_entry = ctk.CTkEntry(
                self.master,
                height=40,
                width=100,
                corner_radius=10,
                bg_color=COLORS["BACKGROUND_COLOR"],
                fg_color=COLORS["LIGHT_ENTRY_COLOR"],
                placeholder_text="iter.",
                placeholder_text_color=COLORS["TEXT_GREY_COLOR"],
                text_color=COLORS["BLACK"],
            )
            self.it_entry.place(relx=0.72, rely=0.37)
            self.x0_entry = ctk.CTkEntry(
                self.master,
                height=40,
                width=40,
                corner_radius=10,
                bg_color=COLORS["BACKGROUND_COLOR"],
                fg_color=COLORS["LIGHT_ENTRY_COLOR"],
                placeholder_text="x0",
                placeholder_text_color=COLORS["TEXT_GREY_COLOR"],
                text_color=COLORS["BLACK"],
            )
            self.x0_entry.place(relx=0.84, rely=0.37)

        if (
            self.eq_type == "równanie nieliniowe, metoda siecznych"
            or self.eq_type == "non linear eq., secant method"
            or self.eq_type == "równanie nieliniowe, metoda bisekcji"
            or self.eq_type == "non linear eq., bisection method"
            or self.eq_type == "równanie różniczkowe zwyczajne, pierwszy stopień"
            or self.eq_type == "ODE, first order"
        ):
            self.x1_entry = ctk.CTkEntry(
                self.master,
                height=40,
                width=40,
                corner_radius=10,
                bg_color=COLORS["BACKGROUND_COLOR"],
                fg_color=COLORS["LIGHT_ENTRY_COLOR"],
                placeholder_text="x1",
                placeholder_text_color=COLORS["TEXT_GREY_COLOR"],
                text_color=COLORS["BLACK"],
            )
            self.x1_entry.place(relx=0.89, rely=0.37)
        if (
            self.eq_type == "równanie nieliniowe, metoda bisekcji"
            or self.eq_type == "non linear eq., bisection method"
        ):
            self.x0_entry.configure(placeholder_text="a")
            self.x1_entry.configure(placeholder_text="b")
        if (
            self.eq_type == "równanie różniczkowe zwyczajne, pierwszy stopień"
            or self.eq_type == "ODE, first order"
        ):
            self.it_entry.configure(placeholder_text="y(0)")
            self.x0_entry.configure(placeholder_text="a")
            self.x1_entry.configure(placeholder_text="b")

    def solve_choosen_type(self):
        eq_type_to_func_pl = {
            "równanie liniowe": self.solve_equation,
            "równanie kwadratowe": self.solve_quadratic_equation,
            "układ równań liniowych": self.solve_system_of_equations,
            "równanie nieliniowe, metoda Newtona - Raphsona": self.solve_non_linear_equation_by_newton_raphson,
            "równanie nieliniowe, metoda siecznych": self.solve_non_linear_equation_by_secant,
            "równanie nieliniowe, metoda bisekcji": self.solve_non_linear_equation_by_bisection,
            "równanie różniczkowe zwyczajne, pierwszy stopień": self.solve_first_ode,
        }
        eq_type_to_func_en = {
            "linear equations": self.solve_equation,
            "quadratic eq.": self.solve_quadratic_equation,
            "system of l. eq.": self.solve_system_of_equations,
            "non linear eq., Newton - Raphson method": self.solve_non_linear_equation_by_newton_raphson,
            "non linear eq., secant method": self.solve_non_linear_equation_by_secant,
            "non linear eq., bisection method": self.solve_non_linear_equation_by_bisection,
            "ODE, first order": self.solve_first_ode,
        }
        if self.translator.language == "pl":
            eq_type_to_func = eq_type_to_func_pl
        else:
            eq_type_to_func = eq_type_to_func_en
        selected_func = eq_type_to_func.get(self.eq_type)
        if selected_func:
            selected_func()

    def show_history(self):
        if (
            self.toplevel_window_history is None
            or not self.toplevel_window_history.winfo_exists()
        ):
            self.toplevel_window_history = TopLevelHistory(self.language_manager)
            self.toplevel_window_history.after(1, self.toplevel_window_history.lift)

    def show_step_by_step(self):
        acceptable_types = [
            "równanie kwadratowe",
            "równanie liniowe",
            "linear equations",
            "quadratic eq.",
        ]
        entry_content = self.get_entry_content()
        if (
            (
                self.toplevel_window_step_by_step is None
                or not self.toplevel_window_step_by_step.winfo_exists()
            )
            and not (not entry_content)
            and (self.eq_type.lower() in map(str.lower, acceptable_types))
        ):
            self.toplevel_window_step_by_step = TopLevelWindowStepByStep(
                self.language_manager, entry_content, self.eq_type
            )
            self.toplevel_window_step_by_step.after(
                1, self.toplevel_window_step_by_step.lift
            )

    def show_instrcutions(self):
        if (
            self.toplevel_window_instructions is None
            or not self.toplevel_window_instructions.winfo_exists()
        ):
            self.toplevel_window_instructions = TopLevelInstructions(
                self.language_manager
            )
            self.toplevel_window_instructions.after(
                1, self.toplevel_window_instructions.lift
            )

    def export_to_file(self):
        result = self.solution
        if (
            self.toplevel_window_export is None
            or not self.toplevel_window_export.winfo_exists()
        ):
            self.toplevel_window_export = TopLevelExport(result, self.language_manager)
            self.toplevel_window_export.after(1, self.toplevel_window_export.lift)

    def display_scan_eq_opt(self):
        if (
            self.toplevel_window_pic_choser is None
            or not self.toplevel_window_pic_choser.winfo_exists()
        ):
            self.toplevel_window_pic_choser = ToplevelWindowPicChoser(
                self.language_manager
            )
            self.toplevel_window_pic_choser.after(
                1, self.toplevel_window_pic_choser.lift
            )
