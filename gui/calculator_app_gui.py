import json
import os
import tkinter
from tkinter import *
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image
from pytesseract import pytesseract

from eq_solvers.common_eq_solv import EquationSolver
from gui.top_level_windows.toplevel_window_export import TopLevelExport
from gui.top_level_windows.toplevel_window_history import TopLevelHistory
from gui.top_level_windows.toplevel_window_instructions import TopLevelInstructions
from gui.top_level_windows.toplevel_window_plots import TopLevelPlots
from gui.top_level_windows.toplevel_window_solid_type import TopLevelSolidType
from gui.top_level_windows.toplevel_window_step_by_step import TopLevelWindowStepByStep
from options.equations_history import EquationHistory
from options.help_materials import HelpMaterials
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
        self.toplevel_window_solid_type = None
        self.equation_history = EquationHistory(self.language_manager)
        self.toplevel_window_history = None
        self.create_slider()
        self.toplevel_window_step_by_step = None
        self.help_materials = HelpMaterials(self.translator)
        self.value = 0
        self.toplevel_window_plots = None
        self.equation_value = None

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
            "Choose type of equation or value to calculate",
            "linear equations",
            "system of l. equations",
            "quadratic equation",
            "system of non linear equations",
            "non linear eq., Newton - Raphson method",
            "non linear eq., secant method",
            "non linear eq., bisection method",
            "ODE, first order",
            "definite integral, trapeze method",
            "definite integral, Simpson method",
            "improper, definite integral",
            "field below function",
            "volume of solid under curve",
        ]
        self.eq_types_pl = [
            "Wybierz typ równania lub wartość do policzenia",
            "równanie liniowe",
            "układ równań liniowych",
            "równanie kwadratowe",
            "układ równań nieliniowych",
            "równanie nieliniowe, metoda Newtona - Raphsona",
            "równanie nieliniowe, metoda siecznych",
            "równanie nieliniowe, metoda bisekcji",
            "równanie różniczkowe zwyczajne, pierwszy stopień",
            "całka oznaczona, metoda trapezów",
            "całka oznaczona, metoda Simpsona",
            "całka oznaczona, niewłaściwa",
            "pole pod wykresem",
            "objętość bryły ograniczonej funkcją",
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
        self.create_main_button(
            "graph", 0.7, 0.6, 260, 32, ctk.CENTER, lambda: self.display_plot()
        )

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

        if hasattr(self, "int_symbol") and self.int_symbol.winfo_exists():
            self.int_symbol.destroy()

        self.eq_entry.delete(0, len(self.get_entry_content()))
        self.result_label.configure(text="")

    def slider_event(self, value):
        rounded_value = round(float(value))
        self.slider.set(rounded_value)
        self.change_language(rounded_value)

    def open_help(self):
        self.help_materials.open_help_materials(self.eq_type)

    def get_type_content(self, choice):
        self.eq_type = choice
        self.create_options_to_solve_eq()

    def solve_equation(self):
        equation_content = self.get_entry_content()
        result = self.equation_solver.solve_linear_equation(equation_content)
        self.update_label_and_history(result)

    def solve_quadratic_equation(self):
        try:
            equation_content = self.get_entry_content()
            result = self.equation_solver.solve_quadratic_equation(equation_content)
        except ValueError:
            result = "Wrong format"
        self.update_label_and_history(result)

    def solve_system_of_equations(self):
        try:
            equation_content = self.get_entry_content()
            result = self.equation_solver.solve_system_of_equation(equation_content)
        except ValueError:
            result = "Wrong format"
        self.update_label_and_history(result)

    def solve_non_linear_equation_by_newton_raphson(self):
        try:
            num_of_it = self.it_entry.get()
            equation_content = self.get_entry_content()
            result = self.equation_solver.solve_non_linear_equation_by_newton_raphson(
                equation_content, max_iter=int(num_of_it), x0=int(self.x0_entry.get())
            )
        except ValueError:
            result = "Wrong format"
        self.update_label_and_history(result)

    def solve_non_linear_equation_by_secant(self):
        try:
            equation_content = self.get_entry_content()
            result = self.equation_solver.solve_non_linear_equation_by_secant(
                equation_content,
                max_iter=int(self.it_entry.get()),
                x0=int(self.x0_entry.get()),
                x1=int(self.x1_entry.get()),
            )
        except ValueError:
            result = "Wrong format"
        self.update_label_and_history(result)

    def solve_non_linear_equation_by_bisection(self):
        try:
            equation_content = self.get_entry_content()
            result = self.equation_solver.solve_non_linear_equation_by_bisection(
                equation_content,
                max_iter=int(self.it_entry.get()),
                a=int(self.x0_entry.get()),
                b=int(self.x1_entry.get()),
            )
        except ValueError:
            result = "Wrong format"
        self.update_label_and_history(result)

    def solve_first_ode(self):
        try:
            equation_content = self.get_entry_content()
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
        except ValueError:
            result = "Wrong format"
        self.update_label_and_history(result)

    def solve_integral_trapeze_method(self):
        try:
            equation_content = self.get_entry_content()
            result = self.equation_solver.solve_integral_trapeze_method(
                equation_content,
                a=float(self.x0_entry.get()),
                b=float(self.x1_entry.get()),
                num_of_ranges=int(self.it_entry.get()),
            )
        except ValueError:
            result = "Wrong format"
        self.update_label_and_history(result)

    def solve_integral_simpson_method(self):
        try:
            equation_content = self.get_entry_content()
            result = self.equation_solver.solve_integral_simpson_method(
                equation_content,
                a=float(self.x0_entry.get()),
                b=float(self.x1_entry.get()),
                num_of_inter=int(self.it_entry.get()),
            )
        except ValueError:
            result = "Wrong format"
        self.update_label_and_history(result)

    def solve_improper_integral(self):
        try:
            equation_content = self.get_entry_content()
            result = self.equation_solver.solve_improper_integral(
                equation_content,
                a=(self.x0_entry.get()),
                b=(self.x1_entry.get()),
            )
        except ValueError:
            result = "Wrong format"
        self.update_label_and_history(result)

    def field_below_f(self):
        try:
            equation_content = self.get_entry_content()
            result = self.equation_solver.field_below_f(
                equation_content,
                a=float(self.x0_entry.get()),
                b=float(self.x1_entry.get()),
            )
        except ValueError:
            result = "Wrong format"
        self.update_label_and_history(result)

    def volume_below_f(self):
        try:
            equation_content = self.get_entry_content()

            solid_type_value = self.toplevel_window_solid_type.get_type()
            if self.x0_entry.get() and self.x1_entry.get():
                result = self.equation_solver.volume_below_f(
                    equation_content,
                    a=float(self.x0_entry.get()),
                    b=float(self.x1_entry.get()),
                    solid=solid_type_value,
                )
        except ValueError:
            result = "Wrong format"
        self.update_label_and_history(result)

    def solve_system_of_non_linear_equation(self):
        try:
            equation_content = self.get_entry_content()
            result = self.equation_solver.solve_system_of_non_linear_equation(
                equation_content
            )
        except ValueError:
            result = "Wrong format"
        self.update_label_and_history(result)

    def update_label_and_history(self, result):
        text_color = COLORS["BLACK"]
        if result == "Wrong format":
            text_color = COLORS["RED"]
        self.solution = result
        self.result_label.configure(text=result, text_color=text_color)
        self.equation_history.add_equation(self.get_entry_content(), str(result))

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
            "całka oznaczona, metoda trapezów",
            "definite integral, trapeze method",
            "całka oznaczona, metoda Simpsona",
            "definite integral, Simpson method",
            "improper, definite integral",
            "całka oznaczona, niewłaściwa",
            "field below function",
            "pole pod wykresem",
            "objętość bryły ograniczonej funkcją",
            "volume of solid under curve",
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
            or self.eq_type == "definite integral, trapeze method"
            or self.eq_type == "całka oznaczona, metoda trapezów"
            or self.eq_type == "całka oznaczona, metoda Simpsona"
            or self.eq_type == "definite integral, Simpson method"
            or self.eq_type == "improper, definite integral"
            or self.eq_type == "całka oznaczona, niewłaściwa"
            or self.eq_type == "field below function"
            or self.eq_type == "pole pod wykresem"
            or self.eq_type == "objętość bryły ograniczonej funkcją"
            or self.eq_type == "volume of solid under curve"
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
            self.x0_entry.configure(placeholder_text="a")
            self.x1_entry.configure(placeholder_text="b")
        if (
            self.eq_type == "równanie różniczkowe zwyczajne, pierwszy stopień"
            or self.eq_type == "ODE, first order"
        ):
            self.it_entry.configure(placeholder_text="y(0)")
            self.x0_entry.configure(placeholder_text="a")
            self.x1_entry.configure(placeholder_text="b")
        if (
            self.eq_type == "definite integral, trapeze method"
            or self.eq_type == "całka oznaczona, metoda trapezów"
            or self.eq_type == "całka oznaczona, metoda Simpsona"
            or self.eq_type == "definite integral, Simpson method"
            or self.eq_type == "improper, definite integral"
            or self.eq_type == "całka oznaczona, niewłaściwa"
            or self.eq_type == "field below function"
            or self.eq_type == "pole pod wykresem"
            or self.eq_type == "objętość bryły ograniczonej funkcją"
            or self.eq_type == "volume of solid under curve"
        ):
            self.it_entry.configure(placeholder_text="num of int.")
            image_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "icons"
            )

            img_integral = ctk.CTkImage(
                Image.open(os.path.join(image_path, "integral.jpg"))
            )
            self.int_symbol = self.create_image_button(
                img_integral,
                None,
                COLORS["BACKGROUND_COLOR"],
                COLORS["BACKGROUND_COLOR"],
                COLORS["BACKGROUND_COLOR"],
                40,
                60,
            )
            self.int_symbol.place(relx=0.04, rely=0.36)
        if (
            self.eq_type == "improper, definite integral"
            or self.eq_type == "całka oznaczona, niewłaściwa"
            or self.eq_type == "field below function"
            or self.eq_type == "pole pod wykresem"
            or self.eq_type == "objętość bryły ograniczonej funkcją"
            or self.eq_type == "volume of solid under curve"
        ):
            self.it_entry.destroy()
            self.x0_entry.place(relx=0.72, rely=0.37)
            self.x1_entry.place(relx=0.77, rely=0.37)
        if (
            self.eq_type == "field below function"
            or self.eq_type == "pole pod wykresem"
            or self.eq_type == "objętość bryły ograniczonej funkcją"
            or self.eq_type == "volume of solid under curve"
        ):
            self.int_symbol.destroy()

        if (
            self.eq_type == "objętość bryły ograniczonej funkcją"
            or self.eq_type == "volume of solid under curve"
        ):
            self.fill_label.destroy()
            self.choose_solid_type()

    def choose_solid_type(self):
        if (
            self.toplevel_window_solid_type is None
            or not self.toplevel_window_solid_type.winfo_exists()
        ):
            self.toplevel_window_solid_type = TopLevelSolidType(self.language_manager)
            self.toplevel_window_solid_type.after(
                1, self.toplevel_window_solid_type.lift
            )
        else:
            self.toplevel_window_solid_type.set_value()

    def solve_choosen_type(self):
        eq_type_to_func_pl = {
            "równanie liniowe": self.solve_equation,
            "równanie kwadratowe": self.solve_quadratic_equation,
            "układ równań liniowych": self.solve_system_of_equations,
            "układ równań nieliniowych": self.solve_system_of_non_linear_equation,
            "równanie nieliniowe, metoda Newtona - Raphsona": self.solve_non_linear_equation_by_newton_raphson,
            "równanie nieliniowe, metoda siecznych": self.solve_non_linear_equation_by_secant,
            "równanie nieliniowe, metoda bisekcji": self.solve_non_linear_equation_by_bisection,
            "równanie różniczkowe zwyczajne, pierwszy stopień": self.solve_first_ode,
            "całka oznaczona, metoda trapezów": self.solve_integral_trapeze_method,
            "całka oznaczona, metoda Simpsona": self.solve_integral_simpson_method,
            "całka oznaczona, niewłaściwa": self.solve_improper_integral,
            "pole pod wykresem": self.field_below_f,
            "objętość bryły ograniczonej funkcją": self.volume_below_f,
        }
        eq_type_to_func_en = {
            "linear equations": self.solve_equation,
            "quadratic equation": self.solve_quadratic_equation,
            "system of l. equations": self.solve_system_of_equations,
            "system of non linear equations": self.solve_system_of_non_linear_equation,
            "non linear eq., Newton - Raphson method": self.solve_non_linear_equation_by_newton_raphson,
            "non linear eq., secant method": self.solve_non_linear_equation_by_secant,
            "non linear eq., bisection method": self.solve_non_linear_equation_by_bisection,
            "ODE, first order": self.solve_first_ode,
            "definite integral, trapeze method": self.solve_integral_trapeze_method,
            "definite integral, Simpson method": self.solve_integral_simpson_method,
            "improper, definite integral": self.solve_improper_integral,
            "field below function": self.field_below_f,
            "volume of solid under curve": self.volume_below_f,
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
            self.toplevel_window_history = TopLevelHistory(self.language_manager, self)
            self.toplevel_window_history.after(1, self.toplevel_window_history.lift)

    def show_step_by_step(self):
        acceptable_types = [
            "równanie kwadratowe",
            "równanie liniowe",
            "linear equations",
            "quadratic equation",
            "układ równań liniowych",
            "system of l. equations",
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
                self.translator, self.eq_type
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
        try:
            file_path = filedialog.askopenfilename(
                title="",
                filetypes=[("Pliki obrazów", "*.png;*.jpg;*.jpeg;")],
            )
            path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            image_path = file_path
            img = Image.open(image_path)
            pytesseract.tesseract_cmd = path_to_tesseract
            text = pytesseract.image_to_string(img)
            text = text.lower().replace("", "").replace("X", "x")
            self.eq_entry.delete(0, END)
            self.eq_entry.insert(0, text)
        except AttributeError:
            return

    def display_plot(self):
        if (
            self.toplevel_window_plots is None
            or not self.toplevel_window_plots.winfo_exists()
        ):
            a = None
            b = None
            if hasattr(self, "x0_entry") and self.x0_entry.winfo_exists():
                a = self.x0_entry.get()

                if hasattr(self, "x1_entry") and self.x1_entry.winfo_exists():
                    b = self.x1_entry.get()

            self.toplevel_window_plots = TopLevelPlots(
                self.translator, self.get_entry_content(), self.eq_type, a, b
            )
            self.toplevel_window_plots.after(1, self.toplevel_window_plots.lift)

    def set_equation_value(self, value):
        self.eq_entry.delete(0, END)
        self.eq_entry.insert(0, value)
