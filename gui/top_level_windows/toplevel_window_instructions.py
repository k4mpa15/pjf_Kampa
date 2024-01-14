import json

import customtkinter as ctk
from PIL import Image

with open("gui/colors.json") as f:
    colors_data = json.load(f)

COLORS = colors_data.get("COLORS", {})


class TopLevelInstructions(ctk.CTkToplevel):
    def __init__(self, translator, eq_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x170")
        self.translator = translator
        self.eq_type = eq_type
        self.create_widgets()
        self.resizable(False, False)
        self.configure(fg_color=COLORS["BACKGROUND_COLOR"])
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.title("Instrukcje")
        self.grab_set()

    def on_close(self):
        self.destroy()

    def get_image(self):
        self.images_to_help_pl = {
            "Wybierz typ równania lub wartość do policzenia": "gui\instructions\instructions_blank.png",
            "równanie liniowe": "gui\instructions\instructions_linear_eq.png",
            "równanie kwadratowe": "gui\instructions\instructions_quadratic.png",
            "układ równań liniowych": "gui\instructions\instructions_system_of_linear.png",
            "układ równań nieliniowych": "gui\instructions\instructions_system_of_nonlinear.png",
            "równanie nieliniowe, metoda Newtona - Raphsona": "gui\instructions\instructions_non_linear_eq.png",
            "równanie nieliniowe, metoda siecznych": "gui\instructions\instructions_non_linear_eq.png",
            "równanie nieliniowe, metoda bisekcji": "gui\instructions\instructions_non_linear_eq.png",
            "równanie różniczkowe zwyczajne, pierwszy stopień": "gui\instructions\instructions_ode_int.png",
            "całka oznaczona, metoda trapezów": "gui\instructions\instructions_integral.png",
            "całka oznaczona, metoda Simpsona": "gui\instructions\instructions_integral.png",
            "całka oznaczona, niewłaściwa": "gui\instructions\instructions_integral.png",
            "pole pod wykresem": "gui\instructions\instructions_field_below_f.png",
            "objętość bryły ograniczonej funkcją": "gui\instructions\instructions_volume_below_f.png",
        }
        self.images_to_help_eng = {
            "Choose type of equation or value to calculate": "gui\instructions\instructions_blank.png",
            "linear equations": "gui\instructions\instructions_linear_eq.png",
            "quadratic equation": "gui\instructions\instructions_quadratic.png",
            "system of l. equations": "gui\instructions\instructions_system_of_linear.png",
            "system of non linear equations": "gui\instructions\instructions_system_of_nonlinear.png",
            "non linear eq., Newton - Raphson method": "gui\instructions\instructions_non_linear_eq.png",
            "non linear eq., secant method": "gui\instructions\instructions_non_linear_eq.png",
            "non linear eq., bisection method": "gui\instructions\instructions_non_linear_eq.png",
            "ODE, first order": "gui\instructions\instructions_ode_int.png",
            "definite integral, trapeze method": "gui\instructions\instructions_integral.png",
            "definite integral, Simpson method": "gui\instructions\instructions_integral.png",
            "improper, definite integral": "gui\instructions\instructions_integral.png",
            "field below function": "gui\instructions\instructions_field_below_f.png",
            "volume of solid under curve": "gui\instructions\instructions_volume_below_f.png",
        }
        try:
            if self.translator.language == "pl":
                self.images_to_help = self.images_to_help_pl
            else:
                self.images_to_help = self.images_to_help_eng
            img = self.images_to_help.get(self.eq_type)
            return img
        except TypeError:
            return

    def create_widgets(self):
        img = self.get_image()
        my_image = ctk.CTkImage(
            light_image=Image.open(img),
            dark_image=None,
            size=(300, 170),
        )

        ctk.CTkLabel(self, image=my_image, text="", anchor="center").place(
            relx=0.0, rely=0.0
        )
